---
id: add-transfer
type: ADD
artifact: tasks
---

# Tasks: Add Fund Transfer

## Implementation Tasks

- [ ] Add `ATM.transfer(amount: float, destination_account_number: str) -> float` to
      `src/atm/atm.py`
- [ ] Write `tests/test_transfer.py` covering all scenarios in the delta spec
- [ ] Update `README.md` to mention transfer as an available feature

## Verification

- [ ] All new tests pass
- [ ] Existing tests unaffected (no regressions)

## Promotion

- [ ] Move `openspec/changes/add-transfer/specs/transfer/spec.md`
      → `openspec/specs/transfer/spec.md`
- [ ] Update spec status from `proposed` → `accepted`
- [ ] Archive or remove `openspec/changes/add-transfer/`
