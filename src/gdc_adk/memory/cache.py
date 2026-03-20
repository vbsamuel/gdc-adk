from __future__ import annotations

from datetime import UTC, datetime
from typing import Iterable

from gdc_adk.memory.contracts import CacheExportResult, CacheLifecycleResult, CacheRecord


_CACHE: dict[str, CacheRecord] = {}


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def put_result(key: str, payload: dict[str, object], metadata: dict[str, object]) -> CacheLifecycleResult:
    if not isinstance(key, str) or not key.strip():
        raise ValueError("key must be a non-empty string.")
    if not isinstance(payload, dict) or not payload:
        raise ValueError("payload must be a non-empty dict.")
    if not isinstance(metadata, dict):
        raise ValueError("metadata must be a dict.")

    record = CacheRecord(
        cache_key=key,
        payload=dict(payload),
        metadata=dict(metadata),
        created_at=_utc_now(),
        expires_at=str(metadata["expires_at"]) if "expires_at" in metadata else None,
    )
    _CACHE[key] = record
    return CacheLifecycleResult(status="stored", cache_record=record, message="Cache record stored.")


def get_result(key: str) -> CacheLifecycleResult | None:
    if not isinstance(key, str) or not key.strip():
        raise ValueError("key must be a non-empty string.")
    record = _CACHE.get(key)
    if record is None or record.invalidated_at is not None:
        return None
    return CacheLifecycleResult(status="hit", cache_record=record, message="Cache hit.")


def invalidate_result(key: str) -> CacheLifecycleResult:
    if not isinstance(key, str) or not key.strip():
        raise ValueError("key must be a non-empty string.")
    record = _CACHE.get(key)
    if record is None:
        raise ValueError(f"Unknown cache key: {key}")
    invalidated_record = CacheRecord(
        cache_key=record.cache_key,
        payload=record.payload,
        metadata=record.metadata,
        created_at=record.created_at,
        expires_at=record.expires_at,
        invalidated_at=_utc_now(),
    )
    _CACHE[key] = invalidated_record
    return CacheLifecycleResult(status="invalidated", cache_record=invalidated_record, message="Cache record invalidated.")


def export_results(filter_spec: dict[str, object] | None = None) -> CacheExportResult:
    filter_spec = dict(filter_spec or {})
    scope_value = filter_spec.get("scope")
    records: list[CacheRecord] = []
    for record in _CACHE.values():
        if scope_value is not None and record.metadata.get("scope") != scope_value:
            continue
        records.append(record)
    return CacheExportResult(records=tuple(records))


def reset_cache_store() -> None:
    _CACHE.clear()


def load_cache_records(records: Iterable[CacheRecord]) -> None:
    if not isinstance(records, Iterable):
        raise ValueError("records must be an iterable of CacheRecord.")
    reset_cache_store()
    for record in records:
        if not isinstance(record, CacheRecord):
            raise ValueError("all records must be CacheRecord instances.")
        if record.cache_key in _CACHE:
            raise ValueError(f"Duplicate cache_key during load: {record.cache_key}")
        _CACHE[record.cache_key] = record
