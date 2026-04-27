"""Exercise 2 — Fix three bugs in buggy_validate.

The function below has three bugs related to None checks and truthiness.
Find and fix each one. Edit the function body directly — do not rename it.

Bug 1 — wrong value in the comparison (line marked below)
Bug 2 — catches one falsy value but misses None and negative numbers
Bug 3 — catches empty string but misses None

After fixing all three, run the file — the assertions will verify your work.

Hint: the None trap demo in 04_none_truthiness.py shows the correct patterns.

Run:
    python3 src/04_ex2_fix_buggy_validate.py
"""


def buggy_validate(order):
    if order["status"] == "None":     # Bug 1: comparing to the string "None", not actual None
        return False, "missing status"

    quantity = order.get("quantity")
    if quantity == False:             # Bug 2: catches 0 (since 0 == False in Python) but not None
        return False, "no quantity"   #        and misses negative numbers entirely

    warehouse = order.get("warehouse")
    if warehouse == "":               # Bug 3: misses the case where warehouse is None
        return False, "missing warehouse"

    return True, None


# ─── assertions ───────────────────────────────────────────────────────────────

# Bug 1: status=None should be caught
assert buggy_validate({"status": None,      "quantity": 5,    "warehouse": "north"}) == (False, "missing status"), \
    "Bug 1: status=None should return (False, 'missing status')"

# Bug 2: quantity=None should be caught
assert buggy_validate({"status": "pending", "quantity": None, "warehouse": "north"}) == (False, "no quantity"), \
    "Bug 2: quantity=None should return (False, 'no quantity')"

# Bug 2: negative quantity should also be caught
assert buggy_validate({"status": "pending", "quantity": -1,   "warehouse": "north"}) == (False, "no quantity"), \
    "Bug 2: quantity=-1 should return (False, 'no quantity')"

# Bug 3: warehouse=None should be caught
assert buggy_validate({"status": "pending", "quantity": 3,    "warehouse": None})    == (False, "missing warehouse"), \
    "Bug 3: warehouse=None should return (False, 'missing warehouse')"

# these should still work after your fixes
assert buggy_validate({"status": "pending", "quantity": 0,    "warehouse": "north"}) == (False, "no quantity"),       "quantity=0 should be caught"
assert buggy_validate({"status": "pending", "quantity": 3,    "warehouse": ""})      == (False, "missing warehouse"), "empty warehouse should be caught"
assert buggy_validate({"status": "pending", "quantity": 3,    "warehouse": "north"}) == (True,  None),               "valid order"

print("Exercise 2 passed — all bugs fixed.")
