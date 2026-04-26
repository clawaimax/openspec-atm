---
id: withdrawal
title: Cash Withdrawal
status: accepted
version: 1.0.0
---

# Cash Withdrawal

## Overview

An authenticated user can withdraw cash from their account. The ATM verifies that:

1. The account has sufficient funds.
2. The ATM machine itself has sufficient physical cash.

On success the account balance is reduced and the ATM cash level is updated. The
transaction is recorded on the account.

## Actors

- **User** — the authenticated person operating the ATM
- **ATM** — validates funds, dispenses cash, and records the transaction

## Preconditions

- The user is authenticated (PIN verified, session not locked).
- The requested amount is a positive number.

---

## Scenarios

### Scenario: Successful cash withdrawal

**Given** the user is authenticated with account `1001` having a balance of `$2,500.00`  
**And** the ATM has `$10,000.00` cash available  
**When** the user requests a withdrawal of `$500.00`  
**Then** the ATM dispenses `$500.00`  
**And** the account balance is updated to `$2,000.00`  
**And** the ATM cash level is reduced to `$9,500.00`  
**And** a transaction record is created for the withdrawal

---

### Scenario: Withdrawal refused due to insufficient account funds

**Given** the user is authenticated with account `1001` having a balance of `$200.00`  
**And** the ATM has sufficient cash  
**When** the user requests a withdrawal of `$500.00`  
**Then** the withdrawal is refused  
**And** the account balance remains `$200.00`  
**And** the ATM cash level is unchanged  
**And** the system reports "insufficient funds"

---

### Scenario: Withdrawal refused due to insufficient ATM cash

**Given** the user is authenticated with account `1001` having a balance of `$2,500.00`  
**And** the ATM has only `$100.00` cash available  
**When** the user requests a withdrawal of `$500.00`  
**Then** the withdrawal is refused  
**And** the account balance remains `$2,500.00`  
**And** the ATM cash level remains `$100.00`  
**And** the system reports "insufficient ATM cash"

---

### Scenario: Withdrawal of zero or negative amount is rejected

**Given** the user is authenticated  
**When** the user requests a withdrawal of `$0.00` or a negative amount  
**Then** the withdrawal is rejected immediately  
**And** the system reports that the amount must be positive

---

### Scenario: Unauthenticated user cannot withdraw

**Given** the user has inserted their card but has not entered their PIN  
**When** the user attempts a withdrawal  
**Then** the system rejects the request  
**And** prompts the user to authenticate first

---

## Implementation Notes

- `ATM.withdraw()` raises `InsufficientFundsError` when account balance is too low.
- `ATM.withdraw()` raises `InsufficientCashError` when ATM cash is too low.
- `ATM.withdraw()` raises `ATMError` for zero/negative amounts.
- Balance and cash level are mutated atomically (single-threaded in-memory demo).
- The transaction is appended to `Account.transactions` for auditing.
