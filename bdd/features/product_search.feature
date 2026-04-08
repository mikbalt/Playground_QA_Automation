Feature: Product Browsing
  As a logged in user
  I want to browse and sort products
  So that I can find what I need

  Background:
    Given I am logged in as "standard_user"

  @smoke
  Scenario: View all products
    When I am on the inventory page
    Then I should see 6 products displayed

  Scenario: Sort products by price low to high
    When I sort products by "Price (low to high)"
    Then the products should be sorted by price ascending

  Scenario: Sort products by name Z to A
    When I sort products by "Name (Z to A)"
    Then the products should be sorted by name descending
