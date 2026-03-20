from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime

from gdc_adk.workflows.state_machine import WorkflowRun, transition_workflow_state


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class RevisionDelta:
    prior_artifact_id: str
    revised_artifact_id: str
    revision_reason: str
    related_finding_ids: tuple[str, ...]
    delta_recorded_at: str
    carry_forward_finding_ids: tuple[str, ...]
    resolved_finding_ids: tuple[str, ...]


@dataclass(frozen=True)
class IterativeFlowResult:
    workflow_run: WorkflowRun
    revision_deltas: tuple[RevisionDelta, ...] = ()


def _require_iterative_run(workflow_run: WorkflowRun) -> WorkflowRun:
    if not isinstance(workflow_run, WorkflowRun):
        raise ValueError("workflow_run must be a WorkflowRun.")
    if workflow_run.workflow_mode != "iterative":
        raise ValueError("workflow_run.workflow_mode must be 'iterative'.")
    return workflow_run


def start_iterative_flow(workflow_run: WorkflowRun, input_artifact_ids: tuple[str, ...] | list[str]) -> IterativeFlowResult:
    run = _require_iterative_run(workflow_run)
    artifact_ids = tuple(str(artifact_id) for artifact_id in input_artifact_ids)
    if not artifact_ids:
        raise ValueError("input_artifact_ids must contain at least one artifact identifier.")
    updated_run = replace(run, input_artifact_ids=artifact_ids)
    transitioned_run = transition_workflow_state(updated_run, "planned", "Iterative flow planned.")
    return IterativeFlowResult(workflow_run=transitioned_run)


def plan_iteration(workflow_run: WorkflowRun, plan_reason: str) -> IterativeFlowResult:
    run = _require_iterative_run(workflow_run)
    transitioned_run = transition_workflow_state(run, "executing", plan_reason)
    return IterativeFlowResult(workflow_run=transitioned_run)


def record_revision_delta(
    workflow_run: WorkflowRun,
    prior_artifact_id: str,
    revised_artifact_id: str,
    revision_reason: str,
    related_finding_ids: tuple[str, ...] | list[str],
) -> IterativeFlowResult:
    run = _require_iterative_run(workflow_run)
    if not prior_artifact_id.strip() or not revised_artifact_id.strip():
        raise ValueError("prior_artifact_id and revised_artifact_id must be non-empty.")
    if prior_artifact_id == revised_artifact_id:
        raise ValueError("prior_artifact_id and revised_artifact_id must differ.")
    if not revision_reason.strip():
        raise ValueError("revision_reason must be non-empty.")
    normalized_finding_ids = tuple(str(finding_id) for finding_id in related_finding_ids)
    if prior_artifact_id not in run.input_artifact_ids + run.output_artifact_ids:
        raise ValueError("prior_artifact_id must already exist in workflow lineage.")
    revision_delta = RevisionDelta(
        prior_artifact_id=prior_artifact_id,
        revised_artifact_id=revised_artifact_id,
        revision_reason=revision_reason,
        related_finding_ids=normalized_finding_ids,
        delta_recorded_at=_utc_now(),
        carry_forward_finding_ids=normalized_finding_ids,
        resolved_finding_ids=(),
    )
    updated_run = replace(
        run,
        output_artifact_ids=run.output_artifact_ids + (revised_artifact_id,),
        finding_ids=tuple(dict.fromkeys(run.finding_ids + normalized_finding_ids)),
    )
    return IterativeFlowResult(workflow_run=updated_run, revision_deltas=(revision_delta,))


def attach_prior_findings(workflow_run: WorkflowRun, finding_ids: tuple[str, ...] | list[str]) -> IterativeFlowResult:
    run = _require_iterative_run(workflow_run)
    normalized_finding_ids = tuple(str(finding_id) for finding_id in finding_ids)
    if not normalized_finding_ids:
        raise ValueError("finding_ids must contain at least one identifier.")
    updated_run = replace(run, finding_ids=tuple(dict.fromkeys(run.finding_ids + normalized_finding_ids)))
    return IterativeFlowResult(workflow_run=updated_run)


def advance_iteration(workflow_run: WorkflowRun, next_state: str, reason: str) -> IterativeFlowResult:
    run = _require_iterative_run(workflow_run)
    transitioned_run = transition_workflow_state(run, next_state, reason)
    return IterativeFlowResult(workflow_run=transitioned_run)


def complete_iteration(workflow_run: WorkflowRun, completion_reason: str) -> IterativeFlowResult:
    run = _require_iterative_run(workflow_run)
    transitioned_run = transition_workflow_state(run, "completed", completion_reason)
    return IterativeFlowResult(workflow_run=transitioned_run)


def reopen_iteration(workflow_run: WorkflowRun, reopen_reason: str) -> IterativeFlowResult:
    run = _require_iterative_run(workflow_run)
    transitioned_run = transition_workflow_state(run, "reopened", reopen_reason)
    return IterativeFlowResult(workflow_run=transitioned_run)
