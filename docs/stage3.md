# Stage 3 implementation

- Added encryption-at-rest service for code storage (Fernet).
- Implemented inventory code creation/list/reveal with masking + audit events.
- Implemented order create/reserve/fulfill with real DB state transitions.
- Added reservation linkage `code_items.current_order_id` and Stage 3 migration.
- Added stage3 tests (encryption roundtrip, reserve->fulfill flow).
