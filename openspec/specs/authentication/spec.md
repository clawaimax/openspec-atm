---
id: authentication
title: User Authentication
status: accepted
version: 1.0.0
---

# User Authentication

## Overview

A user identifies themselves by inserting a card (providing an account number) and entering
a PIN. The system validates the PIN and either grants or denies access. After three consecutive
failed PIN attempts the account is locked for the session, preventing further access.

## Actors

- **User** — the person operating the ATM
- **ATM** — the machine that validates credentials and manages sessions

## Preconditions

- The ATM is powered on and has an active network/database connection (represented in-memory
  for this demo).

---

## Scenarios

### Scenario: Successful authentication with correct PIN

**Given** a registered account with account number `1001` and PIN `1234`  
**And** the user inserts their card (provides account number `1001`)  
**When** the user enters PIN `1234`  
**Then** the session is authenticated  
**And** the user is granted access to ATM services

---

### Scenario: Incorrect PIN is rejected

**Given** a registered account with account number `1001` and PIN `1234`  
**And** the user has inserted their card  
**When** the user enters an incorrect PIN  
**Then** authentication is denied  
**And** the failed-attempt counter increments by 1  
**And** the session remains unauthenticated

---

### Scenario: Account locked after three consecutive failed PIN attempts

**Given** a registered account with account number `1001`  
**And** the user has inserted their card  
**When** the user enters an incorrect PIN three times in a row  
**Then** the account is locked for this session  
**And** further PIN attempts are rejected regardless of correctness  
**And** ATM services are unavailable until a new session is started

---

### Scenario: Locked account rejects a correct PIN

**Given** a registered account that has been locked due to three failed PIN attempts  
**When** the user attempts to enter the correct PIN  
**Then** authentication is still denied  
**And** the system reports that the account is locked

---

### Scenario: Card not found

**Given** no account exists with account number `9999`  
**When** the user tries to insert a card with account number `9999`  
**Then** the system reports that the account was not found  
**And** no session is started

---

## Implementation Notes

- The PIN is compared as a plain string in this demo; production systems must hash PINs.
- Session locking is per-session; restarting a session (re-inserting the card) resets the
  attempt counter.
- The failed-attempt limit is 3 (constant `MAX_PIN_ATTEMPTS` in `session.py`).
