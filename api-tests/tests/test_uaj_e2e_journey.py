"""
UAJ Test Suite — End-to-End Journey Tests
==========================================
ISTQB Level: System Testing (Ch 2.2)

These tests verify the COMPLETE attendee journey across all integrated platforms.
If individual unit tests pass but E2E fails, it means the INTEGRATION has a defect.

Each test combines multiple user stories into a single flow:
  US-001 (Register) → US-002 (Sync) → US-006 (Check-in)
"""

import allure
import httpx
import pytest

from models.uaj import (
    RegisterResponse,
    SyncStatus,
    ExpoAttendee,
    SessionAttendee,
    CheckinResponse,
    CheckinStatus,
)


@allure.epic("UAJ — Unified Attendee Journey")
@allure.feature("End-to-End Journey")
class TestE2EJourney:
    """Full attendee journey tests — the ultimate integration validation."""

    @allure.story("Standard Attendee Journey")
    @allure.title("TC-100: Full journey — Standard attendee")
    @pytest.mark.smoke
    @pytest.mark.e2e
    def test_full_journey_standard(self, uaj_client: httpx.Client):
        """
        Complete journey for Standard ticket:
        Register → Sync → Verify on all platforms → Email → Check-in
        → Verify VIP lounge denied → Verify check-in status
        """
        # Step 1: Register
        with allure.step("Step 1: Register Standard attendee"):
            reg_resp = uaj_client.post("/api/v1/register", json={
                "first_name": "Standard", "last_name": "Journey",
                "email": "standard.journey@test.com", "company": "Journey Corp",
                "job_title": "Tester", "ticket_type": "standard",
                "payment_token": "tok_valid_visa",
            })
            assert reg_resp.status_code == 201
            reg = RegisterResponse(**reg_resp.json())
            aid = reg.attendee_id
            qr = reg.qr_code

        # Step 2: Verify sync completed
        with allure.step("Step 2: Verify cross-platform sync"):
            sync_resp = uaj_client.get(f"/api/v1/sync/status/{aid}")
            assert sync_resp.status_code == 200
            sync = SyncStatus(**sync_resp.json())
            assert sync.sync_status == "completed"

        # Step 3: Verify data on ExpoConnect
        with allure.step("Step 3: Verify profile on ExpoConnect"):
            expo_resp = uaj_client.get(f"/api/v1/expo/attendee/{aid}")
            assert expo_resp.status_code == 200
            expo = ExpoAttendee(**expo_resp.json())
            assert expo.first_name == "Standard"
            assert expo.ticket_type == "standard"

        # Step 4: Verify data on SessionHub
        with allure.step("Step 4: Verify profile on SessionHub"):
            sess_resp = uaj_client.get(f"/api/v1/sessions/attendee/{aid}")
            assert sess_resp.status_code == 200
            sess = SessionAttendee(**sess_resp.json())
            assert sess.first_name == "Standard"
            assert sess.ticket_type == "standard"

        # Step 5: Verify confirmation email
        with allure.step("Step 5: Verify confirmation email sent"):
            emails = uaj_client.get("/test/emails").json()
            assert len(emails) == 1
            assert emails[0]["to"] == "standard.journey@test.com"
            assert emails[0]["ticket_type"] == "standard"

        # Step 6: Check-in at main entrance
        with allure.step("Step 6: Check-in at main entrance"):
            ci1 = uaj_client.post("/api/v1/checkin", json={"qr_code": qr, "checkpoint": "main_entrance"})
            assert ci1.status_code == 200

        # Step 7: Check-in at expo hall
        with allure.step("Step 7: Check-in at expo hall"):
            ci2 = uaj_client.post("/api/v1/checkin", json={"qr_code": qr, "checkpoint": "expo_hall"})
            assert ci2.status_code == 200

        # Step 8: VIP lounge DENIED for Standard
        with allure.step("Step 8: Verify VIP lounge access DENIED"):
            ci3 = uaj_client.post("/api/v1/checkin", json={"qr_code": qr, "checkpoint": "vip_lounge"})
            assert ci3.status_code == 403

        # Step 9: Verify check-in status shows 2 entries
        with allure.step("Step 9: Verify check-in status"):
            status = uaj_client.get(f"/api/v1/checkin/status/{aid}")
            checkins = CheckinStatus(**status.json())
            assert len(checkins.checkins) == 2

    @allure.story("VIP Attendee Journey")
    @allure.title("TC-101: Full journey — VIP attendee")
    @pytest.mark.smoke
    @pytest.mark.e2e
    def test_full_journey_vip(self, uaj_client: httpx.Client):
        """
        Complete journey for VIP ticket:
        Register → Sync → Verify ticket_type='vip' EVERYWHERE → Check-in
        → VIP lounge ALLOWED → Verify all check-ins
        """
        # Step 1: Register VIP
        with allure.step("Step 1: Register VIP attendee"):
            reg_resp = uaj_client.post("/api/v1/register", json={
                "first_name": "VIP", "last_name": "Journey",
                "email": "vip.journey@test.com", "company": "VIP Corp",
                "ticket_type": "vip", "payment_token": "tok_valid_visa",
            })
            assert reg_resp.status_code == 201
            reg = RegisterResponse(**reg_resp.json())
            aid = reg.attendee_id
            qr = reg.qr_code

        # Step 2: CRITICAL — Verify ticket_type = 'vip' on ALL platforms
        with allure.step("Step 2: Verify ticket_type='vip' across all platforms"):
            reg_profile = uaj_client.get(f"/api/v1/attendee/{aid}").json()
            expo_profile = uaj_client.get(f"/api/v1/expo/attendee/{aid}").json()
            sess_profile = uaj_client.get(f"/api/v1/sessions/attendee/{aid}").json()

            assert reg_profile["ticket_type"] == "vip", "RegPlatform: VIP not preserved!"
            assert expo_profile["ticket_type"] == "vip", "ExpoConnect: VIP not preserved!"
            assert sess_profile["ticket_type"] == "vip", "SessionHub: VIP not preserved!"

        # Step 3: Verify email shows VIP
        with allure.step("Step 3: Verify email shows VIP ticket type"):
            emails = uaj_client.get("/test/emails").json()
            assert emails[0]["ticket_type"] == "vip"

        # Step 4: Check-in at main entrance
        with allure.step("Step 4: Check-in at main entrance"):
            ci1 = uaj_client.post("/api/v1/checkin", json={"qr_code": qr, "checkpoint": "main_entrance"})
            assert ci1.status_code == 200

        # Step 5: VIP lounge ALLOWED
        with allure.step("Step 5: Check-in at VIP lounge (should be ALLOWED)"):
            ci2 = uaj_client.post("/api/v1/checkin", json={"qr_code": qr, "checkpoint": "vip_lounge"})
            assert ci2.status_code == 200

        # Step 6: Verify all check-ins
        with allure.step("Step 6: Verify check-in history"):
            status = CheckinStatus(**uaj_client.get(f"/api/v1/checkin/status/{aid}").json())
            assert len(status.checkins) == 2
            checkpoints = [c.checkpoint for c in status.checkins]
            assert "main_entrance" in checkpoints
            assert "vip_lounge" in checkpoints

    @allure.story("Press Attendee Journey")
    @allure.title("TC-102: Full journey — Press attendee (no payment)")
    @pytest.mark.smoke
    @pytest.mark.e2e
    def test_full_journey_press(self, uaj_client: httpx.Client):
        """
        Complete journey for Press ticket:
        Register (no payment) → Sync → Email (no payment ref) →
        Check-in at main → VIP lounge ALLOWED (press has access)
        """
        # Step 1: Register Press (no payment)
        with allure.step("Step 1: Register Press attendee (no payment)"):
            reg_resp = uaj_client.post("/api/v1/register", json={
                "first_name": "Press", "last_name": "Journey",
                "email": "press.journey@test.com", "company": "News Daily",
                "ticket_type": "press", "payment_token": None,
            })
            assert reg_resp.status_code == 201
            reg = RegisterResponse(**reg_resp.json())
            aid = reg.attendee_id
            qr = reg.qr_code

        # Step 2: Verify sync
        with allure.step("Step 2: Verify sync completed"):
            sync = uaj_client.get(f"/api/v1/sync/status/{aid}").json()
            assert sync["sync_status"] == "completed"

        # Step 3: Check-in main entrance
        with allure.step("Step 3: Check-in at main entrance"):
            ci1 = uaj_client.post("/api/v1/checkin", json={"qr_code": qr, "checkpoint": "main_entrance"})
            assert ci1.status_code == 200

        # Step 4: VIP lounge — Press ALLOWED
        with allure.step("Step 4: Check-in at VIP lounge (Press has access)"):
            ci2 = uaj_client.post("/api/v1/checkin", json={"qr_code": qr, "checkpoint": "vip_lounge"})
            assert ci2.status_code == 200

    @allure.story("Journey with Sync Failure")
    @allure.title("TC-103: Journey with sync failure and recovery")
    @pytest.mark.regression
    @pytest.mark.e2e
    def test_journey_sync_failure_recovery(self, uaj_client: httpx.Client):
        """
        Attendee journey despite sync failure:
        Register → Sync FAILS → Verify partial state → Platform recovers →
        Manual re-sync → Full data available → Check-in works
        """
        # Step 1: Break ExpoConnect
        with allure.step("Step 1: Simulate ExpoConnect failure"):
            uaj_client.post("/test/sync-failure", params={"expo_connect": True})

        # Step 2: Register (sync will be partial)
        with allure.step("Step 2: Register attendee (sync will partially fail)"):
            reg_resp = uaj_client.post("/api/v1/register", json={
                "first_name": "Recovery", "last_name": "Journey",
                "email": "recovery@test.com", "company": "Test Co",
                "ticket_type": "standard", "payment_token": "tok_valid_visa",
            })
            assert reg_resp.status_code == 201
            aid = reg_resp.json()["attendee_id"]
            qr = reg_resp.json()["qr_code"]

        # Step 3: Verify partial sync
        with allure.step("Step 3: Verify sync is partial (ExpoConnect failed)"):
            sync = uaj_client.get(f"/api/v1/sync/status/{aid}").json()
            assert sync["sync_status"] == "partial"
            assert sync["platforms"]["expo_connect"]["status"] == "failed"
            assert sync["platforms"]["session_hub"]["status"] == "synced"

        # Step 4: ExpoConnect not available
        with allure.step("Step 4: ExpoConnect returns 404 (not synced)"):
            expo = uaj_client.get(f"/api/v1/expo/attendee/{aid}")
            assert expo.status_code == 404

        # Step 5: Platform recovers + manual re-sync
        with allure.step("Step 5: Platform recovers, trigger manual re-sync"):
            uaj_client.post("/test/sync-failure", params={"expo_connect": False})
            resync = uaj_client.post("/api/v1/sync/trigger", json={"attendee_id": aid})
            assert resync.json()["sync_status"] == "completed"

        # Step 6: ExpoConnect now has data
        with allure.step("Step 6: Verify ExpoConnect now has attendee data"):
            expo = uaj_client.get(f"/api/v1/expo/attendee/{aid}")
            assert expo.status_code == 200
            assert expo.json()["first_name"] == "Recovery"

        # Step 7: Check-in still works
        with allure.step("Step 7: Check-in works after recovery"):
            ci = uaj_client.post("/api/v1/checkin", json={"qr_code": qr, "checkpoint": "main_entrance"})
            assert ci.status_code == 200
