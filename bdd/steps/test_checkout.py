from pytest_bdd import given, when, then, scenarios, parsers
from playwright.sync_api import Page, expect

scenarios('../features/checkout.feature')


@given(parsers.parse('I have added "{product_name}" to the cart'))
def add_product_to_cart(page: Page, product_name: str):
    item = page.locator('[data-test="inventory-item"]', has=page.locator(
        '[data-test="inventory-item-name"]', has_text=product_name
    ))
    item.locator('button', has_text='Add to cart').click()
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text('1')


@when('I go to the cart')
def go_to_cart(page: Page):
    page.locator('[data-test="shopping-cart-link"]').click()
    expect(page).to_have_url('https://www.saucedemo.com/cart.html')


@when('I proceed to checkout')
def proceed_to_checkout(page: Page):
    page.locator('[data-test="checkout"]').click()
    expect(page).to_have_url('https://www.saucedemo.com/checkout-step-one.html')


@when(parsers.parse('I fill in first name "{first_name}" and last name "{last_name}" and postal code "{postal_code}"'))
def fill_checkout_info(page: Page, first_name: str, last_name: str, postal_code: str):
    if first_name:
        page.locator('[data-test="firstName"]').fill(first_name)
    if last_name:
        page.locator('[data-test="lastName"]').fill(last_name)
    if postal_code:
        page.locator('[data-test="postalCode"]').fill(postal_code)


@when(parsers.parse('I fill in only first name "{first_name}" and last name "{last_name}"'))
def fill_checkout_info_no_zip(page: Page, first_name: str, last_name: str):
    page.locator('[data-test="firstName"]').fill(first_name)
    page.locator('[data-test="lastName"]').fill(last_name)


@when('I continue to the overview')
def continue_to_overview(page: Page):
    page.locator('[data-test="continue"]').click()


@when('I continue without filling information')
def continue_without_info(page: Page):
    page.locator('[data-test="continue"]').click()


@when('I finish the order')
def finish_order(page: Page):
    expect(page).to_have_url('https://www.saucedemo.com/checkout-step-two.html')
    page.locator('[data-test="finish"]').click()


@then(parsers.parse('I should see the order confirmation message "{message}"'))
def verify_order_confirmation(page: Page, message: str):
    expect(page).to_have_url('https://www.saucedemo.com/checkout-complete.html')
    expect(page.locator('[data-test="complete-header"]')).to_have_text(message)


@then(parsers.parse('I should see checkout error "{error_message}"'))
def verify_checkout_error(page: Page, error_message: str):
    error_element = page.locator('[data-test="error"]')
    expect(error_element).to_be_visible()
    expect(error_element).to_have_text(error_message)
