import { expect, test } from '@playwright/test';

test.describe('Dark Data Workbench mobile layout', () => {
  test('collapses panels without horizontal overflow', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { name: 'Dark Data Workbench' })).toBeVisible();
    await expect(page.getByText('ready')).toBeVisible();
    await expect(page.getByRole('searchbox', { name: /Search sources/i })).toBeVisible();

    const hasHorizontalOverflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
    expect(hasHorizontalOverflow).toBe(false);

    await page.getByRole('button', { name: 'Checks' }).click();
    await expect(page.getByRole('heading', { name: 'No-AI Saved Checks' })).toBeVisible();
  });
});
