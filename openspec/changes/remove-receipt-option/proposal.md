---
id: remove-receipt-option
type: REMOVE
status: proposed
target_spec: openspec/specs/balance-inquiry/spec.md
---

# Proposal: Remove Receipt Option from Balance Inquiry

## Summary

Remove the receipt acknowledgement behaviour from the **Balance Inquiry** spec. The
receipt option was added in an earlier iteration but is unused in the terminal-based
demo and adds noise to the spec without corresponding implementation.

## Motivation

- The terminal app has no printer; the receipt concept is a placeholder.
- Downstream implementers are confused by a scenario with no corresponding code path.
- Removing it keeps the spec accurate and implementation-true.

## What Is Removed

| Item | Location |
|------|----------|
| Receipt acknowledgement mention in the Overview | `openspec/specs/balance-inquiry/spec.md` — Overview paragraph |
| Any "receipt" scenario or reference | Same file |

## What Stays

All other Balance Inquiry scenarios remain in `v1.1.0` of the spec:
- Authenticated user checks their balance
- Balance reflects previous withdrawals
- Unauthenticated user cannot check balance
- Locked session cannot check balance

## Acceptance Criteria

- The word "receipt" no longer appears in `openspec/specs/balance-inquiry/spec.md`.
- No tests reference a receipt-related code path (none exist — nothing to delete).
- The spec version bumps to `1.1.0`.
