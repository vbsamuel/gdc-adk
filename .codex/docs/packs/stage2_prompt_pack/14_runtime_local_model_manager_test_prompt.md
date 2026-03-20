# Tests only: `src/gdc_adk/runtime/local_model_manager.py`

## Required assertions
- `set_active_model` stores active model state
- `get_active_model` returns the stored model
- `clear_active_model` clears the stored state
- repeated set and clear behavior is stable
- invalid model-name lifecycle transition fails explicitly if validation exists
