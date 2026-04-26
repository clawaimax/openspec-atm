---
id: deposit
title: Cash Deposit
status: proposed
version: 0.1.0
change: add-deposit
---

# Cash Deposit  *(delta spec — proposed addition)*

## Overview

An authenticated user can deposit cash into their account via the ATM. The deposited
amount is added to the account balance and the ATM cash level is updated accordingly.

## Preconditions

- The user is authenticated (PIN verified, session not locked).
- The deposit amount is a positive number.

---

## Scenarios

### Scenario: Successful cash deposit

**Given** the user is authenticated with account `1001` having a balance of `$800.00`  
**And** the ATM has `$10,000.00` cash available  
**When** the user deposits `$200.00`  
**Then** the account balance is updated to `$1,000.00`  
**And** the ATM cash level increases to `$10,200.00`  
**And** a deposit transaction record is created

---

### Scenario: Deposit of zero or negative amount is rejected

**Given** the user is authenticated  
**When** the user attempts to deposit `$0.00` or a negative amount  
**Then** the deposit is rejected  
**And** the system reports that the amount must be positive  
**And** the balance is unchanged

---

### Scenario: Unauthenticated user cannot deposit

**Given** the user has inserted their card but has not entered their PIN  
**When** the user attempts a deposit  
**Then** the system rejects the request  
**And** prompts the user to authenticate first

---

## Implementation Notes

- Mirrors `ATM.withdraw()` in structure; see `design.md` in this change for the method
  signature.
- ATM cash level increases on deposit (physical cash added to the machine).
