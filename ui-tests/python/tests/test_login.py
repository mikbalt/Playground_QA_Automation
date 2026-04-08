import sys
import os

import allure
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from data.users import STANDARD_USER, LOCKED_OUT_USER, PASSWORD
from pages.login_page import LoginPage


@allure.epic("Sauce Demo")
@allure.feature("Login")
class TestLogin:
    """Tests for the Sauce Demo login functionality."""

    @allure.title("Successful login with standard user")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_successful_login(self, page):
        """Verify that a standard user can log in and reach the inventory page."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(STANDARD_USER, PASSWORD)

        page.wait_for_url("**/inventory.html")
        assert "inventory.html" in page.url

    @allure.title("Locked out user receives error message")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_locked_out_user(self, page):
        """Verify that a locked-out user sees the appropriate error message."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(LOCKED_OUT_USER, PASSWORD)

        error = login_page.get_error_message()
        assert "Sorry, this user has been locked out" in error

    @allure.title("Invalid credentials show error message")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_invalid_credentials(self, page):
        """Verify that invalid credentials produce an error message."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("invalid_user", "wrong_password")

        error = login_page.get_error_message()
        assert "Username and password do not match" in error

    @allure.title("Empty username shows error message")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_username(self, page):
        """Verify that submitting without a username shows an error."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("", PASSWORD)

        error = login_page.get_error_message()
        assert "Username is required" in error

    @allure.title("Empty password shows error message")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_password(self, page):
        """Verify that submitting without a password shows an error."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(STANDARD_USER, "")

        error = login_page.get_error_message()
        assert "Password is required" in error
