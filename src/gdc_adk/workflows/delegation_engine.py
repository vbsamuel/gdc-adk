from __future__ import annotations

from gdc_adk.validation.agent_governance import check_stop_conditions

from gdc_adk.validation.handoff_validator import (
    validate_handoff_artifacts,
    validate_review_requirements,
)

from gdc_adk.workflows.agent_contracts import (
    AgentTraceRecord,
    DelegationResult,
    GovernanceCheckResult,
    HandoffArtifact,
    create_agent_trace_record,
    validate_handoff_contract,
)
from gdc_adk.workflows.agent_roles import can_role_delegate, get_allowed_handoff_targets, get_role_permissions
from gdc_adk.workflows.handoff_manager import get_coordination_envelope, initiate_handoff
from gdc_adk.workflows.state_machine import WorkflowRun


def validate_delegation(from_role: str, to_role: str, workflow_run: WorkflowRun) -> None:
    if not isinstance(workflow_run, WorkflowRun):
        raise ValueError("workflow_run must be a WorkflowRun.")
    if not can_role_delegate(from_role):
        raise ValueError(f"Role may not delegate: {from_role}")
    if to_role not in get_allowed_handoff_targets(from_role):
        raise ValueError(f"Delegation target '{to_role}' is not allowed for role '{from_role}'.")
    if from_role == to_role:
        raise ValueError("Delegation may not self-escalate to the same role.")


def check_delegation_limits(
    workflow_run: WorkflowRun,
    agent_trace: tuple[AgentTraceRecord, ...] | list[AgentTraceRecord],
) -> GovernanceCheckResult:
    return check_stop_conditions(workflow_run, agent_trace)


def delegate_task(from_role: str, to_role: str, handoff_artifact: HandoffArtifact, workflow_run: WorkflowRun) -> DelegationResult:
    if not isinstance(workflow_run, WorkflowRun):
        raise ValueError("workflow_run must be a WorkflowRun.")
    validate_handoff_contract(handoff_artifact)
    validation_result = validate_handoff_artifacts(handoff_artifact)
    review_validation = validate_review_requirements(handoff_artifact, workflow_run)

    if not review_validation.is_valid:
        governance_result = GovernanceCheckResult(
            status="blocked",
            blocked=True,
            violations=("review_requirements_invalid",),
            message=review_validation.message,
        )
        return DelegationResult(
            status="rejected",
            governance_result=governance_result,
            validation_result=review_validation,
            message=review_validation.message,
        )


    if not validation_result.is_valid:
        governance_result = GovernanceCheckResult(
            status="blocked",
            blocked=True,
            violations=("handoff_reference_invalid",),
            message=validation_result.message,
        )
        return DelegationResult(
            status="rejected",
            governance_result=governance_result,
            validation_result=validation_result,
            message=validation_result.message,
        )

    try:
        validate_delegation(from_role, to_role, workflow_run)
    except ValueError as exc:
        governance_result = GovernanceCheckResult(
            status="blocked",
            blocked=True,
            violations=("unauthorized_delegation",),
            message=str(exc),
        )
        return DelegationResult(
            status="rejected",
            governance_result=governance_result,
            validation_result=validation_result,
            message=str(exc),
        )

    target_permissions = get_role_permissions(to_role)
    disallowed_actions = tuple(
        action for action in handoff_artifact.requested_actions if action not in target_permissions["allowed_actions"]
    )
    if disallowed_actions:
        governance_result = GovernanceCheckResult(
            status="blocked",
            blocked=True,
            violations=("over_broad_task_scope",),
            message=f"Requested actions are outside the allowed scope for role '{to_role}'.",
        )
        return DelegationResult(
            status="rejected",
            governance_result=governance_result,
            validation_result=validation_result,
            message=governance_result.message,
        )

    if handoff_artifact.workflow_run_id != workflow_run.workflow_run_id:
        governance_result = GovernanceCheckResult(
            status="blocked",
            blocked=True,
            violations=("workflow_scope_mismatch",),
            message="Delegation must stay within one workflow_run_id.",
        )
        return DelegationResult(
            status="rejected",
            governance_result=governance_result,
            validation_result=validation_result,
            message=governance_result.message,
        )

    coordination_envelope = get_coordination_envelope(workflow_run.workflow_run_id)
    current_trace = () if coordination_envelope is None else coordination_envelope.trace_records
    proposed_trace = current_trace + (create_agent_trace_record(handoff_artifact, "delegation_requested", "pending"),)
    governance_result = check_delegation_limits(workflow_run, proposed_trace)
    if governance_result.blocked:
        return DelegationResult(
            status="rejected",
            governance_result=governance_result,
            validation_result=validation_result,
            message=governance_result.message,
        )

    lifecycle_result = initiate_handoff(handoff_artifact, workflow_run)
    return DelegationResult(
        status="accepted",
        handoff=lifecycle_result.handoff,
        coordination_envelope=lifecycle_result.coordination_envelope,
        governance_result=governance_result,
        validation_result=validation_result,
        message="Delegation accepted within Stage 6 governance limits.",
    )
