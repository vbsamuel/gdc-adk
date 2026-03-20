from __future__ import annotations

from typing import Mapping, Sequence

from gdc_adk.validation.validator import ReviewFinding, create_validation_finding


def _require_grounding_inputs(
    artifact: Mapping[str, object],
    source_artifacts: Sequence[Mapping[str, object]],
) -> tuple[Mapping[str, object], Sequence[Mapping[str, object]]]:
    if not isinstance(artifact, Mapping):
        raise ValueError("artifact must be a mapping.")
    if not isinstance(source_artifacts, Sequence) or not source_artifacts:
        raise ValueError("source_artifacts must be a non-empty sequence.")
    artifact_id = str(artifact.get("artifact_id", "")).strip()
    if not artifact_id:
        raise ValueError("artifact must include a non-empty artifact_id.")
    return artifact, source_artifacts


def _related_artifact_ids(artifact: Mapping[str, object], source_artifacts: Sequence[Mapping[str, object]]) -> tuple[str, ...]:
    source_ids = tuple(str(source.get("artifact_id", "")).strip() for source in source_artifacts)
    return tuple(item for item in (str(artifact.get("artifact_id")), *source_ids) if item)


def check_unsupported_claims(
    artifact: Mapping[str, object],
    source_artifacts: Sequence[Mapping[str, object]],
) -> list[ReviewFinding]:
    checked_artifact, checked_sources = _require_grounding_inputs(artifact, source_artifacts)
    supported_claims = {
        str(claim)
        for source in checked_sources
        for claim in source.get("supported_claims", ())
    }
    findings: list[ReviewFinding] = []
    for claim in checked_artifact.get("claims", ()):
        if str(claim) not in supported_claims:
            findings.append(
                create_validation_finding(
                    "unsupported_claim",
                    "high",
                    f"Claim '{claim}' is not supported by the provided sources.",
                    _related_artifact_ids(checked_artifact, checked_sources),
                    {"claim": claim},
                    "grounding_checker",
                )
            )
    return findings


def check_contradictions(
    artifact: Mapping[str, object],
    source_artifacts: Sequence[Mapping[str, object]],
) -> list[ReviewFinding]:
    checked_artifact, checked_sources = _require_grounding_inputs(artifact, source_artifacts)
    contradictory_claims = {
        str(claim)
        for source in checked_sources
        for claim in source.get("contradicted_claims", ())
    }
    findings: list[ReviewFinding] = []
    for claim in checked_artifact.get("claims", ()):
        if str(claim) in contradictory_claims:
            findings.append(
                create_validation_finding(
                    "contradiction",
                    "high",
                    f"Claim '{claim}' contradicts a provided source.",
                    _related_artifact_ids(checked_artifact, checked_sources),
                    {"claim": claim},
                    "grounding_checker",
                )
            )
    return findings


def check_missing_cases(
    artifact: Mapping[str, object],
    source_artifacts: Sequence[Mapping[str, object]],
) -> list[ReviewFinding]:
    checked_artifact, checked_sources = _require_grounding_inputs(artifact, source_artifacts)
    expected_cases = {
        str(case_name)
        for source in checked_sources
        for case_name in source.get("expected_cases", ())
    }
    covered_cases = {str(case_name) for case_name in checked_artifact.get("covered_cases", ())}
    missing_cases = sorted(expected_cases - covered_cases)
    if not missing_cases:
        return []
    return [
        create_validation_finding(
            "missing_case",
            "medium",
            "Artifact is missing required grounded cases.",
            _related_artifact_ids(checked_artifact, checked_sources),
            {"missing_cases": missing_cases},
            "grounding_checker",
        )
    ]


def check_grounding(
    artifact: Mapping[str, object],
    source_artifacts: Sequence[Mapping[str, object]],
) -> list[ReviewFinding]:
    checked_artifact, checked_sources = _require_grounding_inputs(artifact, source_artifacts)
    return (
        check_unsupported_claims(checked_artifact, checked_sources)
        + check_contradictions(checked_artifact, checked_sources)
        + check_missing_cases(checked_artifact, checked_sources)
    )
