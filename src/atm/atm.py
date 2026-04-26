from dataclasses import dataclass, field
from typing import Dict, Optional

from .account import Account
from .session import Session


class ATMError(Exception):
    pass


class NotAuthenticatedError(ATMError):
    pass


class InsufficientFundsError(ATMError):
    pass


class InsufficientCashError(ATMError):
    pass


class AccountLockedError(ATMError):
    pass


class AccountNotFoundError(ATMError):
    pass


@dataclass
class ATM:
    cash_available: float
    _accounts: Dict[str, Account] = field(default_factory=dict)
    _session: Optional[Session] = field(default=None, init=False)

    def load_account(self, account: Account) -> None:
        self._accounts[account.account_number] = account

    @property
    def current_session(self) -> Optional[Session]:
        return self._session

    def insert_card(self, account_number: str) -> Session:
        account = self._accounts.get(account_number)
        if account is None:
            raise AccountNotFoundError(f"Account {account_number!r} not found.")
        self._session = Session(account=account)
        return self._session

    def _require_auth(self) -> Session:
        if self._session is None:
            raise NotAuthenticatedError("No active session.")
        if self._session.is_locked:
            raise AccountLockedError("Account is locked after too many failed PIN attempts.")
        if not self._session.is_authenticated:
            raise NotAuthenticatedError("PIN not verified. Please enter your PIN.")
        return self._session

    def enter_pin(self, pin: str) -> bool:
        if self._session is None:
            raise NotAuthenticatedError("No active session.")
        if self._session.is_locked:
            raise AccountLockedError("Account is locked after too many failed PIN attempts.")
        return self._session.enter_pin(pin)

    def check_balance(self) -> float:
        session = self._require_auth()
        return session.account.balance

    def withdraw(self, amount: float) -> float:
        session = self._require_auth()
        if amount <= 0:
            raise ATMError("Withdrawal amount must be positive.")
        if amount > session.account.balance:
            raise InsufficientFundsError(
                f"Requested {amount}, but account balance is {session.account.balance}."
            )
        if amount > self.cash_available:
            raise InsufficientCashError(
                f"Requested {amount}, but ATM only has {self.cash_available} available."
            )
        session.account.balance -= amount
        self.cash_available -= amount
        session.account.record("withdraw", amount, f"Withdrawal of {amount}")
        return session.account.balance

    def end_session(self) -> None:
        self._session = None
