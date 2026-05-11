from dataclasses import dataclass, field
from typing import List


@dataclass
class Transaction:
    kind: str  # "withdraw", "deposit", "transfer", "deposit_check"
    amount: float
    description: str
    pending: bool = False


@dataclass
class Account:
    account_number: str
    owner_name: str
    pin: str
    balance: float
    transactions: List[Transaction] = field(default_factory=list)

    def record(self, kind: str, amount: float, description: str, pending: bool = False) -> None:
        self.transactions.append(Transaction(kind, amount, description, pending))
