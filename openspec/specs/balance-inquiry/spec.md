---
id: balance-inquiry
title: Balance Inquiry
status: accepted
version: 1.0.0
---

# Balance Inquiry

## Overview

An authenticated user can request their current account balance at any point during an
active session. The ATM displays the available balance. A simple receipt acknowledgement
is optionally represented (see `openspec/changes/remove-receipt-option/` for a proposed
removal of this behaviour).

## Actors

- **User** — the authenticated person operating the ATM
- **ATM** — returns the current balance from the in-memory account store

## Preconditions

- The user has successfully authenticated (PIN verified, session not locked).

---

## Scenarios

### Scenario: Authenticated user checks their balance

**Given** the user is authenticated with account `1001` having a balance of `$2,500.00`  
**When** the user requests a balance inquiry  
**Then** the ATM displays `$2,500.00`

---

### Scenario: Balance reflects previous withdrawals

**Given** the user is authenticated with account `1001` having a balance of `$2,500.00`  
**And** the user has previously withdrawn `$200.00` in the same session  
**When** the user requests a balance inquiry  
**Then** the ATM displays `$2,300.00`

---

### Scenario: Unauthenticated user cannot check balance

**Given** the user has inserted their card but has not yet entered their PIN  
**When** the user attempts a balance inquiry  
**Then** the system rejects the request  
**And** prompts the user to authenticate first

---

### Scenario: Locked session cannot check balance

**Given** the user's account has been locked due to three failed PIN attempts  
**When** the user attempts a balance inquiry  
**Then** the system rejects the request  
**And** reports that the account is locked

---

## Implementation Notes

- `ATM.check_balance()` raises `NotAuthenticatedError` if the session is not verified.
- `ATM.check_balance()` raises `AccountLockedError` if the session is locked.
- Balance is stored as a `float` on `Account.balance`; production systems should use `Decimal`.
