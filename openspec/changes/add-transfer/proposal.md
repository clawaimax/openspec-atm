---
id: add-transfer
type: ADD
status: proposed
target_spec: openspec/specs/transfer/spec.md
---

# Proposal: Add Fund Transfer Between Accounts

## Summary

Allow an authenticated user to transfer funds from their own account to another account
held at the same ATM system. This adds a new `transfer` spec and a new `ATM.transfer()`
method.

## Motivation

Users currently have no way to move money between accounts without withdrawing and
re-depositing manually. A transfer operation is a core banking feature and completes
the basic money-movement story (withdraw → deposit → transfer).

## Scope

| Area | Change |
|------|--------|
| New spec | `openspec/specs/transfer/spec.md` (see delta spec in this change) |
| ATM domain | Add `ATM.transfer(amount, destination_account_number)` method |
| Tests | New test file `tests/test_transfer.py` |

## Out of Scope

- Transfers to external banks or routing numbers.
- Scheduled / recurring transfers.
- Transfer fees.

## Acceptance Criteria

- Authenticated user can transfer a positive amount to a valid destination account.
- Source account balance decreases; destination account balance increases.
- Transfer fails if source has insufficient funds.
- Transfer fails if destination account does not exist.
- Zero or negative amounts are rejected.
- Unauthenticated / locked sessions cannot transfer.
