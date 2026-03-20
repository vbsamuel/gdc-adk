"""Stage 6 acceptance mapping for the bounded multi-agent slice.

Requirement mapping:
- FX-R014: multi-agent execution uses typed handoff artifacts, bounded roles, explicit governance, and replay-safe coordination

Acceptance scenarios:
- Scenario A: valid typed handoff creation and bounded delegation succeed for allowed roles
- Scenario B: malformed or unauthorized delegation is rejected explicitly
- Scenario C: over-broad task scope and governance stop conditions are enforced
- Scenario D: review and validation requirements block invalid handoff completion
- Scenario E: Stage 5 -> Stage 6 boundary and replay-safe coordination lifecycle are proven
- Scenario F: Stage 6 -> Stage 7 forward-boundary contract readiness is proven without Stage 7 implementation
"""

from __future__ import annotations

from dataclasses import asdict, replace

import pytest

from gdc_adk.memory.context_store import put_context_block, reset_context_store
from gdc_adk.memory.continuity import create_snapshot, reset_continuity_store
from gdc_adk.memory.contracts import ContextBlock, ContinuitySnapshot
from gdc_adk.validation.agent_governance import (
    MAX_UNRESOLVED_HANDOFFS,
    check_stop_conditions,
    detect_swarm_violation,
    validate_agent_sequence,
)
from gdc_adk.validation.handoff_validator import (
    validate_handoff_artifacts,
    validate_review_requirements,
    validate_traceability_links,
)
from gdc_adk.validation.validator import create_validation_finding
from gdc_adk.workflows.agent_contracts import (
    CoordinationEnvelope,
    HandoffArtifact,
    build_stage7_forward_envelope,
    create_agent_trace_record,
    create_handoff_artifact,
    serialize_coordination_envelope,
    serialize_handoff_artifact,
    serialize_stage7_forward_envelope,
)
from gdc_adk.workflows.agent_roles import (
    can_role_delegate,
    get_allowed_handoff_targets,
    get_role_definition,
    list_allowed_roles,
    requires_independent_review,
)
from gdc_adk.workflows.delegation_engine import delegate_task
from gdc_adk.workflows.handoff_manager import (
    complete_handoff,
    export_coordination_envelopes,
    export_handoffs,
    get_coordination_envelope,
    get_handoff,
    load_coordination_envelopes,
    load_handoffs,
    reject_handoff,
    reset_handoff_manager,
)
from gdc_adk.workflows.state_machine import create_workflow_run, transition_workflow_state


@pytest.fixture(autouse=True)
def reset_stage6_state() -> None:
    reset_handoff_manager()
    reset_context_store()
    reset_continuity_store()


def _build_context_block() -> ContextBlock:
    return ContextBlock(
        context_block_id="ctx_stage6",
        block_type="coordination_context",
        content={"summary": "Planner notes for the executor."},
        source_artifact_ids=("art_input",),
        created_at="2026-03-20T12:00:00Z",
        tags=("stage6",),
    )


def _build_workflow_run():
    workflow_run = create_workflow_run("dynamic_flow", ("art_input",), issue_ids=("iss_stage6",))
    classified = transition_workflow_state(workflow_run, "classified", "Classified.")
    activated = transition_workflow_state(classified, "activated", "Activated.")
    planned = transition_workflow_state(activated, "planned", "Planned.")
    return planned


def _build_snapshot(workflow_run_id: str, workflow_mode: str, workflow_state: str) -> ContinuitySnapshot:
    return ContinuitySnapshot(
        snapshot_id="snap_stage6",
        workflow_run_id=workflow_run_id,
        workflow_mode=workflow_mode,
        current_state=workflow_state,
        state_history=(
            {
                "from_state": "classified",
                "to_state": workflow_state,
                "reason": "Stage 6 boundary proof.",
                "changed_at": "2026-03-20T12:01:00Z",
            },
        ),
        artifact_ids=("art_input",),
        issue_ids=("iss_stage6",),
        finding_ids=("finding_stage6",),
        context_refs=("ctx_stage6",),
        pending_actions=("execute_artifact",),
        created_at="2026-03-20T12:02:00Z",
    )


def test_stage6_valid_typed_handoff_artifact_creation() -> None:
    artifact = create_handoff_artifact(
        workflow_run_id="wr_stage6",
        from_role="planner",
        to_role="executor",
        handoff_reason="Execute the approved plan.",
        requested_actions=("execute_artifact",),
        artifact_ids=("art_input",),
    )

    assert isinstance(artifact, HandoffArtifact)
    assert artifact.status == "pending"
    assert serialize_handoff_artifact(artifact)["requested_actions"] == ("execute_artifact",)


def test_stage6_valid_bounded_delegation_from_allowed_role_to_allowed_target() -> None:
    workflow_run = _build_workflow_run()
    handoff = create_handoff_artifact(
        workflow_run_id=workflow_run.workflow_run_id,
        from_role="planner",
        to_role="executor",
        handoff_reason="Execute the dynamic plan.",
        requested_actions=("execute_artifact",),
        artifact_ids=("art_input",),
        issue_ids=("iss_stage6",),
    )

    result = delegate_task("planner", "executor", handoff, workflow_run)

    assert result.status == "accepted"
    assert result.handoff is not None and result.handoff.status == "accepted"
    assert result.coordination_envelope is not None
    assert get_handoff(result.handoff.handoff_id) is not None


def test_stage6_malformed_handoff_is_rejected() -> None:
    malformed = HandoffArtifact(
        handoff_id="handoff_bad",
        workflow_run_id="wr_stage6",
        from_role="planner",
        to_role="executor",
        artifact_ids=(),
        issue_ids=(),
        finding_ids=(),
        context_block_ids=(),
        continuity_snapshot_id=None,
        created_at="2026-03-20T12:00:00Z",
        handoff_reason="",
        requested_actions=("execute_artifact",),
    )

    result = validate_handoff_artifacts(malformed)

    assert result.is_valid is False
    assert "contract_invalid" in result.violations


def test_stage6_unauthorized_delegation_is_rejected() -> None:
    workflow_run = _build_workflow_run()
    handoff = create_handoff_artifact(
        workflow_run_id=workflow_run.workflow_run_id,
        from_role="validator",
        to_role="executor",
        handoff_reason="Illegally try to delegate work.",
        requested_actions=("execute_artifact",),
        artifact_ids=("art_input",),
    )

    result = delegate_task("validator", "executor", handoff, workflow_run)

    assert result.status == "rejected"
    assert result.governance_result is not None
    assert "unauthorized_delegation" in result.governance_result.violations


def test_stage6_over_broad_task_scope_is_rejected() -> None:
    workflow_run = _build_workflow_run()
    handoff = create_handoff_artifact(
        workflow_run_id=workflow_run.workflow_run_id,
        from_role="planner",
        to_role="reviewer",
        handoff_reason="Ask reviewer to execute work they do not own.",
        requested_actions=("execute_artifact",),
        artifact_ids=("art_input",),
    )

    result = delegate_task("planner", "reviewer", handoff, workflow_run)

    assert result.status == "rejected"
    assert result.governance_result is not None
    assert "over_broad_task_scope" in result.governance_result.violations


def test_stage6_review_and_validation_requirements_block_invalid_completion() -> None:
    workflow_run = _build_workflow_run()
    handoff = create_handoff_artifact(
        workflow_run_id=workflow_run.workflow_run_id,
        from_role="executor",
        to_role="validator",
        handoff_reason="Attempt to bypass reviewer on a reviewable artifact.",
        requested_actions=("validate_output",),
        artifact_ids=("art_input",),
        review_required=True,
        validation_required=True,
    )

    result = delegate_task("executor", "validator", handoff, workflow_run)
    review_validation = validate_review_requirements(handoff, workflow_run)

    assert result.status == "rejected"
    assert review_validation.is_valid is False
    assert get_handoff(handoff.handoff_id) is None
    envelope = get_coordination_envelope(workflow_run.workflow_run_id)
    assert envelope is None or handoff.handoff_id not in envelope.active_handoff_ids


def test_stage5_to_stage6_boundary_and_negative_boundary_path_exist() -> None:
    workflow_run = _build_workflow_run()
    put_context_block(_build_context_block())
    create_snapshot(_build_snapshot(workflow_run.workflow_run_id, workflow_run.workflow_mode, workflow_run.workflow_state))
    handoff = create_handoff_artifact(
        workflow_run_id=workflow_run.workflow_run_id,
        from_role="planner",
        to_role="executor",
        handoff_reason="Resume from Stage 5 continuity snapshot.",
        requested_actions=("execute_artifact",),
        artifact_ids=("art_input",),
        issue_ids=("iss_stage6",),
        context_block_ids=("ctx_stage6",),
        continuity_snapshot_id="snap_stage6",
    )

    result = delegate_task("planner", "executor", handoff, workflow_run)
    artifact_validation = validate_handoff_artifacts(handoff)
    trace_validation = validate_traceability_links(result.handoff, workflow_run)

    assert result.status == "accepted"
    assert artifact_validation.is_valid is True
    assert trace_validation.is_valid is True

    bad_handoff = create_handoff_artifact(
        workflow_run_id=workflow_run.workflow_run_id,
        from_role="planner",
        to_role="executor",
        handoff_reason="Broken continuity reference.",
        requested_actions=("execute_artifact",),
        artifact_ids=("art_input",),
        continuity_snapshot_id="snap_missing",
    )
    bad_result = delegate_task("planner", "executor", bad_handoff, workflow_run)

    assert bad_result.status == "rejected"
    assert bad_result.validation_result is not None
    assert "continuity_snapshot_missing" in bad_result.validation_result.violations


def test_stage6_replay_safe_export_reset_load_and_complete_work() -> None:
    workflow_run = _build_workflow_run()
    put_context_block(_build_context_block())
    create_snapshot(_build_snapshot(workflow_run.workflow_run_id, workflow_run.workflow_mode, workflow_run.workflow_state))
    handoff = create_handoff_artifact(
        workflow_run_id=workflow_run.workflow_run_id,
        from_role="planner",
        to_role="executor",
        handoff_reason="Persist and resume bounded delegation.",
        requested_actions=("execute_artifact",),
        artifact_ids=("art_input",),
        issue_ids=("iss_stage6",),
        context_block_ids=("ctx_stage6",),
        continuity_snapshot_id="snap_stage6",
    )

    accepted = delegate_task("planner", "executor", handoff, workflow_run)
    exported_handoffs = export_handoffs()
    exported_envelopes = export_coordination_envelopes()

    reset_handoff_manager()
    assert export_handoffs().handoffs == ()

    load_handoffs(exported_handoffs.handoffs)
    load_coordination_envelopes(exported_envelopes.coordination_envelopes)
    completed = complete_handoff(accepted.handoff.handoff_id, workflow_run)

    assert completed.status == "completed"
    assert completed.pending_actions == ("execute_artifact",)
    assert get_coordination_envelope(workflow_run.workflow_run_id) is not None


def test_stage6_governance_stop_conditions_detect_unbounded_trace() -> None:
    workflow_run = _build_workflow_run()
    handoff = create_handoff_artifact(
        workflow_run_id=workflow_run.workflow_run_id,
        from_role="planner",
        to_role="executor",
        handoff_reason="Generate an invalid deep delegation trace.",
        requested_actions=("execute_artifact",),
        artifact_ids=("art_input",),
        delegation_depth=4,
    )
    trace = (create_agent_trace_record(handoff, "delegation_requested", "pending"),)
    governance_result = check_stop_conditions(workflow_run, trace)

    assert governance_result.blocked is True
    assert "delegation_depth_exceeded" in governance_result.violations


def test_stage6_validate_agent_sequence_accepts_allowed_chain_and_rejects_cross_workflow_trace() -> None:
    workflow_run = _build_workflow_run()
    allowed_handoff = create_handoff_artifact(
        workflow_run_id=workflow_run.workflow_run_id,
        from_role="planner",
        to_role="executor",
        handoff_reason="Allowed execution chain.",
        requested_actions=("execute_artifact",),
        artifact_ids=("art_input",),
        issue_ids=("iss_stage6",),
    )
    allowed_trace = (create_agent_trace_record(allowed_handoff, "handoff_initiated", "accepted"),)

    allowed_result = validate_agent_sequence(workflow_run.workflow_run_id, allowed_trace)

    assert allowed_result.blocked is False

    invalid_handoff = create_handoff_artifact(
        workflow_run_id="wr_other",
        from_role="planner",
        to_role="executor",
        handoff_reason="Cross-workflow trace should reject.",
        requested_actions=("execute_artifact",),
        artifact_ids=("art_input",),
    )
    invalid_trace = (create_agent_trace_record(invalid_handoff, "handoff_initiated", "accepted"),)

    invalid_result = validate_agent_sequence(workflow_run.workflow_run_id, invalid_trace)

    assert invalid_result.blocked is True
    assert "trace_outside_workflow_scope" in invalid_result.violations


def test_stage6_detect_swarm_violation_reports_same_role_repetition() -> None:
    workflow_run = _build_workflow_run()
    handoff_one = create_handoff_artifact(
        workflow_run_id=workflow_run.workflow_run_id,
        from_role="planner",
        to_role="executor",
        handoff_reason="First executor delegation.",
        requested_actions=("execute_artifact",),
        artifact_ids=("art_input",),
    )
    handoff_two = create_handoff_artifact(
        workflow_run_id=workflow_run.workflow_run_id,
        from_role="planner",
        to_role="executor",
        handoff_reason="Second executor delegation.",
        requested_actions=("execute_artifact",),
        artifact_ids=("art_input",),
    )
    handoff_three = create_handoff_artifact(
        workflow_run_id=workflow_run.workflow_run_id,
        from_role="planner",
        to_role="executor",
        handoff_reason="Third executor delegation.",
        requested_actions=("execute_artifact",),
        artifact_ids=("art_input",),
    )
    trace = (
        create_agent_trace_record(handoff_one, "handoff_initiated", "accepted"),
        create_agent_trace_record(handoff_two, "handoff_initiated", "accepted"),
        create_agent_trace_record(handoff_three, "handoff_initiated", "accepted"),
    )

    violations = detect_swarm_violation(workflow_run, trace)

    assert violations
    assert any("same_role_repetition_exceeded:executor" in violation.violations for violation in violations)


def test_stage6_same_role_repetition_violation_blocks_unresolved_handoff_limit() -> None:
    workflow_run = _build_workflow_run()
    trace_records = tuple(
        create_agent_trace_record(
            create_handoff_artifact(
                workflow_run_id=workflow_run.workflow_run_id,
                from_role="planner",
                to_role="executor",
                handoff_reason=f"Pending delegation {index}.",
                requested_actions=("execute_artifact",),
                artifact_ids=("art_input",),
            ),
            "delegation_requested",
            "pending",
        )
        for index in range(MAX_UNRESOLVED_HANDOFFS + 1)
    )

    governance_result = check_stop_conditions(workflow_run, trace_records)

    assert governance_result.blocked is True
    assert "unresolved_handoff_limit_exceeded" in governance_result.violations


def test_stage6_same_role_delegation_rejects_explicitly() -> None:
    workflow_run = _build_workflow_run()
    handoff = create_handoff_artifact(
        workflow_run_id=workflow_run.workflow_run_id,
        from_role="executor",
        to_role="executor",
        handoff_reason="Self-escalation should reject.",
        requested_actions=("execute_artifact",),
        artifact_ids=("art_input",),
    )

    result = delegate_task("executor", "executor", handoff, workflow_run)

    assert result.status == "rejected"
    assert result.governance_result is not None
    assert "unauthorized_delegation" in result.governance_result.violations


def test_stage6_reviewer_independence_violation_rejects_before_acceptance() -> None:
    workflow_run = _build_workflow_run()
    with pytest.raises(ValueError):
        create_handoff_artifact(
            workflow_run_id=workflow_run.workflow_run_id,
            from_role="reviewer",
            to_role="reviewer",
            handoff_reason="Reviewer may not review own delegated work.",
            requested_actions=("review_artifact",),
            artifact_ids=("art_input",),
            review_required=True,
        )


def test_stage6_out_of_workflow_traceability_validation_rejects() -> None:
    workflow_run = _build_workflow_run()
    put_context_block(_build_context_block())
    create_snapshot(_build_snapshot(workflow_run.workflow_run_id, workflow_run.workflow_mode, workflow_run.workflow_state))
    handoff = create_handoff_artifact(
        workflow_run_id="wr_other",
        from_role="planner",
        to_role="executor",
        handoff_reason="Wrong workflow linkage.",
        requested_actions=("execute_artifact",),
        artifact_ids=("art_input",),
        issue_ids=("iss_stage6",),
        context_block_ids=("ctx_stage6",),
        continuity_snapshot_id="snap_stage6",
    )

    traceability_validation = validate_traceability_links(handoff, workflow_run)

    assert traceability_validation.is_valid is False
    assert "workflow_run_mismatch" in traceability_validation.violations


def test_stage6_role_catalog_is_finite_and_review_independence_is_explicit() -> None:
    assert list_allowed_roles() == ["planner", "executor", "reviewer", "fixer", "validator"]
    assert can_role_delegate("planner") is True
    assert get_allowed_handoff_targets("executor") == ["reviewer", "validator", "fixer"]
    assert get_role_definition("reviewer")["may_reopen_finding"] is True
    assert requires_independent_review("executor", artifact_type="code_artifact") is True


def test_stage6_stage7_forward_boundary_contract_is_serializable_only() -> None:
    workflow_run = _build_workflow_run()
    put_context_block(_build_context_block())
    create_snapshot(_build_snapshot(workflow_run.workflow_run_id, workflow_run.workflow_mode, workflow_run.workflow_state))
    finding = create_validation_finding(
        "quality_gap",
        "medium",
        "Review before completion.",
        ("art_input",),
        {"workflow_run_id": workflow_run.workflow_run_id},
        "reviewer",
    )
    workflow_run = replace(workflow_run, finding_ids=(finding.finding_id,))
    handoff = create_handoff_artifact(
        workflow_run_id=workflow_run.workflow_run_id,
        from_role="planner",
        to_role="reviewer",
        handoff_reason="Prepare a review handoff for later orchestration.",
        requested_actions=("review_artifact",),
        artifact_ids=("art_input",),
        issue_ids=("iss_stage6",),
        finding_ids=(finding.finding_id,),
        context_block_ids=("ctx_stage6",),
        continuity_snapshot_id="snap_stage6",
        review_required=True,
    )

    accepted = delegate_task("planner", "reviewer", handoff, workflow_run)
    envelope = accepted.coordination_envelope
    assert isinstance(envelope, CoordinationEnvelope)

    stage7_forward = build_stage7_forward_envelope(
        workflow_run.workflow_run_id,
        export_handoffs().handoffs,
        envelope,
    )

    assert asdict(stage7_forward)["workflow_run_id"] == workflow_run.workflow_run_id
    assert serialize_coordination_envelope(envelope)["workflow_run_id"] == workflow_run.workflow_run_id
    assert serialize_stage7_forward_envelope(stage7_forward)["handoff_ids"] == (accepted.handoff.handoff_id,)


def test_stage6_reject_handoff_records_traceable_rejection() -> None:
    workflow_run = _build_workflow_run()
    handoff = create_handoff_artifact(
        workflow_run_id=workflow_run.workflow_run_id,
        from_role="planner",
        to_role="executor",
        handoff_reason="Reject this handoff explicitly.",
        requested_actions=("execute_artifact",),
        artifact_ids=("art_input",),
        issue_ids=("iss_stage6",),
    )

    accepted = delegate_task("planner", "executor", handoff, workflow_run)
    rejected = reject_handoff(accepted.handoff.handoff_id, workflow_run, "Cancelled by planner.")

    assert rejected.status == "rejected"
    assert rejected.trace_record is not None
    assert rejected.coordination_envelope is not None
    assert rejected.handoff is not None and rejected.handoff.status == "rejected"
