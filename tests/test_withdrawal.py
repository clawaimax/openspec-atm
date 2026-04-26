"""
Tests for: openspec/specs/withdrawal/spec.md

Each test corresponds to one scenario in that spec.
"""
import pytest

from atm.atm import (
    ATM,
    ATMError,
    InsufficientCashError,
    InsufficientFundsError,
    NotAuthenticatedError,
)
from atm.account import Account


# ---------------------------------------------------------------------------
# Scenario: Successful cash withdrawal
# ---------------------------------------------------------------------------

def test_successful_cash_withdrawal(authenticated_session):
    new_balance = authenticated_session.withdraw(500.00)

    assert new_balance == 2_000.00
    assert authenticated_session.cash_available == 9_500.00


def test_successful_withdrawal_records_transaction(authenticated_session):
    authenticated_session.withdraw(500.00)

    session = authenticated_session.current_session
    assert len(session.account.transactions) == 1
    assert session.account.transactions[0].kind == "withdraw"
    assert session.account.transactions[0].amount == 500.00


# ---------------------------------------------------------------------------
# Scenario: Withdrawal refused due to insufficient account funds
# ---------------------------------------------------------------------------

def test_withdrawal_refused_due_to_insufficient_account_funds(authenticated_session):
    # Alice has $2,500; try to withdraw more
    with pytest.raises(InsufficientFundsError):
        authenticated_session.withdraw(3_000.00)

    assert authenticated_session.check_balance() == 2_500.00
    assert authenticated_session.cash_available == 10_000.00


# ---------------------------------------------------------------------------
# Scenario: Withdrawal refused due to insufficient ATM cash
# ---------------------------------------------------------------------------

def test_withdrawal_refused_due_to_insufficient_atm_cash():
    low_cash_atm = ATM(cash_available=100.00)
    account = Account("1001", "Alice Smith", "1234", 2_500.00)
    low_cash_atm.load_account(account)
    low_cash_atm.insert_card("1001")
    low_cash_atm.enter_pin("1234")

    with pytest.raises(InsufficientCashError):
        low_cash_atm.withdraw(500.00)

    assert account.balance == 2_500.00
    assert low_cash_atm.cash_available == 100.00


# ---------------------------------------------------------------------------
# Scenario: Withdrawal of zero or negative amount is rejected
# ---------------------------------------------------------------------------

def test_withdrawal_of_zero_is_rejected(authenticated_session):
    with pytest.raises(ATMError):
        authenticated_session.withdraw(0.00)


def test_withdrawal_of_negative_amount_is_rejected(authenticated_session):
    with pytest.raises(ATMError):
        authenticated_session.withdraw(-50.00)


# ---------------------------------------------------------------------------
# Scenario: Unauthenticated user cannot withdraw
# ---------------------------------------------------------------------------

def test_unauthenticated_user_cannot_withdraw(atm):
    atm.insert_card("1001")
    # PIN not entered

    with pytest.raises(NotAuthenticatedError):
        atm.withdraw(100.00)
