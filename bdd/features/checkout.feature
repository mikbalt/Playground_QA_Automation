Feature: Checkout Process
  As a logged in user
  I want to complete the checkout process
  So that I can purchase products

  Background:
    Given I am logged in as "standard_user"
    And I have added "Sauce Labs Backpack" to the cart

  @smoke @critical
  Scenario: Complete checkout with valid information
    When I go to the cart
    And I proceed to checkout
    And I fill in first name "John" and last name "Doe" and postal code "12345"
    And I continue to the overview
    And I finish the order
    Then I should see the order confirmation message "Thank you for your order!"

  @negative
  Scenario: Checkout fails without required information
    When I go to the cart
    And I proceed to checkout
    And I continue without filling information
    Then I should see checkout error "Error: First Name is required"

  @negative
  Scenario: Checkout fails with missing postal code
    When I go to the cart
    And I proceed to checkout
    And I fill in only first name "John" and last name "Doe"
    And I continue to the overview
    Then I should see checkout error "Error: Postal Code is required"
