from __future__ import annotations

from collections import Counter

from gdc_adk.workflows.agent_contracts import AgentTraceRecord, GovernanceCheckResult
from gdc_adk.workflows.state_machine import WorkflowRun


MAX_DELEGATION_DEPTH = 3
MAX_SAME_ROLE_REPETITION = 2
MAX_UNRESOLVED_HANDOFFS = 3


def _normalize_trace(agent_trace: tuple[AgentTraceRecord, ...] | list[AgentTraceRecord]) -> tuple[AgentTraceRecord, ...]:
    normalized = tuple(agent_trace)
    for record in normalized:
        if not isinstance(record, AgentTraceRecord):
            raise ValueError("agent_trace must contain only AgentTraceRecord entries.")
    return normalized


def validate_agent_sequence(workflow_run_id: str, agent_trace: tuple[AgentTraceRecord, ...] | list[AgentTraceRecord]) -> GovernanceCheckResult:
    if not isinstance(workflow_run_id, str) or not workflow_run_id.strip():
        raise ValueError("workflow_run_id must be a non-empty string.")
    normalized_trace = _normalize_trace(agent_trace)
    violations: list[str] = []
    for record in normalized_trace:
        if record.workflow_run_id != workflow_run_id:
            violations.append("trace_outside_workflow_scope")
        if record.action_type == "handoff_completed" and record.from_role == record.to_role:
            violations.append("self_escalation_detected")
    return GovernanceCheckResult(
        status="blocked" if violations else "accepted",
        blocked=bool(violations),
        violations=tuple(dict.fromkeys(violations)),
        message="Agent sequence blocked." if violations else "Agent sequence valid.",
    )


def detect_swarm_violation(
    workflow_run: WorkflowRun,
    agent_trace: tuple[AgentTraceRecord, ...] | list[AgentTraceRecord],
) -> tuple[GovernanceCheckResult, ...]:
    if not isinstance(workflow_run, WorkflowRun):
        raise ValueError("workflow_run must be a WorkflowRun.")
    normalized_trace = _normalize_trace(agent_trace)
    violations: list[GovernanceCheckResult] = []
    same_role_counter = Counter(record.to_role for record in normalized_trace if record.status != "rejected")
    for role_name, repetition_count in same_role_counter.items():
        if repetition_count > MAX_SAME_ROLE_REPETITION:
            violations.append(
                GovernanceCheckResult(
                    status="blocked",
                    blocked=True,
                    violations=(f"same_role_repetition_exceeded:{role_name}",),
                    message=f"Role repetition exceeded for {role_name}.",
                )
            )
    if any(record.delegation_depth > MAX_DELEGATION_DEPTH for record in normalized_trace):
        violations.append(
            GovernanceCheckResult(
                status="blocked",
                blocked=True,
                violations=("delegation_depth_exceeded",),
                message="Delegation depth exceeded.",
            )
        )
    if any(
        record.action_type == "handoff_completed" and record.from_role == "reviewer" and record.to_role == "reviewer"
        for record in normalized_trace
    ):
        violations.append(
            GovernanceCheckResult(
                status="blocked",
                blocked=True,
                violations=("independent_review_bypassed",),
                message="Reviewer independence was bypassed.",
            )
        )
    return tuple(violations)


def check_stop_conditions(
    workflow_run: WorkflowRun,
    agent_trace: tuple[AgentTraceRecord, ...] | list[AgentTraceRecord],
) -> GovernanceCheckResult:
    if not isinstance(workflow_run, WorkflowRun):
        raise ValueError("workflow_run must be a WorkflowRun.")
    normalized_trace = _normalize_trace(agent_trace)
    violations: list[str] = []
    unresolved_count = sum(1 for record in normalized_trace if record.status in {"pending", "accepted"})
    if unresolved_count > MAX_UNRESOLVED_HANDOFFS:
        violations.append("unresolved_handoff_limit_exceeded")
    if any(record.delegation_depth > MAX_DELEGATION_DEPTH for record in normalized_trace):
        violations.append("delegation_depth_exceeded")
    if any(record.from_role == record.to_role for record in normalized_trace):
        violations.append("self_escalation_detected")
    if violations:
        return GovernanceCheckResult(
            status="blocked",
            blocked=True,
            violations=tuple(dict.fromkeys(violations)),
            message="Delegation blocked by governance stop conditions.",
        )
    return GovernanceCheckResult(
        status="accepted",
        blocked=False,
        message="Delegation remains within bounded governance limits.",
    )
