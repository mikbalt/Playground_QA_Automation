import pytest
import httpx


@pytest.fixture(scope="session")
def base_url() -> str:
    """Base URL for the DummyJSON API."""
    return "https://dummyjson.com"


@pytest.fixture(scope="session")
def auth_token(base_url: str) -> str:
    """Authenticate with DummyJSON and return a valid token."""
    response = httpx.post(
        f"{base_url}/auth/login",
        json={"username": "emilys", "password": "emilyspass"},
    )
    response.raise_for_status()
    data = response.json()
    return data["accessToken"]


@pytest.fixture()
def client(base_url: str) -> httpx.Client:
    """HTTP client pre-configured with the base URL."""
    with httpx.Client(base_url=base_url, timeout=30.0) as c:
        yield c


@pytest.fixture()
def auth_client(base_url: str, auth_token: str) -> httpx.Client:
    """HTTP client pre-configured with the base URL and auth token."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    with httpx.Client(base_url=base_url, headers=headers, timeout=30.0) as c:
        yield c
