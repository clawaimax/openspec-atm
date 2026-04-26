# Cash Withdrawal Specification

## Purpose
Cash dispensing with balance and ATM cash level validation for authenticated users.

## Requirements

### Requirement: Cash Withdrawal
The system SHALL allow authenticated users to withdraw cash, subject to account balance
and ATM cash availability checks.

#### Scenario: Successful cash withdrawal
- GIVEN the user is authenticated with account `1001` having a balance of `$2,500.00`
- AND the ATM has `$10,000.00` cash available
- WHEN the user requests a withdrawal of `$500.00`
- THEN the ATM dispenses `$500.00`
- AND the account balance is updated to `$2,000.00`
- AND the ATM cash level is reduced to `$9,500.00`
- AND a withdrawal transaction record is created

#### Scenario: Withdrawal refused due to insufficient account funds
- GIVEN the user is authenticated with account `1001` having a balance of `$200.00`
- AND the ATM has sufficient cash
- WHEN the user requests a withdrawal of `$500.00`
- THEN the withdrawal is refused
- AND the account balance remains `$200.00`
- AND the ATM cash level is unchanged
- AND the system reports "insufficient funds"

#### Scenario: Withdrawal refused due to insufficient ATM cash
- GIVEN the user is authenticated with account `1001` having a balance of `$2,500.00`
- AND the ATM has only `$100.00` cash available
- WHEN the user requests a withdrawal of `$500.00`
- THEN the withdrawal is refused
- AND the account balance remains `$2,500.00`
- AND the ATM cash level remains `$100.00`
- AND the system reports "insufficient ATM cash"

#### Scenario: Withdrawal of zero or negative amount is rejected
- GIVEN the user is authenticated
- WHEN the user requests a withdrawal of `$0.00` or a negative amount
- THEN the withdrawal is rejected immediately
- AND the system reports that the amount must be positive

### Requirement: Withdrawal Access Control
The system SHALL reject withdrawal attempts from unauthenticated sessions.

#### Scenario: Unauthenticated user cannot withdraw
- GIVEN the user has inserted their card but has not entered their PIN
- WHEN the user attempts a withdrawal
- THEN the system rejects the request
- AND prompts the user to authenticate first
