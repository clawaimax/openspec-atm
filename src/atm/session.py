from dataclasses import dataclass, field
from typing import Optional

from .account import Account

MAX_PIN_ATTEMPTS = 3


@dataclass
class Session:
    account: Account
    _attempts: int = field(default=0, init=False)
    _authenticated: bool = field(default=False, init=False)
    _locked: bool = field(default=False, init=False)

    @property
    def is_authenticated(self) -> bool:
        return self._authenticated

    @property
    def is_locked(self) -> bool:
        return self._locked

    @property
    def failed_attempts(self) -> int:
        return self._attempts

    def enter_pin(self, pin: str) -> bool:
        if self._locked:
            return False
        if pin == self.account.pin:
            self._authenticated = True
            return True
        self._attempts += 1
        if self._attempts >= MAX_PIN_ATTEMPTS:
            self._locked = True
        return False
