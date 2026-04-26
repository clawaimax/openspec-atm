# Proposal: Configurable Authentication Lockout Threshold

## Intent
Security teams need different ATMs (e.g., high-traffic public kiosks vs. branch vestibule
machines) to enforce different lockout policies without code changes. The current hard-coded
constant (`MAX_PIN_ATTEMPTS = 3` in `session.py`) cannot be overridden at deployment time.

## Scope
In scope:
- `ATM` dataclass accepts `max_pin_attempts: int = 3` at construction
- `Session` receives the threshold value instead of reading the module constant
- Authentication spec updated to say "configured threshold" instead of "three"
- New test scenario verifying a non-default threshold is respected

Out of scope:
- Persistent lockout across sessions (still session-scoped)
- Admin UI or runtime config changes after ATM startup

## Approach
Add `max_pin_attempts: int = 3` to the `ATM` dataclass. Pass it to each new `Session`
via `insert_card()`. Replace the `MAX_PIN_ATTEMPTS` module constant with an instance
field on `Session`. Default of `3` preserves existing behaviour with no breaking change.
