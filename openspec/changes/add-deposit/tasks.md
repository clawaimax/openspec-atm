---
id: add-deposit
type: ADD
artifact: tasks
---

# Tasks: Add Deposit Functionality

## Implementation Tasks

- [ ] Add `ATM.deposit(amount: float) -> float` method to `src/atm/atm.py`
- [ ] Write `tests/test_deposit.py` covering all scenarios in the delta spec
- [ ] Update `README.md` to mention deposit as an available feature

## Verification

- [ ] All new tests pass
- [ ] Existing tests unaffected (no regressions)
- [ ] Delta spec scenarios match test function names 1-to-1

## Promotion

- [ ] Move `openspec/changes/add-deposit/specs/deposit/spec.md`
      → `openspec/specs/deposit/spec.md`
- [ ] Update spec status from `proposed` → `accepted`
- [ ] Archive or remove `openspec/changes/add-deposit/`
