"""
Tests for: openspec/specs/authentication/spec.md

Each test corresponds to one scenario in that spec. The test function name
mirrors the scenario title so the mapping is immediately visible.
"""
import pytest

from atm.atm import (
    ATM,
    AccountLockedError,
    AccountNotFoundError,
    NotAuthenticatedError,
)


# ---------------------------------------------------------------------------
# Scenario: Successful authentication with correct PIN
# ---------------------------------------------------------------------------

def test_successful_authentication_with_correct_pin(atm):
    session = atm.insert_card("1001")
    result = atm.enter_pin("1234")

    assert result is True
    assert session.is_authenticated is True


# ---------------------------------------------------------------------------
# Scenario: Incorrect PIN is rejected
# ---------------------------------------------------------------------------

def test_incorrect_pin_is_rejected(atm):
    session = atm.insert_card("1001")
    result = atm.enter_pin("0000")

    assert result is False
    assert session.is_authenticated is False
    assert session.failed_attempts == 1


# ---------------------------------------------------------------------------
# Scenario: Account locked after three consecutive failed PIN attempts
# ---------------------------------------------------------------------------

def test_account_locked_after_three_consecutive_failed_pin_attempts(atm):
    session = atm.insert_card("1001")

    atm.enter_pin("wrong")
    atm.enter_pin("wrong")
    atm.enter_pin("wrong")

    assert session.is_locked is True
    assert session.is_authenticated is False


# ---------------------------------------------------------------------------
# Scenario: Locked account rejects a correct PIN
# ---------------------------------------------------------------------------

def test_locked_account_rejects_a_correct_pin(atm):
    atm.insert_card("1001")
    atm.enter_pin("wrong")
    atm.enter_pin("wrong")
    atm.enter_pin("wrong")

    with pytest.raises(AccountLockedError):
        atm.enter_pin("1234")


# ---------------------------------------------------------------------------
# Scenario: Card not found
# ---------------------------------------------------------------------------

def test_card_not_found(atm):
    with pytest.raises(AccountNotFoundError):
        atm.insert_card("9999")

    assert atm.current_session is None


# ---------------------------------------------------------------------------
# Scenario: Services unavailable without a session
# ---------------------------------------------------------------------------

def test_no_session_raises_not_authenticated_on_service_access(atm):
    with pytest.raises(NotAuthenticatedError):
        atm.check_balance()


# ---------------------------------------------------------------------------
# Scenario: ATM services unavailable after lock (checking balance while locked)
# ---------------------------------------------------------------------------

def test_atm_services_unavailable_after_account_lock(atm):
    atm.insert_card("1001")
    atm.enter_pin("wrong")
    atm.enter_pin("wrong")
    atm.enter_pin("wrong")

    with pytest.raises(AccountLockedError):
        atm.check_balance()
