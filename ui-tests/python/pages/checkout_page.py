import allure

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page object for the Sauce Demo checkout pages (step-one, step-two, complete)."""

    def __init__(self, page):
        super().__init__(page)
        # Checkout Step One - Your Information
        self.first_name_input = page.locator("[data-test='firstName']")
        self.last_name_input = page.locator("[data-test='lastName']")
        self.zip_code_input = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.error_message = page.locator("[data-test='error']")

        # Checkout Step Two - Overview
        self.finish_button = page.locator("[data-test='finish']")
        self.total_label = page.locator("[data-test='total-label']")

        # Checkout Complete
        self.complete_header = page.locator("[data-test='complete-header']")

    @allure.step("Fill checkout information: {first_name} {last_name}, {zip_code}")
    def fill_information(self, first_name: str, last_name: str, zip_code: str):
        """Fill in the first name, last name, and zip code on the checkout info page."""
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.zip_code_input.fill(zip_code)

    @allure.step("Click Continue on checkout")
    def continue_checkout(self):
        """Click the Continue button to proceed from step one to step two."""
        self.continue_button.click()

    @allure.step("Click Finish on checkout")
    def finish_checkout(self):
        """Click the Finish button to complete the purchase."""
        self.finish_button.click()

    def get_total_price(self) -> str:
        """Return the total price text from the checkout overview page."""
        self.total_label.wait_for(state="visible")
        return self.total_label.text_content()

    def get_error_message(self) -> str:
        """Return the error message text on the checkout page."""
        self.error_message.wait_for(state="visible")
        return self.error_message.text_content()

    def get_confirmation_message(self) -> str:
        """Return the confirmation header text (e.g. 'Thank you for your order!')."""
        self.complete_header.wait_for(state="visible")
        return self.complete_header.text_content()
