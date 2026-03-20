# Tests only: `src/gdc_adk/memory/contracts.py`

## Required assertions
- `MemoryStore` defines the required public methods
- `ContextStore` defines the required public methods
- `ContinuityStore` defines the required public methods
- interface method outputs can be represented as serializable structures
- interfaces do not require opaque runtime-only objects
- interface surface is backend-agnostic by design
- missing required methods fail contract expectations explicitly
