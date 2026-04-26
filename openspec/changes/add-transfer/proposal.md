# Proposal: Add Fund Transfer Between Accounts

## Intent
Users have no way to move money between accounts without withdrawing cash and
re-depositing manually. A transfer operation completes the core money-movement story
(withdraw → deposit → transfer) and is a standard ATM capability.

## Scope
In scope:
- Account-to-account transfer within the same ATM system
- New `ATM.transfer(amount, destination_account_number)` method
- New spec `openspec/specs/transfer/spec.md`
- New test file `tests/test_transfer.py`

Out of scope:
- Transfers to external banks or routing numbers
- Scheduled or recurring transfers
- Transfer fees

## Approach
Authenticate via `_require_auth()`, look up the destination account in `self._accounts`,
then mutate both balances atomically. Raise `InsufficientFundsError` if source funds are
insufficient, `AccountNotFoundError` if the destination account does not exist, or
`ATMError` for invalid amounts. No partial state — both balance mutations happen together.
