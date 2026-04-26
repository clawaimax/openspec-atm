---
id: modify-authentication-lockout
type: MODIFY
artifact: tasks
---

# Tasks: Configurable Lockout Threshold

## Implementation Tasks

- [ ] Add `max_pin_attempts: int = 3` field to `ATM` dataclass (`src/atm/atm.py`)
- [ ] Pass `max_attempts=self.max_pin_attempts` to `Session(...)` in `ATM.insert_card()`
- [ ] Replace module-level `MAX_PIN_ATTEMPTS` constant in `session.py` with
      `max_attempts: int = 3` instance field on `Session`
- [ ] Update `Session.enter_pin()` to use `self.max_attempts` instead of the constant

## Testing Tasks

- [ ] Add `test_account_locked_after_custom_attempt_limit` to `tests/test_authentication.py`
- [ ] Confirm existing lockout tests still pass (default remains 3)

## Spec Promotion

- [ ] Merge delta spec language into `openspec/specs/authentication/spec.md`
- [ ] Bump spec version to `1.1.0`
- [ ] Archive or remove `openspec/changes/modify-authentication-lockout/`
