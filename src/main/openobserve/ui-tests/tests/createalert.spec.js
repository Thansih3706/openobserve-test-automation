const { LoginPage } = require('../pages/login.page');
const { TemplatePage } = require('../pages/template.page');
const { DestinationPage } = require('../pages/destination.page');
const { AlertsPage } = require('../pages/alerts.page');
const { ingestLogs, searchLogs } = require('../helpers/api.helper');
const { createAlertTestData } = require('../helpers/test-data.helper');
const { test, expect } = require('../fixtures/test-options');

test.describe('Module 2 - Alerts', () => {
  test('create template, destination, realtime alert, trigger it, and verify destination stream', async ({
    page,
    request,
    username,
    password,
  }) => {
    const loginPage = new LoginPage(page);
    const templatePage = new TemplatePage(page);
    const destinationPage = new DestinationPage(page);
    const alertsPage = new AlertsPage(page);

    const {
      sourceStream,
      destinationStream,
      templateName,
      destinationName,
      alertName,
      value,
      column,
      header,
      headerValue,
      templateBody,
    } = createAlertTestData();

    await test.step('Login to OpenObserve', async () => {
      if (!username || !password) {
        throw new Error('Missing USERNAME or PASSWORD in .env');
      }

      await loginPage.goto();
      await loginPage.login(username, password);
    });

    await test.step('Seed source stream so it exists in alert setup', async () => {
      const seedResponse = await ingestLogs(request, sourceStream, [
        { level: 'info', message: 'seed stream' },
      ]);

      expect(seedResponse.status()).toBe(200);
    });

    await test.step('Open alerts page', async () => {
      await alertsPage.goto();
    });

    await test.step('Create template', async () => {
      await templatePage.createNewTemplate(templateName, templateBody);
    });

    await test.step('Create destination pointing to another stream', async () => {
      await destinationPage.createNewDestination(
        destinationName,
        destinationStream,
        templateName,
        header,
        headerValue
      );
    });

    await test.step('Create real-time alert with condition level Contains error', async () => {
      await alertsPage.createRealTimeAlert(
        alertName,
        sourceStream,
        destinationName,
        column,
        value
      );
    });

    await test.step('Trigger alert by ingesting matching log', async () => {
      const payload = [
        { level: 'error', message: 'trigger alert now' },
      ];

      const triggerResponse = await ingestLogs(request, sourceStream, payload);
      expect(triggerResponse.status()).toBe(200);
    });

    await test.step('Verify destination stream receives alert data with expected fields', async () => {
      let hits = [];
      let lastStatus = null;

      for (let attempt = 1; attempt <= 6; attempt++) {
        const response = await searchLogs(request, destinationStream, 30);
        lastStatus = response.status();

        if (lastStatus !== 200) {
          continue;
        }

        const body = await response.json();
        hits = body.hits || [];

        if (hits.length > 0) {
          break;
        }

      }

      expect(lastStatus, `Destination stream search failed after retries`).toBe(200);
      expect(Array.isArray(hits)).toBeTruthy();
      expect(hits.length).toBeGreaterThan(0);

      const matchingAlert = hits.find(
        (hit) =>
          hit.alert_name === alertName &&
          hit.stream_name === sourceStream
      );

      expect(matchingAlert).toBeTruthy();
      expect(matchingAlert.org_name).toBe('default');
      expect(matchingAlert.alert_type).toBeTruthy();
      expect(matchingAlert.timestamp).toBeTruthy();
    });
  });
});