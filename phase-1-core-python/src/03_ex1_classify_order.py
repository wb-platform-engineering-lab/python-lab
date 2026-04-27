"""Exercise 1 — classify_order with early returns (guard clauses).

Implement `classify_order` using early returns.

Rules (check in this order — return as soon as one matches):
  1. status == "cancelled"             → return "cancelled"
  2. status == "shipped"               → return "archived"
  3. quantity == 0                     → return "rejected"
  4. warehouse not in VALID_WAREHOUSES → return "unroutable"
  5. otherwise                         → return "dispatchable"

Pattern: each guard is one condition and one return on the next line.
No nesting, no elif needed. The final return only runs when all guards passed.

Run:
    python3 src/03_ex1_classify_order.py
"""

VALID_WAREHOUSES = {"north", "south", "west"}


def classify_order(order):
    pass   # replace with your code


# ─── assertions ───────────────────────────────────────────────────────────────
assert classify_order({"status": "cancelled", "warehouse": "north", "quantity": 2}) == "cancelled",   "cancelled order"
assert classify_order({"status": "shipped",   "warehouse": "north", "quantity": 2}) == "archived",    "shipped order"
assert classify_order({"status": "pending",   "warehouse": "west",  "quantity": 0}) == "rejected",    "zero quantity"
assert classify_order({"status": "pending",   "warehouse": "east",  "quantity": 3}) == "unroutable",  "unknown warehouse"
assert classify_order({"status": "pending",   "warehouse": "north", "quantity": 2}) == "dispatchable","valid order"
assert classify_order({"status": "pending",   "warehouse": "south", "quantity": 1}) == "dispatchable","valid order"

print("Exercise 1 passed.")
