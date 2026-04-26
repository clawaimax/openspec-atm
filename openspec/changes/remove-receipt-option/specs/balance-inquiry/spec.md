---
id: balance-inquiry
title: Balance Inquiry
status: proposed
version: 1.1.0
change: remove-receipt-option
delta_type: REMOVE
---

# Balance Inquiry  *(delta spec — proposed modification via REMOVE)*

## What This Delta Removes

The following text is **removed** from `openspec/specs/balance-inquiry/spec.md`:

> ~~A simple receipt acknowledgement is optionally represented (see
> `openspec/changes/remove-receipt-option/` for a proposed removal of this behaviour).~~

No scenarios are removed; only the receipt reference in the Overview is struck.

## Resulting Overview (post-merge)

An authenticated user can request their current account balance at any point during an
active session. The ATM displays the available balance.

## Version

Bumped `1.0.0` → `1.1.0` (minor — removal of a non-implemented reference).

## Audit Note

The receipt option was added as a placeholder in the initial spec but was never
implemented. Removing it keeps the spec accurate and avoids misleading downstream
implementers.
