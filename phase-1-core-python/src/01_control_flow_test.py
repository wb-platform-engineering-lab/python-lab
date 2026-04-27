"""Control flow — quick-check exercises.

Run this file directly:
    python3 src/01_control_flow_test.py

Each function below has a stub body (`pass`). Replace `pass` with your
implementation. The assert statements at the bottom will tell you whether
your code is correct — a passing run prints nothing extra, a failure prints
an AssertionError with the value that was wrong.

Read `01_control_flow.py` first to understand the patterns, then close it
and implement these from memory.
"""

VALID_WAREHOUSES = {"north", "south", "west"}


# ── Exercise 1 ────────────────────────────────────────────────────────────────
# Implement `get_queue` so it returns the correct queue name for a customer tier.
# Rules:
#   "enterprise" → "priority queue"
#   "pro"        → "standard queue"
#   anything else → "self-service"
#
# Use if/elif/else. No ternary expression for this one — be explicit.

def get_queue(tier):
    pass   # replace with your code


# ── Exercise 2 ────────────────────────────────────────────────────────────────
# Implement `classify_quantity` using chained comparisons and if/elif/else.
# Rules:
#   quantity <= 0          → "invalid"
#   1  ≤ quantity ≤ 5      → "small"
#   6  ≤ quantity ≤ 12     → "standard"
#   quantity > 12          → "bulk"

def classify_quantity(quantity):
    pass   # replace with your code


# ── Exercise 3 ────────────────────────────────────────────────────────────────
# Implement `is_routable` using logical operators.
# An order is routable when ALL of these are true:
#   - status is "pending"
#   - warehouse is in VALID_WAREHOUSES
#   - quantity is greater than 0
# Return True or False.
#
# Write this as a single `return` with `and` — do not use if/else.

def is_routable(status, warehouse, quantity):
    pass   # replace with your code


# ── Exercise 4 ────────────────────────────────────────────────────────────────
# Implement `priority_label` using a ternary expression.
# Return "priority" if tier is "enterprise", else "standard".
# One line. No if/elif/else block.

def priority_label(tier):
    pass   # replace with your code


# ─── verification ─────────────────────────────────────────────────────────────
# Run this file. If all asserts pass, you'll see "All checks passed."
# If an assert fails, it will show you which value was wrong.

assert get_queue("enterprise") == "priority queue",  f"got: {get_queue('enterprise')}"
assert get_queue("pro")        == "standard queue",  f"got: {get_queue('pro')}"
assert get_queue("free")       == "self-service",    f"got: {get_queue('free')}"
assert get_queue("unknown")    == "self-service",    f"got: {get_queue('unknown')}"

assert classify_quantity(0)   == "invalid",   f"got: {classify_quantity(0)}"
assert classify_quantity(-1)  == "invalid",   f"got: {classify_quantity(-1)}"
assert classify_quantity(1)   == "small",     f"got: {classify_quantity(1)}"
assert classify_quantity(5)   == "small",     f"got: {classify_quantity(5)}"
assert classify_quantity(6)   == "standard",  f"got: {classify_quantity(6)}"
assert classify_quantity(12)  == "standard",  f"got: {classify_quantity(12)}"
assert classify_quantity(13)  == "bulk",      f"got: {classify_quantity(13)}"

assert is_routable("pending",   "north",   3)  is True
assert is_routable("cancelled", "north",   3)  is False
assert is_routable("pending",   "unknown", 3)  is False
assert is_routable("pending",   "west",    0)  is False

assert priority_label("enterprise") == "priority"
assert priority_label("pro")        == "standard"
assert priority_label("free")       == "standard"

print("All checks passed.")
