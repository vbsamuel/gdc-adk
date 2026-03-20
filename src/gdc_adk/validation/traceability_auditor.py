from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from gdc_adk.validation.validator import ReviewFinding, create_validation_finding


@dataclass(frozen=True)
class RequirementCoverageResult:
    requirement_id: str
    status: str
    missing_acceptance_evidence: bool
    missing_observability_evidence: bool
    finding: ReviewFinding | None = None


@dataclass(frozen=True)
class TraceabilityAuditResult:
    status: str
    requirement_ids: tuple[str, ...]
    coverage_results: tuple[RequirementCoverageResult, ...]
    findings: tuple[ReviewFinding, ...]


def build_traceability_gap_finding(
    requirement_id: str,
    gap_description: str,
    related_artifact_ids: tuple[str, ...] | list[str],
) -> ReviewFinding:
    return create_validation_finding(
        "traceability_gap",
        "medium",
        gap_description,
        related_artifact_ids,
        {"requirement_id": requirement_id},
        "traceability_auditor",
    )


def check_requirement_coverage(requirement_id: str, evidence_bundle: Mapping[str, object]) -> RequirementCoverageResult:
    if not requirement_id.strip():
        raise ValueError("requirement_id must be non-empty.")
    if not isinstance(evidence_bundle, Mapping):
        raise ValueError("evidence_bundle must be a mapping.")

    missing_acceptance_evidence = not bool(evidence_bundle.get("acceptance_tests"))
    missing_observability_evidence = not bool(evidence_bundle.get("observability_requirements"))

    if missing_acceptance_evidence or missing_observability_evidence:
        raise ValueError(f"Requirement {requirement_id} is missing required traceability evidence.")

    return RequirementCoverageResult(
        requirement_id=requirement_id,
        status="passed",
        missing_acceptance_evidence=False,
        missing_observability_evidence=False,
    )


def audit_traceability(subject: Mapping[str, Mapping[str, object]], requirement_ids: tuple[str, ...] | list[str]) -> TraceabilityAuditResult:
    if not isinstance(subject, Mapping):
        raise ValueError("subject must be a mapping of requirement_id to evidence_bundle.")
    normalized_requirement_ids = tuple(str(requirement_id) for requirement_id in requirement_ids)
    if not normalized_requirement_ids:
        raise ValueError("requirement_ids must contain at least one requirement_id.")

    coverage_results: list[RequirementCoverageResult] = []
    findings: list[ReviewFinding] = []
    for requirement_id in normalized_requirement_ids:
        if requirement_id not in subject:
            raise ValueError(f"Missing evidence bundle for requirement_id: {requirement_id}")
        coverage_result = check_requirement_coverage(requirement_id, subject[requirement_id])
        coverage_results.append(coverage_result)
        if coverage_result.finding is not None:
            findings.append(coverage_result.finding)

    status = "passed" if not findings else "failed"
    return TraceabilityAuditResult(
        status=status,
        requirement_ids=normalized_requirement_ids,
        coverage_results=tuple(coverage_results),
        findings=tuple(findings),
    )
