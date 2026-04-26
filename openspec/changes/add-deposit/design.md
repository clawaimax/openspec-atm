# Design: Deposit Functionality

## Technical Approach
Deposit is the mirror image of withdrawal. Both `deposit_cash()` and `deposit_check()`
reuse the same authentication guard (`_require_auth()`) and transaction recording pattern
established for `ATM.withdraw()`. Cash deposits increase both account balance and ATM cash
level. Cheque deposits update the account balance and create a transaction with a
pending-hold flag representing clearance lag; they do not add physical cash to the machine.

## Architecture Decisions

### Decision: Mirror Withdrawal Pattern
Reusing `_require_auth()` and `Account.record()` because deposit preconditions are
identical to withdrawal (authenticated session, positive amount), and consistent error
handling reduces surface area.

### Decision: Separate Cash and Cheque Methods
Using `deposit_cash()` and `deposit_check()` instead of a single `deposit(type, amount)`
because their side effects differ (cash level vs. hold state) and explicit method names
make the domain model self-documenting without a type-switch inside one method.

## Data Flow
```
User calls deposit_cash(amount) or deposit_check(amount)
 │
 ▼
_require_auth() — raises NotAuthenticatedError or AccountLockedError if invalid
 │
 ▼
Validate amount > 0 — raises ATMError if not
 │
 ▼
Update Account.balance
Update ATM.cash_available  (cash only — cheque does not add physical cash)
Append Transaction record  (cheque record includes pending-hold flag)
 │
 ▼
Return new balance
```

## Error Cases

| Condition | Exception |
|-----------|-----------|
| Not authenticated | `NotAuthenticatedError` |
| Account locked | `AccountLockedError` |
| Amount ≤ 0 | `ATMError` |

## File Changes
- `src/atm/atm.py` — add `deposit_cash()` and `deposit_check()` methods
- `tests/test_deposit.py` — new file, one test per scenario in the delta spec
