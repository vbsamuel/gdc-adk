"""Stage 5 acceptance mapping for the bounded memory slice.

Requirement mapping:
- FX-R010: operational memory remains explicit, replayable, exportable, and replaceable

Acceptance scenarios:
- Scenario A: cache and context store persist valid typed records
- Scenario B: continuity snapshots can be created, exported, resumed, and rehydrated
- Scenario C: replay packages export, validate, and rehydrate through public APIs
- Scenario D: invalid cache/context/continuity/replay inputs are rejected
- Scenario E: Stage 4 -> Stage 5 continuity boundary and Stage 5 -> Stage 6 forward-boundary contract readiness are proven
"""

from __future__ import annotations

from dataclasses import asdict

import pytest

from gdc_adk.memory.cache import (
    export_results,
    get_result,
    invalidate_result,
    load_cache_records,
    put_result,
    reset_cache_store,
)
from gdc_adk.memory.context_store import (
    export_context_blocks,
    get_context_block,
    list_context_blocks_by_artifact,
    load_context_blocks,
    mark_context_block_superseded,
    put_context_block,
    reset_context_store,
)
from gdc_adk.memory.continuity import (
    create_snapshot,
    export_snapshots,
    get_snapshot,
    list_snapshots_for_workflow,
    load_snapshots,
    mark_snapshot_superseded,
    rehydrate_snapshot,
    reset_continuity_store,
)
from gdc_adk.memory.contracts import (
    CacheRecord,
    ContextBlock,
    ContinuitySnapshot,
    ReplayPackage,
)
from gdc_adk.memory.replay import (
    build_replay_package,
    export_replay_package,
    rehydrate_replay_package,
    validate_replay_package,
)
from gdc_adk.validation.validator import create_validation_finding
from gdc_adk.workflows.state_machine import create_workflow_run, transition_workflow_state


@pytest.fixture(autouse=True)
def reset_stage5_state() -> None:
    reset_cache_store()
    reset_context_store()
    reset_continuity_store()


def _build_context_block() -> ContextBlock:
    return ContextBlock(
        context_block_id="ctx_1",
        block_type="grounding_fragment",
        content={"summary": "Release notes context."},
        source_artifact_ids=("art_1",),
        created_at="2026-03-20T10:00:00Z",
        tags=("release",),
    )


def _build_snapshot() -> ContinuitySnapshot:
    return ContinuitySnapshot(
        snapshot_id="snap_1",
        workflow_run_id="wr_1",
        workflow_mode="iterative",
        current_state="reopened",
        state_history=(
            {
                "from_state": "awaiting_review",
                "to_state": "reopened",
                "reason": "Regression detected.",
                "changed_at": "2026-03-20T10:01:00Z",
            },
        ),
        artifact_ids=("art_1", "art_2"),
        issue_ids=("iss_1",),
        finding_ids=("finding_1",),
        context_refs=("ctx_1",),
        pending_actions=("revise_artifact",),
        created_at="2026-03-20T10:02:00Z",
        blocked_reason=None,
        completion_reason=None,
    )


def test_stage5_cache_stores_retrieves_invalidates_and_exports_valid_entries() -> None:
    stored = put_result("cache:key:1", {"answer": "ok"}, {"scope": "workflow", "workflow_run_id": "wr_1"})
    fetched = get_result("cache:key:1")
    invalidated = invalidate_result("cache:key:1")
    exported = export_results({"scope": "workflow"})

    assert stored.status == "stored"
    assert fetched is not None and fetched.status == "hit"
    assert invalidated.cache_record is not None and invalidated.cache_record.invalidated_at is not None
    assert exported.records[0].cache_key == "cache:key:1"


def test_stage5_context_store_stores_retrieves_supersedes_and_exports_records() -> None:
    context_block = _build_context_block()
    stored = put_context_block(context_block)
    fetched = get_context_block("ctx_1")
    listed = list_context_blocks_by_artifact("art_1")
    superseded = mark_context_block_superseded("ctx_1", "ctx_2")
    exported = export_context_blocks({"artifact_id": "art_1"})

    assert stored.status == "stored"
    assert fetched is not None and fetched.context_block is not None
    assert listed[0].context_block_id == "ctx_1"
    assert superseded.context_block is not None and superseded.context_block.superseded_by == "ctx_2"
    assert exported.context_blocks[0].context_block_id == "ctx_1"


def test_stage5_continuity_snapshots_create_export_resume_and_rehydrate() -> None:
    put_context_block(_build_context_block())
    snapshot = _build_snapshot()
    stored = create_snapshot(snapshot)
    fetched = get_snapshot("snap_1")
    listed = list_snapshots_for_workflow("wr_1")
    rehydrated = rehydrate_snapshot("snap_1")
    superseded = mark_snapshot_superseded("snap_1", "snap_2")
    exported = export_snapshots({"workflow_run_id": "wr_1"})

    assert stored.status == "stored"
    assert fetched is not None and fetched.snapshot is not None
    assert listed[0].snapshot_id == "snap_1"
    assert rehydrated.rehydration_result is not None and rehydrated.rehydration_result.rehydration_status == "success"
    assert superseded.snapshot is not None and superseded.snapshot.superseded_by == "snap_2"
    assert exported.snapshots[0].snapshot_id == "snap_1"


def test_stage5_replay_export_reset_load_and_rehydrate_work() -> None:
    put_result("cache:key:1", {"answer": "ok"}, {"scope": "workflow", "workflow_run_id": "wr_1"})
    put_context_block(_build_context_block())
    create_snapshot(_build_snapshot())

    replay_package = export_replay_package({"workflow_run_id": "wr_1"})
    reset_cache_store()
    reset_context_store()
    reset_continuity_store()
    rehydrated = rehydrate_replay_package(replay_package)

    assert validate_replay_package(replay_package).status == "passed"
    assert rehydrated.status == "success"
    assert rehydrated.continuity_snapshots[0].workflow_run_id == "wr_1"
    assert rehydrated.context_blocks[0].context_block_id == "ctx_1"


def test_stage5_replaceability_assumptions_remain_contract_level() -> None:
    replay_package = ReplayPackage(
        replay_package_id="replay_contract",
        schema_version="stage5.v1",
        exported_at="2026-03-20T10:00:00Z",
        workflow_run_ids=("wr_1",),
        snapshot_ids=("snap_1",),
        context_block_ids=("ctx_1",),
        artifact_summary_refs=("art_1",),
        issue_evidence_refs=("iss_1",),
        export_source="memory.replay",
    )

    assert asdict(replay_package)["schema_version"] == "stage5.v1"
    assert "workflow_run_ids" in asdict(replay_package)


def test_stage5_invalid_cache_input_is_rejected() -> None:
    with pytest.raises(ValueError):
        put_result("", {"answer": "ok"}, {})

    with pytest.raises(ValueError):
        put_result("cache:key:1", {}, {})

    with pytest.raises(ValueError):
        load_cache_records([{"cache_key": "cache:key:1", "metadata": {}, "created_at": "2026-03-20T10:00:00Z"}])


def test_stage5_invalid_context_input_is_rejected() -> None:
    with pytest.raises(ValueError):
        put_context_block(
            ContextBlock(
                context_block_id="ctx_bad",
                block_type="grounding_fragment",
                content={"summary": "bad"},
                source_artifact_ids=(),
                created_at="2026-03-20T10:00:00Z",
            )
        )

    with pytest.raises(ValueError):
        load_context_blocks(
            [
                {
                    "context_block_id": "ctx_1",
                    "block_type": "grounding_fragment",
                    "content": {},
                    "created_at": "2026-03-20T10:00:00Z",
                }
            ]
        )


def test_stage5_invalid_continuity_snapshot_input_is_rejected() -> None:
    with pytest.raises(ValueError):
        create_snapshot(
            ContinuitySnapshot(
                snapshot_id="snap_bad",
                workflow_run_id="",
                workflow_mode="iterative",
                current_state="reopened",
                state_history=(),
                artifact_ids=(),
                issue_ids=(),
                finding_ids=(),
                context_refs=(),
                pending_actions=(),
                created_at="2026-03-20T10:00:00Z",
            )
        )

    with pytest.raises(ValueError):
        load_snapshots(
            [
                {
                    "snapshot_id": "snap_1",
                    "workflow_run_id": "wr_1",
                    "workflow_mode": "iterative",
                }
            ]
        )


def test_stage5_malformed_replay_input_and_duplicate_identifiers_are_rejected() -> None:
    with pytest.raises(ValueError):
        validate_replay_package({"replay_package": {}})

    with pytest.raises(ValueError):
        load_cache_records(
            [
                {
                    "cache_key": "cache:key:1",
                    "payload": {"answer": "ok"},
                    "metadata": {},
                    "created_at": "2026-03-20T10:00:00Z",
                },
                {
                    "cache_key": "cache:key:1",
                    "payload": {"answer": "ok"},
                    "metadata": {},
                    "created_at": "2026-03-20T10:00:00Z",
                },
            ]
        )

    with pytest.raises(ValueError):
        load_context_blocks(
            [
                {
                    "context_block_id": "ctx_1",
                    "block_type": "grounding_fragment",
                    "content": {"summary": "ok"},
                    "source_artifact_ids": ("art_1",),
                    "created_at": "2026-03-20T10:00:00Z",
                },
                {
                    "context_block_id": "ctx_1",
                    "block_type": "grounding_fragment",
                    "content": {"summary": "ok"},
                    "source_artifact_ids": ("art_1",),
                    "created_at": "2026-03-20T10:00:00Z",
                },
            ]
        )

    with pytest.raises(ValueError):
        load_snapshots(
            [
                {
                    "snapshot_id": "snap_1",
                    "workflow_run_id": "wr_1",
                    "workflow_mode": "iterative",
                    "current_state": "reopened",
                    "state_history": (),
                    "artifact_ids": (),
                    "issue_ids": (),
                    "finding_ids": (),
                    "context_refs": (),
                    "pending_actions": (),
                    "created_at": "2026-03-20T10:00:00Z",
                },
                {
                    "snapshot_id": "snap_1",
                    "workflow_run_id": "wr_1",
                    "workflow_mode": "iterative",
                    "current_state": "reopened",
                    "state_history": (),
                    "artifact_ids": (),
                    "issue_ids": (),
                    "finding_ids": (),
                    "context_refs": (),
                    "pending_actions": (),
                    "created_at": "2026-03-20T10:00:00Z",
                },
            ]
        )


def test_stage4_to_stage5_boundary_and_stage5_to_stage6_forward_boundary_exist() -> None:
    workflow_run = create_workflow_run("iterative", ("art_1",), issue_ids=("iss_1",), continuity_requirements=("resume_required",))
    activated = transition_workflow_state(
        transition_workflow_state(workflow_run, "classified", "classified"),
        "activated",
        "activated",
    )
    finding = create_validation_finding(
        "quality_gap",
        "medium",
        "Needs another pass.",
        ("art_1",),
        {"workflow_run_id": activated.workflow_run_id},
        "validator",
    )
    put_context_block(_build_context_block())
    snapshot = ContinuitySnapshot(
        snapshot_id="snap_boundary",
        workflow_run_id=activated.workflow_run_id,
        workflow_mode=activated.workflow_mode,
        current_state=activated.workflow_state,
        state_history=tuple(asdict(item) for item in activated.history),
        artifact_ids=activated.input_artifact_ids,
        issue_ids=activated.issue_ids,
        finding_ids=(finding.finding_id,),
        context_refs=("ctx_1",),
        pending_actions=("resume_iteration",),
        created_at="2026-03-20T10:05:00Z",
    )
    stored = create_snapshot(snapshot)
    replay_package = build_replay_package({"workflow_run_id": activated.workflow_run_id})
    stage6_ready_contract = {
        "workflow_run_ids": replay_package.replay_package.workflow_run_ids,
        "snapshot_ids": replay_package.replay_package.snapshot_ids,
        "context_block_ids": replay_package.replay_package.context_block_ids,
        "finding_ids": snapshot.finding_ids,
    }

    assert stored.snapshot is not None and stored.snapshot.workflow_run_id == activated.workflow_run_id
    assert stage6_ready_contract["snapshot_ids"] == ("snap_boundary",)
    assert stage6_ready_contract["finding_ids"] == (finding.finding_id,)

    with pytest.raises(ValueError):
        rehydrate_replay_package("not_a_replay_build_result")


def test_stage5_partial_rehydration_declares_missing_context_refs() -> None:
    snapshot = ContinuitySnapshot(
        snapshot_id="snap_partial",
        workflow_run_id="wr_partial",
        workflow_mode="iterative",
        current_state="reopened",
        state_history=({"from_state": "validated", "to_state": "reopened", "reason": "new issue", "changed_at": "2026-03-20T10:00:00Z"},),
        artifact_ids=("art_1",),
        issue_ids=(),
        finding_ids=(),
        context_refs=(),
        pending_actions=("resume_iteration",),
        created_at="2026-03-20T10:06:00Z",
    )
    create_snapshot(snapshot)
    rehydrated = rehydrate_snapshot("snap_partial")

    assert rehydrated.rehydration_result is not None
    assert rehydrated.rehydration_result.rehydration_status == "partial"
    assert rehydrated.rehydration_result.missing_references == ("context_refs",)


