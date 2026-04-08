import allure

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the Sauce Demo login page."""

    URL = "https://www.saucedemo.com"

    def __init__(self, page):
        super().__init__(page)
        self.username_input = page.locator("[data-test='username']")
        self.password_input = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-button']")
        self.error_message = page.locator("[data-test='error']")

    def open(self):
        """Navigate to the login page."""
        self.navigate(self.URL)
        return self

    @allure.step("Login with username '{username}'")
    def login(self, username: str, password: str):
        """Fill in credentials and click the login button."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self) -> str:
        """Return the text of the error message displayed on failed login."""
        self.error_message.wait_for(state="visible")
        return self.error_message.text_content()
