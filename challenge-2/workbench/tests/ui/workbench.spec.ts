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

const facet = (page: Page, name: string) => page.getByRole('group', { name: new RegExp(`Facet ${name}`, 'i') });

const openFacet = async (page: Page, name: string) => {
  const group = facet(page, name);
  await group.getByRole('button', { name, exact: true }).click();
  await expect(group.locator('.facet-values')).toBeVisible();
  return group;
};

test.describe('Dark Data Workbench', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { name: 'Dark Data Workbench' })).toBeVisible();
    await expect(page.getByText('ready', { exact: true })).toBeVisible();
  });

  test('loads the Challenge 2 corpus and supports search', async ({ page }) => {
    await expect(page.getByText('43', { exact: true }).first()).toBeVisible();
    await expect(page.locator('.source-card')).toHaveCount(43);

    await page.getByLabel('Question to answer').fill('Which DHP guidance should an adviser cite?');
    await expect(page.getByLabel('Question to answer')).toHaveValue('Which DHP guidance should an adviser cite?');

    await page.getByRole('searchbox', { name: /Search sources/i }).fill('DOC-HB-002');

    await expect(page.locator('.source-card')).toHaveCount(1);
    await expect(page.locator('.source-card')).toContainText('Discretionary Housing Payments');
  });

  test('switches workbench packs through the header links without a manual reload', async ({ page }) => {
    await page.getByRole('link', { name: 'HMRC narrative pack' }).click();
    await expect(page.getByRole('heading', { name: 'HMRC Beyond The Hype Narrative Arc' })).toBeVisible();
    expect(new URL(page.url()).searchParams.get('pack')).toBe('hmrc-narrative');
    await expect(page.locator('.source-card')).toHaveCount(234);

    await page.getByRole('link', { name: 'Challenge 2 corpus' }).click();
    await expect(page.locator('.topbar h1')).toHaveText('Dark Data Workbench');
    expect(new URL(page.url()).searchParams.get('pack')).toBeNull();
    await expect(page.locator('.source-card')).toHaveCount(43);
  });

  test('filters by status, topic, and department', async ({ page }) => {
    const statusFacet = await openFacet(page, 'Status');
    const currentStatus = statusFacet.getByRole('button', { name: /^current\b/i });
    await pressButton(currentStatus);
    await expect(page.locator('.stage-toolbar h2')).toContainText('17 visible sources');
    const currentCount = await page.locator('.source-card').count();
    expect(currentCount).toBeGreaterThan(10);
    expect(currentCount).toBeLessThan(43);

    const topicFacet = await openFacet(page, 'Topic');
    const housingTopic = topicFacet.getByRole('button', { name: /^housing-benefit\b/i });
    await pressButton(housingTopic);
    await expect(page.locator('.stage-toolbar h2')).not.toContainText('17 visible sources');
    const topicCount = await page.locator('.source-card').count();
    expect(topicCount).toBeGreaterThan(0);
    expect(topicCount).toBeLessThanOrEqual(currentCount);

    const departmentFacet = await openFacet(page, 'Department');
    const dluhc = departmentFacet.getByRole('button', { name: /^DLUHC\b/i });
    await pressButton(dluhc);
    await expect(page.locator('.source-card').first()).toContainText('DLUHC');
  });

  test('folds facets by default, preserves active facets, and respects pins', async ({ page }) => {
    const statusFacet = facet(page, 'Status');
    const departmentFacet = facet(page, 'Department');
    const topicFacet = facet(page, 'Topic');

    await expect(statusFacet.locator('.facet-values')).toHaveCount(0);
    await expect(departmentFacet.locator('.facet-values')).toHaveCount(0);

    await openFacet(page, 'Status');
    await expect(statusFacet.getByRole('button', { name: /^current\b/i })).toBeVisible();

    await openFacet(page, 'Department');
    await expect(statusFacet.locator('.facet-values')).toHaveCount(0);
    await expect(departmentFacet.getByRole('button', { name: /^DWP\b/i })).toBeVisible();

    await openFacet(page, 'Status');
    await statusFacet.getByRole('button', { name: /^current\b/i }).click();
    await openFacet(page, 'Department');
    await expect(statusFacet.getByRole('button', { name: /^current\b/i })).toBeVisible();

    await departmentFacet.getByRole('button', { name: /^Pin Department$/ }).click();
    await openFacet(page, 'Topic');
    await expect(departmentFacet.locator('.facet-values')).toBeVisible();
    await expect(topicFacet.getByRole('button', { name: /^housing-benefit\b/i })).toBeVisible();
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

    await expect(page.locator('.reader-heading h2')).toContainText('Discretionary Housing Payments');
    const readerMetadata = page.locator('.metadata-table');
    await expect(readerMetadata.getByText('Raw source')).toBeVisible();
    await expect(readerMetadata.getByText('structured_files/DOC-HB-002-discretionary-housing-payments.md')).toBeVisible();
    await expect(readerMetadata.getByText('wiki/sources/doc-hb-002')).toBeVisible();

    const noteHref = await page.getByRole('link', { name: 'Open note' }).getAttribute('href');
    expect(noteHref).toBeTruthy();
    const noteResponse = await page.request.get(new URL(noteHref!, page.url()).toString());
    expect(noteResponse.status()).toBe(200);
    expect(await noteResponse.text()).toContain('DOC-HB-002');

    await expect(page.getByRole('button', { name: 'Preview', exact: true })).toHaveClass(/active/);
    await expect(page.locator('.note-preview h1').first()).toContainText('Discretionary Housing Payments');
    await expect(page.locator('.note-preview table').first()).toContainText('Source ID');
    await expect(page.locator('.note-preview')).not.toContainText('source_id: "DOC-HB-002"');

    await page.getByRole('button', { name: 'Text', exact: true }).click();
    await expect(page.locator('.note-reader')).toContainText('source_id: "DOC-HB-002"');
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
    await expect(page.getByLabel('Question to answer')).toHaveValue('Which Council Tax Reduction guidance is current?');
    await expect(page.locator('.query-results')).toContainText('DOC-HB-009');
    await expect(page.locator('.query-results')).not.toContainText('DOC-HB-003');
  });

  test('exports browser AI context and renders MCP setup', async ({ page }) => {
    await page.getByRole('searchbox', { name: /Search sources/i }).fill('DOC-HB-002');
    await page.getByLabel('Question to answer').fill('What are the gateway conditions for Discretionary Housing Payments?');
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
    expect(json.view.question).toBe('What are the gateway conditions for Discretionary Housing Payments?');
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

  test('loads the HMRC narrative datapack with thumbnails and SeeLinks-style highlight controls', async ({ page }) => {
    await page.goto('/?pack=hmrc-narrative');
    await expect(page.getByRole('heading', { name: 'HMRC Beyond The Hype Narrative Arc' })).toBeVisible();
    await expect(page.locator('.source-card')).toHaveCount(234);
    await expect(page.locator('.thumbnail-button img[src*="assets/visuals"]')).toHaveCount(73);

    const sourceFamilyFacet = await openFacet(page, 'Source Family');
    await sourceFamilyFacet.getByRole('button', { name: /^Challenge 2 visuals\b/i }).click();
    await expect(page.locator('.source-card')).toHaveCount(23);

    await page.locator('.source-card').first().getByRole('button', { name: 'Open', exact: true }).click();
    await expect(page.locator('.reader-heading h2')).toContainText('Challenge 2 Unlocking Dark Data - Slide 01');
    const narrativeNoteHref = await page.getByRole('link', { name: 'Open note' }).getAttribute('href');
    expect(narrativeNoteHref).toContain('/api/source-note/hmrc-challenge-2-unlocking-dark-data-01');
    const narrativeNoteResponse = await page.request.get(new URL(narrativeNoteHref!, page.url()).toString());
    expect(narrativeNoteResponse.status()).toBe(200);
    expect(await narrativeNoteResponse.text()).toContain('Challenge 2 Unlocking Dark Data - Slide 01');
    await page.getByRole('button', { name: 'Grid' }).click();

    await page.locator('.source-card').first().getByRole('button', { name: 'Mark' }).click();
    await expect(page.locator('.source-card').first()).toHaveClass(/highlighted/);
    await page.getByRole('button', { name: 'Keep marked' }).click();
    await expect(page.locator('.source-card')).toHaveCount(1);
    await page.getByRole('button', { name: 'Restore' }).click();
    await expect(page.locator('.source-card')).toHaveCount(23);

    const dragPayload = await page.evaluateHandle(() => new DataTransfer());
    await page.getByRole('button', { name: 'Talk Section', exact: true }).dispatchEvent('dragstart', { dataTransfer: dragPayload });
    await page.locator('.source-grid').dispatchEvent('dragenter', { dataTransfer: dragPayload });
    await page.locator('.source-grid').dispatchEvent('dragover', { dataTransfer: dragPayload });
    await page.locator('.source-grid').dispatchEvent('drop', { dataTransfer: dragPayload });
    await expect(page.locator('.colour-legend')).toContainText('Talk Section');
    await expect(page.locator('.source-card').first()).toHaveAttribute('style', /--source-card-bg/);
  });

  test('supports SeeLinks parity controls on the HMRC pack', async ({ page }) => {
    await page.goto('/?pack=hmrc-narrative');
    await expect(page.locator('.source-card')).toHaveCount(234);

    const orderDrop = page.locator('.order-panel');
    const sourceFamilyTitle = page.getByRole('button', { name: 'Source Family', exact: true }).first();
    const orderPayload = await page.evaluateHandle(() => new DataTransfer());
    await sourceFamilyTitle.dispatchEvent('dragstart', { dataTransfer: orderPayload });
    await page.locator('.order-list').dispatchEvent('dragenter', { dataTransfer: orderPayload });
    await page.locator('.order-list').dispatchEvent('dragover', { dataTransfer: orderPayload });
    await page.locator('.order-list').dispatchEvent('drop', { dataTransfer: orderPayload });
    await expect(orderDrop).toContainText('Source Family');
    await orderDrop.getByRole('button', { name: 'Reverse Source Family' }).click();
    await expect(orderDrop.locator('.order-index')).toHaveText('1↓');

    await expect(page.getByRole('group', { name: /Facet Topic Group/i })).toHaveCount(0);
    await page.getByLabel('Metadata').check();
    await expect(page.getByRole('group', { name: /Facet Topic Group/i })).toBeVisible();

    const talkSection = page.getByRole('group', { name: /Facet Talk Section/i });
    await talkSection.getByRole('button', { name: /^Pin Talk Section$/ }).click();
    await expect(talkSection.getByRole('button', { name: /^Unpin Talk Section$/ })).toBeVisible();
    await talkSection.getByRole('button', { name: 'Auto order' }).click();
    await expect(talkSection.getByRole('button', { name: 'Clear order' })).toBeEnabled();

    const sourceFamily = await openFacet(page, 'Source Family');
    await sourceFamily.getByRole('button', { name: /^Challenge 2 visuals\b/i }).click({ button: 'right' });
    await expect(page.locator('.stage-toolbar')).toContainText('23 marked in view');
    await page.getByRole('button', { name: 'Choose highlighted' }).click();
    await expect(page.locator('.source-card')).toHaveCount(23);
    await page.getByRole('button', { name: 'Undo view' }).click();
    await expect(page.locator('.source-card')).toHaveCount(234);

    const rollupPayload = await page.evaluateHandle(() => new DataTransfer());
    await sourceFamily.getByRole('button', { name: /^Challenge 2 visuals\b/i }).dispatchEvent('dragstart', { dataTransfer: rollupPayload });
    await page.locator('.source-grid').dispatchEvent('dragenter', { dataTransfer: rollupPayload });
    await page.locator('.source-grid').dispatchEvent('dragover', { dataTransfer: rollupPayload });
    await page.locator('.source-grid').dispatchEvent('drop', { dataTransfer: rollupPayload });
    await expect(page.locator('.rollup-card')).toContainText('Challenge 2 visuals');

    await page.locator('.source-card:not(.rollup-card)').first().dblclick();
    await expect(page.locator('.detail-dock')).toBeVisible();
    await expect(page.getByRole('button', { name: /Images/ })).toBeVisible();
    await expect(page.locator('.detail-links a').first()).toBeVisible();

    await page.getByLabel('Tile title field').selectOption('sourceId');
    await expect(page.locator('.source-card:not(.rollup-card)').first().locator('h3')).toContainText(/^hmrc-/);
  });

  test('double-clicking a facet value reduces the view without losing the selected value', async ({ page }) => {
    await page.goto('/?pack=hmrc-narrative');
    const sourceFamily = await openFacet(page, 'Source Family');

    await sourceFamily.getByRole('button', { name: /^Challenge 2 visuals\b/i }).dblclick();

    await expect(page.locator('.source-card')).toHaveCount(23);
    await expect(page.locator('.stage-toolbar')).toContainText('Highlighted');
    await expect(sourceFamily.getByRole('button', { name: /^Challenge 2 visuals\b/i })).toHaveClass(/active/);
  });

  test('saves local collections and renders outline and timeline views', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('.source-card')).toHaveCount(43);
    await page.locator('.source-card').first().getByRole('button', { name: 'Add' }).click();
    await page.getByLabel('Collection name').fill('UI parity smoke');
    await page.getByRole('button', { name: 'Save collection' }).click();
    await expect(page.getByText('UI parity smoke (1)')).toBeVisible();

    await page.getByText('UI parity smoke (1)').locator('..').getByRole('button', { name: 'Open' }).click();
    await expect(page.locator('.source-card')).toHaveCount(1);

    await switchView(page, 'Outline', '.outline-view');
    await expect(page.locator('.outline-group').first()).toBeVisible();
    await switchView(page, 'Timeline', '.timeline-view');
    await expect(page.locator('.timeline-group').first()).toBeVisible();
  });
});
