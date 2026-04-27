"""Exercise 3 — Routability check with logical operators.

Implement `is_routable` using logical operators (and).

An order is routable when ALL of these are true:
  - status is "pending"
  - warehouse is in VALID_WAREHOUSES
  - quantity is greater than 0

Return True or False.

Rule: write this as a single `return` expression using `and`.
Do not use if/else — the condition itself is the answer.

Run:
    python3 src/01_ex3_is_routable.py
"""

VALID_WAREHOUSES = {"north", "south", "west"}


def is_routable(status, warehouse, quantity):
    pass   # replace with your code


# ─── assertions ───────────────────────────────────────────────────────────────
assert is_routable("pending",   "north",   3)  is True,  "should be routable"
assert is_routable("cancelled", "north",   3)  is False, "cancelled → not routable"
assert is_routable("pending",   "unknown", 3)  is False, "bad warehouse → not routable"
assert is_routable("pending",   "west",    0)  is False, "zero qty → not routable"
assert is_routable("pending",   "south",   1)  is True,  "should be routable"
assert is_routable("shipped",   "north",   5)  is False, "shipped → not routable"

print("Exercise 3 passed.")
