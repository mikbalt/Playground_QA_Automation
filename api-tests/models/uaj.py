"""Pydantic models for UAJ API responses."""

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# RegPlatform
# ---------------------------------------------------------------------------
class RegisterResponse(BaseModel):
    attendee_id: str
    qr_code: str
    status: str


class AttendeeProfile(BaseModel):
    attendee_id: str
    first_name: str
    last_name: str
    email: str
    company: str
    job_title: str | None = None
    ticket_type: str
    status: str
    qr_code: str
    registered_at: str


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------
class PlatformSyncDetail(BaseModel):
    status: str  # synced | pending | failed
    last_sync: str | None = None


class SyncStatus(BaseModel):
    attendee_id: str
    sync_status: str  # completed | partial | failed | pending
    platforms: dict[str, PlatformSyncDetail]


# ---------------------------------------------------------------------------
# ExpoConnect
# ---------------------------------------------------------------------------
class ExpoAttendee(BaseModel):
    attendee_id: str
    first_name: str
    last_name: str
    email: str
    company: str
    ticket_type: str


# ---------------------------------------------------------------------------
# SessionHub
# ---------------------------------------------------------------------------
class SessionAttendee(BaseModel):
    attendee_id: str
    first_name: str
    last_name: str
    email: str
    ticket_type: str


# ---------------------------------------------------------------------------
# Check-in
# ---------------------------------------------------------------------------
class CheckinResponse(BaseModel):
    attendee_id: str
    name: str
    ticket_type: str
    status: str
    checkpoint: str
    timestamp: str


class CheckinEntry(BaseModel):
    checkpoint: str
    timestamp: str


class CheckinStatus(BaseModel):
    attendee_id: str
    checkins: list[CheckinEntry]


# ---------------------------------------------------------------------------
# Error
# ---------------------------------------------------------------------------
class ErrorResponse(BaseModel):
    error: str
    message: str | None = None
    details: list[str] | None = None
