"""Stage 1 acceptance mapping for the current bounded slice.

Requirement mapping:
- FX-R007: request artifacts are created, linked, and reloadable through public substrate contracts
- FX-R008: fix_flow creates a typed issue linked to artifacts in both directions
- FX-R009: dispatch creates a structured workflow entry, emits Stage 1 events, and rejects unsupported hints

Scenario A:
- meaningful input creates a request artifact and traceable workflow entry

Scenario C:
- fix_flow input creates a typed issue linked to the artifact in both directions

Scenario D:
- dispatch emits structured Stage 1 events and rejects unsupported workflow hints
"""

import pytest

from gdc_adk.core import state, contracts
from gdc_adk.substrate import event_spine, artifact_store, issue_tracker, provenance, versioning, dispatch_system


@pytest.fixture(autouse=True)
def reset_state():
    event_spine.EVENTS.clear()
    artifact_store.reset_artifact_store()
    issue_tracker.reset_issue_store()
    provenance.reset_provenance_records()
    versioning.reset_version_records()
    dispatch_system.reset_workflow_runs()


def test_state_validators_and_helpers():
    assert state.validate_workflow_mode("single_run") == "single_run"
    assert state.validate_workflow_state("completed") == "completed"
    assert state.validate_issue_type("defect") == "defect"
    assert state.validate_issue_status("open") == "open"
    assert state.validate_severity("medium") == "medium"
    assert state.validate_event_type("request_received") == "request_received"
    with pytest.raises(ValueError):
        state.validate_workflow_mode("done")
    assert state.is_terminal_workflow_state("completed") is True
    assert state.is_terminal_workflow_state("executing") is False
    assert state.is_reopenable_issue_status("closed") is True
    assert state.is_reopenable_issue_status("open") is False


def test_event_spine_append_and_lookup():
    event = event_spine.create_event("request_received", "corr_1", {"foo": "bar"}, workflow_run_id=None)
    assert event_spine.get_event(event["event_id"]) == event
    assert event_spine.list_events_by_correlation_id("corr_1") == [event]
    assert event_spine.list_events_by_event_type("request_received") == [event]
    with pytest.raises(ValueError):
        event_spine.record_event(event)


def test_artifact_store_lifecycle():
    artifact = artifact_store.new_artifact("text_input", "hello")
    artifact_store.create_artifact(artifact)
    assert artifact_store.get_artifact(artifact["artifact_id"])["artifact_kind"] == "text_input"
    found = artifact_store.list_artifacts_by_workflow_run_id(None)
    assert artifact in found
    rev = artifact_store.create_artifact_revision(artifact)
    assert rev["artifact_id"] != artifact["artifact_id"]
    linked = artifact_store.link_parent_artifacts(rev["artifact_id"], [artifact["artifact_id"]])
    assert artifact["artifact_id"] in linked["parent_artifact_ids"]
    artifact_store.update_artifact_workflow_run(artifact["artifact_id"], "wr_1")
    assert artifact_store.get_artifact(artifact["artifact_id"])["workflow_run_id"] == "wr_1"
    exported_records = artifact_store.export_artifact_records()
    artifact_store.reset_artifact_store()
    assert artifact_store.list_artifacts() == []
    artifact_store.load_artifact_records(exported_records)
    assert artifact_store.get_artifact(artifact["artifact_id"])["workflow_run_id"] == "wr_1"


def test_load_artifact_records_rejects_invalid_payload():
    with pytest.raises(ValueError):
        artifact_store.load_artifact_records(
            [
                {
                    "artifact_id": "art_invalid",
                    "artifact_kind": "request",
                    "content": None,
                    "content_ref": None,
                    "source": {"origin": "unit_test"},
                    "metadata": {},
                    "created_at": "2025-01-01T00:00:00Z",
                    "parent_artifact_ids": [],
                    "workflow_run_id": None,
                    "issue_ids": [],
                }
            ]
        )


def test_load_artifact_records_rejects_duplicate_artifact_ids():
    duplicate_artifact = {
        "artifact_id": "art_duplicate",
        "artifact_kind": "request",
        "content": "hello",
        "content_ref": None,
        "source": {"origin": "unit_test"},
        "metadata": {},
        "created_at": "2025-01-01T00:00:00Z",
        "parent_artifact_ids": [],
        "workflow_run_id": None,
        "issue_ids": [],
    }
    with pytest.raises(ValueError):
        artifact_store.load_artifact_records([duplicate_artifact, dict(duplicate_artifact)])


def test_invalid_artifact_contract_payload_is_rejected():
    invalid_artifact = {
        "artifact_id": "art_invalid",
        "artifact_kind": "request",
        "content": None,
        "content_ref": None,
        "source": {"origin": "unit_test"},
        "metadata": {},
        "created_at": "2025-01-01T00:00:00Z",
        "parent_artifact_ids": [],
        "workflow_run_id": None,
        "issue_ids": [],
    }
    with pytest.raises(ValueError):
        contracts.validate_artifact_record(invalid_artifact)


def test_issue_tracker_lifecycle():
    issue = {
        "issue_id": "iss_1",
        "issue_type": "defect",
        "title": "Bug",
        "description": "Something is wrong",
        "severity": "high",
        "status": "open",
        "related_artifact_ids": [],
        "related_finding_ids": [],
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
        "reopen_count": 0,
    }
    issue_tracker.create_issue(issue)
    got = issue_tracker.get_issue("iss_1")
    assert got["issue_type"] == "defect"
    issue_tracker.update_issue_status("iss_1", "resolved")
    assert issue_tracker.get_issue("iss_1")["status"] == "resolved"
    issue_tracker.reopen_issue("iss_1")
    assert issue_tracker.get_issue("iss_1")["status"] == "reopened"
    issue_tracker.link_issue_to_artifact("iss_1", "art_abc")
    assert "art_abc" in issue_tracker.get_issue("iss_1")["related_artifact_ids"]
    exported_records = issue_tracker.export_issue_records()
    issue_tracker.reset_issue_store()
    assert issue_tracker.list_issues() == []
    issue_tracker.load_issue_records(exported_records)
    assert issue_tracker.get_issue("iss_1")["status"] == "reopened"


def test_provenance_and_versioning():
    artifact = artifact_store.new_artifact("text_input", "hello")
    artifact_store.create_artifact(artifact)
    provenance.record_artifact_source(artifact["artifact_id"], {"origin": "test"})
    assert provenance.get_artifact_provenance(artifact["artifact_id"])["source"]["origin"] == "test"
    exported_provenance_records = provenance.export_provenance_records()
    provenance.reset_provenance_records()
    assert provenance.get_artifact_provenance(artifact["artifact_id"]) == {
        "artifact_id": artifact["artifact_id"],
        "source": {},
        "parents": [],
    }
    provenance.load_provenance_records(exported_provenance_records)
    assert provenance.get_artifact_provenance(artifact["artifact_id"])["source"]["origin"] == "test"

    versioning.create_version_record(artifact["artifact_id"], 1, None)
    assert versioning.get_version_history(artifact["artifact_id"])[0]["version_number"] == 1
    with pytest.raises(ValueError):
        versioning.create_version_record(artifact["artifact_id"], 1, None)
    other_artifact = artifact_store.new_artifact("text_input", "v2")
    artifact_store.create_artifact(other_artifact)
    versioning.mark_artifact_superseded(artifact["artifact_id"], other_artifact["artifact_id"])
    with pytest.raises(ValueError):
        versioning.mark_artifact_superseded(artifact["artifact_id"], artifact["artifact_id"])
    exported_version_records = versioning.export_version_records()
    versioning.reset_version_records()
    assert versioning.get_version_history(artifact["artifact_id"]) == []
    versioning.load_version_records(exported_version_records)
    assert versioning.get_version_history(artifact["artifact_id"])[0]["version_number"] == 1
    assert versioning.get_superseded_by(artifact["artifact_id"]) == other_artifact["artifact_id"]


def test_dispatch_system_single_and_fix_flow():
    request = {
        "request_id": "req_1",
        "raw_signal": "Hello world",
        "source_metadata": {"origin": "unit_test"},
        "workflow_hint": None,
        "artifact_reference_ids": [],
        "correlation_id": "corr_1",
    }
    result = dispatch_system.dispatch_request(request)
    assert result["workflow_run"]["workflow_mode"] == "single_run"
    assert result["created_issue"] is None
    assert result["request_artifact"]["workflow_run_id"] == result["workflow_run"]["workflow_run_id"]

    fix_request = {**request, "request_id": "req_2", "raw_signal": "There is a bug"}
    result_fix = dispatch_system.dispatch_request(fix_request)
    assert result_fix["workflow_run"]["workflow_mode"] == "fix_flow"
    assert result_fix["created_issue"] is not None
    assert result_fix["request_artifact"]["workflow_run_id"] == result_fix["workflow_run"]["workflow_run_id"]
    assert result_fix["created_issue"]["issue_id"] in result_fix["request_artifact"]["issue_ids"]
    assert artifact_store.list_artifacts_by_issue_id(result_fix["created_issue"]["issue_id"]) == [result_fix["request_artifact"]]
    assert [event_spine.get_event(event_id)["event_type"] for event_id in result_fix["emitted_event_ids"]] == [
        "request_received",
        "artifact_created",
        "workflow_started",
        "workflow_transitioned",
        "issue_created",
    ]


def test_dispatch_request_rejects_unsupported_workflow_hint():
    request = {
        "request_id": "req_unsupported",
        "raw_signal": "Investigate this",
        "source_metadata": {"origin": "unit_test"},
        "workflow_hint": "iterative",
        "artifact_reference_ids": [],
        "correlation_id": "corr_unsupported",
    }
    with pytest.raises(ValueError):
        dispatch_system.dispatch_request(request)


def test_dispatch_text_request_returns_typed_stage1_result():
    result = dispatch_system.dispatch_text_request("Need a fix for this bug")
    assert result["workflow_run"]["workflow_mode"] == "fix_flow"
    assert result["request_artifact"]["workflow_run_id"] == result["workflow_run"]["workflow_run_id"]
    exported_workflow_runs = dispatch_system.export_workflow_runs()
    dispatch_system.reset_workflow_runs()
    assert dispatch_system.export_workflow_runs() == []
    dispatch_system.load_workflow_runs(exported_workflow_runs)
    assert dispatch_system.export_workflow_runs()[0]["workflow_run_id"] == result["workflow_run"]["workflow_run_id"]
