const { expect } = require('@playwright/test');
const testLogger = require('../utils/test-logger.js');
const Actions = require('../utils/actions.js');

class DestinationPage {
  constructor(page) {
    this.page = page;
    this.actions = new Actions(page);

    // Navigation
    this.settingsMenuItem = '[data-test="menu-link-settings-item"]';
    this.destinationsTab = '[data-test="alert-destinations-tab"]';
    this.destinationsListTitle = '[data-test="alert-destinations-list-title"]';

    // Destination
    this.destinationTypeCard = '[data-test="destination-type-card"]';
    this.addDestinationButton = '[data-test="alert-destination-list-add-alert-btn"]';
    this.destinationNameInput = '[data-test="add-destination-name-input"]';
    this.templateSelect = '[data-test="add-destination-template-select"]';
    this.urlInput = '[data-test="add-destination-url-input"]';
    this.submitButton = '[data-test="add-destination-submit-btn"]';
    this.txtHeader = '[data-test="add-destination-header--key-input"]';
    this.successMessage = 'Destination saved';
    this.nextPageButton = 'button:has(mat-icon:text("chevron_right")), button:has-text("chevron_right")';
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

    testLogger.info('Selected destination type and form loaded');
  }

  async navigateToDestinations() {
    await this.page.locator(this.settingsMenuItem).click();
    await this.page.locator(this.destinationsTab).click();
    await expect(this.page.locator(this.destinationsListTitle)).toBeVisible();
  }

  async createNewDestination(destinationName, destinationStream, templateName, header, headerValue) {
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


    const valueInput1 = this.page.locator(
      `[data-test="add-destination-header-${header}-value-input"]`
    );
    await valueInput1.click();
    await valueInput1.fill(headerValue);


    await this.page.locator(this.submitButton).click();
    await expect(this.page.getByText(this.successMessage)).toBeVisible();

    await this.verifyDestinationExists(destinationName);
  }

  async findDestinationAcrossPages(destinationName) {
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
    const found = await this.findDestinationAcrossPages(destinationName);
    if (!found) {
      throw new Error(`Destination ${destinationName} not found after checking all pages`);
    }
  }
}

module.exports = { DestinationPage };