$ErrorActionPreference = "Stop"

Set-Location "C:\Users\bruno\projects\gdc-adk"

$backupRoot = ".\_stage5_contract_tightening_backup"
New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null

Copy-Item ".\src\gdc_adk\memory\contracts.py"     "$backupRoot\contracts.py.bak"     -Force
Copy-Item ".\src\gdc_adk\memory\cache.py"         "$backupRoot\cache.py.bak"         -Force
Copy-Item ".\src\gdc_adk\memory\context_store.py" "$backupRoot\context_store.py.bak" -Force
Copy-Item ".\src\gdc_adk\memory\continuity.py"    "$backupRoot\continuity.py.bak"    -Force
Copy-Item ".\src\gdc_adk\memory\replay.py"        "$backupRoot\replay.py.bak"        -Force

$contracts = @'
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class CacheRecord:
    cache_key: str
    payload: dict[str, object]
    metadata: dict[str, object]
    created_at: str
    expires_at: str | None = None
    invalidated_at: str | None = None


@dataclass(frozen=True)
class CacheLifecycleResult:
    status: str
    cache_record: CacheRecord | None = None
    message: str = ""


@dataclass(frozen=True)
class CacheExportResult:
    records: tuple[CacheRecord, ...] = ()


@dataclass(frozen=True)
class ContextBlock:
    context_block_id: str
    block_type: str
    content: dict[str, object]
    source_artifact_ids: tuple[str, ...]
    created_at: str
    tags: tuple[str, ...] = ()
    validity_window: dict[str, str] | None = None
    superseded_by: str | None = None


@dataclass(frozen=True)
class ContextStoreResult:
    status: str
    context_block: ContextBlock | None = None
    context_blocks: tuple[ContextBlock, ...] = ()
    message: str = ""


@dataclass(frozen=True)
class ContextExportResult:
    context_blocks: tuple[ContextBlock, ...] = ()


@dataclass(frozen=True)
class ContinuitySnapshot:
    snapshot_id: str
    workflow_run_id: str
    workflow_mode: str
    current_state: str
    state_history: tuple[dict[str, object], ...]
    artifact_ids: tuple[str, ...]
    issue_ids: tuple[str, ...]
    finding_ids: tuple[str, ...]
    context_refs: tuple[str, ...]
    pending_actions: tuple[str, ...]
    created_at: str
    completion_reason: str | None = None
    blocked_reason: str | None = None
    superseded_by: str | None = None


@dataclass(frozen=True)
class RehydrationResult:
    rehydration_status: str
    snapshot: ContinuitySnapshot | None
    missing_references: tuple[str, ...] = ()
    message: str = ""


@dataclass(frozen=True)
class ContinuityStoreResult:
    status: str
    snapshot: ContinuitySnapshot | None = None
    snapshots: tuple[ContinuitySnapshot, ...] = ()
    rehydration_result: RehydrationResult | None = None
    message: str = ""


@dataclass(frozen=True)
class ContinuityExportResult:
    snapshots: tuple[ContinuitySnapshot, ...] = ()


@dataclass(frozen=True)
class ReplayPackage:
    replay_package_id: str
    schema_version: str
    exported_at: str
    workflow_run_ids: tuple[str, ...]
    snapshot_ids: tuple[str, ...]
    context_block_ids: tuple[str, ...]
    artifact_summary_refs: tuple[str, ...]
    issue_evidence_refs: tuple[str, ...]
    export_source: str
    integrity_metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class ReplayBuildResult:
    replay_package: ReplayPackage
    snapshots: tuple[ContinuitySnapshot, ...] = ()
    context_blocks: tuple[ContextBlock, ...] = ()
    cache_records: tuple[CacheRecord, ...] = ()


@dataclass(frozen=True)
class ReplayValidationResult:
    status: str
    replay_package: ReplayPackage | None = None
    missing_sections: tuple[str, ...] = ()
    message: str = ""


@dataclass(frozen=True)
class ReplayRehydrationResult:
    status: str
    replay_package: ReplayPackage | None
    continuity_snapshots: tuple[ContinuitySnapshot, ...] = ()
    context_blocks: tuple[ContextBlock, ...] = ()
    cache_records: tuple[CacheRecord, ...] = ()
    missing_references: tuple[str, ...] = ()
    message: str = ""


class MemoryStore(Protocol):
    def put_result(self, key: str, payload: dict[str, object], metadata: dict[str, object]) -> CacheLifecycleResult: ...
    def get_result(self, key: str) -> CacheLifecycleResult | None: ...
    def invalidate_result(self, key: str) -> CacheLifecycleResult: ...
    def export_results(self, filter_spec: dict[str, object] | None = None) -> CacheExportResult: ...
    def reset_store(self) -> None: ...
    def load_records(self, records: tuple[CacheRecord, ...]) -> None: ...


class ContextStore(Protocol):
    def put_context_block(self, context_block: ContextBlock) -> ContextStoreResult: ...
    def get_context_block(self, context_block_id: str) -> ContextStoreResult | None: ...
    def list_context_blocks_by_artifact(self, artifact_id: str) -> list[ContextBlock]: ...
    def export_context_blocks(self, filter_spec: dict[str, object] | None = None) -> ContextExportResult: ...
    def reset_store(self) -> None: ...
    def load_records(self, records: tuple[ContextBlock, ...]) -> None: ...


class ContinuityStore(Protocol):
    def create_snapshot(self, snapshot_payload: ContinuitySnapshot) -> ContinuityStoreResult: ...
    def get_snapshot(self, snapshot_id: str) -> ContinuityStoreResult | None: ...
    def list_snapshots_for_workflow(self, workflow_run_id: str) -> list[ContinuitySnapshot]: ...
    def export_snapshots(self, filter_spec: dict[str, object] | None = None) -> ContinuityExportResult: ...
    def rehydrate_snapshot(self, snapshot_or_id: str | ContinuitySnapshot) -> ContinuityStoreResult: ...
    def reset_store(self) -> None: ...
    def load_records(self, records: tuple[ContinuitySnapshot, ...]) -> None: ...


def cache_record_to_dict(cache_record: CacheRecord) -> dict[str, object]:
    return asdict(cache_record)


def context_block_to_dict(context_block: ContextBlock) -> dict[str, object]:
    return asdict(context_block)


def continuity_snapshot_to_dict(snapshot: ContinuitySnapshot) -> dict[str, object]:
    return asdict(snapshot)


def replay_package_to_dict(replay_package: ReplayPackage) -> dict[str, object]:
    return asdict(replay_package)
'@

$cache = @'
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
'@

$contextStore = @'
from __future__ import annotations

from typing import Iterable

from gdc_adk.memory.contracts import ContextBlock, ContextExportResult, ContextStoreResult


_CONTEXT_BLOCKS: dict[str, ContextBlock] = {}


def put_context_block(context_block: ContextBlock) -> ContextStoreResult:
    if not isinstance(context_block, ContextBlock):
        raise ValueError("context_block must be a ContextBlock.")
    if not context_block.source_artifact_ids:
        raise ValueError("context_block.source_artifact_ids must contain at least one artifact identifier.")
    if context_block.context_block_id in _CONTEXT_BLOCKS:
        raise ValueError(f"context_block_id already exists: {context_block.context_block_id}")
    _CONTEXT_BLOCKS[context_block.context_block_id] = context_block
    return ContextStoreResult(status="stored", context_block=context_block, message="Context block stored.")


def get_context_block(context_block_id: str) -> ContextStoreResult | None:
    if not isinstance(context_block_id, str) or not context_block_id.strip():
        raise ValueError("context_block_id must be a non-empty string.")
    block = _CONTEXT_BLOCKS.get(context_block_id)
    if block is None:
        return None
    return ContextStoreResult(status="found", context_block=block, message="Context block found.")


def list_context_blocks_by_artifact(artifact_id: str) -> list[ContextBlock]:
    if not isinstance(artifact_id, str) or not artifact_id.strip():
        raise ValueError("artifact_id must be a non-empty string.")
    return [block for block in _CONTEXT_BLOCKS.values() if artifact_id in block.source_artifact_ids]


def mark_context_block_superseded(context_block_id: str, superseded_by_id: str) -> ContextStoreResult:
    if not isinstance(superseded_by_id, str) or not superseded_by_id.strip():
        raise ValueError("superseded_by_id must be a non-empty string.")
    result = get_context_block(context_block_id)
    if result is None or result.context_block is None:
        raise ValueError(f"Unknown context_block_id: {context_block_id}")
    updated_block = ContextBlock(
        context_block_id=result.context_block.context_block_id,
        block_type=result.context_block.block_type,
        content=result.context_block.content,
        source_artifact_ids=result.context_block.source_artifact_ids,
        created_at=result.context_block.created_at,
        tags=result.context_block.tags,
        validity_window=result.context_block.validity_window,
        superseded_by=superseded_by_id,
    )
    _CONTEXT_BLOCKS[context_block_id] = updated_block
    return ContextStoreResult(status="superseded", context_block=updated_block, message="Context block superseded.")


def export_context_blocks(filter_spec: dict[str, object] | None = None) -> ContextExportResult:
    filter_spec = dict(filter_spec or {})
    artifact_id = filter_spec.get("artifact_id")
    records: list[ContextBlock] = []
    for block in _CONTEXT_BLOCKS.values():
        if artifact_id is not None and artifact_id not in block.source_artifact_ids:
            continue
        records.append(block)
    return ContextExportResult(context_blocks=tuple(records))


def reset_context_store() -> None:
    _CONTEXT_BLOCKS.clear()


def load_context_blocks(records: Iterable[ContextBlock]) -> None:
    if not isinstance(records, Iterable):
        raise ValueError("records must be an iterable of ContextBlock.")
    reset_context_store()
    for record in records:
        if not isinstance(record, ContextBlock):
            raise ValueError("all records must be ContextBlock instances.")
        if record.context_block_id in _CONTEXT_BLOCKS:
            raise ValueError(f"Duplicate context_block_id during load: {record.context_block_id}")
        if not record.source_artifact_ids:
            raise ValueError("context block source_artifact_ids must be non-empty.")
        _CONTEXT_BLOCKS[record.context_block_id] = record
'@

$continuity = @'
from __future__ import annotations

from typing import Iterable

from gdc_adk.memory.contracts import (
    ContinuityExportResult,
    ContinuitySnapshot,
    ContinuityStoreResult,
    RehydrationResult,
)


_SNAPSHOTS: dict[str, ContinuitySnapshot] = {}


def create_snapshot(snapshot_payload: ContinuitySnapshot) -> ContinuityStoreResult:
    if not isinstance(snapshot_payload, ContinuitySnapshot):
        raise ValueError("snapshot_payload must be a ContinuitySnapshot.")
    if snapshot_payload.snapshot_id in _SNAPSHOTS:
        raise ValueError(f"snapshot_id already exists: {snapshot_payload.snapshot_id}")
    if not snapshot_payload.workflow_run_id.strip():
        raise ValueError("snapshot_payload.workflow_run_id must be non-empty.")
    _SNAPSHOTS[snapshot_payload.snapshot_id] = snapshot_payload
    return ContinuityStoreResult(status="stored", snapshot=snapshot_payload, message="Continuity snapshot stored.")


def get_snapshot(snapshot_id: str) -> ContinuityStoreResult | None:
    if not isinstance(snapshot_id, str) or not snapshot_id.strip():
        raise ValueError("snapshot_id must be a non-empty string.")
    snapshot = _SNAPSHOTS.get(snapshot_id)
    if snapshot is None:
        return None
    return ContinuityStoreResult(status="found", snapshot=snapshot, message="Continuity snapshot found.")


def list_snapshots_for_workflow(workflow_run_id: str) -> list[ContinuitySnapshot]:
    if not isinstance(workflow_run_id, str) or not workflow_run_id.strip():
        raise ValueError("workflow_run_id must be a non-empty string.")
    return [snapshot for snapshot in _SNAPSHOTS.values() if snapshot.workflow_run_id == workflow_run_id]


def export_snapshots(filter_spec: dict[str, object] | None = None) -> ContinuityExportResult:
    filter_spec = dict(filter_spec or {})
    workflow_run_id = filter_spec.get("workflow_run_id")
    records: list[ContinuitySnapshot] = []
    for snapshot in _SNAPSHOTS.values():
        if workflow_run_id is not None and snapshot.workflow_run_id != workflow_run_id:
            continue
        records.append(snapshot)
    return ContinuityExportResult(snapshots=tuple(records))


def mark_snapshot_superseded(snapshot_id: str, superseded_by_id: str) -> ContinuityStoreResult:
    if not isinstance(superseded_by_id, str) or not superseded_by_id.strip():
        raise ValueError("superseded_by_id must be a non-empty string.")
    result = get_snapshot(snapshot_id)
    if result is None or result.snapshot is None:
        raise ValueError(f"Unknown snapshot_id: {snapshot_id}")
    snapshot = result.snapshot
    updated_snapshot = ContinuitySnapshot(
        snapshot_id=snapshot.snapshot_id,
        workflow_run_id=snapshot.workflow_run_id,
        workflow_mode=snapshot.workflow_mode,
        current_state=snapshot.current_state,
        state_history=snapshot.state_history,
        artifact_ids=snapshot.artifact_ids,
        issue_ids=snapshot.issue_ids,
        finding_ids=snapshot.finding_ids,
        context_refs=snapshot.context_refs,
        pending_actions=snapshot.pending_actions,
        created_at=snapshot.created_at,
        completion_reason=snapshot.completion_reason,
        blocked_reason=snapshot.blocked_reason,
        superseded_by=superseded_by_id,
    )
    _SNAPSHOTS[snapshot_id] = updated_snapshot
    return ContinuityStoreResult(status="superseded", snapshot=updated_snapshot, message="Snapshot superseded.")


def rehydrate_snapshot(snapshot_or_id: str | ContinuitySnapshot) -> ContinuityStoreResult:
    if isinstance(snapshot_or_id, str):
        result = get_snapshot(snapshot_or_id)
        if result is None or result.snapshot is None:
            raise ValueError(f"Unknown snapshot_id: {snapshot_or_id}")
        snapshot = result.snapshot
    elif isinstance(snapshot_or_id, ContinuitySnapshot):
        snapshot = snapshot_or_id
    else:
        raise ValueError("snapshot_or_id must be a snapshot_id or ContinuitySnapshot.")

    missing_references: list[str] = []
    if not snapshot.context_refs:
        missing_references.append("context_refs")
    if not snapshot.state_history:
        missing_references.append("state_history")

    if missing_references:
        rehydration_result = RehydrationResult(
            rehydration_status="partial",
            snapshot=snapshot,
            missing_references=tuple(missing_references),
            message="Snapshot rehydrated partially with explicit missing references.",
        )
        return ContinuityStoreResult(status="rehydrated", snapshot=snapshot, rehydration_result=rehydration_result)

    rehydration_result = RehydrationResult(
        rehydration_status="success",
        snapshot=snapshot,
        message="Snapshot rehydrated successfully.",
    )
    return ContinuityStoreResult(status="rehydrated", snapshot=snapshot, rehydration_result=rehydration_result)


def reset_continuity_store() -> None:
    _SNAPSHOTS.clear()


def load_snapshots(records: Iterable[ContinuitySnapshot]) -> None:
    if not isinstance(records, Iterable):
        raise ValueError("records must be an iterable of ContinuitySnapshot.")
    reset_continuity_store()
    for record in records:
        if not isinstance(record, ContinuitySnapshot):
            raise ValueError("all records must be ContinuitySnapshot instances.")
        if record.snapshot_id in _SNAPSHOTS:
            raise ValueError(f"Duplicate snapshot_id during load: {record.snapshot_id}")
        _SNAPSHOTS[record.snapshot_id] = record
'@

$replay = @'
from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from gdc_adk.memory.cache import export_results, load_cache_records
from gdc_adk.memory.context_store import export_context_blocks, load_context_blocks
from gdc_adk.memory.continuity import export_snapshots, load_snapshots
from gdc_adk.memory.contracts import (
    ReplayBuildResult,
    ReplayPackage,
    ReplayRehydrationResult,
    ReplayValidationResult,
)


SCHEMA_VERSION = "stage5.v1"


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def build_replay_package(scope_spec: dict[str, object]) -> ReplayBuildResult:
    if not isinstance(scope_spec, dict):
        raise ValueError("scope_spec must be a dict.")

    snapshot_records = export_snapshots(scope_spec).snapshots
    context_records = export_context_blocks(scope_spec).context_blocks
    cache_records = export_results(scope_spec).records

    workflow_run_ids = tuple(sorted({record.workflow_run_id for record in snapshot_records}))
    snapshot_ids = tuple(record.snapshot_id for record in snapshot_records)
    context_block_ids = tuple(record.context_block_id for record in context_records)
    artifact_summary_refs = tuple(
        sorted(
            {
                artifact_id
                for record in snapshot_records
                for artifact_id in record.artifact_ids
            }
        )
    )
    issue_evidence_refs = tuple(
        sorted(
            {
                issue_id
                for record in snapshot_records
                for issue_id in record.issue_ids
            }
        )
    )

    replay_package = ReplayPackage(
        replay_package_id=f"replay_{uuid4().hex[:12]}",
        schema_version=SCHEMA_VERSION,
        exported_at=_utc_now(),
        workflow_run_ids=workflow_run_ids,
        snapshot_ids=snapshot_ids,
        context_block_ids=context_block_ids,
        artifact_summary_refs=artifact_summary_refs,
        issue_evidence_refs=issue_evidence_refs,
        export_source="memory.replay",
        integrity_metadata={
            "snapshot_count": len(snapshot_records),
            "context_block_count": len(context_records),
            "cache_record_count": len(cache_records),
        },
    )

    return ReplayBuildResult(
        replay_package=replay_package,
        snapshots=snapshot_records,
        context_blocks=context_records,
        cache_records=cache_records,
    )


def validate_replay_package(replay_bundle: ReplayBuildResult) -> ReplayValidationResult:
    if not isinstance(replay_bundle, ReplayBuildResult):
        raise ValueError("replay_bundle must be a ReplayBuildResult.")

    replay_package = replay_bundle.replay_package
    if not isinstance(replay_package, ReplayPackage):
        raise ValueError("replay_bundle.replay_package must be a ReplayPackage.")

    if not replay_package.replay_package_id.strip():
        raise ValueError("Replay package id must be non-empty.")
    if replay_package.schema_version != SCHEMA_VERSION:
        raise ValueError(f"Unsupported replay schema version: {replay_package.schema_version}")

    return ReplayValidationResult(
        status="passed",
        replay_package=replay_package,
        message="Replay package is valid.",
    )


def rehydrate_replay_package(replay_bundle: ReplayBuildResult) -> ReplayRehydrationResult:
    validation_result = validate_replay_package(replay_bundle)
    if validation_result.replay_package is None:
        raise ValueError("Replay package validation did not produce a replay package.")

    load_snapshots(replay_bundle.snapshots)
    load_context_blocks(replay_bundle.context_blocks)
    load_cache_records(replay_bundle.cache_records)

    context_block_ids = {block.context_block_id for block in replay_bundle.context_blocks}
    missing_references = tuple(
        sorted(
            {
                context_ref
                for snapshot in replay_bundle.snapshots
                for context_ref in snapshot.context_refs
                if context_ref not in context_block_ids
            }
        )
    )

    status = "partial" if missing_references else "success"
    message = "Replay package rehydrated successfully." if status == "success" else "Replay package rehydrated partially."

    return ReplayRehydrationResult(
        status=status,
        replay_package=validation_result.replay_package,
        continuity_snapshots=replay_bundle.snapshots,
        context_blocks=replay_bundle.context_blocks,
        cache_records=replay_bundle.cache_records,
        missing_references=missing_references,
        message=message,
    )


def export_replay_package(scope_spec: dict[str, object]) -> ReplayBuildResult:
    replay_bundle = build_replay_package(scope_spec)
    validate_replay_package(replay_bundle)
    return replay_bundle
'@

$contracts   | Set-Content ".\src\gdc_adk\memory\contracts.py"     -Encoding UTF8
$cache       | Set-Content ".\src\gdc_adk\memory\cache.py"         -Encoding UTF8
$contextStore| Set-Content ".\src\gdc_adk\memory\context_store.py" -Encoding UTF8
$continuity  | Set-Content ".\src\gdc_adk\memory\continuity.py"    -Encoding UTF8
$replay      | Set-Content ".\src\gdc_adk\memory\replay.py"        -Encoding UTF8

Write-Host "`n=== Changed files diff ===" -ForegroundColor Cyan
git --no-pager diff -- src/gdc_adk/memory/contracts.py `
                    src/gdc_adk/memory/cache.py `
                    src/gdc_adk/memory/context_store.py `
                    src/gdc_adk/memory/continuity.py `
                    src/gdc_adk/memory/replay.py

Write-Host "`n=== Running Stage 5 tests ===" -ForegroundColor Cyan
$env:PYTHONPATH = "src"
& "C:\ProgramData\anaconda3\python.exe" -m pytest .\tests\test_stage5.py -o cache_dir="$env:TEMP\pytest-cache-gdc"