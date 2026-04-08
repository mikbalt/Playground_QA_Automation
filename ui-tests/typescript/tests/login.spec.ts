import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login-page';

test.describe('Login Tests', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('successful login with standard user', async ({ page }) => {
    await loginPage.login('standard_user', 'secret_sauce');
    await expect(page).toHaveURL(/.*inventory.html/);
    await expect(page.locator('[data-test="title"]')).toHaveText('Products');
  });

  test('login fails with locked out user', async () => {
    await loginPage.login('locked_out_user', 'secret_sauce');
    const errorMsg = await loginPage.getErrorMessage();
    expect(errorMsg).toContain('Sorry, this user has been locked out');
  });

  test('login fails with invalid credentials', async () => {
    await loginPage.login('invalid_user', 'wrong_pass');
    const errorMsg = await loginPage.getErrorMessage();
    expect(errorMsg).toContain('Username and password do not match');
  });
});
