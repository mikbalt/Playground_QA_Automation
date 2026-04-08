import sys
import os

import pytest
from playwright.sync_api import sync_playwright

# Add the parent directory to sys.path so page objects can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from data.users import STANDARD_USER, PASSWORD
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def browser():
    """Launch a Chromium browser instance for the entire test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def browser_context(browser):
    """Create a new browser context for each test function."""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(browser_context):
    """Create a new page within the browser context for each test function."""
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def logged_in_page(page):
    """Return a page that is already logged in as the standard user."""
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(STANDARD_USER, PASSWORD)
    page.wait_for_url("**/inventory.html")
    return page
