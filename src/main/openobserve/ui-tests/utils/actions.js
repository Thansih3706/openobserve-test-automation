const testLogger = require('../utils/test-logger.js');

class Actions {
  constructor(page) {
    this.page = page;
  }

  async scrollAndFindOption(optionName, optionType) {
    const dropdown = this.page.locator('.q-menu:visible').first();
    const scrollAmount = 1000;
    let maxScrolls = 50;

    while (maxScrolls > 0) {
      const option =
        optionType === 'template'
          ? dropdown.getByText(optionName, { exact: true })
          : dropdown.getByRole('option', { name: optionName });

      if ((await option.count()) > 0 && await option.first().isVisible()) {
        if (optionType === 'template') {
          await option.first().click();
        } else {
          const span = option.first().locator('span').first();
          if (await span.count()) {
            await span.click();
          } else {
            await option.first().click();
          }
        }

        testLogger.info(`Found ${optionType}: ${optionName}`);
        return true;
      }

      const { scrollTop, scrollHeight, clientHeight } = await dropdown.evaluate((el) => ({
        scrollTop: el.scrollTop,
        scrollHeight: el.scrollHeight,
        clientHeight: el.clientHeight,
      }));

      if (scrollTop + clientHeight >= scrollHeight) {
        await dropdown.evaluate((el) => {
          el.scrollTop = 0;
        });
      } else {
        await dropdown.evaluate((el, amount) => {
          el.scrollTop += amount;
        }, scrollAmount);
      }
      maxScrolls--;
    }

    throw new Error(`${optionType} not found: ${optionName}`);
  }
}

module.exports = Actions;