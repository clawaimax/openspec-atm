# Delta for Deposit

## ADDED Requirements

### Requirement: Deposit Cash
The system SHALL allow authenticated users to deposit physical cash into their account.

#### Scenario: Successful cash deposit
- GIVEN the user is authenticated with account `1001` having a balance of `$800.00`
- AND the ATM has `$10,000.00` cash available
- WHEN the user deposits `$200.00` in cash
- THEN the account balance is updated to `$1,000.00`
- AND the ATM cash level increases to `$10,200.00`
- AND a cash deposit transaction record is created

#### Scenario: Cash deposit of zero or negative amount is rejected
- GIVEN the user is authenticated
- WHEN the user attempts to deposit `$0.00` or a negative amount in cash
- THEN the deposit is rejected
- AND the system reports that the amount must be positive
- AND the balance is unchanged

#### Scenario: Unauthenticated user cannot deposit cash
- GIVEN the user has inserted their card but has not entered their PIN
- WHEN the user attempts a cash deposit
- THEN the system rejects the request
- AND prompts the user to authenticate first

### Requirement: Deposit Check
The system SHALL allow authenticated users to deposit a cheque into their account,
with the deposited amount held pending clearance.

#### Scenario: Successful cheque deposit
- GIVEN the user is authenticated with account `1001` having a balance of `$800.00`
- WHEN the user inserts a cheque for `$500.00`
- THEN the account balance is updated to `$1,300.00`
- AND a cheque deposit transaction record is created with a pending-hold flag

#### Scenario: Cheque deposit does not increase ATM cash level
- GIVEN the user is authenticated
- AND the ATM has `$10,000.00` cash available
- WHEN the user deposits a cheque for `$500.00`
- THEN the ATM cash level remains `$10,000.00`
- AND only the account balance increases

#### Scenario: Unauthenticated user cannot deposit a cheque
- GIVEN the user has inserted their card but has not entered their PIN
- WHEN the user attempts a cheque deposit
- THEN the system rejects the request
- AND prompts the user to authenticate first
