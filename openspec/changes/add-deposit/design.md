---
id: add-deposit
type: ADD
artifact: design
---

# Design: Deposit Functionality

## Approach

Deposit is the mirror image of withdrawal. It re-uses the same authentication guard
(`_require_auth`) and transaction recording pattern already established for withdrawal.

## Interface

```python
# src/atm/atm.py
def deposit(self, amount: float) -> float:
    """
    Deposit cash into the current session's account.

    Returns the new account balance.
    Raises ATMError for non-positive amounts.
    Raises NotAuthenticatedError / AccountLockedError if session is invalid.
    """
    session = self._require_auth()
    if amount <= 0:
        raise ATMError("Deposit amount must be positive.")
    session.account.balance += amount
    self.cash_available += amount
    session.account.record("deposit", amount, f"Deposit of {amount}")
    return session.account.balance
```

## Error Cases

| Condition | Exception |
|-----------|-----------|
| Not authenticated | `NotAuthenticatedError` |
| Account locked | `AccountLockedError` |
| Amount ≤ 0 | `ATMError` |

## Data Impact

- `Account.balance` increases.
- `ATM.cash_available` increases (models physical cash added to the machine).
- `Account.transactions` gains a new `"deposit"` record.

## Testing Strategy

Mirror the withdrawal test structure in `tests/test_deposit.py`. Each scenario in
`openspec/changes/add-deposit/specs/deposit/spec.md` maps to one test function.
