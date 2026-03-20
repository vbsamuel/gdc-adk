from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional
import uuid

from gdc_adk.core.contracts import Event
from gdc_adk.core.state import validate_event_type
from gdc_adk.core.contracts import validate_event_record

EVENTS: List[Event] = []


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _ensure_unique_event_id(event_id: str) -> None:
    if any(existing["event_id"] == event_id for existing in EVENTS):
        raise ValueError(f"Duplicate event_id: {event_id}")


def record_event(event: Event) -> Event:
    validate_event_record(event)
    _ensure_unique_event_id(event["event_id"])
    EVENTS.append(dict(event))
    return event


def reset_events() -> None:
    EVENTS.clear()


def export_event_records() -> List[Event]:
    return [dict(event) for event in EVENTS]


def load_event_records(events: List[Event]) -> None:
    reset_events()
    for event in events:
        record_event(event)


def get_event(event_id: str) -> Event:
    for event in EVENTS:
        if event["event_id"] == event_id:
            return event
    raise KeyError(f"Event not found: {event_id}")


def list_events() -> List[Event]:
    return list(EVENTS)


def list_events_by_correlation_id(correlation_id: str) -> List[Event]:
    return [e for e in EVENTS if e["correlation_id"] == correlation_id]


def list_events_by_workflow_run_id(workflow_run_id: Optional[str]) -> List[Event]:
    return [e for e in EVENTS if e["workflow_run_id"] == workflow_run_id]


def list_events_by_event_type(event_type: str) -> List[Event]:
    validate_event_type(event_type)
    return [e for e in EVENTS if e["event_type"] == event_type]


def create_event(event_type: str, correlation_id: str, payload: dict, workflow_run_id: Optional[str] = None) -> Event:
    event: Event = {
        "event_id": f"evt_{uuid.uuid4().hex[:12]}",
        "event_type": validate_event_type(event_type),
        "created_at": _now_iso(),
        "correlation_id": correlation_id,
        "workflow_run_id": workflow_run_id,
        "payload": payload,
    }
    return record_event(event)
