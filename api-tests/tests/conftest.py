"""
Fixtures for UAJ (Unified Attendee Journey) API tests.

Requires the UAJ mock server running at http://localhost:8000.
Start with: cd target-apps/uaj_mock_api && uvicorn app:app --port 8000
"""

import pytest
import httpx

UAJ_BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="session")
def uaj_base_url() -> str:
    return UAJ_BASE_URL


@pytest.fixture(autouse=True)
def reset_uaj_state(uaj_base_url: str):
    """Reset mock server state before each test for isolation."""
    httpx.post(f"{uaj_base_url}/test/reset")
    yield


@pytest.fixture()
def uaj_client(uaj_base_url: str) -> httpx.Client:
    with httpx.Client(base_url=uaj_base_url, timeout=30.0) as c:
        yield c


@pytest.fixture()
def registered_standard(uaj_client: httpx.Client) -> dict:
    """Pre-register a Standard attendee and return full context."""
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "company": "Acme Corp",
        "job_title": "Engineer",
        "ticket_type": "standard",
        "payment_token": "tok_valid_visa",
    }
    resp = uaj_client.post("/api/v1/register", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    return {**payload, **data}


@pytest.fixture()
def registered_vip(uaj_client: httpx.Client) -> dict:
    """Pre-register a VIP attendee and return full context."""
    payload = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@test.com",
        "company": "VIP Global",
        "job_title": "CEO",
        "ticket_type": "vip",
        "payment_token": "tok_valid_visa",
    }
    resp = uaj_client.post("/api/v1/register", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    return {**payload, **data}


@pytest.fixture()
def registered_press(uaj_client: httpx.Client) -> dict:
    """Pre-register a Press attendee and return full context."""
    payload = {
        "first_name": "Alex",
        "last_name": "Reporter",
        "email": "alex@press.com",
        "company": "News Daily",
        "ticket_type": "press",
        "payment_token": None,
    }
    resp = uaj_client.post("/api/v1/register", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    return {**payload, **data}
