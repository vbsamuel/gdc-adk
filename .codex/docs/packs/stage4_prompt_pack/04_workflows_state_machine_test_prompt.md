# Tests only: `src/gdc_adk/workflows/state_machine.py`

## Required assertions
- each workflow mode has explicit allowed transitions
- invalid transitions reject explicitly
- valid transitions succeed
- direct `received -> completed` rejects for non-trivial paths
- fix-flow extended states are supported
- reopen transitions are supported where legal
- terminal-state detection is correct
- transition results remain serializable
