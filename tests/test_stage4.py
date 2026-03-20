"""Stage 4 acceptance mapping for the bounded workflow and validation slice.

Requirement mapping:
- FX-R011: review findings are first-class, structured, machine-checkable validation outputs
- FX-R012: workflow execution uses an explicit state machine with typed transitions

Acceptance scenarios:
- Scenario A: engine and state machine execute a valid bounded workflow path
- Scenario B: fix_flow preserves issue linkage, remediation evidence, verification, and closure semantics
- Scenario C: iterative_flow preserves revision lineage and prior findings context
- Scenario D: validation, drift, traceability, and grounding checks emit independent structured findings
- Scenario E: Stage 3 -> Stage 4 workflow entry and Stage 4 -> Stage 5 forward-boundary contract readiness are proven
"""

from __future__ import annotations

from dataclasses import asdict

import pytest

from gdc_adk.information_plane.activation.trigger_router import build_activation_trigger
from gdc_adk.information_plane.activation.workflow_activation import activate_workflow
from gdc_adk.information_plane.indexing.artifact_index import build_indexed_artifact
from gdc_adk.information_plane.ingestion.document_ingestor import ingest_text_signal
from gdc_adk.information_plane.normalization.canonicalizer import normalize_signal
from gdc_adk.validation.drift_checker import (
    check_constitution_drift,
    check_hidden_state_drift,
    check_lineage_drift,
    check_provider_policy_drift,
)
from gdc_adk.validation.grounding_checker import (
    check_contradictions,
    check_grounding,
    check_missing_cases,
    check_unsupported_claims,
)
from gdc_adk.validation.traceability_auditor import audit_traceability, check_requirement_coverage
from gdc_adk.validation.validator import (
    ValidationResult,
    create_validation_finding,
    reopen_validation_finding,
    resolve_validation_finding,
    transition_finding_status,
    validate_artifact,
    validate_workflow_output,
)
from gdc_adk.workflows.engine import (
    apply_validation_gate,
    block_workflow,
    complete_workflow,
    fail_workflow,
    reopen_workflow,
    start_workflow,
    advance_workflow,
)
from gdc_adk.workflows.fix_flow import (
    attach_remediation_evidence,
    build_verification_result,
    close_fix_flow,
    mark_verification_pending,
    record_remediation_attempt,
    reopen_fix_flow,
    start_fix_flow,
    verify_resolution,
)
from gdc_adk.workflows.iterative_flow import (
    attach_prior_findings,
    complete_iteration,
    plan_iteration,
    record_revision_delta,
    reopen_iteration,
    start_iterative_flow,
    advance_iteration,
)
from gdc_adk.workflows.state_machine import (
    WorkflowRun,
    create_workflow_run,
    get_allowed_transitions,
    is_terminal_state,
    transition_workflow_state,
    validate_transition,
)


def _build_stage3_activation_output(raw_text: str):
    raw_signal = ingest_text_signal(raw_text, {"source_kind": "stage3_activation"})
    canonical_signal = normalize_signal(raw_signal)
    indexed_artifact = build_indexed_artifact(canonical_signal)
    activation_output = activate_workflow(
        canonical_signal,
        (indexed_artifact.artifact_id,),
        build_activation_trigger(canonical_signal),
    )
    return canonical_signal, indexed_artifact, activation_output


def test_stage4_engine_and_state_machine_execute_valid_bounded_workflow_path() -> None:
    _, indexed_artifact, activation_output = _build_stage3_activation_output("Summarize this grounded release note.")
    workflow_run = create_workflow_run("single_run", (indexed_artifact.artifact_id,))

    started = start_workflow(workflow_run, activation_output)
    assert started.workflow_run.workflow_state == "activated"
    assert started.workflow_run.input_artifact_ids == (indexed_artifact.artifact_id,)

    advanced_planned = advance_workflow(started.workflow_run, "planned", "Plan bounded execution.", {})
    advanced_executing = advance_workflow(advanced_planned.workflow_run, "executing", "Execute bounded workflow.", {})
    advanced_review = advance_workflow(advanced_executing.workflow_run, "awaiting_review", "Await review.", {})

    validation_result = validate_workflow_output(
        {"artifact_id": "art_output", "grounded_sources": ("src_1",), "quality_status": "passed"},
        {"workflow_run_id": advanced_review.workflow_run.workflow_run_id},
    )
    gated = apply_validation_gate(advanced_review.workflow_run, validation_result)
    completed = complete_workflow(gated.workflow_run, "Validation gate passed.")

    assert "activated" in get_allowed_transitions("single_run", "classified")
    assert is_terminal_state("single_run", completed.workflow_run.workflow_state) is True
    assert completed.workflow_run.workflow_state == "completed"
    assert len(completed.workflow_run.history) >= 6


def test_stage4_state_machine_rejects_invalid_transition_and_preserves_reasons() -> None:
    workflow_run = create_workflow_run("single_run", ("art_1",))
    validate_transition("single_run", "received", "classified")
    with pytest.raises(ValueError):
        validate_transition("single_run", "received", "completed")

    classified = transition_workflow_state(workflow_run, "classified", "Initial classification.")
    blocked = block_workflow(classified, "Waiting on user clarification.")
    reopened = reopen_workflow(blocked.workflow_run, "Clarification received.")
    failed = fail_workflow(reopened.workflow_run, "Execution failed after retry.")

    assert blocked.workflow_run.last_reason == "Waiting on user clarification."
    assert reopened.workflow_run.workflow_state == "reopened"
    assert failed.workflow_run.workflow_state == "failed"


def test_stage4_fix_flow_handles_issue_aware_remediation_and_verification() -> None:
    _, indexed_artifact, activation_output = _build_stage3_activation_output("Fix the broken deployment check immediately.")
    workflow_run = create_workflow_run("fix_flow", (indexed_artifact.artifact_id,))
    started = start_workflow(workflow_run, activation_output)

    fix_started = start_fix_flow(started.workflow_run, "iss_1", ("art_remediation",))
    remediation = record_remediation_attempt(
        fix_started.workflow_run,
        "iss_1",
        "Applied remediation patch.",
        ("art_patch",),
    )
    evidence = attach_remediation_evidence(remediation.workflow_run, "iss_1", ("art_evidence",))
    pending = mark_verification_pending(evidence.workflow_run, "iss_1")
    verification_result = build_verification_result(
        "iss_1",
        pending.workflow_run.workflow_run_id,
        ("art_evidence",),
        "passed",
        "validator",
        "Evidence confirms remediation.",
    )
    verified = verify_resolution(pending.workflow_run, "iss_1", verification_result)
    gate_result = validate_artifact(
        {"artifact_id": "art_fix_output", "grounded_sources": ("src_1",), "quality_status": "passed"},
        {"workflow_run_id": verified.workflow_run.workflow_run_id},
    )
    gated = apply_validation_gate(verified.workflow_run, gate_result)
    closed = close_fix_flow(gated.workflow_run, "iss_1", "Fix validated and closed.")

    assert "iss_1" in fix_started.workflow_run.issue_ids
    assert verification_result.evidence_artifact_ids == ("art_evidence",)
    assert closed.workflow_run.workflow_state == "completed"


def test_stage4_fix_flow_rejects_missing_issue_linkage_and_invalid_closure() -> None:
    workflow_run = create_workflow_run("fix_flow", ("art_1",), issue_ids=("iss_1",))
    activated = transition_workflow_state(
        transition_workflow_state(workflow_run, "classified", "classified"),
        "activated",
        "activated",
    )

    with pytest.raises(ValueError):
        record_remediation_attempt(activated, "iss_missing", "Attempted fix.", ("art_patch",))

    with pytest.raises(ValueError):
        close_fix_flow(activated, "iss_1", "Cannot close before validation.")

    reopened = reopen_fix_flow(
        transition_workflow_state(
            transition_workflow_state(
                transition_workflow_state(activated, "issue_opened", "opened"),
                "remediation_in_progress",
                "remediating",
            ),
            "verification_pending",
            "pending verification",
        ),
        "iss_1",
        "Verification failed.",
    )
    assert reopened.workflow_run.workflow_state == "reopened"


def test_stage4_iterative_flow_preserves_lineage_and_prior_findings() -> None:
    workflow_run = create_workflow_run("iterative", ("art_input",))
    activated = transition_workflow_state(
        transition_workflow_state(workflow_run, "classified", "classified"),
        "activated",
        "activated",
    )
    started = start_iterative_flow(activated, ("art_input",))
    planned = plan_iteration(started.workflow_run, "Plan refinement.")
    with_findings = attach_prior_findings(planned.workflow_run, ("finding_1",))
    revision = record_revision_delta(
        with_findings.workflow_run,
        "art_input",
        "art_revision_1",
        "Address validator feedback.",
        ("finding_1",),
    )
    review_ready = advance_iteration(revision.workflow_run, "awaiting_review", "Ready for review.")
    validation_result = ValidationResult(
        status="passed",
        findings=(),
        related_artifact_ids=("art_revision_1",),
        summary="Iteration validated.",
    )
    gated = apply_validation_gate(review_ready.workflow_run, validation_result)
    completed = complete_iteration(gated.workflow_run, "Iteration complete.")

    assert revision.revision_deltas[0].prior_artifact_id == "art_input"
    assert revision.revision_deltas[0].revised_artifact_id == "art_revision_1"
    assert "finding_1" in completed.workflow_run.finding_ids
    assert completed.workflow_run.workflow_state == "completed"


def test_stage4_iterative_flow_rejects_missing_lineage_and_allows_reopen() -> None:
    workflow_run = create_workflow_run("iterative", ("art_input",))
    activated = transition_workflow_state(
        transition_workflow_state(workflow_run, "classified", "classified"),
        "activated",
        "activated",
    )
    started = start_iterative_flow(activated, ("art_input",))

    with pytest.raises(ValueError):
        record_revision_delta(started.workflow_run, "art_missing", "art_revision_1", "Missing lineage.", ())

    reopened = reopen_iteration(
        transition_workflow_state(
            transition_workflow_state(
                transition_workflow_state(started.workflow_run, "executing", "executing"),
                "awaiting_review",
                "awaiting review",
            ),
            "revising",
            "revising",
        ),
        "New findings require another pass.",
    )
    assert reopened.workflow_run.workflow_state == "reopened"


def test_stage4_validation_spine_emits_independent_structured_findings() -> None:
    validation_result = validate_artifact(
        {"artifact_id": "art_1", "quality_status": "failed", "grounded_sources": ()},
        {"workflow_run_id": "wr_1"},
    )
    finding = validation_result.findings[0]
    accepted = transition_finding_status(finding, "accepted", "Confirmed finding.")
    resolved = resolve_validation_finding(accepted, "Addressed by revision.")
    reopened = reopen_validation_finding(resolved, "Regression detected.")

    drift_findings = check_hidden_state_drift({"prompt_carry_state": True, "related_artifact_ids": ("art_1",)})
    traceability_result = audit_traceability(
        {
            "FX-R011": {
                "acceptance_tests": ("tests/test_stage4.py",),
                "observability_requirements": ("finding_created",),
                "related_artifact_ids": ("art_1",),
            }
        },
        ("FX-R011",),
    )
    grounding_findings = check_grounding(
        {
            "artifact_id": "art_1",
            "claims": ("claim_a", "claim_b"),
            "covered_cases": ("case_a",),
        },
        (
            {
                "artifact_id": "src_1",
                "supported_claims": ("claim_a",),
                "expected_cases": ("case_a", "case_b"),
                "contradicted_claims": ("claim_b",),
            },
        ),
    )

    assert validation_result.status == "failed"
    assert reopened.status == "reopened"
    assert drift_findings[0].finding_type == "hidden_state_drift"
    assert traceability_result.status == "passed"
    assert len(grounding_findings) == 3


def test_stage4_validator_rejects_invalid_input_contracts() -> None:
    with pytest.raises(ValueError):
        validate_artifact({"quality_status": "failed"}, {"workflow_run_id": "wr_1"})

    with pytest.raises(ValueError):
        create_validation_finding("gap", "critical", "bad severity", ("art_1",), {}, "validator")


def test_stage4_drift_checker_identifies_valid_negative_examples_and_rejects_malformed_input() -> None:
    constitution_findings = check_constitution_drift({"adapter_owned_logic": True, "related_artifact_ids": ("art_1",)})
    provider_findings = check_provider_policy_drift(
        {
            "provider_path": "cloud_fallback",
            "local_provider_available": True,
            "related_artifact_ids": ("art_1",),
        }
    )
    lineage_findings = check_lineage_drift({"lineage_broken": True, "related_artifact_ids": ("art_1",)})

    assert constitution_findings[0].finding_type == "constitution_drift"
    assert provider_findings[0].finding_type == "provider_policy_drift"
    assert lineage_findings[0].finding_type == "lineage_drift"

    with pytest.raises(ValueError):
        check_hidden_state_drift("bad_subject")  # type: ignore[arg-type]


def test_stage4_traceability_auditor_and_grounding_checker_reject_incomplete_input() -> None:
    with pytest.raises(ValueError):
        check_requirement_coverage("FX-R011", {"observability_requirements": ("finding_created",)})

    with pytest.raises(ValueError):
        audit_traceability({}, ("FX-R011",))

    with pytest.raises(ValueError):
        check_unsupported_claims({"artifact_id": "art_1", "claims": ("claim_a",)}, ())

    with pytest.raises(ValueError):
        check_contradictions({"artifact_id": "art_1", "claims": ("claim_a",)}, ())

    with pytest.raises(ValueError):
        check_missing_cases({"artifact_id": "art_1", "covered_cases": ("case_a",)}, ())


def test_stage3_to_stage4_boundary_and_stage4_to_stage5_forward_boundary_exist() -> None:
    _, indexed_artifact, activation_output = _build_stage3_activation_output("Fix the broken onboarding checklist.")
    workflow_run = create_workflow_run("fix_flow", (indexed_artifact.artifact_id,))
    started = start_workflow(workflow_run, activation_output)

    continuity_ready_finding = create_validation_finding(
        "quality_gap",
        "medium",
        "Needs follow-up verification.",
        (indexed_artifact.artifact_id,),
        {"activation_output_id": activation_output.activation_output_id},
        "validator",
    )
    continuity_ready_record = {
        "workflow_run": asdict(started.workflow_run),
        "finding": asdict(continuity_ready_finding),
    }

    assert started.workflow_run.input_artifact_ids == activation_output.related_artifact_ids
    assert continuity_ready_record["workflow_run"]["workflow_state"] == "activated"
    assert "history" in continuity_ready_record["workflow_run"]
    assert continuity_ready_record["finding"]["related_artifact_ids"] == continuity_ready_finding.related_artifact_ids

    with pytest.raises(ValueError):
        start_workflow(create_workflow_run("single_run", (indexed_artifact.artifact_id,)), activation_output)
