# Design: Configurable Lockout Threshold

## Technical Approach
Replace the module-level `MAX_PIN_ATTEMPTS = 3` constant with instance fields on both
`ATM` and `Session`. `ATM` accepts the threshold at construction and passes it to each
new `Session` in `insert_card()`, keeping `Session` as an internal detail that never
reads from global state.

## Architecture Decisions

### Decision: Instance Field Over Module Constant
Storing the threshold on `ATM` and `Session` instances because:
- Enables per-machine configuration without code changes
- Avoids global mutable state
- Default of `3` preserves all existing callers with no breaking change

### Decision: ATM Owns the Configuration
`ATM` receives `max_pin_attempts` and forwards it to `Session`, rather than `Session`
reading from an external config, because `ATM` is the public API boundary and `Session`
is an internal implementation detail.

## Data Flow
```
ATM(cash_available=..., max_pin_attempts=5) constructed
 │
 ▼
insert_card() creates Session(account=..., max_attempts=5)
 │
 ▼
enter_pin() increments _attempts, compares to max_attempts
 │
 ▼
Lockout fires after N failures  (N = configured threshold)
```

## File Changes
- `src/atm/atm.py` — add `max_pin_attempts: int = 3` field; pass to `Session` in `insert_card()`
- `src/atm/session.py` — replace `MAX_PIN_ATTEMPTS` constant with `max_attempts: int = 3` instance field
- `tests/test_authentication.py` — add custom threshold scenario test
