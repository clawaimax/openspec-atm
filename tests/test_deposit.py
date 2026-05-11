"""
Tests for: openspec/changes/add-deposit/specs/deposit/spec.md

Each test corresponds to one scenario in that spec.
"""
import pytest

from atm.atm import ATM, ATMError, NotAuthenticatedError
from atm.account import Account


# ---------------------------------------------------------------------------
# Scenario: Successful cash deposit
# ---------------------------------------------------------------------------

def test_successful_cash_deposit(atm):
    account = Account("1003", "Charlie", "0000", 800.00)
    atm.load_account(account)
    atm.insert_card("1003")
    atm.enter_pin("0000")

    new_balance = atm.deposit_cash(200.00)

    assert new_balance == 1_000.00
    assert atm.cash_available == 10_200.00
    assert account.transactions[-1].kind == "deposit_cash"
    assert account.transactions[-1].amount == 200.00


# ---------------------------------------------------------------------------
# Scenario: Cash deposit of zero or negative amount is rejected
# ---------------------------------------------------------------------------

def test_cash_deposit_of_zero_is_rejected(authenticated_session):
    with pytest.raises(ATMError):
        authenticated_session.deposit_cash(0.00)


def test_cash_deposit_of_negative_amount_is_rejected(authenticated_session):
    with pytest.raises(ATMError):
        authenticated_session.deposit_cash(-100.00)

    session = authenticated_session.current_session
    assert session.account.balance == 2_500.00


# ---------------------------------------------------------------------------
# Scenario: Unauthenticated user cannot deposit cash
# ---------------------------------------------------------------------------

def test_unauthenticated_user_cannot_deposit_cash(atm):
    atm.insert_card("1001")
    # PIN not entered

    with pytest.raises(NotAuthenticatedError):
        atm.deposit_cash(200.00)


# ---------------------------------------------------------------------------
# Scenario: Successful cheque deposit
# ---------------------------------------------------------------------------

def test_successful_cheque_deposit(atm):
    account = Account("1003", "Charlie", "0000", 800.00)
    atm.load_account(account)
    atm.insert_card("1003")
    atm.enter_pin("0000")

    new_balance = atm.deposit_check(500.00)

    assert new_balance == 1_300.00
    assert account.transactions[-1].kind == "deposit_check"
    assert account.transactions[-1].amount == 500.00
    assert account.transactions[-1].pending is True


# ---------------------------------------------------------------------------
# Scenario: Cheque deposit does not increase ATM cash level
# ---------------------------------------------------------------------------

def test_cheque_deposit_does_not_increase_atm_cash_level(authenticated_session):
    cash_before = authenticated_session.cash_available

    authenticated_session.deposit_check(500.00)

    assert authenticated_session.cash_available == cash_before


# ---------------------------------------------------------------------------
# Scenario: Unauthenticated user cannot deposit a cheque
# ---------------------------------------------------------------------------

def test_unauthenticated_user_cannot_deposit_a_cheque(atm):
    atm.insert_card("1001")
    # PIN not entered

    with pytest.raises(NotAuthenticatedError):
        atm.deposit_check(500.00)
