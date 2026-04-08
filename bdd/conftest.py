import pytest
from pytest_bdd import given, parsers
from playwright.sync_api import sync_playwright, Browser, Page, expect


@pytest.fixture(scope='session')
def browser():
    """Create a browser instance shared across the test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope='function')
def page(browser: Browser):
    """Create a new browser page for each test function."""
    context = browser.new_context(
        viewport={'width': 1280, 'height': 720},
        ignore_https_errors=True,
    )
    page = context.new_page()
    yield page
    page.close()
    context.close()


@given(parsers.parse('I am logged in as "{username}"'))
def login_as_user(page: Page, username: str):
    page.goto('https://www.saucedemo.com/')
    page.locator('[data-test="username"]').fill(username)
    page.locator('[data-test="password"]').fill('secret_sauce')
    page.locator('[data-test="login-button"]').click()
    expect(page).to_have_url('https://www.saucedemo.com/inventory.html')
