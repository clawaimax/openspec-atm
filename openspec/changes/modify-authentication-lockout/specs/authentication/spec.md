# Delta for Authentication

## MODIFIED Requirements

### Requirement: Account Lockout
The system MUST lock the account after the configured number of consecutive failed PIN
attempts in a single session.
(Previously: hard-coded to exactly 3 attempts)

#### Scenario: Account locked after configured number of failed PIN attempts
- GIVEN a registered account with account number `1001`
- AND the ATM is configured with a lockout threshold of `N` attempts
- AND the user has inserted their card
- WHEN the user enters an incorrect PIN `N` times in a row
- THEN the account is locked for this session
- AND further PIN attempts are rejected regardless of correctness
- AND ATM services are unavailable until a new session is started

#### Scenario: Custom lockout threshold is respected
- GIVEN the ATM is configured with a lockout threshold of `5`
- AND a registered account with account number `1001`
- AND the user has inserted their card
- WHEN the user enters an incorrect PIN `4` times
- THEN the account is NOT yet locked
- WHEN the user enters an incorrect PIN a 5th time
- THEN the account is locked

#### Scenario: Default lockout threshold is 3
- GIVEN the ATM is configured with the default lockout threshold
- WHEN the user enters an incorrect PIN 3 times in a row
- THEN the account is locked
