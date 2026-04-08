import sys
import os

import allure
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pages.inventory_page import InventoryPage


@allure.epic("Sauce Demo")
@allure.feature("Inventory")
class TestInventory:
    """Tests for the inventory / products page."""

    @allure.title("Products are displayed on the inventory page")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_products_are_displayed(self, logged_in_page):
        """Verify that products are visible after logging in."""
        page = logged_in_page
        inventory_page = InventoryPage(page)

        product_names = inventory_page.get_product_names()
        assert len(product_names) > 0, "No products are displayed on the inventory page"

    @allure.title("Sort products by price low to high")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_by_price_low_to_high(self, logged_in_page):
        """Verify that sorting by price low-to-high orders products correctly."""
        page = logged_in_page
        inventory_page = InventoryPage(page)

        inventory_page.sort_products("lohi")
        prices = inventory_page.get_product_prices()

        assert prices == sorted(prices), (
            f"Prices are not sorted low to high: {prices}"
        )

    @allure.title("Sort products by price high to low")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_by_price_high_to_low(self, logged_in_page):
        """Verify that sorting by price high-to-low orders products correctly."""
        page = logged_in_page
        inventory_page = InventoryPage(page)

        inventory_page.sort_products("hilo")
        prices = inventory_page.get_product_prices()

        assert prices == sorted(prices, reverse=True), (
            f"Prices are not sorted high to low: {prices}"
        )

    @allure.title("Sort products by name A to Z")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_by_name_a_to_z(self, logged_in_page):
        """Verify that sorting by name A-Z orders products alphabetically."""
        page = logged_in_page
        inventory_page = InventoryPage(page)

        inventory_page.sort_products("az")
        names = inventory_page.get_product_names()

        assert names == sorted(names), (
            f"Product names are not sorted A to Z: {names}"
        )

    @allure.title("Adding to cart updates the badge count")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_to_cart_updates_badge(self, logged_in_page):
        """Verify that adding a product increments the cart badge count."""
        page = logged_in_page
        inventory_page = InventoryPage(page)

        assert inventory_page.get_cart_badge_count() == 0

        inventory_page.add_product_to_cart("Sauce Labs Backpack")
        assert inventory_page.get_cart_badge_count() == 1

        inventory_page.add_product_to_cart("Sauce Labs Bike Light")
        assert inventory_page.get_cart_badge_count() == 2

    @allure.title("Inventory page displays 6 products")
    @allure.severity(allure.severity_level.NORMAL)
    def test_product_count(self, logged_in_page):
        """Verify that exactly 6 products are shown on the inventory page."""
        page = logged_in_page
        inventory_page = InventoryPage(page)

        product_names = inventory_page.get_product_names()
        assert len(product_names) == 6, (
            f"Expected 6 products but found {len(product_names)}"
        )
