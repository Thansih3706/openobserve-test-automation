const { expect }  = require('@playwright/test');
const testLogger = require('../utils/test-logger.js');
const Actions = require('../utils/actions.js');
class AlertsPage {
constructor(page) {
  this.page = page;
  this.actions = new Actions(page);

  // Navigation
  this.alertsMenu = '[data-test="menu-link-/alerts-item"]';
  this.settingsButton = page.locator('[data-test="menu-link-settings-item"]');
  this.templatesTab = page.locator('[data-test="alert-templates-tab"]');

  // Template
  this.msgSuccess = page.getByText('Template Saved Successfully.');
  this.templateSearchInput = 'Search Template';
  this.addTemplateButton = '[data-test="template-list-add-btn"]';
  this.templateNameInput = '[data-test="add-template-name-input"]';
  this.templateSubmitButton = '[data-test="add-template-submit-btn"]';

  // Destination
  this.destinationTypeCard = '[data-test="destination-type-card"]';
  this.settingsMenuItem = '[data-test="menu-link-settings-item"]';
  this.destinationsTab = '[data-test="alert-destinations-tab"]';
  this.destinationsListTitle = '[data-test="alert-destinations-list-title"]';

  this.addDestinationButton = '[data-test="alert-destination-list-add-alert-btn"]';
  this.destinationNameInput = '[data-test="add-destination-name-input"]';
  this.templateSelect = '[data-test="add-destination-template-select"]';
  this.urlInput = '[data-test="add-destination-url-input"]';
  this.submitButton = '[data-test="add-destination-submit-btn"]';
  this.successMessage = 'Destination saved';
  this.txtHeader = '[data-test="add-destination-header--key-input"]';
  this.nextPageButton = 'button:has(mat-icon:text("chevron_right")), button:has-text("chevron_right")';

  // Alert
  this.addAlertButton = '[data-test="alert-list-add-alert-btn"]';
  this.alertNameInput = '[data-test="add-alert-name-input"]';
  this.alertSubmitButton = '[data-test="add-alert-submit-btn"]';
  this.silenceNotificationInput = '.silence-notification-input input';

  this.streamTypeDropdown = '[data-test="add-alert-stream-type-select-dropdown"]';
  this.streamNameDropdown = '[data-test="add-alert-stream-name-select-dropdown"]';
  this.realtimeAlertRadio = '[data-test="add-alert-realtime-alert-radio"]';

  // Step 2 - Conditions
  this.conditionColumnSelect = '[data-test="alert-conditions-select-column"]';
  this.operatorSelect = '[data-test="alert-conditions-operator-select"]';
  this.conditionValueInput = '[data-test="alert-conditions-value-input"]';
  this.addConditionButton = '[data-test="alert-conditions-add-condition-btn"]';
  this.alertSuccessMessage = 'Alert saved successfully.';
}
  async goto() {
    await this.page.locator(this.alertsMenu).click();
    
  }


  async createNewTemplate(templateName, templateBody) {
    await this.settingsButton.click();
    await this.templatesTab.click();
    await this.page.locator(this.addTemplateButton).click();
    await this.page.locator(this.templateNameInput).click({ force: true });
    await this.page.locator(this.templateNameInput).fill(templateName);
    const editorViewLines = this.page.locator('[data-test="template-body-editor"] .view-lines, .monaco-editor .view-lines').first();
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
            testLogger.info('Template not found, retry', { attempts });
            await this.page.reload();
            await this.page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
        }
    }
}


async selectDestinationType(type) {
  const card = this.page.locator(`${this.destinationTypeCard}[data-type="${type}"]`);
  await card.waitFor({ state: 'visible', timeout: 10000 });
  await card.click();
  if (type === 'custom') {
      await this.page.waitForSelector(this.urlInput, { state: 'visible', timeout: 10000 });
  } else {
      await this.page.waitForSelector(this.destinationNameInput, { state: 'visible', timeout: 10000 });
  }
  testLogger.info('Selected destination type');
}


async navigateToDestinations() {
  await this.page.locator(this.settingsMenuItem).click();
  await this.page.locator(this.destinationsTab).click();
  await expect(this.page.locator(this.destinationsListTitle)).toBeVisible();
}

async createNewDestination(destinationName, destinationStream, templateName,header,headerValue) {
  await this.navigateToDestinations();
  const addBtn = this.page.locator(this.addDestinationButton);
  await addBtn.waitFor({ state: 'visible', timeout: 30000 });
  await expect(addBtn).toBeEnabled({ timeout: 30000 });
  await addBtn.click();
  await this.selectDestinationType('custom');
  await this.page.locator(this.destinationNameInput).click();
  await this.page.locator(this.destinationNameInput).fill(destinationName);
  await this.page.locator(this.templateSelect).click();
  await this.actions.scrollAndFindOption(templateName, 'template');
  await this.page.locator(this.urlInput).click();
  await this.page.locator(this.urlInput).fill(
      `http://localhost:5080/api/default/${destinationStream}/_json`
    );
  await this.page.locator(this.txtHeader).click();
  await this.page.locator(this.txtHeader).fill(header);
  const valueInput1 = this.page.locator(`[data-test="add-destination-header-${header}-value-input"]`);
  await valueInput1.click();
  await valueInput1.fill(headerValue);
  await this.page.locator(this.submitButton).click();
  await expect(this.page.getByText(this.successMessage)).toBeVisible();
  await this.verifyDestinationExists(destinationName);
}



async findDestination(destinationName) {
  let destinationFound = false;
  let isLastPage = false;
  
  while (!destinationFound && !isLastPage) {
      try {
          await this.page.getByRole('cell', { name: destinationName }).waitFor({ timeout: 2000 });
          destinationFound = true;
          testLogger.info('Found destination', { destinationName });
      } catch (error) {
          const nextPageBtn = this.page.locator(this.nextPageButton).first();
          if (await nextPageBtn.isVisible() && await nextPageBtn.isEnabled()) {
              await nextPageBtn.click();
          } else {
              isLastPage = true;
          }
      }
  }
  return destinationFound;
}

async verifyDestinationExists(destinationName) {
  const found = await this.findDestination(destinationName);
  if (!found) {
      throw new Error(`Destination ${destinationName} not found after checking all pages`);
  }
}

  async selectStreamByName(sourceStream) {
    await this.page.locator(this.streamNameDropdown).click();
    await this.page.fill(this.streamNameDropdown, sourceStream);
    const option = this.page.getByText(sourceStream, { exact: true });
    await option.click();
}
  
    async createRealTimeAlert(alertName, sourceStream, destinationName,column,value) {
      await this.page.locator(this.alertsMenu).click();
      await this.page.locator(this.addAlertButton).click();
      await this.page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
      await expect(this.page.locator(this.alertNameInput)).toBeVisible({ timeout: 10000 });
      await this.page.locator(this.alertNameInput).click();
      await this.page.locator(this.alertNameInput).fill(alertName);
      await this.page.locator(this.streamTypeDropdown).click();
      await expect(this.page.getByRole('option', { name: 'logs' })).toBeVisible({ timeout: 10000 });
      await this.page.getByRole('option', { name: 'logs' }).locator('div').nth(2).click();
      await this.page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
      await this.selectStreamByName(sourceStream);
      await expect(this.page.locator(this.realtimeAlertRadio)).toBeVisible({ timeout: 5000 });
      await this.page.locator(this.realtimeAlertRadio).click();
      await this.page.getByRole('button', { name: 'Continue' }).click();
      await this.page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
      await this.page.locator(this.addConditionButton).first().click();
      const columnSelect = this.page.locator(this.conditionColumnSelect).first();
      await columnSelect.click();
      const visibleMenu = this.page.locator('.q-menu:visible').first();
      await expect(visibleMenu).toBeVisible();
      const options = visibleMenu.locator('[role="option"]');
      const optionTexts = await options.allTextContents();
      testLogger.info('Available columns in dropdown', { optionTexts, requestedColumn: column });
      const columnOption = visibleMenu.getByRole('option', { name: column, exact: true });
      if (await columnOption.count()) {
      await columnOption.click();
      } else {
      throw new Error(`Column not found in dropdown: ${column}`);
      }   
      await expect(this.page.locator(this.operatorSelect).first()).toBeVisible({ timeout: 5000 });
      await this.page.locator(this.operatorSelect).first().click();
      await this.page.getByText('Contains', { exact: true }).click();
      await this.page.locator(this.conditionValueInput).first().locator('input').fill(value);
      await this.page.getByRole('button', { name: 'Continue' }).click();
      await this.page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
      const silenceInput = this.page.locator(this.silenceNotificationInput);
      if (await silenceInput.isVisible({ timeout: 3000 })) {
          await silenceInput.fill('0');
      }
      const destinationSection = this.page.locator('div.flex.items-start').filter({
          has: this.page.locator('span:has-text("Destination")')
      }).first();
      await destinationSection.waitFor({ state: 'visible', timeout: 10000 });
      const destinationDropdown = destinationSection.locator('.q-select').first();
      await destinationDropdown.waitFor({ state: 'visible', timeout: 5000 });
      await destinationDropdown.click();
      const visibleDestMenu = this.page.locator('.q-menu:visible');
      await expect(visibleDestMenu.locator('.q-item').first()).toBeVisible({ timeout: 5000 });
      let destFound = false;
      const destOption = visibleDestMenu.locator('.q-item').filter({ hasText: destinationName }).first();
      if (await destOption.isVisible({ timeout: 3000 }).catch(() => false)) {
          await destOption.click();
          destFound = true;
      }
      if (!destFound) {
          try {
              await this.actions.scrollAndFindOption(destinationName, 'template');
          } catch (scrollError) {
              await visibleDestMenu.locator('.q-item').first().click();
              testLogger.warn('Selected first available destination (fallback)', { requestedDestination: destinationName });
          }
      }
      await this.page.keyboard.press('Escape');
      await this.page.getByRole('button', { name: 'Continue' }).click();
      await this.page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
      await this.page.locator(this.alertSubmitButton).click();
      await expect(this.page.getByText(this.alertSuccessMessage)).toBeVisible({ timeout: 30000 });
      testLogger.info('Successfully created alert', { alertName: alertName });
      return alertName;
  }

}

module.exports = { AlertsPage };



