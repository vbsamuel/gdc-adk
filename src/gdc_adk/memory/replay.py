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
