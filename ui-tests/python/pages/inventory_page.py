from typing import List

import allure

from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Page object for the Sauce Demo inventory / products page."""

    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page):
        super().__init__(page)
        self.product_items = page.locator("[data-test='inventory-item']")
        self.product_names = page.locator("[data-test='inventory-item-name']")
        self.product_prices = page.locator("[data-test='inventory-item-price']")
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")
        self.cart_link = page.locator("[data-test='shopping-cart-link']")

    def open(self):
        """Navigate to the inventory page."""
        self.navigate(self.URL)
        return self

    @allure.step("Get all product names")
    def get_product_names(self) -> List[str]:
        """Return a list of all visible product names."""
        self.product_names.first.wait_for(state="visible")
        return self.product_names.all_text_contents()

    @allure.step("Get all product prices")
    def get_product_prices(self) -> List[float]:
        """Return a list of all visible product prices as floats."""
        self.product_prices.first.wait_for(state="visible")
        raw_prices = self.product_prices.all_text_contents()
        return [float(price.replace("$", "")) for price in raw_prices]

    @allure.step("Add product '{product_name}' to cart")
    def add_product_to_cart(self, product_name: str):
        """Click the 'Add to cart' button for the product with the given name."""
        product_item = self.page.locator(
            "[data-test='inventory-item']",
            has=self.page.locator("[data-test='inventory-item-name']", has_text=product_name),
        )
        product_item.locator("button", has_text="Add to cart").click()

    @allure.step("Sort products by '{option_value}'")
    def sort_products(self, option_value: str):
        """Sort products using the dropdown. Values: 'az', 'za', 'lohi', 'hilo'."""
        self.sort_dropdown.select_option(option_value)

    def get_cart_badge_count(self) -> int:
        """Return the number shown on the cart badge. Returns 0 if badge is not visible."""
        if self.cart_badge.is_visible():
            return int(self.cart_badge.text_content())
        return 0

    @allure.step("Go to cart")
    def go_to_cart(self):
        """Click the shopping cart icon to navigate to the cart page."""
        self.cart_link.click()
