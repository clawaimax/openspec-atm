---
id: authentication
title: User Authentication
status: proposed
version: 1.1.0
change: modify-authentication-lockout
delta_type: MODIFY
---

# User Authentication  *(delta spec — proposed modification)*

## What This Delta Changes

This delta updates the **Account Locked** scenarios to replace the hard-coded reference
to "three" failed attempts with language that refers to the **configured lockout
threshold**. All other scenarios remain unchanged from `v1.0.0`.

> Full spec (post-merge target): `openspec/specs/authentication/spec.md`

---

## Modified Scenarios

### Scenario: Account locked after too many consecutive failed PIN attempts  *(replaces v1.0.0 scenario)*

**Given** a registered account with account number `1001`  
**And** the ATM is configured with a lockout threshold of `N` attempts  
**And** the user has inserted their card  
**When** the user enters an incorrect PIN `N` times in a row  
**Then** the account is locked for this session  
**And** further PIN attempts are rejected regardless of correctness  
**And** ATM services are unavailable until a new session is started

---

### Scenario: Custom lockout threshold is respected  *(new scenario)*

**Given** the ATM is configured with a lockout threshold of `5`  
**And** a registered account with account number `1001`  
**And** the user has inserted their card  
**When** the user enters an incorrect PIN `4` times  
**Then** the account is NOT yet locked  
**When** the user enters an incorrect PIN a 5th time  
**Then** the account is locked

---

### Scenario: Default lockout threshold is 3  *(unchanged — restated for clarity)*

**Given** the ATM is configured with the default lockout threshold  
**When** the user enters an incorrect PIN 3 times in a row  
**Then** the account is locked

---

## Unchanged Scenarios (reference only — not re-listed)

- Successful authentication with correct PIN
- Incorrect PIN is rejected
- Locked account rejects a correct PIN
- Card not found
