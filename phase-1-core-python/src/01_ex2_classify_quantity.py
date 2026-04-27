"""Exercise 2 — Quantity classification with chained comparisons.

Implement `classify_quantity` using chained comparisons and if/elif/else.

Rules:
  quantity <= 0          → "invalid"
  1  ≤ quantity ≤ 5      → "small"
  6  ≤ quantity ≤ 12     → "standard"
  quantity > 12          → "bulk"

Hint: Python lets you write `1 <= quantity <= 5` directly — use that form.

Run:
    python3 src/01_ex2_classify_quantity.py
"""


def classify_quantity(quantity):
    pass   # replace with your code


# ─── assertions ───────────────────────────────────────────────────────────────
assert classify_quantity(0)   == "invalid",   f"got: {classify_quantity(0)}"
assert classify_quantity(-1)  == "invalid",   f"got: {classify_quantity(-1)}"
assert classify_quantity(1)   == "small",     f"got: {classify_quantity(1)}"
assert classify_quantity(5)   == "small",     f"got: {classify_quantity(5)}"
assert classify_quantity(6)   == "standard",  f"got: {classify_quantity(6)}"
assert classify_quantity(12)  == "standard",  f"got: {classify_quantity(12)}"
assert classify_quantity(13)  == "bulk",      f"got: {classify_quantity(13)}"
assert classify_quantity(100) == "bulk",      f"got: {classify_quantity(100)}"

print("Exercise 2 passed.")
