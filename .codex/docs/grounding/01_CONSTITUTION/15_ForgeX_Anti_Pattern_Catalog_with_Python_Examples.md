# Forge-X Anti-Pattern Catalog with Python Examples

## Purpose

This document shows what NOT to do in the repo. These are not style nits. These are recurring engineering failures that cause drift, misplacement of logic, or future rewrite pain.

## 1. Adapter-owned business logic

### Anti-pattern
```python
# labs/adk/weather_time_agent/agent.py
from google.adk.agents import Agent

def get_weather(city: str) -> dict:
    # hidden domain logic in adapter
    ...
```

### Why it is wrong
- logic is trapped in an adapter surface
- core system cannot reuse it
- class framework becomes architecture

### Correct pattern
```python
# labs/adk/weather_time_agent/agent.py
from gdc_adk.adapters.adk.weather_time_agent_adapter import build_weather_time_agent

root_agent = build_weather_time_agent()
```

---

## 2. Provider-owned routing logic

### Anti-pattern
```python
class GoogleProvider:
    def generate(self, req):
        if "weather" in req.prompt:
            return call_weather_tool(...)
```

### Why it is wrong
- providers must not choose task semantics
- routing belongs to control_plane

### Correct pattern
```python
selected_provider = select_provider(task_type="research_local")
response = execute_task(task_type="research_local", req=request)
```

---

## 3. Hardcoded cloud-first defaults

### Anti-pattern
```python
DEFAULT_PROVIDER = "google"
```

### Why it is wrong
- violates local-first
- bypasses config and policy

### Correct pattern
```python
def get_default_provider() -> str:
    config = load_yaml_config()
    return str(config.get("routing", {}).get("default_provider", "")).strip()
```

---

## 4. Generic variable soup

### Anti-pattern
```python
def process(data):
    obj = make(data)
    result = handle(obj)
    return result
```

### Why it is wrong
- no semantic traceability
- impossible to audit

### Correct pattern
```python
def process_input_signal(raw_signal: dict) -> dict:
    normalized_signal = normalize_signal(raw_signal)
    activation_result = activate_workflow_from_signal(normalized_signal)
    return activation_result
```

---

## 5. Hidden state in prompt text

### Anti-pattern
```python
prompt = f"Remember previous issue and continue from there: {user_text}"
```

### Why it is wrong
- state is trapped in chat text
- not replayable
- not auditable

### Correct pattern
```python
workflow_snapshot = load_continuity_snapshot(workflow_run_id)
context_blocks = get_context_blocks_for_workflow(workflow_run_id)
```

---

## 6. Fake “placeholder” grounding docs treated as real controls

### Anti-pattern
```text
# Architecture
Substrate, Control Plane, Memory.
```

### Why it is wrong
- sounds structured
- constrains nothing
- produces false confidence

### Correct pattern
Write ownership, contracts, import direction, forbidden responsibilities, and acceptance conditions.

---

## 7. `helpers.py` dumping ground

### Anti-pattern
```python
# helpers.py
def format_time(...): ...
def create_issue(...): ...
def route_provider(...): ...
def parse_pdf(...): ...
```

### Why it is wrong
- destroys ownership boundaries
- accumulates accidental architecture

### Correct pattern
Put each function in the owning subsystem module.

---

## 8. Review as prose only

### Anti-pattern
```python
return {"text": "This looks okay but may need more validation"}
```

### Why it is wrong
- no finding object
- cannot reopen or track

### Correct pattern
```python
finding = create_review_finding(
    finding_type="grounding_gap",
    severity="medium",
    description="Claim lacks source linkage",
    related_artifact_ids=[artifact_id],
)
```

---

## 9. Overwriting artifacts with no lineage

### Anti-pattern
```python
artifact_store[artifact_id] = revised_content
```

### Why it is wrong
- destroys replay and diffability

### Correct pattern
```python
revised_artifact = create_artifact(
    artifact_kind="revised_spec",
    content=revised_content,
    parent_artifact_ids=[prior_artifact_id],
)
```

---

## 10. Unbounded multi-agent loops

### Anti-pattern
```python
while True:
    planner_result = planner(...)
    reviewer_result = reviewer(planner_result)
```

### Why it is wrong
- no stop condition
- no role contract
- no artifact handoff

### Correct pattern
Use explicit workflow state, max retries, and typed handoff artifacts.
