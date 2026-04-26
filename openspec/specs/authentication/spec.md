# Authentication Specification

## Purpose
PIN-based user authentication and session lockout for the ATM.

## Requirements

### Requirement: User Authentication
The system SHALL authenticate a user by validating their PIN after card insertion.

#### Scenario: Successful authentication with correct PIN
- GIVEN a registered account with account number `1001` and PIN `1234`
- WHEN the user inserts their card and enters PIN `1234`
- THEN the session is authenticated
- AND the user is granted access to ATM services

#### Scenario: Incorrect PIN is rejected
- GIVEN a registered account with account number `1001` and PIN `1234`
- AND the user has inserted their card
- WHEN the user enters an incorrect PIN
- THEN authentication is denied
- AND the failed-attempt counter increments by 1
- AND the session remains unauthenticated

#### Scenario: Card not found
- GIVEN no account exists with account number `9999`
- WHEN the user tries to insert a card with account number `9999`
- THEN the system reports that the account was not found
- AND no session is started

#### Scenario: Services unavailable without a session
- GIVEN no card has been inserted
- WHEN the user attempts to access ATM services
- THEN the system rejects the request

### Requirement: Account Lockout
The system SHALL lock the account after three consecutive failed PIN attempts in a single session.

#### Scenario: Account locked after three consecutive failed PIN attempts
- GIVEN a registered account with account number `1001`
- AND the user has inserted their card
- WHEN the user enters an incorrect PIN three times in a row
- THEN the account is locked for this session
- AND further PIN attempts are rejected regardless of correctness
- AND ATM services are unavailable until a new session is started

#### Scenario: Locked account rejects a correct PIN
- GIVEN a registered account that has been locked due to three failed PIN attempts
- WHEN the user attempts to enter the correct PIN
- THEN authentication is still denied
- AND the system reports that the account is locked

#### Scenario: ATM services unavailable after account lock
- GIVEN the account has been locked due to three failed PIN attempts
- WHEN the user attempts to check balance or withdraw
- THEN the system rejects the request
- AND reports the account is locked
