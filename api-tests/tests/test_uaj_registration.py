"""
UAJ Test Suite — US-001: Attendee Registration
================================================
ISTQB Techniques: EP, BVA, Decision Table, Error Guessing

Covers:
- 1A. Field Validation (EP + BVA)
- 1B. Payment Scenarios (Decision Table)
- 1C. Duplicate & Edge Cases (Error Guessing)
- 1D. Confirmation Email
"""

import allure
import httpx
import pytest

from models.uaj import RegisterResponse


# ===================================================================
# 1A. FIELD VALIDATION — Equivalence Partitioning + Boundary Value Analysis
# ===================================================================
@allure.epic("UAJ — Unified Attendee Journey")
@allure.feature("US-001: Registration")
class TestRegistrationFieldValidation:
    """
    ISTQB Technique: EP + BVA

    EP: Divide inputs into valid/invalid partitions → one test per partition.
    BVA: Test at boundary values (min, min-1, max, max+1).

    first_name: 1-50 chars, required
    last_name:  1-50 chars, required
    company:    1-100 chars, required
    job_title:  0-100 chars, optional
    email:      valid format, required, unique per event
    """

    VALID_PAYLOAD = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@test.com",
        "company": "Acme Corp",
        "ticket_type": "standard",
        "payment_token": "tok_valid_visa",
    }

    def _payload(self, **overrides) -> dict:
        """Helper to create payload with overrides."""
        data = {**self.VALID_PAYLOAD, **overrides}
        return data

    # --- EP: Valid partition (happy path) ---

    @allure.story("Field Validation")
    @allure.title("TC-001: Valid registration — all required fields")
    @pytest.mark.smoke
    def test_valid_registration(self, uaj_client: httpx.Client):
        """[EP — valid partition] All required fields provided correctly."""
        resp = uaj_client.post("/api/v1/register", json=self.VALID_PAYLOAD)

        assert resp.status_code == 201
        data = RegisterResponse(**resp.json())
        assert data.attendee_id is not None
        assert data.qr_code is not None
        assert data.status == "registered"

    # --- BVA: first_name boundaries ---

    @allure.story("Field Validation")
    @allure.title("TC-002: first_name at minimum boundary (1 char)")
    @pytest.mark.regression
    def test_first_name_min_boundary(self, uaj_client: httpx.Client):
        """[BVA — lower boundary] first_name = 1 character → should pass."""
        resp = uaj_client.post("/api/v1/register", json=self._payload(first_name="A"))

        assert resp.status_code == 201

    @allure.story("Field Validation")
    @allure.title("TC-003: first_name at maximum boundary (50 chars)")
    @pytest.mark.regression
    def test_first_name_max_boundary(self, uaj_client: httpx.Client):
        """[BVA — upper boundary] first_name = 50 characters → should pass."""
        resp = uaj_client.post(
            "/api/v1/register",
            json=self._payload(first_name="A" * 50, email="max50@test.com"),
        )

        assert resp.status_code == 201

    @allure.story("Field Validation")
    @allure.title("TC-004: first_name empty (below boundary)")
    @pytest.mark.negative
    def test_first_name_empty(self, uaj_client: httpx.Client):
        """[BVA — below lower] first_name = '' (0 chars) → should fail."""
        resp = uaj_client.post("/api/v1/register", json=self._payload(first_name=""))

        assert resp.status_code == 422  # FastAPI validation error

    @allure.story("Field Validation")
    @allure.title("TC-005: first_name exceeds max (51 chars)")
    @pytest.mark.negative
    def test_first_name_exceeds_max(self, uaj_client: httpx.Client):
        """[BVA — above upper] first_name = 51 characters → should fail."""
        resp = uaj_client.post(
            "/api/v1/register",
            json=self._payload(first_name="A" * 51),
        )

        assert resp.status_code == 422

    # --- EP: Missing required field ---

    @allure.story("Field Validation")
    @allure.title("TC-006: Missing required field (email)")
    @pytest.mark.negative
    def test_missing_email(self, uaj_client: httpx.Client):
        """[EP — invalid partition: missing] email omitted → should fail."""
        payload = self._payload()
        del payload["email"]

        resp = uaj_client.post("/api/v1/register", json=payload)

        assert resp.status_code == 422

    # --- EP: Invalid email format ---

    @allure.story("Field Validation")
    @allure.title("TC-007: Malformed email format")
    @pytest.mark.negative
    def test_invalid_email_format(self, uaj_client: httpx.Client):
        """[EP — invalid partition: format] email without @ → should fail."""
        resp = uaj_client.post(
            "/api/v1/register",
            json=self._payload(email="not-an-email"),
        )

        assert resp.status_code == 422

    # --- EP: Optional field omitted ---

    @allure.story("Field Validation")
    @allure.title("TC-008: Optional field omitted (job_title)")
    @pytest.mark.regression
    def test_optional_job_title_omitted(self, uaj_client: httpx.Client):
        """[EP — optional field] job_title not provided → should pass."""
        payload = self._payload(email="nojob@test.com")
        payload.pop("job_title", None)

        resp = uaj_client.post("/api/v1/register", json=payload)

        assert resp.status_code == 201

    # --- BVA: company boundaries ---

    @allure.story("Field Validation")
    @allure.title("TC-009: company at max boundary (100 chars)")
    @pytest.mark.regression
    def test_company_max_boundary(self, uaj_client: httpx.Client):
        """[BVA — upper boundary] company = 100 characters → should pass."""
        resp = uaj_client.post(
            "/api/v1/register",
            json=self._payload(company="X" * 100, email="comp100@test.com"),
        )

        assert resp.status_code == 201

    @allure.story("Field Validation")
    @allure.title("TC-010: company exceeds max (101 chars)")
    @pytest.mark.negative
    def test_company_exceeds_max(self, uaj_client: httpx.Client):
        """[BVA — above upper] company = 101 characters → should fail."""
        resp = uaj_client.post(
            "/api/v1/register",
            json=self._payload(company="X" * 101, email="comp101@test.com"),
        )

        assert resp.status_code == 422


# ===================================================================
# 1B. PAYMENT SCENARIOS — Decision Table Testing
# ===================================================================
@allure.epic("UAJ — Unified Attendee Journey")
@allure.feature("US-001: Registration")
class TestRegistrationPayment:
    """
    ISTQB Technique: Decision Table

    Decision Table:
    | Rule | Ticket Type | Payment Token | Expected     |
    |------|-------------|--------------|--------------|
    | R1   | standard    | valid        | 201 success  |
    | R2   | standard    | declined     | 402 failed   |
    | R3   | standard    | missing      | 400 error    |
    | R4   | vip         | valid        | 201 success  |
    | R5   | vip         | declined     | 402 failed   |
    | R6   | vip         | missing      | 400 error    |
    | R7   | press       | null         | 201 success  |
    | R8   | press       | provided     | 201 success  |
    | --   | invalid     | any          | 422 error    |
    """

    @allure.story("Payment — Decision Table")
    @allure.title("TC-011: Standard + valid payment → success")
    @pytest.mark.smoke
    def test_standard_valid_payment(self, uaj_client: httpx.Client):
        """[DT Rule R1] Standard ticket with valid payment token."""
        resp = uaj_client.post("/api/v1/register", json={
            "first_name": "R1", "last_name": "Test", "email": "r1@test.com",
            "company": "Test Co", "ticket_type": "standard", "payment_token": "tok_valid_visa",
        })

        assert resp.status_code == 201

    @allure.story("Payment — Decision Table")
    @allure.title("TC-012: Standard + declined payment → 402")
    @pytest.mark.negative
    def test_standard_declined_payment(self, uaj_client: httpx.Client):
        """[DT Rule R2] Standard ticket with declined payment token."""
        resp = uaj_client.post("/api/v1/register", json={
            "first_name": "R2", "last_name": "Test", "email": "r2@test.com",
            "company": "Test Co", "ticket_type": "standard", "payment_token": "tok_declined",
        })

        assert resp.status_code == 402
        assert resp.json()["detail"]["error"] == "payment_failed"

    @allure.story("Payment — Decision Table")
    @allure.title("TC-013: Standard + no payment → 400")
    @pytest.mark.negative
    def test_standard_no_payment(self, uaj_client: httpx.Client):
        """[DT Rule R3] Standard ticket without payment token."""
        resp = uaj_client.post("/api/v1/register", json={
            "first_name": "R3", "last_name": "Test", "email": "r3@test.com",
            "company": "Test Co", "ticket_type": "standard", "payment_token": None,
        })

        assert resp.status_code == 400

    @allure.story("Payment — Decision Table")
    @allure.title("TC-014: VIP + valid payment → success (ticket_type must be 'vip')")
    @pytest.mark.smoke
    def test_vip_valid_payment(self, uaj_client: httpx.Client):
        """
        [DT Rule R4] VIP ticket with valid payment.
        CRITICAL: Verify ticket_type='vip' in response (ref: last year's incident
        where VIP was stored as 'standard').
        """
        resp = uaj_client.post("/api/v1/register", json={
            "first_name": "R4", "last_name": "Test", "email": "r4@test.com",
            "company": "Test Co", "ticket_type": "vip", "payment_token": "tok_valid_visa",
        })

        assert resp.status_code == 201

        # Verify ticket_type stored correctly
        attendee_id = resp.json()["attendee_id"]
        profile = uaj_client.get(f"/api/v1/attendee/{attendee_id}").json()
        assert profile["ticket_type"] == "vip", \
            f"CRITICAL: VIP ticket stored as '{profile['ticket_type']}' — repeat of last year's incident!"

    @allure.story("Payment — Decision Table")
    @allure.title("TC-015: VIP + declined payment → 402")
    @pytest.mark.negative
    def test_vip_declined_payment(self, uaj_client: httpx.Client):
        """[DT Rule R5] VIP ticket with declined payment token."""
        resp = uaj_client.post("/api/v1/register", json={
            "first_name": "R5", "last_name": "Test", "email": "r5@test.com",
            "company": "Test Co", "ticket_type": "vip", "payment_token": "tok_declined",
        })

        assert resp.status_code == 402

    @allure.story("Payment — Decision Table")
    @allure.title("TC-016: VIP + no payment → 400")
    @pytest.mark.negative
    def test_vip_no_payment(self, uaj_client: httpx.Client):
        """[DT Rule R6] VIP ticket without payment token."""
        resp = uaj_client.post("/api/v1/register", json={
            "first_name": "R6", "last_name": "Test", "email": "r6@test.com",
            "company": "Test Co", "ticket_type": "vip", "payment_token": None,
        })

        assert resp.status_code == 400

    @allure.story("Payment — Decision Table")
    @allure.title("TC-017: Press + no payment → success (no charge)")
    @pytest.mark.smoke
    def test_press_no_payment(self, uaj_client: httpx.Client):
        """[DT Rule R7] Press ticket without payment — should succeed."""
        resp = uaj_client.post("/api/v1/register", json={
            "first_name": "R7", "last_name": "Test", "email": "r7@test.com",
            "company": "Test Co", "ticket_type": "press", "payment_token": None,
        })

        assert resp.status_code == 201
        attendee_id = resp.json()["attendee_id"]
        profile = uaj_client.get(f"/api/v1/attendee/{attendee_id}").json()
        assert profile["ticket_type"] == "press"

    @allure.story("Payment — Decision Table")
    @allure.title("TC-018: Press + payment provided → success (token ignored)")
    @pytest.mark.regression
    def test_press_with_payment_token(self, uaj_client: httpx.Client):
        """[DT Rule R8] Press ticket with payment token — should ignore token."""
        resp = uaj_client.post("/api/v1/register", json={
            "first_name": "R8", "last_name": "Test", "email": "r8@test.com",
            "company": "Test Co", "ticket_type": "press", "payment_token": "tok_valid_visa",
        })

        assert resp.status_code == 201

    @allure.story("Payment — Decision Table")
    @allure.title("TC-019: Invalid ticket type → 422")
    @pytest.mark.negative
    def test_invalid_ticket_type(self, uaj_client: httpx.Client):
        """[EP — invalid partition] Non-existent ticket type."""
        resp = uaj_client.post("/api/v1/register", json={
            "first_name": "Bad", "last_name": "Type", "email": "bad@test.com",
            "company": "Test Co", "ticket_type": "premium", "payment_token": "tok_valid",
        })

        assert resp.status_code == 422


# ===================================================================
# 1C. DUPLICATE & EDGE CASES — Error Guessing
# ===================================================================
@allure.epic("UAJ — Unified Attendee Journey")
@allure.feature("US-001: Registration")
class TestRegistrationEdgeCases:
    """
    ISTQB Technique: Error Guessing (EG)

    Experience-based technique — anticipate real-world defects:
    duplicate submissions, special characters, injection, concurrency.
    """

    @allure.story("Edge Cases")
    @allure.title("TC-020: Duplicate email — same event → 409")
    @pytest.mark.negative
    def test_duplicate_email(self, uaj_client: httpx.Client):
        """[EG] Same email registered twice → should reject second."""
        payload = {
            "first_name": "Dup", "last_name": "Test", "email": "dup@test.com",
            "company": "Test Co", "ticket_type": "standard", "payment_token": "tok_valid_visa",
        }

        resp1 = uaj_client.post("/api/v1/register", json=payload)
        assert resp1.status_code == 201

        resp2 = uaj_client.post("/api/v1/register", json=payload)
        assert resp2.status_code == 409
        assert resp2.json()["detail"]["error"] == "duplicate_email"

    @allure.story("Edge Cases")
    @allure.title("TC-022: SQL injection attempt in name field")
    @pytest.mark.security
    def test_sql_injection_in_name(self, uaj_client: httpx.Client):
        """[EG — security] SQL injection string should be safely handled."""
        resp = uaj_client.post("/api/v1/register", json={
            "first_name": "Robert'; DROP TABLE attendees;--",
            "last_name": "Test", "email": "sqli@test.com",
            "company": "Test Co", "ticket_type": "press",
        })

        # Should either reject or safely store — never execute SQL
        assert resp.status_code in (201, 400, 422)
        if resp.status_code == 201:
            attendee_id = resp.json()["attendee_id"]
            profile = uaj_client.get(f"/api/v1/attendee/{attendee_id}").json()
            assert profile["first_name"] is not None  # data wasn't destroyed

    @allure.story("Edge Cases")
    @allure.title("TC-023: XSS attempt in company field")
    @pytest.mark.security
    def test_xss_in_company(self, uaj_client: httpx.Client):
        """[EG — security] XSS payload should be safely handled."""
        resp = uaj_client.post("/api/v1/register", json={
            "first_name": "XSS", "last_name": "Test", "email": "xss@test.com",
            "company": "<script>alert('xss')</script>",
            "ticket_type": "press",
        })

        assert resp.status_code in (201, 400, 422)

    @allure.story("Edge Cases")
    @allure.title("TC-024: Unicode characters in name fields")
    @pytest.mark.regression
    def test_unicode_in_name(self, uaj_client: httpx.Client):
        """[EG — i18n] Unicode names should be preserved correctly."""
        resp = uaj_client.post("/api/v1/register", json={
            "first_name": "José",
            "last_name": "Müller",
            "email": "jose@test.com",
            "company": "München GmbH",
            "ticket_type": "press",
        })

        assert resp.status_code == 201
        attendee_id = resp.json()["attendee_id"]
        profile = uaj_client.get(f"/api/v1/attendee/{attendee_id}").json()
        assert profile["first_name"] == "José"
        assert profile["last_name"] == "Müller"
        assert profile["company"] == "München GmbH"


# ===================================================================
# 1D. CONFIRMATION EMAIL
# ===================================================================
@allure.epic("UAJ — Unified Attendee Journey")
@allure.feature("US-001: Registration")
class TestConfirmationEmail:
    """Verify confirmation email is sent with correct content."""

    @allure.story("Confirmation Email")
    @allure.title("TC-028: Email sent after successful registration")
    @pytest.mark.smoke
    def test_email_sent_on_success(self, uaj_client: httpx.Client):
        """Email should be sent after successful registration."""
        uaj_client.post("/api/v1/register", json={
            "first_name": "Email", "last_name": "Test", "email": "email@test.com",
            "company": "Test Co", "ticket_type": "standard", "payment_token": "tok_valid_visa",
        })

        emails = uaj_client.get("/test/emails").json()
        assert len(emails) == 1
        assert emails[0]["to"] == "email@test.com"
        assert emails[0]["ticket_type"] == "standard"
        assert emails[0]["qr_code"] is not None

    @allure.story("Confirmation Email")
    @allure.title("TC-029: No email sent after failed registration")
    @pytest.mark.negative
    def test_no_email_on_failure(self, uaj_client: httpx.Client):
        """No email should be sent when registration fails."""
        uaj_client.post("/api/v1/register", json={
            "first_name": "Fail", "last_name": "Test", "email": "fail@test.com",
            "company": "Test Co", "ticket_type": "standard", "payment_token": "tok_declined",
        })

        emails = uaj_client.get("/test/emails").json()
        assert len(emails) == 0

    @allure.story("Confirmation Email")
    @allure.title("TC-030: VIP email shows correct ticket type")
    @pytest.mark.smoke
    def test_vip_email_correct_ticket_type(self, uaj_client: httpx.Client):
        """
        VIP email must display 'vip', not 'standard'.
        Ref: Last year's incident where VIP was displayed as Standard.
        """
        uaj_client.post("/api/v1/register", json={
            "first_name": "VIP", "last_name": "Check", "email": "vipmail@test.com",
            "company": "VIP Co", "ticket_type": "vip", "payment_token": "tok_valid_visa",
        })

        emails = uaj_client.get("/test/emails").json()
        assert len(emails) == 1
        assert emails[0]["ticket_type"] == "vip", \
            f"Email shows '{emails[0]['ticket_type']}' instead of 'vip'"
