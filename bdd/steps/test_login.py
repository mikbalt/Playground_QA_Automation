import pytest
from pytest_bdd import given, when, then, scenarios, parsers
from playwright.sync_api import Page, expect

scenarios('../features/login.feature')


@given('I am on the login page')
def navigate_to_login(page: Page):
    page.goto('https://www.saucedemo.com/')


@when(
    parsers.parse('I login with username "{username}" and password "{password}"'),
    target_fixture='login_result',
)
def login_with_credentials(page: Page, username: str, password: str):
    page.locator('[data-test="username"]').fill(username)
    page.locator('[data-test="password"]').fill(password)
    page.locator('[data-test="login-button"]').click()


@then('I should be redirected to the inventory page')
def verify_inventory_page(page: Page):
    expect(page).to_have_url('https://www.saucedemo.com/inventory.html')
    expect(page.locator('[data-test="title"]')).to_have_text('Products')


@then(parsers.parse('I should see error message "{message}"'))
def verify_error_message(page: Page, message: str):
    error_element = page.locator('[data-test="error"]')
    expect(error_element).to_be_visible()
    error_text = error_element.inner_text()
    assert message in error_text, f"Expected '{message}' in '{error_text}'"
