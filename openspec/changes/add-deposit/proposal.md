---
id: add-deposit
type: ADD
status: proposed
target_spec: openspec/specs/deposit/spec.md
---

# Proposal: Add Deposit Functionality

## Summary

Introduce a new **Deposit** capability that allows an authenticated user to deposit
physical cash into their account at the ATM. This adds a new spec and a new method
to the ATM domain model.

## Motivation

Users currently have no way to add funds without visiting a teller. An in-machine deposit
slot is a standard ATM feature and rounds out the core money-movement capabilities alongside
withdrawal and (future) transfer.

## Scope

| Area | Change |
|------|--------|
| New spec | `openspec/specs/deposit/spec.md` (see `specs/deposit/spec.md` in this change) |
| ATM domain | Add `ATM.deposit(amount)` method |
| Session | No change — authentication precondition is the same |
| Tests | New test file `tests/test_deposit.py` |

## Out of Scope

- Envelope-based deposit validation (requires hardware integration).
- Cheque deposits.
- Partial hold periods.

## Acceptance Criteria

- Authenticated users can deposit a positive amount.
- The account balance increases by the deposited amount.
- The ATM cash level increases by the deposited amount.
- A transaction record is created.
- Unauthenticated or locked sessions cannot deposit.
- Zero or negative deposit amounts are rejected.
