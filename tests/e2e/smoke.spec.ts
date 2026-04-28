import { expect, test } from "@playwright/test";

test("redirects the root route to add", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveURL(/\/add$/);
});
