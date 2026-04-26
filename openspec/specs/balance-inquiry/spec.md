# Balance Inquiry Specification

## Purpose
Account balance display for authenticated ATM users.

## Requirements

### Requirement: Balance Display
The system SHALL display the current account balance to authenticated users.

#### Scenario: Authenticated user checks their balance
- GIVEN the user is authenticated with account `1001` having a balance of `$2,500.00`
- WHEN the user requests a balance inquiry
- THEN the ATM displays `$2,500.00`

#### Scenario: Balance reflects previous withdrawals
- GIVEN the user is authenticated with account `1001` having a balance of `$2,500.00`
- AND the user has previously withdrawn `$200.00` in the same session
- WHEN the user requests a balance inquiry
- THEN the ATM displays `$2,300.00`

### Requirement: Access Control
The system SHALL reject balance inquiries from unauthenticated or locked sessions.

#### Scenario: Unauthenticated user cannot check balance
- GIVEN the user has inserted their card but has not yet entered their PIN
- WHEN the user attempts a balance inquiry
- THEN the system rejects the request
- AND prompts the user to authenticate first

#### Scenario: Locked session cannot check balance
- GIVEN the user's account has been locked due to three failed PIN attempts
- WHEN the user attempts a balance inquiry
- THEN the system rejects the request
- AND reports that the account is locked
