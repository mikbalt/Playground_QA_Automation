from typing import Any

import httpx


class ApiClient:
    """HTTP client abstraction for API testing."""

    def __init__(self, base_url: str, token: str | None = None, timeout: float = 30.0):
        self.base_url = base_url
        self.token = token
        self.timeout = timeout
        self._client: httpx.Client | None = None

    @property
    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _ensure_client(self) -> httpx.Client:
        if self._client is None or self._client.is_closed:
            self._client = httpx.Client(
                base_url=self.base_url,
                headers=self._headers,
                timeout=self.timeout,
            )
        return self._client

    def get(self, path: str, params: dict[str, Any] | None = None) -> httpx.Response:
        """Send a GET request."""
        client = self._ensure_client()
        return client.get(path, params=params)

    def post(self, path: str, json: dict[str, Any] | None = None) -> httpx.Response:
        """Send a POST request."""
        client = self._ensure_client()
        return client.post(path, json=json)

    def put(self, path: str, json: dict[str, Any] | None = None) -> httpx.Response:
        """Send a PUT request."""
        client = self._ensure_client()
        return client.put(path, json=json)

    def delete(self, path: str) -> httpx.Response:
        """Send a DELETE request."""
        client = self._ensure_client()
        return client.delete(path)

    def set_token(self, token: str) -> None:
        """Set or update the auth token and recreate the client."""
        self.token = token
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP client."""
        if self._client and not self._client.is_closed:
            self._client.close()
            self._client = None

    def __enter__(self) -> "ApiClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
