"""Exercise 2 — enumerate().

Implement `format_warehouses` so it returns a list of strings with
1-based position numbers, built using enumerate().

Expected result for ["north", "south", "west"]:
  ["1. north", "2. south", "3. west"]

Rules:
  - Use enumerate() — do not use range(len(...))
  - Position numbers start at 1, not 0
  - Build and return a list of formatted strings

Run:
    python3 src/02_ex2_enumerate_warehouses.py
"""


def format_warehouses(warehouses):
    """Return list of "N. name" strings, numbered from 1."""
    pass   # replace with your code


# ─── assertions ───────────────────────────────────────────────────────────────
warehouses = ["north", "south", "west"]

result = format_warehouses(warehouses)
assert result == ["1. north", "2. south", "3. west"], f"got: {result}"
assert format_warehouses([])       == [],          "empty list → empty list"
assert format_warehouses(["east"]) == ["1. east"], "single item"

print("Exercise 2 passed.")
print("Output:", result)
