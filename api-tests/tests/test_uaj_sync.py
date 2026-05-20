"""
UAJ Test Suite — US-002: Cross-Platform Sync
==============================================
ISTQB Techniques: EP, BVA, Decision Table, State Transition, Error Guessing

Covers:
- 2A. Happy Path Sync (EP)
- 2B. Data Integrity (Decision Table)
- 2C. Failure & Retry (State Transition)
- 2D. Sync Status
"""

import allure
import httpx
import pytest

from models.uaj import SyncStatus, ExpoAttendee, SessionAttendee


# ===================================================================
# 2A. HAPPY PATH SYNC — Equivalence Partitioning
# ===================================================================
@allure.epic("UAJ — Unified Attendee Journey")
@allure.feature("US-002: Cross-Platform Sync")
class TestSyncHappyPath:
    """
    ISTQB Technique: Equivalence Partitioning

    Partitions: ticket_type (standard, vip, press) × trigger (auto, manual)
    Each partition should result in sync_status = "completed".
    """

    @allure.story("Auto Sync")
    @allure.title("TC-040: Auto-sync after Standard registration")
    @pytest.mark.smoke
    def test_auto_sync_standard(self, uaj_client: httpx.Client, registered_standard: dict):
        """[EP] Auto-sync triggers on registration — Standard ticket."""
        resp = uaj_client.get(f"/api/v1/sync/status/{registered_standard['attendee_id']}")

        assert resp.status_code == 200
        sync = SyncStatus(**resp.json())
        assert sync.sync_status == "completed"
        assert sync.platforms["expo_connect"].status == "synced"
        assert sync.platforms["session_hub"].status == "synced"

    @allure.story("Auto Sync")
    @allure.title("TC-041: Auto-sync after VIP registration")
    @pytest.mark.smoke
    def test_auto_sync_vip(self, uaj_client: httpx.Client, registered_vip: dict):
        """[EP] Auto-sync triggers on registration — VIP ticket."""
        resp = uaj_client.get(f"/api/v1/sync/status/{registered_vip['attendee_id']}")

        assert resp.status_code == 200
        sync = SyncStatus(**resp.json())
        assert sync.sync_status == "completed"

    @allure.story("Auto Sync")
    @allure.title("TC-042: Auto-sync after Press registration")
    @pytest.mark.smoke
    def test_auto_sync_press(self, uaj_client: httpx.Client, registered_press: dict):
        """[EP] Auto-sync triggers on registration — Press ticket."""
        resp = uaj_client.get(f"/api/v1/sync/status/{registered_press['attendee_id']}")

        assert resp.status_code == 200
        sync = SyncStatus(**resp.json())
        assert sync.sync_status == "completed"

    @allure.story("Manual Sync")
    @allure.title("TC-043: Manual re-sync trigger")
    @pytest.mark.regression
    def test_manual_resync(self, uaj_client: httpx.Client, registered_standard: dict):
        """[EP] Manual re-sync for already synced attendee."""
        resp = uaj_client.post(
            "/api/v1/sync/trigger",
            json={"attendee_id": registered_standard["attendee_id"]},
        )

        assert resp.status_code == 200
        assert resp.json()["sync_status"] == "completed"


# ===================================================================
# 2B. DATA INTEGRITY — Decision Table
# ===================================================================
@allure.epic("UAJ — Unified Attendee Journey")
@allure.feature("US-002: Cross-Platform Sync")
class TestSyncDataIntegrity:
    """
    ISTQB Technique: Decision Table (Data Mapping Validation)

    Field Mapping:
    | Field        | RegPlatform | ExpoConnect | SessionHub |
    |--------------|:-----------:|:-----------:|:----------:|
    | first_name   |     ✅      |     ✅      |     ✅     |
    | last_name    |     ✅      |     ✅      |     ✅     |
    | email        |     ✅      |     ✅      |     ✅     |
    | company      |     ✅      |     ✅      |     ❌     |
    | job_title    |     ✅      |     ❌      |     ❌     |
    | ticket_type  |     ✅      |     ✅      |     ✅     |
    | payment_token|     ✅      |     ❌      |     ❌     |
    | qr_code      |     ✅      |     ❌      |     ❌     |
    """

    @allure.story("Data Integrity")
    @allure.title("TC-045: ExpoConnect receives correct fields")
    @pytest.mark.smoke
    def test_expo_correct_fields(self, uaj_client: httpx.Client, registered_vip: dict):
        """[DT] Verify ExpoConnect gets: name, email, company, ticket_type."""
        resp = uaj_client.get(f"/api/v1/expo/attendee/{registered_vip['attendee_id']}")

        assert resp.status_code == 200
        expo = ExpoAttendee(**resp.json())
        assert expo.first_name == registered_vip["first_name"]
        assert expo.last_name == registered_vip["last_name"]
        assert expo.email == registered_vip["email"]
        assert expo.company == registered_vip["company"]
        assert expo.ticket_type == "vip"

    @allure.story("Data Integrity")
    @allure.title("TC-046: SessionHub receives correct fields")
    @pytest.mark.smoke
    def test_session_correct_fields(self, uaj_client: httpx.Client, registered_vip: dict):
        """[DT] Verify SessionHub gets: name, email, ticket_type (NO company)."""
        resp = uaj_client.get(f"/api/v1/sessions/attendee/{registered_vip['attendee_id']}")

        assert resp.status_code == 200
        session = SessionAttendee(**resp.json())
        assert session.first_name == registered_vip["first_name"]
        assert session.last_name == registered_vip["last_name"]
        assert session.email == registered_vip["email"]
        assert session.ticket_type == "vip"

    @allure.story("Data Integrity")
    @allure.title("TC-046b: SessionHub does NOT have company field")
    @pytest.mark.regression
    def test_session_no_company(self, uaj_client: httpx.Client, registered_vip: dict):
        """[DT] SessionHub should not expose company field."""
        resp = uaj_client.get(f"/api/v1/sessions/attendee/{registered_vip['attendee_id']}")

        data = resp.json()
        assert "company" not in data, "SessionHub should NOT contain company field"

    @allure.story("Data Integrity")
    @allure.title("TC-047: VIP ticket_type preserved across all platforms")
    @pytest.mark.smoke
    def test_vip_ticket_type_preserved(self, uaj_client: httpx.Client, registered_vip: dict):
        """
        [DT + EG] Verify ticket_type = 'vip' on ALL platforms.
        Ref: Last year's incident where VIP was stored as 'standard'.
        """
        aid = registered_vip["attendee_id"]

        reg = uaj_client.get(f"/api/v1/attendee/{aid}").json()
        expo = uaj_client.get(f"/api/v1/expo/attendee/{aid}").json()
        session = uaj_client.get(f"/api/v1/sessions/attendee/{aid}").json()

        assert reg["ticket_type"] == "vip", f"RegPlatform: {reg['ticket_type']}"
        assert expo["ticket_type"] == "vip", f"ExpoConnect: {expo['ticket_type']}"
        assert session["ticket_type"] == "vip", f"SessionHub: {session['ticket_type']}"

    @allure.story("Data Integrity")
    @allure.title("TC-048: Unicode characters synced correctly")
    @pytest.mark.regression
    def test_unicode_sync(self, uaj_client: httpx.Client):
        """[EG — i18n] Unicode names must be preserved across platforms."""
        resp = uaj_client.post("/api/v1/register", json={
            "first_name": "José", "last_name": "Müller", "email": "jose.sync@test.com",
            "company": "München GmbH", "ticket_type": "press",
        })
        aid = resp.json()["attendee_id"]

        expo = uaj_client.get(f"/api/v1/expo/attendee/{aid}").json()
        session = uaj_client.get(f"/api/v1/sessions/attendee/{aid}").json()

        assert expo["first_name"] == "José"
        assert expo["last_name"] == "Müller"
        assert session["first_name"] == "José"
        assert session["last_name"] == "Müller"

    @allure.story("Data Integrity")
    @allure.title("TC-049: Payment data never leaks to ExpoConnect or SessionHub")
    @pytest.mark.security
    def test_payment_data_no_leak(self, uaj_client: httpx.Client, registered_standard: dict):
        """[DT — security] Sensitive payment data must not exist on other platforms."""
        aid = registered_standard["attendee_id"]

        expo_resp = uaj_client.get(f"/api/v1/expo/attendee/{aid}")
        session_resp = uaj_client.get(f"/api/v1/sessions/attendee/{aid}")

        expo_data = expo_resp.json()
        session_data = session_resp.json()

        sensitive_fields = ["payment_token", "qr_code", "job_title"]
        for field in sensitive_fields:
            assert field not in expo_data, f"ExpoConnect leaks: {field}"
        for field in ["payment_token", "qr_code", "job_title", "company"]:
            assert field not in session_data, f"SessionHub leaks: {field}"


# ===================================================================
# 2C. FAILURE & RETRY — State Transition Testing
# ===================================================================
@allure.epic("UAJ — Unified Attendee Journey")
@allure.feature("US-002: Cross-Platform Sync")
class TestSyncFailure:
    """
    ISTQB Technique: State Transition

    Sync State Machine:
    Pending → Syncing → Completed (success)
                     → Partial   (one platform fails)
                     → Failed    (both fail)
                     → DLQ       (after 3 retries)

    Test both valid transitions and recovery paths.
    """

    @allure.story("Sync Failure")
    @allure.title("TC-050: Partial sync — ExpoConnect OK, SessionHub fails")
    @pytest.mark.regression
    def test_partial_sync_session_fails(self, uaj_client: httpx.Client):
        """[ST — partial] One platform fails → partial sync status."""
        # Set SessionHub to fail
        uaj_client.post("/test/sync-failure", params={"session_hub": True})

        resp = uaj_client.post("/api/v1/register", json={
            "first_name": "Partial", "last_name": "Test", "email": "partial1@test.com",
            "company": "Test Co", "ticket_type": "press",
        })
        aid = resp.json()["attendee_id"]

        sync = uaj_client.get(f"/api/v1/sync/status/{aid}").json()
        assert sync["sync_status"] == "partial"
        assert sync["platforms"]["expo_connect"]["status"] == "synced"
        assert sync["platforms"]["session_hub"]["status"] == "failed"

    @allure.story("Sync Failure")
    @allure.title("TC-051: Partial sync — ExpoConnect fails, SessionHub OK")
    @pytest.mark.regression
    def test_partial_sync_expo_fails(self, uaj_client: httpx.Client):
        """[ST — partial] ExpoConnect fails, SessionHub succeeds."""
        uaj_client.post("/test/sync-failure", params={"expo_connect": True})

        resp = uaj_client.post("/api/v1/register", json={
            "first_name": "Partial", "last_name": "Test2", "email": "partial2@test.com",
            "company": "Test Co", "ticket_type": "press",
        })
        aid = resp.json()["attendee_id"]

        sync = uaj_client.get(f"/api/v1/sync/status/{aid}").json()
        assert sync["sync_status"] == "partial"
        assert sync["platforms"]["expo_connect"]["status"] == "failed"
        assert sync["platforms"]["session_hub"]["status"] == "synced"

    @allure.story("Sync Failure")
    @allure.title("TC-052: Full sync failure — both platforms down")
    @pytest.mark.regression
    def test_full_sync_failure(self, uaj_client: httpx.Client):
        """[ST — full failure] Both platforms fail → sync_status 'failed'."""
        uaj_client.post("/test/sync-failure", params={"expo_connect": True, "session_hub": True})

        resp = uaj_client.post("/api/v1/register", json={
            "first_name": "FullFail", "last_name": "Test", "email": "fullfail@test.com",
            "company": "Test Co", "ticket_type": "press",
        })
        aid = resp.json()["attendee_id"]

        sync = uaj_client.get(f"/api/v1/sync/status/{aid}").json()
        assert sync["sync_status"] == "failed"
        assert sync["platforms"]["expo_connect"]["status"] == "failed"
        assert sync["platforms"]["session_hub"]["status"] == "failed"

    @allure.story("Sync Failure")
    @allure.title("TC-055: Manual re-sync recovers from previous failure")
    @pytest.mark.regression
    def test_manual_resync_recovery(self, uaj_client: httpx.Client):
        """[ST — recovery] Sync fails initially, manual re-sync succeeds after platform recovers."""
        # Step 1: Fail both platforms
        uaj_client.post("/test/sync-failure", params={"expo_connect": True, "session_hub": True})

        resp = uaj_client.post("/api/v1/register", json={
            "first_name": "Recover", "last_name": "Test", "email": "recover@test.com",
            "company": "Test Co", "ticket_type": "press",
        })
        aid = resp.json()["attendee_id"]

        sync1 = uaj_client.get(f"/api/v1/sync/status/{aid}").json()
        assert sync1["sync_status"] == "failed"

        # Step 2: Platforms recover
        uaj_client.post("/test/sync-failure", params={"expo_connect": False, "session_hub": False})

        # Step 3: Manual re-sync
        resync = uaj_client.post("/api/v1/sync/trigger", json={"attendee_id": aid})
        assert resync.status_code == 200
        assert resync.json()["sync_status"] == "completed"

        # Step 4: Verify data is now available
        expo = uaj_client.get(f"/api/v1/expo/attendee/{aid}")
        session = uaj_client.get(f"/api/v1/sessions/attendee/{aid}")
        assert expo.status_code == 200
        assert session.status_code == 200

    @allure.story("Sync Failure")
    @allure.title("TC-056: Sync for non-existent attendee → 404")
    @pytest.mark.negative
    def test_sync_nonexistent_attendee(self, uaj_client: httpx.Client):
        """[EG] Trigger sync for an ID that doesn't exist."""
        resp = uaj_client.post(
            "/api/v1/sync/trigger",
            json={"attendee_id": "non-existent-uuid"},
        )

        assert resp.status_code == 404
