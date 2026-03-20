from __future__ import annotations

from datetime import datetime, timezone
from typing import List
import uuid

from gdc_adk.core.contracts import Issue
from gdc_adk.core.contracts import validate_issue_record
from gdc_adk.core.state import validate_issue_status, validate_issue_type, validate_severity

_ISSUES: dict[str, Issue] = {}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def reset_issue_store() -> None:
    _ISSUES.clear()


def export_issue_records() -> List[Issue]:
    return [dict(issue) for issue in _ISSUES.values()]


def load_issue_records(issues: List[Issue]) -> None:
    reset_issue_store()
    for issue in issues:
        create_issue(issue)


def create_issue(issue: Issue) -> Issue:
    validate_issue_record(issue)
    issue_id = issue["issue_id"]
    if issue_id in _ISSUES:
        raise ValueError(f"Duplicate issue_id: {issue_id}")
    _ISSUES[issue_id] = dict(issue)
    return _ISSUES[issue_id]


def get_issue(issue_id: str) -> Issue:
    if issue_id not in _ISSUES:
        raise KeyError(f"Issue not found: {issue_id}")
    return _ISSUES[issue_id]


def list_issues() -> List[Issue]:
    return list(_ISSUES.values())


def list_issues_by_artifact_id(artifact_id: str) -> List[Issue]:
    return [i for i in _ISSUES.values() if artifact_id in i.get("related_artifact_ids", [])]


def update_issue_status(issue_id: str, new_status: str) -> Issue:
    issue = get_issue(issue_id)
    validate_issue_status(new_status)
    issue["status"] = new_status
    issue["updated_at"] = _now_iso()
    return issue


def reopen_issue(issue_id: str) -> Issue:
    issue = get_issue(issue_id)
    if issue["status"] not in {"resolved", "closed"}:
        raise ValueError("Only resolved or closed issues can be reopened")
    issue["status"] = "reopened"
    issue["reopen_count"] = issue.get("reopen_count", 0) + 1
    issue["updated_at"] = _now_iso()
    return issue


def link_issue_to_artifact(issue_id: str, artifact_id: str) -> Issue:
    issue = get_issue(issue_id)
    if artifact_id not in issue.get("related_artifact_ids", []):
        issue["related_artifact_ids"].append(artifact_id)
    issue["updated_at"] = _now_iso()
    return issue
