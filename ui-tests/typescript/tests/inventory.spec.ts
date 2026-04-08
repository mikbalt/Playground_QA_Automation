import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login-page';
import { InventoryPage } from '../pages/inventory-page';

test.describe('Inventory Tests', () => {
  let loginPage: LoginPage;
  let inventoryPage: InventoryPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    inventoryPage = new InventoryPage(page);
    await loginPage.goto();
    await loginPage.login('standard_user', 'secret_sauce');
    await expect(page).toHaveURL(/.*inventory.html/);
  });

  test('all products are displayed', async () => {
    const productNames = await inventoryPage.getProductNames();
    expect(productNames.length).toBe(6);
  });

  test('sort products by price low to high', async () => {
    await inventoryPage.sortBy('lohi');
    const prices = await inventoryPage.getProductPrices();
    for (let i = 1; i < prices.length; i++) {
      expect(prices[i]).toBeGreaterThanOrEqual(prices[i - 1]);
    }
  });

  test('add to cart updates badge count', async () => {
    await inventoryPage.addToCart('Sauce Labs Backpack');
    expect(await inventoryPage.getCartBadgeCount()).toBe(1);

    await inventoryPage.addToCart('Sauce Labs Bike Light');
    expect(await inventoryPage.getCartBadgeCount()).toBe(2);
  });
});
