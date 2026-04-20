#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import os from "node:os";
import { createRequire } from "node:module";

const require = createRequire(new URL("../workbench/package.json", import.meta.url));
let chromium;
try {
  ({ chromium } = require("playwright"));
} catch {
  ({ chromium } = require("@playwright/test"));
}

const args = parseArgs(process.argv.slice(2));
const client = args.client || "microsoft-copilot";
const url = args.url || "https://m365.cloud.microsoft/chat";
const output = required(args.output, "--output");
const artifactDir = args["artifact-dir"] || path.join(path.dirname(output), `${client}.ui`);
const prompt = required(args.prompt, "--prompt");
const preferredMode = args["preferred-mode"] || args["preferred-model"] || "";
const profileDirArg = args["profile-dir"];
const profileDirEnv = process.env.MICROSOFT_COPILOT_PROFILE_DIR;
const profileDirSource = profileDirArg ? "argument" : profileDirEnv ? "environment" : "default";
const profileDir =
  profileDirArg || profileDirEnv || path.join(os.homedir(), ".cache", "challenge2-microsoft-copilot-playwright");
const timeoutMs = Number(args["timeout-ms"] || 180000);
const headless = Boolean(args.headless);

await fs.mkdir(path.dirname(output), { recursive: true });
await fs.mkdir(artifactDir, { recursive: true });

const startedAt = new Date().toISOString();
const metadata = {
  client,
  url,
  profileDirSource,
  profileDirConfigured: profileDirSource !== "default",
  headless,
  startedAt,
  automation: "playwright_web_ui",
  preferredMode: preferredMode || null,
  caveats: [
    "Microsoft Copilot is evaluated through a browser UI adapter rather than a stable headless API.",
    "The adapter requires an authenticated Microsoft session in the Playwright profile.",
    "Selectors, loading states, tenant policies, and model routing can change outside this repository.",
  ],
};

let context;
try {
  context = await chromium.launchPersistentContext(profileDir, {
    headless,
    viewport: { width: 1440, height: 1000 },
    args: ["--disable-dev-shm-usage"],
  });
  const page = context.pages()[0] || (await context.newPage());
  page.setDefaultTimeout(Math.min(timeoutMs, 60000));
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: timeoutMs });
  await page.waitForLoadState("networkidle", { timeout: 30000 }).catch(() => {});

  if (await isAuthenticationPage(page)) {
    await capture(page, artifactDir, "auth-required");
    await writeOutput(output, {
      ...metadata,
      status: "auth_required",
      finishedAt: new Date().toISOString(),
      error: "Microsoft sign-in is required in the Playwright profile before the adapter can submit benchmark prompts.",
    });
    process.exitCode = 4;
  } else {
    const modeSelection = await selectPreferredMode(page, preferredMode, artifactDir);
    const textbox = await findPromptBox(page);
    if (!textbox) {
      await capture(page, artifactDir, "no-prompt-box");
      await writeOutput(output, {
        ...metadata,
        status: "failed",
        modeSelection,
        finishedAt: new Date().toISOString(),
        error: "No prompt textbox was found. The browser may need interactive sign-in, the tenant may block Copilot Chat, or the UI selectors may have changed.",
      });
      process.exitCode = 2;
    } else {
      await textbox.click({ timeout: 30000 });
      await textbox.fill(prompt).catch(async () => {
        await page.keyboard.insertText(prompt);
      });
      await page.keyboard.press("Enter");
      await page.waitForTimeout(45000);
      await page.waitForLoadState("networkidle", { timeout: 30000 }).catch(() => {});
      const answer = await extractAnswer(page, prompt);
      await capture(page, artifactDir, "completed");
      await writeOutput(output, {
        ...metadata,
        status: answer.trim() ? "completed" : "completed_empty",
        modeSelection,
        finishedAt: new Date().toISOString(),
        answer,
      });
      process.exitCode = answer.trim() ? 0 : 3;
    }
  }
} catch (error) {
  await writeOutput(output, {
    ...metadata,
    status: "failed",
    finishedAt: new Date().toISOString(),
    error: String(error && error.stack ? error.stack : error),
  });
  process.exitCode = 1;
} finally {
  if (context) {
    await context.close().catch(() => {});
  }
}

async function isAuthenticationPage(page) {
  const title = await page.title().catch(() => "");
  const pageUrl = page.url();
  if (/sign in|login/i.test(title) || /login\.microsoftonline\.com|login\.live\.com/i.test(pageUrl)) {
    return true;
  }
  const emailInput = page.locator("input[type='email'], input[name='loginfmt']").first();
  return Boolean((await emailInput.count().catch(() => 0)) && (await emailInput.isVisible().catch(() => false)));
}

async function findPromptBox(page) {
  const selectors = [
    "textarea[aria-label*='message' i]",
    "textarea[placeholder*='message' i]",
    "textarea[aria-label*='ask' i]",
    "textarea[placeholder*='ask' i]",
    "[contenteditable='true'][role='textbox']",
    "[role='textbox'][contenteditable='true']",
    "[role='textbox']",
    "textarea",
    "[contenteditable='true']",
  ];
  for (const selector of selectors) {
    const locator = page.locator(selector).last();
    const count = await locator.count().catch(() => 0);
    if (!count) {
      continue;
    }
    if (await locator.isVisible().catch(() => false)) {
      return locator;
    }
  }
  return null;
}

async function selectPreferredMode(page, preferredMode, artifactDir) {
  const requested = String(preferredMode || "").trim();
  if (!requested) {
    return { requested: null, status: "not_requested" };
  }

  const modeButton = page
    .locator(
      [
        "#gptModeSwitcher",
        "button[aria-label*='mode' i]",
        "button[aria-label*='model' i]",
        "button:has-text('Auto')",
        "button:has-text('GPT')",
      ].join(", ")
    )
    .first();
  if (!(await modeButton.count().catch(() => 0)) || !(await modeButton.isVisible().catch(() => false))) {
    await capture(page, artifactDir, "mode-switcher-not-found");
    return { requested, status: "switcher_not_found" };
  }

  await modeButton.click({ timeout: 30000 });
  await page.waitForTimeout(1000);
  await capture(page, artifactDir, "mode-menu-open");

  const labels = preferredModeLabels(requested);
  for (const label of labels) {
    const option = page
      .locator(
        [
          `[role='menuitemradio']:has-text('${cssString(label)}')`,
          `[role='menuitem']:has-text('${cssString(label)}')`,
          `[role='option']:has-text('${cssString(label)}')`,
          `button:has-text('${cssString(label)}')`,
          `div:has-text('${cssString(label)}')`,
        ].join(", ")
      )
      .last();
    if (!(await option.count().catch(() => 0)) || !(await option.isVisible().catch(() => false))) {
      continue;
    }
    await option.click({ timeout: 30000 });
    await page.waitForTimeout(1500);
    await capture(page, artifactDir, "mode-selected");
    return { requested, selected: label, status: "selected" };
  }

  await page.keyboard.press("Escape").catch(() => {});
  return { requested, candidates: labels, status: "option_not_found" };
}

function preferredModeLabels(requested) {
  const labels = [requested];
  if (/think|reason|deep/i.test(requested)) {
    labels.push("Think Deeper", "Thinking", "Deep reasoning", "Reasoning", "GPT-5 Thinking", "GPT-5");
  }
  return [...new Set(labels)];
}

function cssString(value) {
  return String(value).replace(/\\/g, "\\\\").replace(/'/g, "\\'");
}

async function extractAnswer(page, promptText) {
  const selectors = [
    "[data-testid*='message' i]",
    "[data-content='ai-message']",
    "[class*='message' i]",
    "main",
    "[role='main']",
    "body",
  ];
  for (const selector of selectors) {
    const text = await page
      .locator(selector)
      .allTextContents()
      .then((parts) => parts.join("\n").trim())
      .catch(() => "");
    const cleaned = cleanText(text, promptText);
    if (cleaned.length > 200) {
      return cleaned;
    }
  }
  return cleanText(await page.locator("body").innerText().catch(() => ""), promptText);
}

function cleanText(text, promptText) {
  return String(text || "")
    .replace(promptText, "")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

async function capture(page, dir, name) {
  await fs.mkdir(dir, { recursive: true });
  await page.screenshot({ path: path.join(dir, `${name}.png`), fullPage: true }).catch(() => {});
  await fs.writeFile(path.join(dir, `${name}.html`), await page.content(), "utf8").catch(() => {});
}

async function writeOutput(file, record) {
  await fs.writeFile(file, `${JSON.stringify(record, null, 2)}\n`, "utf8");
}

function parseArgs(rawArgs) {
  const parsed = {};
  for (let index = 0; index < rawArgs.length; index += 1) {
    const token = rawArgs[index];
    if (!token.startsWith("--")) {
      continue;
    }
    const key = token.slice(2);
    const next = rawArgs[index + 1];
    if (!next || next.startsWith("--")) {
      parsed[key] = true;
      continue;
    }
    parsed[key] = next;
    index += 1;
  }
  return parsed;
}

function required(value, name) {
  if (!value) {
    throw new Error(`Missing required argument ${name}`);
  }
  return value;
}
