from pytest_bdd import when, then, scenarios, parsers
from playwright.sync_api import Page, expect

scenarios('../features/product_search.feature')


@when('I am on the inventory page')
def on_inventory_page(page: Page):
    expect(page).to_have_url('https://www.saucedemo.com/inventory.html')


@when(parsers.parse('I sort products by "{sort_option}"'))
def sort_products(page: Page, sort_option: str):
    sort_map = {
        'Price (low to high)': 'lohi',
        'Price (high to low)': 'hilo',
        'Name (A to Z)': 'az',
        'Name (Z to A)': 'za',
    }
    value = sort_map.get(sort_option, sort_option)
    page.locator('[data-test="product-sort-container"]').select_option(value)


@then(parsers.parse('I should see {count:d} products displayed'))
def verify_product_count(page: Page, count: int):
    items = page.locator('[data-test="inventory-item"]')
    expect(items).to_have_count(count)


@then('the products should be sorted by price ascending')
def verify_price_ascending(page: Page):
    price_elements = page.locator('[data-test="inventory-item-price"]').all_inner_texts()
    prices = [float(p.replace('$', '')) for p in price_elements]
    for i in range(1, len(prices)):
        assert prices[i] >= prices[i - 1], (
            f"Price at index {i} (${prices[i]}) is less than price at index {i-1} (${prices[i-1]})"
        )


@then('the products should be sorted by name descending')
def verify_name_descending(page: Page):
    name_elements = page.locator('[data-test="inventory-item-name"]').all_inner_texts()
    for i in range(1, len(name_elements)):
        assert name_elements[i] <= name_elements[i - 1], (
            f"Name at index {i} ('{name_elements[i]}') should come before "
            f"name at index {i-1} ('{name_elements[i-1]}') in descending order"
        )
