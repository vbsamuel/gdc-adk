from __future__ import annotations

from dataclasses import dataclass, replace

from gdc_adk.information_plane.activation.workflow_activation import ActivationOutput
from gdc_adk.validation.validator import ValidationResult
from gdc_adk.workflows.state_machine import WorkflowRun, transition_workflow_state


@dataclass(frozen=True)
class WorkflowExecutionResult:
    workflow_run: WorkflowRun
    status: str
    message: str


def _require_workflow_run(workflow_run: WorkflowRun) -> WorkflowRun:
    if not isinstance(workflow_run, WorkflowRun):
        raise ValueError("workflow_run must be a WorkflowRun.")
    return workflow_run


def start_workflow(workflow_run: WorkflowRun, activation_output: ActivationOutput) -> WorkflowExecutionResult:
    run = _require_workflow_run(workflow_run)
    if not isinstance(activation_output, ActivationOutput):
        raise ValueError("activation_output must be an ActivationOutput.")
    if activation_output.candidate_workflow_mode != run.workflow_mode:
        raise ValueError("activation_output.candidate_workflow_mode must match workflow_run.workflow_mode.")
    classified_run = transition_workflow_state(run, "classified", "Workflow classified from activation output.")
    activated_run = transition_workflow_state(classified_run, "activated", "Workflow activation accepted.")
    linked_run = replace(
        activated_run,
        input_artifact_ids=tuple(dict.fromkeys(activated_run.input_artifact_ids + activation_output.related_artifact_ids)),
    )
    return WorkflowExecutionResult(
        workflow_run=linked_run,
        status="started",
        message="Workflow started with explicit activation state.",
    )


def advance_workflow(workflow_run: WorkflowRun, next_state: str, reason: str, context: dict[str, object]) -> WorkflowExecutionResult:
    run = _require_workflow_run(workflow_run)
    transitioned_run = transition_workflow_state(run, next_state, reason)
    updated_output_artifact_ids = transitioned_run.output_artifact_ids
    if context.get("output_artifact_id"):
        updated_output_artifact_ids = transitioned_run.output_artifact_ids + (str(context["output_artifact_id"]),)
    updated_run = replace(transitioned_run, output_artifact_ids=updated_output_artifact_ids)
    return WorkflowExecutionResult(
        workflow_run=updated_run,
        status="advanced",
        message=f"Workflow advanced to {next_state}.",
    )


def block_workflow(workflow_run: WorkflowRun, reason: str) -> WorkflowExecutionResult:
    run = _require_workflow_run(workflow_run)
    transitioned_run = transition_workflow_state(run, "blocked", reason)
    return WorkflowExecutionResult(workflow_run=transitioned_run, status="blocked", message=reason)


def complete_workflow(workflow_run: WorkflowRun, completion_reason: str) -> WorkflowExecutionResult:
    run = _require_workflow_run(workflow_run)
    transitioned_run = transition_workflow_state(run, "completed", completion_reason)
    return WorkflowExecutionResult(workflow_run=transitioned_run, status="completed", message=completion_reason)


def fail_workflow(workflow_run: WorkflowRun, failure_reason: str) -> WorkflowExecutionResult:
    run = _require_workflow_run(workflow_run)
    transitioned_run = transition_workflow_state(run, "failed", failure_reason)
    return WorkflowExecutionResult(workflow_run=transitioned_run, status="failed", message=failure_reason)


def reopen_workflow(workflow_run: WorkflowRun, reopen_reason: str) -> WorkflowExecutionResult:
    run = _require_workflow_run(workflow_run)
    transitioned_run = transition_workflow_state(run, "reopened", reopen_reason)
    return WorkflowExecutionResult(workflow_run=transitioned_run, status="reopened", message=reopen_reason)


def apply_validation_gate(workflow_run: WorkflowRun, validation_result: ValidationResult) -> WorkflowExecutionResult:
    run = _require_workflow_run(workflow_run)
    if not isinstance(validation_result, ValidationResult):
        raise ValueError("validation_result must be a ValidationResult.")
    finding_ids = tuple(finding.finding_id for finding in validation_result.findings)
    updated_run = replace(run, finding_ids=tuple(dict.fromkeys(run.finding_ids + finding_ids)))
    if validation_result.status == "passed":
        transitioned_run = transition_workflow_state(updated_run, "validated", validation_result.summary)
        return WorkflowExecutionResult(
            workflow_run=transitioned_run,
            status="validated",
            message=validation_result.summary,
        )
    transitioned_run = transition_workflow_state(updated_run, "blocked", validation_result.summary)
    return WorkflowExecutionResult(
        workflow_run=transitioned_run,
        status="blocked",
        message=validation_result.summary,
    )
