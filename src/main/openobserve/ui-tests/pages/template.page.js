const { expect } = require('@playwright/test');
const testLogger = require('../utils/test-logger.js');

class TemplatePage {
  constructor(page) {
    this.page = page;

    // Navigation
    this.settingsButton = page.locator('[data-test="menu-link-settings-item"]');
    this.templatesTab = page.locator('[data-test="alert-templates-tab"]');

    // Template
    this.msgSuccess = page.getByText('Template Saved Successfully.');
    this.templateSearchInput = 'Search Template';
    this.addTemplateButton = '[data-test="template-list-add-btn"]';
    this.templateNameInput = '[data-test="add-template-name-input"]';
    this.templateSubmitButton = '[data-test="add-template-submit-btn"]';
  }

  async createNewTemplate(templateName, templateBody) {
    await this.settingsButton.click();
    await this.templatesTab.click();
    await this.page.locator(this.addTemplateButton).click();
 
    await this.page.locator(this.templateNameInput).click({ force: true });
    await this.page.locator(this.templateNameInput).fill(templateName);
    

    const editorViewLines = this.page
      .locator('[data-test="template-body-editor"] .view-lines, .monaco-editor .view-lines')
      .first();

    await editorViewLines.click();
    const selectAllKey = process.platform === 'darwin' ? 'Meta+A' : 'Control+A';
    await this.page.keyboard.press(selectAllKey);
    await this.page.keyboard.press('Backspace');
  
    await this.page.keyboard.insertText(templateBody);


    await this.page.locator(this.templateSubmitButton).click();
    await expect(this.msgSuccess).toBeVisible();

  
    await this.page.reload();
    await this.page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
   

    let firstAttempts = 0;
    const maxAttempts = 3;

    while (firstAttempts < maxAttempts) {
      try {
        await this.page.getByPlaceholder(this.templateSearchInput).click();
        await this.page.getByPlaceholder(this.templateSearchInput).fill(templateName);
    
        await this.page.getByRole('cell', { name: templateName }).waitFor({ timeout: 2000 });
        testLogger.info('Verified template exists successfully ', { templateName });
        return;
      } catch (error) {
        firstAttempts++;
        if (firstAttempts === maxAttempts) {
          throw new Error(`Template ${templateName} not found after ${maxAttempts} attempts`);
        }
        testLogger.info('Template not found, retrying', { attempts: firstAttempts });
        await this.page.reload();
        await this.page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
      }
    }
  }
}

module.exports = { TemplatePage };