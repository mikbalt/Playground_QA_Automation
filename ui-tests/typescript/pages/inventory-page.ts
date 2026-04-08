import { type Page, type Locator } from '@playwright/test';

export class InventoryPage {
  readonly page: Page;
  readonly inventoryItems: Locator;
  readonly itemNames: Locator;
  readonly itemPrices: Locator;
  readonly sortDropdown: Locator;
  readonly cartBadge: Locator;

  constructor(page: Page) {
    this.page = page;
    this.inventoryItems = page.locator('[data-test="inventory-item"]');
    this.itemNames = page.locator('[data-test="inventory-item-name"]');
    this.itemPrices = page.locator('[data-test="inventory-item-price"]');
    this.sortDropdown = page.locator('[data-test="product-sort-container"]');
    this.cartBadge = page.locator('[data-test="shopping-cart-badge"]');
  }

  async getProductNames(): Promise<string[]> {
    return await this.itemNames.allInnerTexts();
  }

  async getProductPrices(): Promise<number[]> {
    const priceTexts = await this.itemPrices.allInnerTexts();
    return priceTexts.map((price) => parseFloat(price.replace('$', '')));
  }

  async addToCart(productName: string) {
    const item = this.page.locator('[data-test="inventory-item"]', {
      has: this.page.locator('[data-test="inventory-item-name"]', { hasText: productName }),
    });
    await item.locator('button', { hasText: 'Add to cart' }).click();
  }

  async sortBy(value: string) {
    await this.sortDropdown.selectOption(value);
  }

  async getCartBadgeCount(): Promise<number> {
    const text = await this.cartBadge.innerText();
    return parseInt(text, 10);
  }
}
