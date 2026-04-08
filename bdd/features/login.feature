Feature: User Login
  As a user
  I want to log in to Sauce Demo
  So that I can access the inventory

  @smoke @critical
  Scenario: Successful login with standard user
    Given I am on the login page
    When I login with username "standard_user" and password "secret_sauce"
    Then I should be redirected to the inventory page

  @negative
  Scenario: Login fails with locked out user
    Given I am on the login page
    When I login with username "locked_out_user" and password "secret_sauce"
    Then I should see error message "Sorry, this user has been locked out"

  @negative
  Scenario: Login fails with invalid credentials
    Given I am on the login page
    When I login with username "invalid_user" and password "wrong_pass"
    Then I should see error message "Username and password do not match"
