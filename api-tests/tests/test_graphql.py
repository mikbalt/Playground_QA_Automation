import allure
import httpx
import pytest


GRAPHQL_URL = "https://countries.trevorblades.com/graphql"


@allure.epic("GraphQL API")
@allure.feature("Countries")
class TestGraphQL:
    """Tests for the Countries GraphQL API."""

    @allure.story("Query Countries")
    @allure.title("Get all countries returns a non-empty list")
    @pytest.mark.smoke
    def test_get_all_countries(self):
        query = """
        {
            countries {
                code
                name
            }
        }
        """

        response = httpx.post(GRAPHQL_URL, json={"query": query}, timeout=30.0)

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "countries" in data["data"]
        assert len(data["data"]["countries"]) > 0

    @allure.story("Filter Countries")
    @allure.title("Filter countries by continent (Asia)")
    @pytest.mark.regression
    def test_filter_countries_by_continent(self):
        query = """
        {
            countries(filter: { continent: { eq: "AS" } }) {
                code
                name
                continent {
                    code
                    name
                }
            }
        }
        """

        response = httpx.post(GRAPHQL_URL, json={"query": query}, timeout=30.0)

        assert response.status_code == 200
        data = response.json()
        countries = data["data"]["countries"]
        assert len(countries) > 0
        for country in countries:
            assert country["continent"]["code"] == "AS"

    @allure.story("Schema Validation")
    @allure.title("Country has name and capital fields")
    @pytest.mark.regression
    def test_country_has_name_and_capital(self):
        query = """
        {
            countries {
                name
                capital
            }
        }
        """

        response = httpx.post(GRAPHQL_URL, json={"query": query}, timeout=30.0)

        assert response.status_code == 200
        data = response.json()
        countries = data["data"]["countries"]
        assert len(countries) > 0
        for country in countries:
            assert "name" in country
            assert "capital" in country

    @allure.story("Single Country")
    @allure.title("Get Indonesia by code 'ID'")
    @pytest.mark.smoke
    def test_get_single_country(self):
        query = """
        {
            country(code: "ID") {
                code
                name
                capital
                currency
                continent {
                    name
                }
            }
        }
        """

        response = httpx.post(GRAPHQL_URL, json={"query": query}, timeout=30.0)

        assert response.status_code == 200
        data = response.json()
        country = data["data"]["country"]
        assert country["code"] == "ID"
        assert country["name"] == "Indonesia"
        assert country["continent"]["name"] == "Asia"

    @allure.story("Error Handling")
    @allure.title("Invalid GraphQL query returns errors in response body")
    @pytest.mark.negative
    def test_graphql_invalid_query(self):
        query = """
        {
            nonExistentField {
                foo
                bar
            }
        }
        """

        response = httpx.post(GRAPHQL_URL, json={"query": query}, timeout=30.0)

        data = response.json()
        assert "errors" in data
        assert len(data["errors"]) > 0

    @allure.story("Error Handling")
    @allure.title("GraphQL always returns HTTP 200 even for invalid queries")
    @pytest.mark.regression
    def test_graphql_always_returns_200(self):
        query = """
        {
            totallyBogusQuery {
                doesNotExist
            }
        }
        """

        response = httpx.post(GRAPHQL_URL, json={"query": query}, timeout=30.0)

        assert response.status_code == 200
