# Proposal: Add Deposit Functionality

## Intent
Users currently have no way to add funds at the ATM without visiting a teller.
Adding deposit capability — both cash and cheque — rounds out the core money-movement
story alongside withdrawal and (future) transfer.

## Scope
In scope:
- Cash deposit: `ATM.deposit_cash(amount)` — account balance and ATM cash level increase
- Cheque deposit: `ATM.deposit_check(amount)` — account balance updated with pending-hold flag
- New spec `openspec/specs/deposit/spec.md` with two requirements (Deposit Cash, Deposit Check)
- New test file `tests/test_deposit.py`

Out of scope:
- Envelope-based deposit validation (requires hardware integration)
- Partial hold period release logic
- Transfers counted as deposit-type transactions

## Approach
Mirror the withdrawal pattern: authenticate via `_require_auth()`, validate the amount,
update balances, record the transaction. Two separate methods keep the side effects explicit
and the domain model self-documenting. Cheque deposits add a pending-hold flag to the
transaction record to represent clearance lag; they do not increase ATM cash level.
