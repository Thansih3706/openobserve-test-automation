const { test, expect } = require('../fixtures/test-options');
const { LoginPage } = require('../pages/login.page');
const { PipelinesPage } = require('../pages/pipelines.page');
const { ingestLogs, searchLogs } = require('../helpers/api.helper');
const { createPipelineTestData } = require('../helpers/test-data.helper');

test.describe('Module 4 - Pipeline', () => {
  test('create pipeline from source stream to destination stream and verify routed data', async ({ username,
    password, page, request }) => {
    const loginPage = new LoginPage(page);
    const pipelinesPage = new PipelinesPage(page);
    const {
        sourceStream,
        destinationStream,
        pipelineName,
        streamType,
        seedPayload,
        triggerPayload,
      } = createPipelineTestData();

    await test.step('Login to OpenObserve', async () => {
        if (!username || !password) {
          throw new Error('Missing USERNAME or PASSWORD in .env');
        }
  
        await loginPage.goto();
        await loginPage.login(username, password);
      });

    await test.step('Seed source stream so it exists in pipeline stream selection', async () => {;

      const seedResponse = await ingestLogs(request, sourceStream, seedPayload);
      const seedText = await seedResponse.text();

      console.log('🔹 Seed source stream payload:', JSON.stringify(seedPayload, null, 2));
      console.log('🔹 Seed response status:', seedResponse.status());
      console.log('🔹 Seed response body:', seedText);

      expect(seedResponse.status()).toBe(200);
    });

    await test.step('Open pipeline page and create source/destination stream pipeline', async () => {
      await pipelinesPage.openPipelineMenu();
      await pipelinesPage.addPipeline();

      await pipelinesPage.addSourceStreamNode(streamType,sourceStream);
      await pipelinesPage.deleteAutoCreatedOutputNodeIfPresent(destinationStream);
      await pipelinesPage.addDestinationStreamNode(streamType,destinationStream);
      await pipelinesPage.connectExistingStreamNodes(sourceStream, destinationStream);
      await pipelinesPage.logEdgeCount();
      await pipelinesPage.savePipeline(pipelineName);
    });

    await test.step('Trigger pipeline by ingesting fresh data into source stream', async () => {;

      const triggerResponse = await ingestLogs(request, sourceStream, triggerPayload);
      const triggerText = await triggerResponse.text();

      console.log('🔹 Trigger payload:', JSON.stringify(triggerPayload, null, 2));
      console.log('🔹 Trigger response status:', triggerResponse.status());
      console.log('🔹 Trigger response body:', triggerText);

      await test.info().attach('Pipeline Trigger Payload', {
        body: JSON.stringify(triggerPayload, null, 2),
        contentType: 'application/json',
      });

      await test.info().attach('Pipeline Trigger Response', {
        body: triggerText,
        contentType: 'application/json',
      });

      expect(triggerResponse.status()).toBe(200);
    });

    await test.step('Verify routed data appears in destination stream', async () => {
      let hits = [];
      let lastStatus = null;
      let lastBodyText = '';

      for (let attempt = 1; attempt <= 6; attempt++) {
        const response = await searchLogs(request, destinationStream, 30);
        lastStatus = response.status();
        lastBodyText = await response.text();

        console.log(`🔄 Pipeline search attempt ${attempt}`);
        console.log('🔹 Destination stream:', destinationStream);
        console.log('🔹 Search status:', lastStatus);
        console.log('🔹 Search body:', lastBodyText);

        await test.info().attach(`Pipeline Search Attempt ${attempt}`, {
          body: lastBodyText,
          contentType: 'application/json',
        });

        if (lastStatus !== 200) {
        
          continue;
        }

        const body = JSON.parse(lastBodyText);
        hits = body.hits || [];

        if (hits.length > 0) {
          break;
        }
      }

      expect(lastStatus, `Destination stream was not created. Last response: ${lastBodyText}`).toBe(200);
      expect(Array.isArray(hits)).toBeTruthy();
      expect(hits.length).toBeGreaterThan(0);

      const matchingRecord = hits.find(
        hit =>
          hit.message === 'trigger pipeline routing' &&
          hit.level === 'error'
      );

      expect(matchingRecord).toBeTruthy();
    });
  });
});