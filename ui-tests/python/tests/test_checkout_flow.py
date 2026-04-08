import sys
import os

import allure
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.epic("Sauce Demo")
@allure.feature("Checkout")
class TestCheckoutFlow:
    """End-to-end tests for the checkout process."""

    @allure.title("Complete checkout with a single item")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_complete_checkout_single_item(self, logged_in_page):
        """Happy path: add Sauce Labs Backpack, go to cart, checkout, fill info, finish."""
        page = logged_in_page

        # Add product to cart
        inventory_page = InventoryPage(page)
        inventory_page.add_product_to_cart("Sauce Labs Backpack")
        assert inventory_page.get_cart_badge_count() == 1

        # Go to cart and verify item
        inventory_page.go_to_cart()
        cart_page = CartPage(page)
        items = cart_page.get_cart_items()
        assert "Sauce Labs Backpack" in items

        # Proceed to checkout
        cart_page.proceed_to_checkout()

        # Fill checkout information
        checkout_page = CheckoutPage(page)
        checkout_page.fill_information("John", "Doe", "12345")
        checkout_page.continue_checkout()

        # Finish the order
        checkout_page.finish_checkout()

        # Verify confirmation
        confirmation = checkout_page.get_confirmation_message()
        assert "Thank you for your order" in confirmation

    @allure.title("Complete checkout with multiple items")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_complete_checkout_multiple_items(self, logged_in_page):
        """Add multiple items, complete checkout, and verify confirmation."""
        page = logged_in_page

        # Add multiple products to cart
        inventory_page = InventoryPage(page)
        inventory_page.add_product_to_cart("Sauce Labs Backpack")
        inventory_page.add_product_to_cart("Sauce Labs Bike Light")
        inventory_page.add_product_to_cart("Sauce Labs Bolt T-Shirt")
        assert inventory_page.get_cart_badge_count() == 3

        # Go to cart and verify items
        inventory_page.go_to_cart()
        cart_page = CartPage(page)
        items = cart_page.get_cart_items()
        assert len(items) == 3
        assert "Sauce Labs Backpack" in items
        assert "Sauce Labs Bike Light" in items
        assert "Sauce Labs Bolt T-Shirt" in items

        # Proceed to checkout
        cart_page.proceed_to_checkout()

        # Fill checkout information
        checkout_page = CheckoutPage(page)
        checkout_page.fill_information("Jane", "Smith", "54321")
        checkout_page.continue_checkout()

        # Finish the order
        checkout_page.finish_checkout()

        # Verify confirmation
        confirmation = checkout_page.get_confirmation_message()
        assert "Thank you for your order" in confirmation

    @allure.title("Checkout without filling information shows error")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_checkout_without_info(self, logged_in_page):
        """Attempt to continue checkout without filling in personal info."""
        page = logged_in_page

        # Add a product and proceed to checkout
        inventory_page = InventoryPage(page)
        inventory_page.add_product_to_cart("Sauce Labs Backpack")
        inventory_page.go_to_cart()

        cart_page = CartPage(page)
        cart_page.proceed_to_checkout()

        # Try to continue without filling info
        checkout_page = CheckoutPage(page)
        checkout_page.continue_checkout()

        # Verify error is shown
        error = checkout_page.get_error_message()
        assert "First Name is required" in error

    @allure.title("Remove item from cart")
    @allure.severity(allure.severity_level.NORMAL)
    def test_remove_item_from_cart(self, logged_in_page):
        """Add items to cart, remove one, and verify it is gone."""
        page = logged_in_page

        # Add products to cart
        inventory_page = InventoryPage(page)
        inventory_page.add_product_to_cart("Sauce Labs Backpack")
        inventory_page.add_product_to_cart("Sauce Labs Bike Light")
        assert inventory_page.get_cart_badge_count() == 2

        # Go to cart
        inventory_page.go_to_cart()
        cart_page = CartPage(page)

        # Remove one item
        cart_page.remove_item("Sauce Labs Backpack")

        # Verify the item is removed
        remaining_items = cart_page.get_cart_items()
        assert "Sauce Labs Backpack" not in remaining_items
        assert "Sauce Labs Bike Light" in remaining_items
        assert len(remaining_items) == 1
