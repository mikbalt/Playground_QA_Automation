from typing import List

import allure

from pages.base_page import BasePage


class CartPage(BasePage):
    """Page object for the Sauce Demo shopping cart page."""

    URL = "https://www.saucedemo.com/cart.html"

    def __init__(self, page):
        super().__init__(page)
        self.cart_items = page.locator("[data-test='inventory-item']")
        self.cart_item_names = page.locator("[data-test='inventory-item-name']")
        self.checkout_button = page.locator("[data-test='checkout']")
        self.continue_shopping_button = page.locator("[data-test='continue-shopping']")

    def open(self):
        """Navigate to the cart page."""
        self.navigate(self.URL)
        return self

    @allure.step("Get cart item names")
    def get_cart_items(self) -> List[str]:
        """Return a list of product names currently in the cart."""
        if self.cart_items.count() == 0:
            return []
        return self.cart_item_names.all_text_contents()

    @allure.step("Remove item '{item_name}' from cart")
    def remove_item(self, item_name: str):
        """Remove an item from the cart by its product name."""
        cart_item = self.page.locator(
            "[data-test='inventory-item']",
            has=self.page.locator("[data-test='inventory-item-name']", has_text=item_name),
        )
        cart_item.locator("button", has_text="Remove").click()

    @allure.step("Proceed to checkout")
    def proceed_to_checkout(self):
        """Click the Checkout button to start the checkout process."""
        self.checkout_button.click()

    @allure.step("Continue shopping")
    def continue_shopping(self):
        """Click Continue Shopping to go back to the inventory page."""
        self.continue_shopping_button.click()
