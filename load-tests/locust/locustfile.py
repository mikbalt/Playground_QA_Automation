from locust import HttpUser, task, between


class ShopUser(HttpUser):
    """Simulates a user browsing and shopping on dummyjson.com."""

    host = "https://dummyjson.com"
    wait_time = between(1, 3)

    def on_start(self):
        """Authenticate the user on start."""
        response = self.client.post(
            "/auth/login",
            json={
                "username": "emilys",
                "password": "emilyspass",
            },
        )
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("accessToken", "")
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = ""
            self.headers = {}

    @task(3)
    def browse_products(self):
        """Browse the product catalog."""
        self.client.get(
            "/products?limit=10",
            headers=self.headers,
            name="/products",
        )

    @task(2)
    def view_product(self):
        """View a specific product detail page."""
        import random

        product_id = random.randint(1, 30)
        self.client.get(
            f"/products/{product_id}",
            headers=self.headers,
            name="/products/[id]",
        )

    @task(1)
    def add_to_cart(self):
        """Add products to the shopping cart."""
        import random

        payload = {
            "userId": 1,
            "products": [
                {"id": random.randint(1, 30), "quantity": random.randint(1, 3)},
            ],
        }
        self.client.post(
            "/carts/add",
            json=payload,
            headers=self.headers,
            name="/carts/add",
        )

    @task(1)
    def search_products(self):
        """Search for products by keyword."""
        import random

        search_terms = ["phone", "laptop", "watch", "shirt", "shoes", "cream"]
        term = random.choice(search_terms)
        self.client.get(
            f"/products/search?q={term}",
            headers=self.headers,
            name="/products/search",
        )
