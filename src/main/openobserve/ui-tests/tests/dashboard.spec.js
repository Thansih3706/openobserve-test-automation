const { LoginPage } = require('../pages/login.page');
const { DashboardPage } = require('../pages/dashboards.page');
const { ingestLogs } = require('../helpers/api.helper');
const { test, expect } = require('../fixtures/test-options');
const { createDashboardTestData } = require('../helpers/test-data.helper');

test.describe('Module 3 - Dashboard', () => {
  test('create dashboard with panel based on ingested data and verify panel is not empty', async ({ username, password, page, request }) => {
    const loginPage = new LoginPage(page);
    const dashboardPage = new DashboardPage(page);
    const { streamName, dashboardName, panelName, logs } = createDashboardTestData();

    await test.step('Login to OpenObserve', async () => {
      if (!username || !password) {
        throw new Error('Missing USERNAME or PASSWORD in .env');
      }
      await loginPage.goto();
      await loginPage.login(username, password);
    });

    await test.step('Seed logs for dashboard panel', async () => {
      const payload = logs;

      const response = await ingestLogs(request, streamName, payload);
      const responseText = await response.text();

      console.log('🔹 Dashboard seed URL:', `/api/default/${streamName}/_json`);
      console.log('🔹 Dashboard seed payload:', JSON.stringify(payload, null, 2));
      console.log('🔹 Dashboard seed status:', response.status());
      console.log('🔹 Dashboard seed response:', responseText);

      await test.info().attach('Dashboard Seed Payload', {
        body: JSON.stringify(payload, null, 2),
        contentType: 'application/json',
      });

      await test.info().attach('Dashboard Seed Response', {
        body: responseText,
        contentType: 'application/json',
      });

      expect(response.status()).toBe(200);
    });

    await test.step('Navigate to Dashboards and create a dashboard', async () => {
      await dashboardPage.navigateToDashboards();
      await dashboardPage.createDashboard(dashboardName);
    });

    await test.step('Add panel with SQL query against seeded stream', async () => {
        await dashboardPage.openAddPanel();
        await dashboardPage.selectStream(streamName);
        await dashboardPage.switchToSqlModeIfNeeded();
        await dashboardPage.enterQuery(`SELECT * FROM "${streamName}"`);
        await dashboardPage.setTimeRangeLast15Minutes();
        await dashboardPage.setPanelName(panelName);
        await dashboardPage.applyPanel();
        await dashboardPage.addFieldsToPanel(['code', 'level', 'message']);
        await dashboardPage.savePanelIfVisible();
        
      });

    await test.step('Verify panel is not empty', async () => {
      await dashboardPage.verifyPanelHasData();
      await expect(page.getByText(panelName, { exact: true })).toBeVisible();
    });
  });
});