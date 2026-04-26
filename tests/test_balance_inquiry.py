"""
Tests for: openspec/specs/balance-inquiry/spec.md

Each test corresponds to one scenario in that spec.
"""
import pytest

from atm.atm import AccountLockedError, NotAuthenticatedError


# ---------------------------------------------------------------------------
# Scenario: Authenticated user checks their balance
# ---------------------------------------------------------------------------

def test_authenticated_user_checks_their_balance(authenticated_session):
    balance = authenticated_session.check_balance()

    assert balance == 2_500.00


# ---------------------------------------------------------------------------
# Scenario: Balance reflects previous withdrawals
# ---------------------------------------------------------------------------

def test_balance_reflects_previous_withdrawals(authenticated_session):
    authenticated_session.withdraw(200.00)

    balance = authenticated_session.check_balance()

    assert balance == 2_300.00


# ---------------------------------------------------------------------------
# Scenario: Unauthenticated user cannot check balance
# ---------------------------------------------------------------------------

def test_unauthenticated_user_cannot_check_balance(atm):
    atm.insert_card("1001")
    # PIN not entered yet

    with pytest.raises(NotAuthenticatedError):
        atm.check_balance()


# ---------------------------------------------------------------------------
# Scenario: Locked session cannot check balance
# ---------------------------------------------------------------------------

def test_locked_session_cannot_check_balance(atm):
    atm.insert_card("1001")
    atm.enter_pin("wrong")
    atm.enter_pin("wrong")
    atm.enter_pin("wrong")

    with pytest.raises(AccountLockedError):
        atm.check_balance()
