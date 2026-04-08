import allure
import httpx
import pytest

from models.user import LoginResponse


@allure.epic("E-Commerce API")
@allure.feature("Authentication")
class TestAuth:
    """Tests for the /auth endpoints."""

    LOGIN_URL = "/auth/login"
    VALID_USERNAME = "emilys"
    VALID_PASSWORD = "emilyspass"

    @allure.story("Login")
    @allure.title("Login with valid credentials returns 200 and a token")
    @pytest.mark.smoke
    def test_login_valid_credentials(self, client: httpx.Client):
        response = client.post(
            self.LOGIN_URL,
            json={"username": self.VALID_USERNAME, "password": self.VALID_PASSWORD},
        )

        assert response.status_code == 200
        data = response.json()
        assert "accessToken" in data
        assert data["username"] == self.VALID_USERNAME

    @allure.story("Login")
    @allure.title("Login with invalid credentials returns 400")
    @pytest.mark.negative
    def test_login_invalid_credentials(self, client: httpx.Client):
        response = client.post(
            self.LOGIN_URL,
            json={"username": "invaliduser", "password": "wrongpassword"},
        )

        assert response.status_code == 400

    @allure.story("Login")
    @allure.title("Login with empty username returns 400")
    @pytest.mark.negative
    def test_login_empty_username(self, client: httpx.Client):
        response = client.post(
            self.LOGIN_URL,
            json={"username": "", "password": self.VALID_PASSWORD},
        )

        assert response.status_code == 400

    @allure.story("Login")
    @allure.title("Login with empty password returns 400")
    @pytest.mark.negative
    def test_login_empty_password(self, client: httpx.Client):
        response = client.post(
            self.LOGIN_URL,
            json={"username": self.VALID_USERNAME, "password": ""},
        )

        assert response.status_code == 400

    @allure.story("Protected Endpoints")
    @allure.title("Access protected endpoint with valid token succeeds")
    @pytest.mark.smoke
    def test_access_protected_endpoint_with_token(
        self, auth_client: httpx.Client
    ):
        response = auth_client.get("/auth/me")

        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "username" in data

    @allure.story("Protected Endpoints")
    @allure.title("Access protected endpoint without token returns 401")
    @pytest.mark.negative
    def test_access_protected_endpoint_without_token(
        self, client: httpx.Client
    ):
        response = client.get("/auth/me")

        assert response.status_code == 401

    @allure.story("Login")
    @allure.title("Token returned on login is a string")
    @pytest.mark.regression
    def test_token_is_string(self, client: httpx.Client):
        response = client.post(
            self.LOGIN_URL,
            json={"username": self.VALID_USERNAME, "password": self.VALID_PASSWORD},
        )

        assert response.status_code == 200
        login_data = LoginResponse(**response.json())
        assert isinstance(login_data.accessToken, str)
        assert len(login_data.accessToken) > 0
