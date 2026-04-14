const { test, expect } = require("@playwright/test");

test("homepage loads", async ({ page, baseURL }) => {
  await page.goto(baseURL);
  await expect(page).toHaveURL(/copychecker\.com/);
});
