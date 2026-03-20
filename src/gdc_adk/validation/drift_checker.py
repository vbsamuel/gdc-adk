from __future__ import annotations

from typing import Mapping

from gdc_adk.validation.validator import ReviewFinding, create_validation_finding


def _require_subject(subject: Mapping[str, object]) -> Mapping[str, object]:
    if not isinstance(subject, Mapping):
        raise ValueError("subject must be a mapping.")
    return subject


def check_constitution_drift(subject: Mapping[str, object]) -> list[ReviewFinding]:
    checked_subject = _require_subject(subject)
    findings: list[ReviewFinding] = []
    if checked_subject.get("adapter_owned_logic") is True:
        findings.append(
            create_validation_finding(
                "constitution_drift",
                "high",
                "Business logic is hidden in an adapter surface.",
                tuple(str(item) for item in checked_subject.get("related_artifact_ids", ())),
                {"adapter_owned_logic": True},
                "drift_checker",
            )
        )
    return findings


def check_provider_policy_drift(subject: Mapping[str, object]) -> list[ReviewFinding]:
    checked_subject = _require_subject(subject)
    findings: list[ReviewFinding] = []
    if checked_subject.get("provider_path") == "cloud_fallback" and checked_subject.get("local_provider_available") is True:
        findings.append(
            create_validation_finding(
                "provider_policy_drift",
                "high",
                "Cloud fallback was selected while a local provider remained available.",
                tuple(str(item) for item in checked_subject.get("related_artifact_ids", ())),
                {
                    "provider_path": checked_subject.get("provider_path"),
                    "local_provider_available": checked_subject.get("local_provider_available"),
                },
                "drift_checker",
            )
        )
    return findings


def check_hidden_state_drift(subject: Mapping[str, object]) -> list[ReviewFinding]:
    checked_subject = _require_subject(subject)
    findings: list[ReviewFinding] = []
    if checked_subject.get("prompt_carry_state") is True:
        findings.append(
            create_validation_finding(
                "hidden_state_drift",
                "high",
                "Workflow state is being carried in prompt text rather than explicit structured state.",
                tuple(str(item) for item in checked_subject.get("related_artifact_ids", ())),
                {"prompt_carry_state": True},
                "drift_checker",
            )
        )
    return findings


def check_lineage_drift(subject: Mapping[str, object]) -> list[ReviewFinding]:
    checked_subject = _require_subject(subject)
    findings: list[ReviewFinding] = []
    if checked_subject.get("lineage_broken") is True:
        findings.append(
            create_validation_finding(
                "lineage_drift",
                "medium",
                "Revision lineage is missing or broken.",
                tuple(str(item) for item in checked_subject.get("related_artifact_ids", ())),
                {"lineage_broken": True},
                "drift_checker",
            )
        )
    return findings
