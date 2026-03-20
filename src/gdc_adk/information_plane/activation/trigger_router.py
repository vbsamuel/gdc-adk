from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from gdc_adk.information_plane.normalization.canonicalizer import CanonicalSignal


@dataclass(frozen=True)
class ActivationReason:
    rationale_code: str
    matched_terms: tuple[str, ...]
    normalized_type: str
    coarse_intent: str | None


@dataclass(frozen=True)
class ActivationTrigger:
    activation_category: str
    candidate_workflow_mode: str
    issue_triggered: bool
    activation_reason: ActivationReason
    next_action_types: tuple[str, ...]


def _require_canonical_signal(normalized_signal: CanonicalSignal) -> CanonicalSignal:
    if not isinstance(normalized_signal, CanonicalSignal):
        raise ValueError("normalized_signal must be a CanonicalSignal.")
    if not normalized_signal.extracted_text:
        raise ValueError("normalized_signal must contain extracted_text.")
    return normalized_signal


def _matched_terms(extracted_text: str) -> tuple[str, ...]:
    keywords = ("bug", "broken", "fix", "error", "failed", "issue", "research", "investigate", "analyze")
    lowered_text = extracted_text.lower()
    return tuple(keyword for keyword in keywords if keyword in lowered_text)


def classify_activation_category(normalized_signal: CanonicalSignal) -> str:
    canonical_signal = _require_canonical_signal(normalized_signal)
    coarse_intent = canonical_signal.coarse_intent
    extracted_text = canonical_signal.extracted_text.lower()
    if canonical_signal.ambiguity_markers:
        return "fuzzy_candidate"
    if any(token in extracted_text for token in ("multi-step", "coordinate", "handoff", "orchestrate")):
        return "dynamic_candidate"
    if coarse_intent == "defect_triage":
        return "issue_candidate"
    if coarse_intent == "analysis_request":
        return "iterative_candidate"
    if coarse_intent in {"weather_lookup", "time_lookup", "geo_lookup"}:
        return "deterministic_candidate"
    return "general_candidate"


def select_workflow_mode(normalized_signal: CanonicalSignal) -> str:
    activation_category = classify_activation_category(normalized_signal)
    if activation_category == "issue_candidate":
        return "fix_flow"
    if activation_category == "iterative_candidate":
        return "iterative"
    if activation_category == "dynamic_candidate":
        return "dynamic_flow"
    if activation_category == "fuzzy_candidate":
        return "fuzzy_logical_flow"
    if activation_category == "deterministic_candidate":
        return "single_run"
    return "single_run"


def should_trigger_issue(normalized_signal: CanonicalSignal) -> bool:
    return select_workflow_mode(normalized_signal) == "fix_flow"


def build_activation_reason(normalized_signal: CanonicalSignal) -> ActivationReason:
    canonical_signal = _require_canonical_signal(normalized_signal)
    activation_category = classify_activation_category(canonical_signal)
    rationale_code = {
        "issue_candidate": "defect_keyword_match",
        "iterative_candidate": "analysis_keyword_match",
        "dynamic_candidate": "dynamic_keyword_match",
        "fuzzy_candidate": "ambiguous_signal_match",
        "deterministic_candidate": "deterministic_lookup_match",
        "general_candidate": "general_text_match",
    }[activation_category]
    return ActivationReason(
        rationale_code=rationale_code,
        matched_terms=_matched_terms(canonical_signal.extracted_text or ""),
        normalized_type=canonical_signal.normalized_type,
        coarse_intent=canonical_signal.coarse_intent,
    )


def build_activation_trigger(normalized_signal: CanonicalSignal) -> ActivationTrigger:
    activation_category = classify_activation_category(normalized_signal)
    candidate_workflow_mode = select_workflow_mode(normalized_signal)
    issue_triggered = should_trigger_issue(normalized_signal)

    if activation_category == "issue_candidate":
        next_action_types = ("local_reasoning",)
    elif activation_category == "deterministic_candidate":
        coarse_intent = normalized_signal.coarse_intent or "general_request"
        next_action_types = (coarse_intent,)
    elif activation_category == "dynamic_candidate":
        next_action_types = ("general_reasoning",)
    elif activation_category == "fuzzy_candidate":
        next_action_types = ("general_reasoning",)
    else:
        next_action_types = ("general_reasoning",)

    return ActivationTrigger(
        activation_category=activation_category,
        candidate_workflow_mode=candidate_workflow_mode,
        issue_triggered=issue_triggered,
        activation_reason=build_activation_reason(normalized_signal),
        next_action_types=next_action_types,
    )


def activation_trigger_to_record(trigger: ActivationTrigger) -> dict[str, Any]:
    return asdict(trigger)
