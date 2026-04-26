"""
Shared pytest fixtures for the ATM OpenSpec demo.

Each fixture reflects the pre-conditions described in the OpenSpec scenarios.
"""
import pytest

from atm.account import Account
from atm.atm import ATM


@pytest.fixture
def alice_account() -> Account:
    return Account("1001", "Alice Smith", "1234", 2_500.00)


@pytest.fixture
def bob_account() -> Account:
    return Account("1002", "Bob Jones", "5678", 800.00)


@pytest.fixture
def atm(alice_account, bob_account) -> ATM:
    machine = ATM(cash_available=10_000.00)
    machine.load_account(alice_account)
    machine.load_account(bob_account)
    return machine


@pytest.fixture
def authenticated_session(atm) -> ATM:
    """ATM with Alice's card inserted and PIN already verified."""
    atm.insert_card("1001")
    atm.enter_pin("1234")
    return atm
