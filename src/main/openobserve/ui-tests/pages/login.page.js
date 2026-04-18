// ui-tests/pages/login.page.js
class LoginPage {
    constructor(page) {
      this.page = page;
      this.emailInput = page.locator('[data-test="login-user-id"]');
      this.passwordInput = page.locator('[data-test="login-password"]');
      this.loginButton = page.locator('[data-cy="login-sign-in"]');
    }
  
    async goto() {
      await this.page.goto('/');
    }
  
    async login(email, password) {
      await this.emailInput.fill(email);
      await this.passwordInput.fill(password);
      await this.loginButton.click();
    }
  }
  
  module.exports = { LoginPage };