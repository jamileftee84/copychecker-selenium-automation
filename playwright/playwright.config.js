// Playwright smoke scaffolding for the migration path.
const { defineConfig } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "./tests",
  timeout: 30000,
  use: {
    baseURL: process.env.BASE_URL || "https://copychecker.com/",
    headless: true,
    viewport: { width: 1440, height: 1080 },
  },
  reporter: [["list"]],
});
