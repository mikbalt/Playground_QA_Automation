import allure


class CartIcon:
    """Component representing the shopping cart icon in the header."""

    @staticmethod
    def get_count(page) -> int:
        """Return the number displayed on the cart badge. Returns 0 if not visible."""
        badge = page.locator("[data-test='shopping-cart-badge']")
        if badge.is_visible():
            return int(badge.text_content())
        return 0

    @staticmethod
    @allure.step("Click cart icon")
    def click(page):
        """Click the shopping cart link to navigate to the cart page."""
        page.locator("[data-test='shopping-cart-link']").click()
