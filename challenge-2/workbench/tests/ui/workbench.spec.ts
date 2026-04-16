import { expect, test, type Locator, type Page } from '@playwright/test';

const pressButton = async (button: Locator) => {
  await button.scrollIntoViewIfNeeded();
  await expect(button).toBeVisible();
  await button.click();
  try {
    await expect(button).toHaveClass(/active/, { timeout: 1000 });
  } catch {
    await button.dispatchEvent('click');
    await expect(button).toHaveClass(/active/, { timeout: 1000 });
  }
};

const switchView = async (page: Page, name: string, selector: string) => {
  await pressButton(page.getByRole('button', { name }));
  await expect(page.locator(selector)).toBeVisible();
};

test.describe('Dark Data Workbench', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { name: 'Dark Data Workbench' })).toBeVisible();
    await expect(page.getByText('ready')).toBeVisible();
  });

  test('loads the Challenge 2 corpus and supports search', async ({ page }) => {
    await expect(page.getByText('43', { exact: true }).first()).toBeVisible();
    await expect(page.locator('.source-card')).toHaveCount(43);

    await page.getByRole('searchbox', { name: /Search sources/i }).fill('DOC-HB-002');

    await expect(page.locator('.source-card')).toHaveCount(1);
    await expect(page.locator('.source-card')).toContainText('Discretionary Housing Payments');
  });

  test('filters by status, topic, and department', async ({ page }) => {
    const currentStatus = page.getByRole('group', { name: /Facet Status/i }).getByRole('button', { name: /^current\b/i });
    await pressButton(currentStatus);
    await expect(page.locator('.stage-toolbar h2')).toContainText('17 visible sources');
    const currentCount = await page.locator('.source-card').count();
    expect(currentCount).toBeGreaterThan(10);
    expect(currentCount).toBeLessThan(43);

    const housingTopic = page.getByRole('group', { name: /Facet Topic/i }).getByRole('button', { name: /^housing-benefit\b/i });
    await pressButton(housingTopic);
    await expect(page.locator('.stage-toolbar h2')).not.toContainText('17 visible sources');
    const topicCount = await page.locator('.source-card').count();
    expect(topicCount).toBeGreaterThan(0);
    expect(topicCount).toBeLessThanOrEqual(currentCount);

    const dluhc = page.getByRole('group', { name: /Facet Department/i }).getByRole('button', { name: /^DLUHC 9$/i });
    await pressButton(dluhc);
    await expect(page.locator('.source-card').first()).toContainText('DLUHC');
  });

  test('adds sources to context, saves, and reopens a context set', async ({ page }) => {
    await page.getByRole('searchbox', { name: /Search sources/i }).fill('DOC-HB-002');
    await expect(page.locator('.source-card')).toHaveCount(1);
    await page.locator('.source-card').getByRole('button', { name: 'Add' }).click();
    await expect(page.getByLabel('Context set')).toContainText('1 selected');

    await page.getByLabel('Context name').fill('Demo Context');
    await page.getByRole('button', { name: /^Save$/ }).click();
    await expect(page.getByText('Demo Context (1)')).toBeVisible();

    await page.getByRole('button', { name: 'Clear context' }).click();
    await expect(page.getByLabel('Context set')).toContainText('0 selected');

    await page.getByText('Demo Context (1)').locator('..').getByRole('button', { name: 'Open' }).click();
    await expect(page.getByLabel('Context set')).toContainText('1 selected');
  });

  test('opens the reader with metadata and provenance links', async ({ page }) => {
    await page.getByRole('searchbox', { name: /Search sources/i }).fill('DOC-HB-002');
    await expect(page.locator('.source-card')).toHaveCount(1);
    await page.locator('.source-card').getByRole('button', { name: 'Open' }).click();

    await expect(page.getByRole('heading', { name: /Discretionary Housing Payments/i })).toBeVisible();
    const readerMetadata = page.locator('.metadata-table');
    await expect(readerMetadata.getByText('Raw source')).toBeVisible();
    await expect(readerMetadata.getByText('structured_files/DOC-HB-002-discretionary-housing-payments.md')).toBeVisible();
    await expect(readerMetadata.getByText('wiki/sources/doc-hb-002')).toBeVisible();
  });

  test('runs the five no-AI saved checks with source-backed results', async ({ page }) => {
    await switchView(page, 'Checks', '.checks-view');

    const checks = [
      'Current CTR guidance',
      'Self-employed HB',
      'Staff policy risks',
      'IT hardware over GBP 5,000',
      'DHP mentions',
    ];

    for (const check of checks) {
      await pressButton(page.getByRole('button', { name: new RegExp(check) }));
      await expect(page.locator('.query-results .result-row').first()).toBeVisible();
    }

    await pressButton(page.getByRole('button', { name: 'Current CTR guidance' }));
    await expect(page.locator('.query-results')).toContainText('DOC-HB-009');
    await expect(page.locator('.query-results')).not.toContainText('DOC-HB-003');
  });

  test('exports browser AI context and renders MCP setup', async ({ page }) => {
    await page.getByRole('searchbox', { name: /Search sources/i }).fill('DOC-HB-002');
    await expect(page.locator('.source-card')).toHaveCount(1);
    await page.locator('.source-card').getByRole('button', { name: 'Add' }).click();
    await page.getByRole('button', { name: 'Browser AI' }).click();

    const downloadPromise = page.waitForEvent('download');
    await page.getByRole('button', { name: 'Download JSON' }).click();
    const download = await downloadPromise;
    expect(download.suggestedFilename()).toBe('dark-data-context.json');

    const path = await download.path();
    expect(path).toBeTruthy();
    const json = JSON.parse(await (await import('node:fs/promises')).readFile(path!, 'utf-8'));
    expect(json.sources[0].source_id).toBe('DOC-HB-002');
    expect(json.instructions.synthetic_data_notice).toContain('synthetic');

    await page.getByRole('button', { name: 'MCP' }).click();
    await expect(page.getByText('python3 challenge-2/tools/workbench_mcp.py')).toBeVisible();
    await expect(page.getByText('workbench.search_sources')).toBeVisible();
  });

  test('renders graph and workbook table views', async ({ page }) => {
    await switchView(page, 'Graph', '.graph-view');
    await expect(page.locator('.graph-view svg')).toBeVisible();
    await expect(page.locator('.summary-meta')).toContainText('topic nodes');

    await switchView(page, 'Table', '.table-view');
    await expect(page.getByRole('heading', { name: 'Workbook Sources' })).toBeVisible();
    await expect(page.getByRole('heading', { name: /UF-PROCUREMENT-THRESHOLDS-2024-25/i })).toBeVisible();
  });
});
