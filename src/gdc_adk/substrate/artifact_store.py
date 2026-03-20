from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional
import uuid

from gdc_adk.core.contracts import Artifact
from gdc_adk.core.contracts import validate_artifact_record

_ARTIFACTS: dict[str, Artifact] = {}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _append_missing_ids(existing_ids: List[str], candidate_ids: List[str]) -> List[str]:
    combined_ids = list(existing_ids)
    for candidate_id in candidate_ids:
        if candidate_id not in combined_ids:
            combined_ids.append(candidate_id)
    return combined_ids


def reset_artifact_store() -> None:
    _ARTIFACTS.clear()


def export_artifact_records() -> List[Artifact]:
    return [dict(artifact) for artifact in _ARTIFACTS.values()]


def load_artifact_records(artifacts: List[Artifact]) -> None:
    reset_artifact_store()
    for artifact in artifacts:
        create_artifact(artifact)


def new_artifact(kind: str, content: Optional[str] = None, source: str = "unknown", metadata: dict | None = None) -> Artifact:
    artifact: Artifact = {
        "artifact_id": f"art_{uuid.uuid4().hex[:12]}",
        "artifact_kind": kind,
        "content": content,
        "content_ref": None,
        "source": {"origin": source},
        "metadata": metadata or {},
        "created_at": _now_iso(),
        "parent_artifact_ids": [],
        "workflow_run_id": None,
        "issue_ids": [],
    }
    validate_artifact_record(artifact)
    return artifact


def create_artifact(artifact: Artifact) -> Artifact:
    validate_artifact_record(artifact)
    artifact_id = artifact["artifact_id"]
    if artifact_id in _ARTIFACTS:
        raise ValueError(f"Duplicate artifact_id: {artifact_id}")
    _ARTIFACTS[artifact_id] = dict(artifact)
    return _ARTIFACTS[artifact_id]


def get_artifact(artifact_id: str) -> Artifact:
    if artifact_id not in _ARTIFACTS:
        raise KeyError(f"Artifact not found: {artifact_id}")
    return _ARTIFACTS[artifact_id]


def list_artifacts() -> List[Artifact]:
    return list(_ARTIFACTS.values())


def list_artifacts_by_workflow_run_id(workflow_run_id: Optional[str]) -> List[Artifact]:
    return [a for a in _ARTIFACTS.values() if a.get("workflow_run_id") == workflow_run_id]


def list_artifacts_by_issue_id(issue_id: str) -> List[Artifact]:
    return [a for a in _ARTIFACTS.values() if issue_id in a.get("issue_ids", [])]


def create_artifact_revision(artifact: Artifact) -> Artifact:
    validate_artifact_record(artifact)
    original_id = artifact["artifact_id"]
    if original_id not in _ARTIFACTS:
        raise KeyError(f"Original artifact not found: {original_id}")

    revised_artifact = dict(artifact)
    revised_artifact["artifact_id"] = f"art_{uuid.uuid4().hex[:12]}"
    revised_artifact["parent_artifact_ids"] = _append_missing_ids(
        revised_artifact.get("parent_artifact_ids", []),
        [original_id],
    )
    revised_artifact["created_at"] = _now_iso()
    validate_artifact_record(revised_artifact)
    _ARTIFACTS[revised_artifact["artifact_id"]] = revised_artifact
    return revised_artifact


def link_parent_artifacts(artifact_id: str, parent_artifact_ids: List[str]) -> Artifact:
    artifact = get_artifact(artifact_id)
    for parent_id in parent_artifact_ids:
        if parent_id not in _ARTIFACTS:
            raise KeyError(f"Parent artifact not found: {parent_id}")
    artifact["parent_artifact_ids"] = _append_missing_ids(
        artifact.get("parent_artifact_ids", []),
        parent_artifact_ids,
    )
    return artifact


def link_issue_to_artifact(artifact_id: str, issue_id: str) -> Artifact:
    artifact = get_artifact(artifact_id)
    artifact["issue_ids"] = _append_missing_ids(artifact.get("issue_ids", []), [issue_id])
    return artifact


def update_artifact_workflow_run(artifact_id: str, workflow_run_id: str) -> Artifact:
    artifact = get_artifact(artifact_id)
    artifact["workflow_run_id"] = workflow_run_id
    return artifact
