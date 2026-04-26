# Proposal: Remove Receipt Option from Balance Inquiry

## Intent
The receipt acknowledgement in the Balance Inquiry spec was added as a placeholder but
was never implemented. It confuses downstream implementers who look for a corresponding
code path that does not exist.

## Scope
In scope:
- Remove the receipt reference from the Balance Inquiry spec Overview
- Bump spec version from `1.0.0` to `1.1.0`

Out of scope:
- Any source code changes (no receipt code exists)
- Any test changes (no receipt tests exist)

## Approach
Edit `openspec/specs/balance-inquiry/spec.md` to remove the receipt sentence from the
Overview. No source or test files require changes. Archive the change folder after the
spec edit is verified with `openspec validate --strict`.
