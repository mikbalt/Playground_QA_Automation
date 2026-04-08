import allure


class BasePage:
    """Base page object that all page objects inherit from."""

    def __init__(self, page):
        self.page = page

    def navigate(self, url: str):
        """Navigate to the specified URL."""
        with allure.step(f"Navigate to {url}"):
            self.page.goto(url)

    def get_title(self) -> str:
        """Return the page title."""
        return self.page.title()

    def wait_for_url(self, url_pattern: str):
        """Wait until the page URL matches the given pattern."""
        with allure.step(f"Wait for URL to match: {url_pattern}"):
            self.page.wait_for_url(url_pattern)

    def screenshot(self, name: str):
        """Take a screenshot and attach it to the Allure report."""
        screenshot_bytes = self.page.screenshot()
        allure.attach(
            screenshot_bytes,
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
