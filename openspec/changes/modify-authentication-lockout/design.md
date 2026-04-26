---
id: modify-authentication-lockout
type: MODIFY
artifact: design
---

# Design: Configurable Lockout Threshold

## ATM Changes

```python
# src/atm/atm.py
@dataclass
class ATM:
    cash_available: float
    max_pin_attempts: int = 3          # new field
    _accounts: Dict[str, Account] = field(default_factory=dict)
    _session: Optional[Session] = field(default=None, init=False)

    def insert_card(self, account_number: str) -> Session:
        account = self._accounts.get(account_number)
        if account is None:
            raise AccountNotFoundError(...)
        self._session = Session(account=account, max_attempts=self.max_pin_attempts)
        return self._session
```

## Session Changes

```python
# src/atm/session.py
@dataclass
class Session:
    account: Account
    max_attempts: int = 3              # was module-level constant MAX_PIN_ATTEMPTS
    _attempts: int = field(default=0, init=False)
    ...

    def enter_pin(self, pin: str) -> bool:
        ...
        self._attempts += 1
        if self._attempts >= self.max_attempts:   # was MAX_PIN_ATTEMPTS
            self._locked = True
        return False
```

## Backward Compatibility

Default value of `max_pin_attempts=3` preserves existing behaviour; no breaking change
to callers that do not pass the parameter.

## Test Coverage

Add `test_account_locked_after_custom_attempt_limit` that creates `ATM(cash_available=...,
max_pin_attempts=5)` and verifies lockout fires after 5 failures, not 3.
