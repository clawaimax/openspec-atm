"""
Tests for: openspec/specs/transfer/spec.md

Each test corresponds to one scenario in that spec.
"""
import pytest

from atm.atm import (
    ATM,
    ATMError,
    AccountNotFoundError,
    InsufficientFundsError,
    NotAuthenticatedError,
)
from atm.account import Account


# ---------------------------------------------------------------------------
# Scenario: Successful fund transfer
# ---------------------------------------------------------------------------

def test_successful_fund_transfer(authenticated_session):
    new_balance = authenticated_session.transfer(300.00, "1002")

    assert new_balance == 2_200.00

    session = authenticated_session.current_session
    bob = authenticated_session._accounts["1002"]
    assert bob.balance == 1_100.00

    assert session.account.transactions[-1].kind == "transfer-out"
    assert session.account.transactions[-1].amount == 300.00
    assert bob.transactions[-1].kind == "transfer-in"
    assert bob.transactions[-1].amount == 300.00


# ---------------------------------------------------------------------------
# Scenario: Transfer refused due to insufficient source funds
# ---------------------------------------------------------------------------

def test_transfer_refused_due_to_insufficient_source_funds(atm):
    account = Account("1003", "Charlie Low", "0000", 100.00)
    atm.load_account(account)
    atm.insert_card("1003")
    atm.enter_pin("0000")

    with pytest.raises(InsufficientFundsError):
        atm.transfer(300.00, "1002")

    assert account.balance == 100.00
    assert atm._accounts["1002"].balance == 800.00


# ---------------------------------------------------------------------------
# Scenario: Transfer to a non-existent account is rejected
# ---------------------------------------------------------------------------

def test_transfer_to_a_non_existent_account_is_rejected(authenticated_session):
    with pytest.raises(AccountNotFoundError):
        authenticated_session.transfer(100.00, "9999")

    session = authenticated_session.current_session
    assert session.account.balance == 2_500.00


# ---------------------------------------------------------------------------
# Scenario: Transfer of zero or negative amount is rejected
# ---------------------------------------------------------------------------

def test_transfer_of_zero_is_rejected(authenticated_session):
    with pytest.raises(ATMError):
        authenticated_session.transfer(0.00, "1002")


def test_transfer_of_negative_amount_is_rejected(authenticated_session):
    with pytest.raises(ATMError):
        authenticated_session.transfer(-50.00, "1002")


# ---------------------------------------------------------------------------
# Scenario: Unauthenticated user cannot transfer
# ---------------------------------------------------------------------------

def test_unauthenticated_user_cannot_transfer(atm):
    atm.insert_card("1001")
    # PIN not entered

    with pytest.raises(NotAuthenticatedError):
        atm.transfer(100.00, "1002")
