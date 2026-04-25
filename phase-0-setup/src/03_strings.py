"""Challenge 3 — String formatting.

Build a formatted daily report using f-strings.
"""

warehouse  = "north"
order_count = 2400
fill_rate   = 0.97
threshold   = 0.95

# f-strings: embed any expression inside {}
# :.1% formats a float as a percentage with 1 decimal place
# :<10 left-aligns in a field of width 10
# :>10 right-aligns in a field of width 10

status = "ON TRACK" if fill_rate >= threshold else "AT RISK"

print("=== Meridian Daily Report ===")
print(f"{'Warehouse':<10} : {warehouse}")
print(f"{'Orders':<10} : {order_count}")
print(f"{'Fill rate':<10} : {fill_rate:.1%}")
print(f"{'Status':<10} : {status}")

# --- useful string methods ---
raw_input = "  TENT-3P-GRN  "
print()
print(f"Original : '{raw_input}'")
print(f"strip()  : '{raw_input.strip()}'")
print(f"lower()  : '{raw_input.strip().lower()}'")
print(f"upper()  : '{raw_input.strip().upper()}'")
print(f"split()  : {raw_input.strip().split('-')}")
print(f"len()    : {len(raw_input.strip())}")

# --- multi-line strings ---
header = """
=== Meridian Inventory System ===
Generated automatically by Python
"""
print(header)
