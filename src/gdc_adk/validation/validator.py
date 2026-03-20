from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from typing import Mapping
from uuid import uuid4


FINDING_STATUSES: frozenset[str] = frozenset({"open", "accepted", "rejected", "resolved", "reopened"})
FINDING_SEVERITIES: frozenset[str] = frozenset({"low", "medium", "high"})


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class FindingHistoryEntry:
    previous_status: str
    next_status: str
    reason: str
    changed_at: str


@dataclass(frozen=True)
class ReviewFinding:
    finding_id: str
    finding_type: str
    severity: str
    description: str
    related_artifact_ids: tuple[str, ...]
    evidence: dict[str, object]
    reviewer_identity: str
    status: str = "open"
    related_workflow_run_id: str | None = None
    history: tuple[FindingHistoryEntry, ...] = ()


@dataclass(frozen=True)
class ValidationResult:
    status: str
    findings: tuple[ReviewFinding, ...]
    related_artifact_ids: tuple[str, ...]
    summary: str


def create_validation_finding(
    finding_type: str,
    severity: str,
    description: str,
    related_artifact_ids: tuple[str, ...] | list[str],
    evidence: Mapping[str, object],
    reviewer_identity: str,
) -> ReviewFinding:
    if not finding_type.strip():
        raise ValueError("finding_type must be non-empty.")
    if severity not in FINDING_SEVERITIES:
        raise ValueError(f"Unsupported severity: {severity}")
    if not description.strip():
        raise ValueError("description must be non-empty.")
    if not reviewer_identity.strip():
        raise ValueError("reviewer_identity must be non-empty.")
    artifact_ids = tuple(str(artifact_id) for artifact_id in related_artifact_ids)
    if any(not artifact_id.strip() for artifact_id in artifact_ids):
        raise ValueError("related_artifact_ids must contain only non-empty identifiers.")
    return ReviewFinding(
        finding_id=f"finding_{uuid4().hex[:12]}",
        finding_type=finding_type,
        severity=severity,
        description=description,
        related_artifact_ids=artifact_ids,
        evidence=dict(evidence),
        reviewer_identity=reviewer_identity,
    )


def transition_finding_status(finding: ReviewFinding, next_status: str, reason: str) -> ReviewFinding:
    if not isinstance(finding, ReviewFinding):
        raise ValueError("finding must be a ReviewFinding.")
    if next_status not in FINDING_STATUSES:
        raise ValueError(f"Unsupported finding status: {next_status}")
    if not reason.strip():
        raise ValueError("reason must be non-empty.")
    history_entry = FindingHistoryEntry(
        previous_status=finding.status,
        next_status=next_status,
        reason=reason,
        changed_at=_utc_now(),
    )
    return replace(finding, status=next_status, history=finding.history + (history_entry,))


def resolve_validation_finding(finding: ReviewFinding, resolution_reason: str) -> ReviewFinding:
    return transition_finding_status(finding, "resolved", resolution_reason)


def reopen_validation_finding(finding: ReviewFinding, reopen_reason: str) -> ReviewFinding:
    return transition_finding_status(finding, "reopened", reopen_reason)


def _validate_review_input(artifact: Mapping[str, object], workflow_context: Mapping[str, object]) -> tuple[str, str]:
    artifact_id = str(artifact.get("artifact_id", "")).strip()
    if not artifact_id:
        raise ValueError("artifact must include a non-empty artifact_id.")
    workflow_run_id = str(workflow_context.get("workflow_run_id", "")).strip()
    if not workflow_run_id:
        raise ValueError("workflow_context must include a non-empty workflow_run_id.")
    return artifact_id, workflow_run_id


def validate_artifact(artifact: Mapping[str, object], workflow_context: Mapping[str, object]) -> ValidationResult:
    artifact_id, workflow_run_id = _validate_review_input(artifact, workflow_context)
    findings: list[ReviewFinding] = []

    if artifact.get("quality_status") == "failed":
        finding = create_validation_finding(
            finding_type="quality_gap",
            severity="high",
            description="Artifact failed the declared quality check.",
            related_artifact_ids=(artifact_id,),
            evidence={"quality_status": artifact.get("quality_status")},
            reviewer_identity="validator",
        )
        findings.append(replace(finding, related_workflow_run_id=workflow_run_id))

    if not artifact.get("grounded_sources"):
        finding = create_validation_finding(
            finding_type="grounding_gap",
            severity="medium",
            description="Artifact is missing grounding sources.",
            related_artifact_ids=(artifact_id,),
            evidence={"grounded_sources": artifact.get("grounded_sources", ())},
            reviewer_identity="validator",
        )
        findings.append(replace(finding, related_workflow_run_id=workflow_run_id))

    status = "passed" if not findings else "failed"
    summary = "Artifact passed validation." if status == "passed" else f"Artifact produced {len(findings)} finding(s)."
    return ValidationResult(
        status=status,
        findings=tuple(findings),
        related_artifact_ids=(artifact_id,),
        summary=summary,
    )


def validate_workflow_output(output_artifact: Mapping[str, object], workflow_context: Mapping[str, object]) -> ValidationResult:
    return validate_artifact(output_artifact, workflow_context)
