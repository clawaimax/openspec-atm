---
id: modify-authentication-lockout
type: MODIFY
status: proposed
target_spec: openspec/specs/authentication/spec.md
---

# Proposal: Modify Authentication — Configurable Lockout Threshold

## Summary

Change the account lockout threshold from a hard-coded constant of **3** failed PIN
attempts to a **configurable value** that can be set per-ATM at startup. This is a
MODIFY to the existing `authentication` spec.

## Motivation

Security teams require different ATMs (e.g., high-traffic public kiosks vs. branch
vestibule machines) to enforce different lockout policies without code changes. The
current constant (`MAX_PIN_ATTEMPTS = 3` in `session.py`) cannot be overridden without
modifying source code.

## What Changes

| Aspect | Before | After |
|--------|--------|-------|
| Lockout threshold | Hard-coded `3` | Configurable per ATM instance (default `3`) |
| `ATM.__init__` | No lockout parameter | Accepts `max_pin_attempts: int = 3` |
| `Session.__init__` | Uses module constant | Receives `max_attempts` from ATM |
| Spec scenarios | Assume exactly 3 attempts | Updated to say "configured number of attempts" |

## Scope

- `openspec/specs/authentication/spec.md` — update language (see delta spec)
- `src/atm/session.py` — accept `max_attempts` parameter
- `src/atm/atm.py` — pass configurable value to Session on `insert_card()`
- `tests/test_authentication.py` — add scenario for non-default threshold

## Out of Scope

- Persistent lockout across sessions (still session-scoped).
- Admin UI to change the threshold at runtime.
