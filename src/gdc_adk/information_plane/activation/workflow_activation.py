from __future__ import annotations

from gdc_adk.information_plane.ingestion.document_ingestor import ingest_text
from gdc_adk.information_plane.normalization.canonicalizer import normalize
from gdc_adk.information_plane.indexing.artifact_index import add as add_to_index
from gdc_adk.information_plane.activation.trigger_router import classify_signal
from gdc_adk.substrate.artifact_store import new_artifact
from gdc_adk.substrate.issue_tracker import create_issue
from gdc_adk.substrate.event_spine import append


def process_input(text: str, source: str = "user_input") -> dict:
    raw = ingest_text(text, source=source)
    normalized = normalize(raw)
    artifact = new_artifact(kind="text_input", content=normalized["text"], source=normalized["source"], metadata={"normalized_type": normalized["normalized_type"]})
    add_to_index(artifact)

    flow = classify_signal(normalized["text"])

    issue = None
    if flow == "fix_flow":
        issue = create_issue(
            title="Auto-triaged issue from input",
            description=normalized["text"],
            issue_type="fix_flow",
            severity="medium",
            related_artifact_id=artifact["artifact_id"],
        )

    append("input_processed", {
        "artifact_id": artifact["artifact_id"],
        "flow": flow,
        "issue_id": None if issue is None else issue["issue_id"],
    })

    return {
        "artifact": artifact,
        "flow": flow,
        "issue": issue,
    }
