# Delta for Transfer

## ADDED Requirements

### Requirement: Fund Transfer Between Accounts
The system SHALL allow authenticated users to transfer a positive amount from their
account to another account within the same ATM system.

#### Scenario: Successful fund transfer
- GIVEN the user is authenticated with account `1001` having a balance of `$2,500.00`
- AND account `1002` exists with a balance of `$800.00`
- WHEN the user transfers `$300.00` to account `1002`
- THEN account `1001` balance is `$2,200.00`
- AND account `1002` balance is `$1,100.00`
- AND a transfer-out record is created on account `1001`
- AND a transfer-in record is created on account `1002`

#### Scenario: Transfer refused due to insufficient source funds
- GIVEN the user is authenticated with account `1001` having a balance of `$100.00`
- WHEN the user attempts to transfer `$300.00` to account `1002`
- THEN the transfer is refused
- AND both account balances are unchanged
- AND the system reports "insufficient funds"

#### Scenario: Transfer to a non-existent account is rejected
- GIVEN the user is authenticated
- WHEN the user attempts to transfer `$100.00` to account `9999` (does not exist)
- THEN the transfer is rejected
- AND the source account balance is unchanged
- AND the system reports "destination account not found"

#### Scenario: Transfer of zero or negative amount is rejected
- GIVEN the user is authenticated
- WHEN the user attempts a transfer of `$0.00` or a negative amount
- THEN the transfer is rejected
- AND no balances change

#### Scenario: Unauthenticated user cannot transfer
- GIVEN the user has inserted their card but has not entered their PIN
- WHEN the user attempts a transfer
- THEN the system rejects the request
