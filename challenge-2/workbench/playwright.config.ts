import { defineConfig, devices } from '@playwright/test';

const PORT = process.env.PORT ?? '5174';
const baseURL = process.env.PLAYWRIGHT_BASE_URL ?? `http://127.0.0.1:${PORT}`;
const skipWebServer = process.env.PLAYWRIGHT_SKIP_WEBSERVER === '1';

export default defineConfig({
  testDir: 'tests/ui',
  timeout: 30000,
  expect: {
    timeout: 10000,
  },
  use: {
    baseURL,
    headless: true,
    acceptDownloads: true,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      testIgnore: /mobile\.spec\.ts/,
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'mobile-chromium',
      testMatch: /mobile\.spec\.ts/,
      use: { ...devices['Pixel 7'] },
    },
  ],
  webServer: skipWebServer
    ? undefined
    : {
        command: `pnpm dev --host 127.0.0.1 --port ${PORT} --strictPort true`,
        url: baseURL,
        reuseExistingServer: true,
        timeout: 180000,
      },
});
