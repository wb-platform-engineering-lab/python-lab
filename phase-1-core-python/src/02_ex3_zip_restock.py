"""Exercise 3 — zip().

Implement `format_restock` so it pairs each SKU with its restock quantity
using zip() and returns a list of formatted strings.

Expected result:
  ["TENT-3P-GRN: restock 50 units",
   "PACK-45L-BLK: restock 30 units",
   "SLEEP-REG-BLU: restock 75 units"]

Rules:
  - Use zip() to iterate over both lists at once
  - Format each pair as: f"{sku}: restock {amount} units"
  - Build and return a list of those strings

Run:
    python3 src/02_ex3_zip_restock.py
"""


def format_restock(skus, amounts):
    """Return list of "SKU: restock N units" strings."""
    pass   # replace with your code


# ─── assertions ───────────────────────────────────────────────────────────────
skus    = ["TENT-3P-GRN", "PACK-45L-BLK", "SLEEP-REG-BLU"]
amounts = [50, 30, 75]

result = format_restock(skus, amounts)
assert result == [
    "TENT-3P-GRN: restock 50 units",
    "PACK-45L-BLK: restock 30 units",
    "SLEEP-REG-BLU: restock 75 units",
], f"got: {result}"
assert format_restock([], []) == [], "empty lists → empty list"

print("Exercise 3 passed.")
print("Output:", result)
