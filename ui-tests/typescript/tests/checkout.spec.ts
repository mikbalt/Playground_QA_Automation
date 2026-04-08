import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login-page';
import { InventoryPage } from '../pages/inventory-page';

test.describe('Checkout Flow Tests', () => {
  let loginPage: LoginPage;
  let inventoryPage: InventoryPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    inventoryPage = new InventoryPage(page);
    await loginPage.goto();
    await loginPage.login('standard_user', 'secret_sauce');
    await expect(page).toHaveURL(/.*inventory.html/);
  });

  test('complete checkout happy path', async ({ page }) => {
    // Add item to cart
    await inventoryPage.addToCart('Sauce Labs Backpack');
    expect(await inventoryPage.getCartBadgeCount()).toBe(1);

    // Go to cart
    await page.locator('[data-test="shopping-cart-link"]').click();
    await expect(page).toHaveURL(/.*cart.html/);
    await expect(page.locator('[data-test="inventory-item-name"]')).toHaveText('Sauce Labs Backpack');

    // Proceed to checkout
    await page.locator('[data-test="checkout"]').click();
    await expect(page).toHaveURL(/.*checkout-step-one.html/);

    // Fill checkout info
    await page.locator('[data-test="firstName"]').fill('John');
    await page.locator('[data-test="lastName"]').fill('Doe');
    await page.locator('[data-test="postalCode"]').fill('12345');
    await page.locator('[data-test="continue"]').click();

    // Verify checkout overview
    await expect(page).toHaveURL(/.*checkout-step-two.html/);
    await expect(page.locator('[data-test="inventory-item-name"]')).toHaveText('Sauce Labs Backpack');

    // Complete order
    await page.locator('[data-test="finish"]').click();
    await expect(page).toHaveURL(/.*checkout-complete.html/);
    await expect(page.locator('[data-test="complete-header"]')).toHaveText('Thank you for your order!');
  });

  test('checkout fails without filling info', async ({ page }) => {
    // Add item to cart
    await inventoryPage.addToCart('Sauce Labs Backpack');

    // Go to cart and proceed to checkout
    await page.locator('[data-test="shopping-cart-link"]').click();
    await page.locator('[data-test="checkout"]').click();

    // Try to continue without filling info
    await page.locator('[data-test="continue"]').click();

    // Verify error message
    await expect(page.locator('[data-test="error"]')).toBeVisible();
    const errorText = await page.locator('[data-test="error"]').innerText();
    expect(errorText).toContain('First Name is required');
  });
});
