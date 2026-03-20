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
