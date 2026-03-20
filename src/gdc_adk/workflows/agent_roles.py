from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class RoleDefinition:
    role_name: str
    allowed_actions: tuple[str, ...]
    forbidden_actions: tuple[str, ...]
    allowed_handoff_targets: tuple[str, ...]
    can_delegate: bool
    requires_review: bool
    may_reopen_workflow: bool
    may_reopen_issue: bool
    may_reopen_finding: bool


_ROLE_DEFINITIONS: dict[str, RoleDefinition] = {
    "planner": RoleDefinition(
        role_name="planner",
        allowed_actions=("plan_work", "request_execution", "request_review", "request_validation"),
        forbidden_actions=("execute_artifact", "approve_own_artifact", "close_review"),
        allowed_handoff_targets=("executor", "reviewer", "validator"),
        can_delegate=True,
        requires_review=True,
        may_reopen_workflow=False,
        may_reopen_issue=False,
        may_reopen_finding=False,
    ),
    "executor": RoleDefinition(
        role_name="executor",
        allowed_actions=("execute_artifact", "request_review", "request_validation", "request_fix"),
        forbidden_actions=("approve_own_artifact", "close_review"),
        allowed_handoff_targets=("reviewer", "validator", "fixer"),
        can_delegate=True,
        requires_review=True,
        may_reopen_workflow=False,
        may_reopen_issue=False,
        may_reopen_finding=False,
    ),
    "reviewer": RoleDefinition(
        role_name="reviewer",
        allowed_actions=("review_artifact", "create_finding", "request_revision"),
        forbidden_actions=("execute_artifact", "approve_own_artifact"),
        allowed_handoff_targets=("validator",),
        can_delegate=True,
        requires_review=False,
        may_reopen_workflow=True,
        may_reopen_issue=False,
        may_reopen_finding=True,
    ),
    "fixer": RoleDefinition(
        role_name="fixer",
        allowed_actions=("remediate_issue", "request_review", "request_validation"),
        forbidden_actions=("approve_own_fix", "close_review"),
        allowed_handoff_targets=("reviewer", "validator"),
        can_delegate=True,
        requires_review=True,
        may_reopen_workflow=True,
        may_reopen_issue=True,
        may_reopen_finding=False,
    ),
    "validator": RoleDefinition(
        role_name="validator",
        allowed_actions=("validate_output", "validate_traceability", "validate_grounding"),
        forbidden_actions=("execute_artifact", "author_artifact"),
        allowed_handoff_targets=(),
        can_delegate=False,
        requires_review=False,
        may_reopen_workflow=True,
        may_reopen_issue=False,
        may_reopen_finding=True,
    ),
}


def _get_definition(role_name: str) -> RoleDefinition:
    role_key = str(role_name).strip()
    if role_key not in _ROLE_DEFINITIONS:
        raise ValueError(f"Unknown role_name: {role_name}")
    return _ROLE_DEFINITIONS[role_key]


def list_allowed_roles() -> list[str]:
    return list(_ROLE_DEFINITIONS)


def get_role_definition(role_name: str) -> dict[str, Any]:
    return asdict(_get_definition(role_name))


def get_role_permissions(role_name: str) -> dict[str, Any]:
    definition = _get_definition(role_name)
    return {
        "role_name": definition.role_name,
        "allowed_actions": list(definition.allowed_actions),
        "forbidden_actions": list(definition.forbidden_actions),
        "can_delegate": definition.can_delegate,
        "may_reopen_workflow": definition.may_reopen_workflow,
        "may_reopen_issue": definition.may_reopen_issue,
        "may_reopen_finding": definition.may_reopen_finding,
    }


def get_allowed_handoff_targets(role_name: str) -> list[str]:
    return list(_get_definition(role_name).allowed_handoff_targets)


def can_role_delegate(role_name: str) -> bool:
    return _get_definition(role_name).can_delegate


def requires_independent_review(role_name: str, artifact_type: str | None = None) -> bool:
    definition = _get_definition(role_name)
    if artifact_type is not None and str(artifact_type).strip() == "trivial_note":
        return False
    return definition.requires_review
