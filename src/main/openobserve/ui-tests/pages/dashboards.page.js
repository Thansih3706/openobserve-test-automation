const { expect } = require('@playwright/test');

class DashboardPage {
  constructor(page) {
    this.page = page;

    this.dashboardsMenu = page.locator('[data-test="menu-link-\\/dashboards-item"]');
    this.newDashboardButton = page.locator('[data-test="dashboard-new"]');
    this.dashboardNameInput = page.locator('[data-test="add-dashboard-name"]');
    this.dashboardSubmitButton = page.locator('[data-test="dashboard-add-submit"]');

    this.addPanelButton = page.locator('[data-test="dashboard-if-no-panel-add-panel-btn"]');
    this.streamDropdown = page.locator('[data-test="index-dropdown-stream"]');
    this.panelNameInput = page.locator('[data-test="dashboard-panel-name"]');
    this.applyButton = page.locator('[data-test="dashboard-apply"]');
    this.savePanelButton = page.locator('[data-test="dashboard-panel-save"]');
    this.tableGraph = page.locator("//img[@src='/web/src/assets/images/dashboard/charts/table.png']")
    this.sqlModeButton = page.getByText('SQL', { exact: true });
    this.sqlCutomeToggle = page.locator('[data-test="dashboard-custom-query-type"]')
    this.queryEditor = page.locator('[data-test="dashboard-panel-query-editor"], textarea, .monaco-editor').first();

    this.noDataText = page.getByText(/no data/i);
  }

  async navigateToDashboards() {
    await this.dashboardsMenu.click();
    await this.page.waitForURL(/.*dashboards.*/);
    await expect(this.newDashboardButton).toBeVisible();
  }

  async createDashboard(dashboardName) {
    await this.newDashboardButton.click();
    await expect(this.dashboardNameInput).toBeVisible();
    await this.dashboardNameInput.fill(dashboardName);
    await expect(this.dashboardSubmitButton).toBeEnabled();
    await this.dashboardSubmitButton.click();
  }

  async openAddPanel() {
    await expect(this.addPanelButton).toBeVisible();
    await this.addPanelButton.click();
  }

  async selectStream(streamName) {
    await this.tableGraph.click();
    await this.streamDropdown.click();
    await this.streamDropdown.fill(streamName);
    await this.page.getByRole('option', { name: streamName, exact: true }).locator('div').nth(2).click();
  }

  async switchToSqlModeIfNeeded() {
    if (await this.sqlModeButton.isVisible().catch(() => false)) {
      await this.sqlModeButton.click();
    }
  }

  async enterQuery(sql) {
    const editorViewLines = this.page
      .locator('.monaco-editor .view-lines')
      .first();
  
    if (await editorViewLines.isVisible().catch(() => false)) {
      await this.sqlCutomeToggle.click();
      await editorViewLines.click();
  
      const selectAllKey = process.platform === 'darwin' ? 'Meta+A' : 'Control+A';
      await this.page.keyboard.press(selectAllKey);
      await this.page.keyboard.press('Backspace');
  
      await this.page.keyboard.insertText(sql);
      return;
    }
  
    // fallback (non-monaco)
    await this.queryEditor.click();
    await this.queryEditor.fill(sql);
  }

  


  async setPanelName(panelName) {
    await expect(this.panelNameInput).toBeVisible();
    await this.panelNameInput.fill(panelName);
  }

  async applyPanel() {
    await expect(this.applyButton).toBeVisible();
    await this.applyButton.click();
    await this.applyButton.click();
  }

  async addFieldsToPanel(fieldNames = ['code', 'level', 'message']) {
    // Click +X for each requested field, then apply changes.
    for (const fieldName of fieldNames) {
      const fieldRow = this.page
        .locator(`xpath=//*[normalize-space(text())="${fieldName}"]/ancestor::*[self::li or self::div][1]`)
        .first();
      const addXButton = fieldRow.locator('[data-test="dashboard-add-x-data"]').first();

      await expect(fieldRow).toBeVisible();
      await expect(addXButton).toBeVisible();
      await addXButton.click();
    }

    await expect(this.applyButton).toBeVisible();
    await this.applyButton.click();
  }

  async savePanelIfVisible() {
    if (await this.savePanelButton.isVisible().catch(() => false)) {

      for (let attempt = 1; attempt <= 3; attempt++) {
        await this.applyButton.click();
  
        const noDataVisible = await this.noDataText.isVisible().catch(() => false);
  
        if (!noDataVisible) {
          break;
        }
      }
      
      await this.savePanelButton.click();
    }
  }

  async verifyPanelHasData() {
    await expect(this.noDataText).not.toBeVisible();
  }

  async setTimeRangeLast15Minutes() {
    const timeButton = this.page.locator('[data-test="date-time-btn"], [data-test="dashboard-date-time-btn"], button').filter({ hasText: /last|past|minutes|hours/i }).first();
  
    await timeButton.click();
  
    const last15Minutes = this.page.getByText(/last 15 minutes|past 15 minutes/i).first();
    await last15Minutes.click();
  }
}

module.exports = { DashboardPage };