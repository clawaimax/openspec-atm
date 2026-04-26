---
id: transfer
title: Fund Transfer Between Accounts
status: proposed
version: 0.1.0
change: add-transfer
---

# Fund Transfer Between Accounts  *(delta spec — proposed addition)*

## Overview

An authenticated user can transfer a positive amount from their account to another
account in the same ATM system. Both account balances are updated atomically.

## Preconditions

- The user is authenticated (PIN verified, session not locked).
- The transfer amount is a positive number.
- The destination account exists in the system.

---

## Scenarios

### Scenario: Successful fund transfer

**Given** the user is authenticated with account `1001` having a balance of `$2,500.00`  
**And** account `1002` exists with a balance of `$800.00`  
**When** the user transfers `$300.00` to account `1002`  
**Then** account `1001` balance is `$2,200.00`  
**And** account `1002` balance is `$1,100.00`  
**And** a transfer-out record is created on account `1001`  
**And** a transfer-in record is created on account `1002`

---

### Scenario: Transfer refused due to insufficient source funds

**Given** the user is authenticated with account `1001` having a balance of `$100.00`  
**When** the user attempts to transfer `$300.00` to account `1002`  
**Then** the transfer is refused  
**And** both account balances are unchanged  
**And** the system reports "insufficient funds"

---

### Scenario: Transfer to a non-existent account is rejected

**Given** the user is authenticated  
**When** the user attempts to transfer `$100.00` to account `9999` (does not exist)  
**Then** the transfer is rejected  
**And** the source account balance is unchanged  
**And** the system reports "destination account not found"

---

### Scenario: Transfer of zero or negative amount is rejected

**Given** the user is authenticated  
**When** the user attempts a transfer of `$0.00` or a negative amount  
**Then** the transfer is rejected  
**And** no balances change

---

### Scenario: Unauthenticated user cannot transfer

**Given** the user has inserted their card but has not entered their PIN  
**When** the user attempts a transfer  
**Then** the system rejects the request

---

## Implementation Notes

- `ATM.transfer()` should call `_require_auth()` then look up the destination account
  in `self._accounts`.
- The two balance mutations should happen together; no partial state.
- Raises `InsufficientFundsError`, `AccountNotFoundError`, or `ATMError` as appropriate.
