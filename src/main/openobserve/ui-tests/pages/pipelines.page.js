const { expect } = require('@playwright/test');

class PipelinesPage {
  constructor(page) {
    this.page = page;
    this.pipelineMenu = page.locator('[data-test="menu-link-\\/pipeline-item"]');
    this.pipelineTab = page.locator('[data-test="stream-pipelines-tab"]');
    this.addPipelineButton = page.locator('[data-test="pipeline-list-add-pipeline-btn"]');
    this.streamButton = page.getByRole('button', { name: 'Stream' }).first();
    this.canvas = page.locator('.vue-flow__pane');
    this.streamTypeSelect = page.locator('[data-test="input-node-stream-type-select"]').first();
    this.streamNameInput = page.getByLabel('Stream Name *');
    this.inputNodeSaveButton = page.locator('[data-test="input-node-stream-save-btn"]');
    this.pipelineNameInput = page.locator('input[placeholder="Enter Pipeline Name"]');
    this.savePipelineButton = page.locator('[data-test="add-pipeline-save-btn"]');
    this.confirmButton = page.locator('[data-test="confirm-button"]');
    this.pipelineSavedMessage = page.getByText('Pipeline saved successfully');
  }

  async openPipelineMenu() {
    await this.pipelineMenu.click();
    await this.pipelineTab.click();
    await expect(this.addPipelineButton).toBeVisible();
  }

  async addPipeline() {
    await this.addPipelineButton.click();
  }

  async dragNodeToCanvas(nodeLocator, offset = { x: 0, y: 0 }) {
    const canvasBox = await this.canvas.boundingBox();
    const nodeBox = await nodeLocator.boundingBox();

    if (!canvasBox || !nodeBox) {
      throw new Error('Unable to get bounding box for drag and drop');
    }

    await this.page.mouse.move(
      nodeBox.x + nodeBox.width / 2,
      nodeBox.y + nodeBox.height / 2
    );
    await this.page.mouse.down();
    await this.page.mouse.move(
      canvasBox.x + canvasBox.width / 2 + offset.x,
      canvasBox.y + canvasBox.height / 2 + offset.y
    );
    await this.page.mouse.up();
  }

  async addSourceStreamNode(streamType, streamName) {
    await this.streamButton.click();
    await this.dragNodeToCanvas(this.streamButton, { x: -120, y: -40 });
    const streamTypeOption = this.page.getByRole('option', { name: streamType, exact: true });
    if (await streamTypeOption.isVisible().catch(() => false)) {
      await streamTypeOption.click();
    }
    await this.streamNameInput.fill(streamName);
    await this.page.getByRole('option', { name: streamName, exact: true }).click();
    await this.inputNodeSaveButton.click();
  }

  async deleteAutoCreatedOutputNodeIfPresent(destinationStream) {
    const outputNodes = this.page.locator('[data-test="pipeline-node-output-stream-node"]');
    const count = await outputNodes.count();
  
    for (let i = 0; i < count; i++) {
      const node = outputNodes.nth(i);
      const text = await node.textContent();
  
      if (!text || !text.includes(destinationStream)) {
        await node.hover();
        await this.page.locator('[data-test="pipeline-node-output-delete-btn"]').nth(i).click();
        await this.confirmButton.click();
        return;
      }
    }
  }

  async addDestinationStreamNode(streamType, streamName) {
    const streamNodeButton = this.page.getByRole('button', { name: 'Stream' }).nth(1);
  
    await streamNodeButton.click();
    await this.dragNodeToCanvas(streamNodeButton, { x: 120, y: 60 });
  
    const streamTypeOption = this.page.getByRole('option', { name: streamType, exact: true });
    if (await streamTypeOption.isVisible().catch(() => false)) {
      await streamTypeOption.click();
    }
  
    await this.streamNameInput.fill(streamName);
    await this.inputNodeSaveButton.click();
  }

  async logEdgeCount() {
    const edges = this.page.locator('.vue-flow__edge, .vue-flow__edge-path');
    const count = await edges.count();
    console.log('🔹 Edge count:', count);
    expect(count).toBeGreaterThan(0);
  }

  async connectExistingStreamNodes(sourceStreamName, destinationStreamName) {
    await expect(this.page.getByText(sourceStreamName, { exact: false }).first()).toBeVisible({
      timeout: 15000,
    });
    await expect(this.page.getByText(destinationStreamName, { exact: false }).first()).toBeVisible({
      timeout: 15000,
    });

    const initialEdgeCount = await this.getEdgeCount();
    let connected = false;
    const sourceNode = this.findStreamNodeByName(sourceStreamName);
    const destinationNode = this.findStreamNodeByName(destinationStreamName);
    const sourceNodeCount = await sourceNode.count();
    const destinationNodeCount = await destinationNode.count();

    if (sourceNodeCount > 0 && destinationNodeCount > 0) {
      const sourceHandle = sourceNode
        .locator('[data-test="pipeline-node-input-output-handle"]')
        .first();
      const destinationHandle = destinationNode
        .locator('[data-test="pipeline-node-output-input-handle"]')
        .first();
      connected = await this.tryConnectWithRetry(sourceHandle, destinationHandle, initialEdgeCount);
    }
    if (!connected) {
      const sourceHandle = this.page.locator('[data-test="pipeline-node-input-output-handle"]').first();
      const destinationHandle = this.page.locator('[data-test="pipeline-node-output-input-handle"]').last();
      connected = await this.tryConnectWithRetry(sourceHandle, destinationHandle, initialEdgeCount);
    }

    if (!connected) {
      throw new Error(
        `Pipeline nodes were found but connection was not created for "${sourceStreamName}" -> "${destinationStreamName}".`
      );
    }
  }

  findStreamNodeByName(streamName) {
    const escapedName = streamName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    return this.page
      .getByRole('group')
      .filter({
        hasText: new RegExp(`(?:^|\\s)(?:logs\\s*-\\s*)?${escapedName}(?:\\s|$)`, 'i'),
      })
      .first();
  }

  async dragBetweenHandles(sourceHandle, destinationHandle) {
    await sourceHandle.waitFor({ state: 'visible', timeout: 10000 });
    await destinationHandle.waitFor({ state: 'visible', timeout: 10000 });

    const sourceBox = await sourceHandle.boundingBox();
    const destinationBox = await destinationHandle.boundingBox();

    if (!sourceBox || !destinationBox) {
      throw new Error('Could not find connector handles for pipeline node connection.');
    }

    await this.page.mouse.move(
      sourceBox.x + sourceBox.width / 2,
      sourceBox.y + sourceBox.height / 2
    );
    await this.page.mouse.down();
    await this.page.mouse.move(
      destinationBox.x + destinationBox.width / 2,
      destinationBox.y + destinationBox.height / 2,
      { steps: 20 }
    );
    await this.page.mouse.up();
  }

  async getEdgeCount() {
    return this.page.locator('.vue-flow__edge').count();
  }

  async tryConnectWithRetry(sourceHandle, destinationHandle, initialEdgeCount, maxAttempts = 3) {
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      await this.dragBetweenHandles(sourceHandle, destinationHandle);

      const currentEdgeCount = await this.getEdgeCount();
      if (currentEdgeCount > initialEdgeCount || currentEdgeCount > 0) {
        return true;
      }
    }

    return false;
  }

  async savePipeline(pipelineName) {
    await this.pipelineNameInput.fill(pipelineName);
    await this.savePipelineButton.click();
    await expect(this.pipelineSavedMessage).toBeVisible({ timeout: 5000 });
  }
}

module.exports = { PipelinesPage };