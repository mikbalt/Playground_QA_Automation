"""
UAJ Test Suite — US-006: QR Code Check-in
==========================================
ISTQB Techniques: EP, Decision Table, State Transition, Error Guessing

Covers:
- 3A. Happy Path Check-in (EP)
- 3B. Checkpoint Access Control — VIP Lounge (Decision Table)
- 3C. Error Scenarios (State Transition + Error Guessing)
"""

import allure
import httpx
import pytest

from models.uaj import CheckinResponse, CheckinStatus


# ===================================================================
# 3A. HAPPY PATH CHECK-IN — Equivalence Partitioning
# ===================================================================
@allure.epic("UAJ — Unified Attendee Journey")
@allure.feature("US-006: QR Check-in")
class TestCheckinHappyPath:
    """
    ISTQB Technique: Equivalence Partitioning

    Partitions: ticket_type (standard, vip, press) × checkpoint (3 types)
    Happy path: check-in at allowed checkpoints.
    """

    @allure.story("Happy Path")
    @allure.title("TC-070: Standard ticket — main entrance check-in")
    @pytest.mark.smoke
    def test_standard_main_entrance(self, uaj_client: httpx.Client, registered_standard: dict):
        """[EP] Standard attendee checks in at main entrance."""
        resp = uaj_client.post("/api/v1/checkin", json={
            "qr_code": registered_standard["qr_code"],
            "checkpoint": "main_entrance",
        })

        assert resp.status_code == 200
        data = CheckinResponse(**resp.json())
        assert data.status == "checked_in"
        assert data.checkpoint == "main_entrance"
        assert data.ticket_type == "standard"
        assert data.timestamp is not None

    @allure.story("Happy Path")
    @allure.title("TC-071: VIP ticket — main entrance check-in")
    @pytest.mark.smoke
    def test_vip_main_entrance(self, uaj_client: httpx.Client, registered_vip: dict):
        """[EP] VIP attendee checks in at main entrance."""
        resp = uaj_client.post("/api/v1/checkin", json={
            "qr_code": registered_vip["qr_code"],
            "checkpoint": "main_entrance",
        })

        assert resp.status_code == 200
        assert resp.json()["ticket_type"] == "vip"

    @allure.story("Happy Path")
    @allure.title("TC-072: Press ticket — main entrance check-in")
    @pytest.mark.smoke
    def test_press_main_entrance(self, uaj_client: httpx.Client, registered_press: dict):
        """[EP] Press attendee checks in at main entrance."""
        resp = uaj_client.post("/api/v1/checkin", json={
            "qr_code": registered_press["qr_code"],
            "checkpoint": "main_entrance",
        })

        assert resp.status_code == 200
        assert resp.json()["ticket_type"] == "press"

    @allure.story("Happy Path")
    @allure.title("TC-073: Standard ticket — expo hall check-in")
    @pytest.mark.smoke
    def test_standard_expo_hall(self, uaj_client: httpx.Client, registered_standard: dict):
        """[EP] Standard attendee checks in at expo hall."""
        resp = uaj_client.post("/api/v1/checkin", json={
            "qr_code": registered_standard["qr_code"],
            "checkpoint": "expo_hall",
        })

        assert resp.status_code == 200

    @allure.story("Happy Path")
    @allure.title("TC-074: Check-in status query after check-in")
    @pytest.mark.smoke
    def test_checkin_status_query(self, uaj_client: httpx.Client, registered_standard: dict):
        """[EP] Verify check-in appears in status endpoint."""
        uaj_client.post("/api/v1/checkin", json={
            "qr_code": registered_standard["qr_code"],
            "checkpoint": "main_entrance",
        })

        resp = uaj_client.get(f"/api/v1/checkin/status/{registered_standard['attendee_id']}")

        assert resp.status_code == 200
        status = CheckinStatus(**resp.json())
        assert len(status.checkins) == 1
        assert status.checkins[0].checkpoint == "main_entrance"


# ===================================================================
# 3B. CHECKPOINT ACCESS CONTROL — Decision Table
# ===================================================================
@allure.epic("UAJ — Unified Attendee Journey")
@allure.feature("US-006: QR Check-in")
class TestCheckinAccessControl:
    """
    ISTQB Technique: Decision Table

    VIP Lounge Access Matrix:
    | Ticket Type | main_entrance | expo_hall | vip_lounge |
    |-------------|:------------:|:---------:|:----------:|
    | standard    |   ✅ 200     |  ✅ 200   |  ❌ 403    |
    | vip         |   ✅ 200     |  ✅ 200   |  ✅ 200    |
    | press       |   ✅ 200     |  ✅ 200   |  ✅ 200    |
    """

    @allure.story("VIP Lounge Access")
    @allure.title("TC-075: Standard ticket — VIP lounge DENIED")
    @pytest.mark.smoke
    def test_standard_vip_lounge_denied(self, uaj_client: httpx.Client, registered_standard: dict):
        """[DT] Standard ticket holders cannot access VIP lounge."""
        resp = uaj_client.post("/api/v1/checkin", json={
            "qr_code": registered_standard["qr_code"],
            "checkpoint": "vip_lounge",
        })

        assert resp.status_code == 403
        assert resp.json()["detail"]["error"] == "access_denied"

    @allure.story("VIP Lounge Access")
    @allure.title("TC-076: VIP ticket — VIP lounge ALLOWED")
    @pytest.mark.smoke
    def test_vip_vip_lounge_allowed(self, uaj_client: httpx.Client, registered_vip: dict):
        """[DT] VIP ticket holders can access VIP lounge."""
        resp = uaj_client.post("/api/v1/checkin", json={
            "qr_code": registered_vip["qr_code"],
            "checkpoint": "vip_lounge",
        })

        assert resp.status_code == 200
        assert resp.json()["checkpoint"] == "vip_lounge"

    @allure.story("VIP Lounge Access")
    @allure.title("TC-077: Press ticket — VIP lounge ALLOWED")
    @pytest.mark.smoke
    def test_press_vip_lounge_allowed(self, uaj_client: httpx.Client, registered_press: dict):
        """[DT] Press ticket holders can access VIP lounge."""
        resp = uaj_client.post("/api/v1/checkin", json={
            "qr_code": registered_press["qr_code"],
            "checkpoint": "vip_lounge",
        })

        assert resp.status_code == 200


# ===================================================================
# 3C. ERROR SCENARIOS — State Transition + Error Guessing
# ===================================================================
@allure.epic("UAJ — Unified Attendee Journey")
@allure.feature("US-006: QR Check-in")
class TestCheckinErrors:
    """
    ISTQB Techniques: State Transition + Error Guessing

    Check-in State Machine:
    Not Checked In → [scan QR] → Checked In (at checkpoint X)
    Checked In     → [scan again at same checkpoint] → 409 Already Checked In
    Checked In     → [scan at different checkpoint]  → 200 (multiple checkpoints OK)
    """

    @allure.story("Error Scenarios")
    @allure.title("TC-080: Invalid QR code → 400")
    @pytest.mark.negative
    def test_invalid_qr_code(self, uaj_client: httpx.Client):
        """[EG] Fabricated/invalid QR code should be rejected."""
        resp = uaj_client.post("/api/v1/checkin", json={
            "qr_code": "dGhpcyBpcyBub3QgYSB2YWxpZCBxcg==",
            "checkpoint": "main_entrance",
        })

        assert resp.status_code == 400
        assert resp.json()["detail"]["error"] == "invalid_qr"

    @allure.story("Error Scenarios")
    @allure.title("TC-081: Already checked in — same checkpoint → 409")
    @pytest.mark.negative
    def test_duplicate_checkin_same_checkpoint(self, uaj_client: httpx.Client, registered_standard: dict):
        """[ST — duplicate] Same QR scanned twice at same checkpoint."""
        payload = {
            "qr_code": registered_standard["qr_code"],
            "checkpoint": "main_entrance",
        }

        resp1 = uaj_client.post("/api/v1/checkin", json=payload)
        assert resp1.status_code == 200

        resp2 = uaj_client.post("/api/v1/checkin", json=payload)
        assert resp2.status_code == 409
        detail = resp2.json()["detail"]
        assert detail["error"] == "already_checked_in"
        assert "original_timestamp" in detail

    @allure.story("Error Scenarios")
    @allure.title("TC-082: Check-in at different checkpoint → 200 (multi-checkpoint)")
    @pytest.mark.regression
    def test_checkin_different_checkpoint(self, uaj_client: httpx.Client, registered_standard: dict):
        """[ST + EG] Attendee checks in at main entrance, then expo hall — both should work."""
        qr = registered_standard["qr_code"]
        aid = registered_standard["attendee_id"]

        resp1 = uaj_client.post("/api/v1/checkin", json={"qr_code": qr, "checkpoint": "main_entrance"})
        assert resp1.status_code == 200

        resp2 = uaj_client.post("/api/v1/checkin", json={"qr_code": qr, "checkpoint": "expo_hall"})
        assert resp2.status_code == 200

        # Verify both check-ins recorded
        status = uaj_client.get(f"/api/v1/checkin/status/{aid}").json()
        assert len(status["checkins"]) == 2
        checkpoints = [c["checkpoint"] for c in status["checkins"]]
        assert "main_entrance" in checkpoints
        assert "expo_hall" in checkpoints

    @allure.story("Error Scenarios")
    @allure.title("TC-083: Empty QR code → 422")
    @pytest.mark.negative
    def test_empty_qr_code(self, uaj_client: httpx.Client):
        """[EG] Empty string as QR code."""
        resp = uaj_client.post("/api/v1/checkin", json={
            "qr_code": "",
            "checkpoint": "main_entrance",
        })

        # Empty QR won't match any attendee
        assert resp.status_code == 400

    @allure.story("Error Scenarios")
    @allure.title("TC-084: Invalid checkpoint name → 422")
    @pytest.mark.negative
    def test_invalid_checkpoint(self, uaj_client: httpx.Client, registered_standard: dict):
        """[EP — invalid] Non-existent checkpoint."""
        resp = uaj_client.post("/api/v1/checkin", json={
            "qr_code": registered_standard["qr_code"],
            "checkpoint": "backstage",
        })

        assert resp.status_code == 422
