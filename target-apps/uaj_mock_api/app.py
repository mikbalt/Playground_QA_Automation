"""
UAJ Mock API Server — Unified Attendee Journey
================================================
A FastAPI mock server simulating the UAJ platform APIs for testing.

Platforms simulated:
- RegPlatform  (registration, attendee profiles)
- Sync Service (cross-platform sync)
- ExpoConnect  (exhibitor-facing attendee data)
- SessionHub   (session-facing attendee data)
- Check-in     (QR code scanning at checkpoints)

Run: uvicorn app:app --port 8000 --reload
"""

import base64
import hashlib
import time
import uuid
from datetime import datetime, timezone
from enum import Enum
from threading import Timer

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator

app = FastAPI(title="UAJ Mock API", version="0.1.0")

# ---------------------------------------------------------------------------
# In-memory stores
# ---------------------------------------------------------------------------
attendees: dict[str, dict] = {}
sync_statuses: dict[str, dict] = {}
checkins: dict[str, list[dict]] = {}
dead_letter_queue: list[dict] = []
emails_sent: list[dict] = []


# ---------------------------------------------------------------------------
# Enums & Models
# ---------------------------------------------------------------------------
class TicketType(str, Enum):
    standard = "standard"
    vip = "vip"
    press = "press"


class Checkpoint(str, Enum):
    main_entrance = "main_entrance"
    expo_hall = "expo_hall"
    vip_lounge = "vip_lounge"


class RegisterRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: str  # validated manually for richer error messages
    company: str = Field(..., min_length=1, max_length=100)
    job_title: str | None = Field(None, max_length=100)
    ticket_type: TicketType
    payment_token: str | None = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not v or not isinstance(v, str):
            raise ValueError("Email is required")
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email format")
        return v.lower().strip()


class SyncTriggerRequest(BaseModel):
    attendee_id: str


class CheckinRequest(BaseModel):
    qr_code: str
    checkpoint: Checkpoint


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
DECLINED_TOKENS = {"tok_declined", "tok_expired", "tok_insufficient"}

# Simulate sync failure mode (toggle via API for testing)
_sync_failure_mode: dict[str, bool] = {"expo_connect": False, "session_hub": False}


def _generate_qr(attendee_id: str) -> str:
    raw = f"UAJ-{attendee_id}".encode()
    return base64.b64encode(raw).decode()


def _find_attendee_by_qr(qr_code: str) -> dict | None:
    for att in attendees.values():
        if att.get("qr_code") == qr_code:
            return att
    return None


def _do_sync(attendee_id: str, attempt: int = 1) -> None:
    """Simulate async sync with retry logic."""
    if attendee_id not in attendees:
        return

    expo_ok = not _sync_failure_mode["expo_connect"]
    session_ok = not _sync_failure_mode["session_hub"]

    if expo_ok and session_ok:
        sync_statuses[attendee_id] = {
            "attendee_id": attendee_id,
            "sync_status": "completed",
            "platforms": {
                "expo_connect": {"status": "synced", "last_sync": _now()},
                "session_hub": {"status": "synced", "last_sync": _now()},
            },
        }
    elif expo_ok or session_ok:
        sync_statuses[attendee_id] = {
            "attendee_id": attendee_id,
            "sync_status": "partial",
            "platforms": {
                "expo_connect": {
                    "status": "synced" if expo_ok else "failed",
                    "last_sync": _now() if expo_ok else None,
                },
                "session_hub": {
                    "status": "synced" if session_ok else "failed",
                    "last_sync": _now() if session_ok else None,
                },
            },
        }
        if attempt < 3:
            # schedule retry (in real system: exponential backoff)
            pass  # mock doesn't actually retry async
    else:
        if attempt >= 3:
            sync_statuses[attendee_id] = {
                "attendee_id": attendee_id,
                "sync_status": "failed",
                "platforms": {
                    "expo_connect": {"status": "failed", "last_sync": None},
                    "session_hub": {"status": "failed", "last_sync": None},
                },
            }
            dead_letter_queue.append(
                {"attendee_id": attendee_id, "failed_at": _now(), "attempts": attempt}
            )
        else:
            sync_statuses[attendee_id] = {
                "attendee_id": attendee_id,
                "sync_status": "failed",
                "platforms": {
                    "expo_connect": {"status": "failed", "last_sync": None},
                    "session_hub": {"status": "failed", "last_sync": None},
                },
            }


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Test Control Endpoints (for test setup/teardown)
# ---------------------------------------------------------------------------
@app.post("/test/reset")
def reset_state():
    """Reset all in-memory data. Call this in test setup."""
    attendees.clear()
    sync_statuses.clear()
    checkins.clear()
    dead_letter_queue.clear()
    emails_sent.clear()
    _sync_failure_mode["expo_connect"] = False
    _sync_failure_mode["session_hub"] = False
    return {"status": "reset"}


@app.post("/test/sync-failure")
def set_sync_failure(expo_connect: bool = False, session_hub: bool = False):
    """Toggle sync failure simulation for testing retry/failure scenarios."""
    _sync_failure_mode["expo_connect"] = expo_connect
    _sync_failure_mode["session_hub"] = session_hub
    return {"expo_connect_failing": expo_connect, "session_hub_failing": session_hub}


@app.get("/test/emails")
def get_sent_emails():
    """Retrieve all confirmation emails sent (for test assertions)."""
    return emails_sent


@app.get("/test/dlq")
def get_dead_letter_queue():
    """Retrieve dead letter queue entries."""
    return dead_letter_queue


# ---------------------------------------------------------------------------
# RegPlatform APIs
# ---------------------------------------------------------------------------
@app.post("/api/v1/register", status_code=201)
def register_attendee(req: RegisterRequest):
    # Check duplicate email
    for att in attendees.values():
        if att["email"] == req.email.lower().strip():
            raise HTTPException(
                status_code=409,
                detail={"error": "duplicate_email", "message": "Email already registered for this event"},
            )

    # Payment validation
    if req.ticket_type in (TicketType.standard, TicketType.vip):
        if not req.payment_token:
            raise HTTPException(
                status_code=400,
                detail={"error": "validation_error", "details": ["Payment token required for standard/vip ticket"]},
            )
        if req.payment_token in DECLINED_TOKENS:
            raise HTTPException(
                status_code=402,
                detail={"error": "payment_failed", "message": f"Payment declined: {req.payment_token}"},
            )

    # Create attendee
    attendee_id = str(uuid.uuid4())
    qr_code = _generate_qr(attendee_id)

    attendee = {
        "attendee_id": attendee_id,
        "first_name": req.first_name,
        "last_name": req.last_name,
        "email": req.email.lower().strip(),
        "company": req.company,
        "job_title": req.job_title,
        "ticket_type": req.ticket_type.value,
        "status": "registered",
        "qr_code": qr_code,
        "registered_at": _now(),
    }
    attendees[attendee_id] = attendee

    # Simulate confirmation email
    emails_sent.append({
        "to": req.email,
        "subject": "Registration Confirmed — EventHub Singapore 2026",
        "attendee_name": f"{req.first_name} {req.last_name}",
        "ticket_type": req.ticket_type.value,
        "qr_code": qr_code,
        "sent_at": _now(),
    })

    # Auto-trigger sync
    _do_sync(attendee_id)

    return {
        "attendee_id": attendee_id,
        "qr_code": qr_code,
        "status": "registered",
    }


@app.get("/api/v1/attendee/{attendee_id}")
def get_attendee(attendee_id: str):
    if attendee_id not in attendees:
        raise HTTPException(status_code=404, detail={"error": "not_found"})
    return attendees[attendee_id]


# ---------------------------------------------------------------------------
# Sync APIs
# ---------------------------------------------------------------------------
@app.post("/api/v1/sync/trigger")
def trigger_sync(req: SyncTriggerRequest):
    if req.attendee_id not in attendees:
        raise HTTPException(status_code=404, detail={"error": "attendee_not_found"})

    _do_sync(req.attendee_id)
    return sync_statuses.get(req.attendee_id, {"sync_status": "pending"})


@app.get("/api/v1/sync/status/{attendee_id}")
def get_sync_status(attendee_id: str):
    if attendee_id not in attendees:
        raise HTTPException(status_code=404, detail={"error": "attendee_not_found"})

    status = sync_statuses.get(attendee_id)
    if not status:
        return {
            "attendee_id": attendee_id,
            "sync_status": "pending",
            "platforms": {
                "expo_connect": {"status": "pending", "last_sync": None},
                "session_hub": {"status": "pending", "last_sync": None},
            },
        }
    return status


# ---------------------------------------------------------------------------
# ExpoConnect APIs
# ---------------------------------------------------------------------------
@app.get("/api/v1/expo/attendee/{attendee_id}")
def get_expo_attendee(attendee_id: str):
    if attendee_id not in attendees:
        raise HTTPException(status_code=404, detail={"error": "not_found"})

    sync = sync_statuses.get(attendee_id)
    if not sync or sync["platforms"]["expo_connect"]["status"] != "synced":
        raise HTTPException(status_code=404, detail={"error": "not_synced"})

    att = attendees[attendee_id]
    # ExpoConnect only gets: name, email, company, ticket_type (NO job_title, payment, qr)
    return {
        "attendee_id": att["attendee_id"],
        "first_name": att["first_name"],
        "last_name": att["last_name"],
        "email": att["email"],
        "company": att["company"],
        "ticket_type": att["ticket_type"],
    }


# ---------------------------------------------------------------------------
# SessionHub APIs
# ---------------------------------------------------------------------------
@app.get("/api/v1/sessions/attendee/{attendee_id}")
def get_session_attendee(attendee_id: str):
    if attendee_id not in attendees:
        raise HTTPException(status_code=404, detail={"error": "not_found"})

    sync = sync_statuses.get(attendee_id)
    if not sync or sync["platforms"]["session_hub"]["status"] != "synced":
        raise HTTPException(status_code=404, detail={"error": "not_synced"})

    att = attendees[attendee_id]
    # SessionHub only gets: name, email, ticket_type (NO company, job_title, payment, qr)
    return {
        "attendee_id": att["attendee_id"],
        "first_name": att["first_name"],
        "last_name": att["last_name"],
        "email": att["email"],
        "ticket_type": att["ticket_type"],
    }


# ---------------------------------------------------------------------------
# Check-in APIs
# ---------------------------------------------------------------------------
@app.post("/api/v1/checkin")
def checkin(req: CheckinRequest):
    # Find attendee by QR code
    attendee = _find_attendee_by_qr(req.qr_code)
    if not attendee:
        raise HTTPException(
            status_code=400,
            detail={"error": "invalid_qr", "message": "QR code is not valid"},
        )

    attendee_id = attendee["attendee_id"]

    # VIP lounge access control
    if req.checkpoint == Checkpoint.vip_lounge:
        if attendee["ticket_type"] == "standard":
            raise HTTPException(
                status_code=403,
                detail={"error": "access_denied", "message": "VIP lounge requires VIP or Press ticket"},
            )

    # Check for duplicate check-in at same checkpoint
    existing = checkins.get(attendee_id, [])
    for ci in existing:
        if ci["checkpoint"] == req.checkpoint.value:
            raise HTTPException(
                status_code=409,
                detail={
                    "error": "already_checked_in",
                    "message": "Already checked in at this checkpoint",
                    "original_timestamp": ci["timestamp"],
                },
            )

    # Record check-in
    checkin_record = {
        "checkpoint": req.checkpoint.value,
        "timestamp": _now(),
    }
    if attendee_id not in checkins:
        checkins[attendee_id] = []
    checkins[attendee_id].append(checkin_record)

    return {
        "attendee_id": attendee_id,
        "name": f"{attendee['first_name']} {attendee['last_name']}",
        "ticket_type": attendee["ticket_type"],
        "status": "checked_in",
        "checkpoint": req.checkpoint.value,
        "timestamp": checkin_record["timestamp"],
    }


@app.get("/api/v1/checkin/status/{attendee_id}")
def get_checkin_status(attendee_id: str):
    if attendee_id not in attendees:
        raise HTTPException(status_code=404, detail={"error": "not_found"})

    return {
        "attendee_id": attendee_id,
        "checkins": checkins.get(attendee_id, []),
    }


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok", "timestamp": _now()}
