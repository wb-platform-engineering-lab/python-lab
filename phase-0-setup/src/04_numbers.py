"""Challenge 4 — Numbers and arithmetic.

Inventory calculations for a single SKU.
"""

# Inventory check
total_stock = 1200
reserved    = 340     # units locked in pending orders
available   = total_stock - reserved

reorder_threshold = 200
needs_reorder = available < reorder_threshold

unit_price  = 89.99
order_qty   = 15
order_value = unit_price * order_qty

print(f"Available stock : {available} units")
print(f"Needs reorder   : {needs_reorder}")
print(f"Order value     : ${order_value:.2f}")

# --- integer vs float division ---
print()
units_in_shipment = 250
units_per_pallet  = 12

full_pallets = units_in_shipment // 12    # floor division → integer
leftover     = units_in_shipment % 12     # remainder

print(f"Shipment : {units_in_shipment} units")
print(f"Pallets  : {full_pallets} full  ({leftover} units left over)")

# --- comparison operators ---
print()
stock_levels = [860, 95, 312, 18, 1400]
low_threshold = 100

print("Stock levels vs reorder threshold:")
for level in stock_levels:
    flag = " ← REORDER" if level < low_threshold else ""
    print(f"  {level:>6} units{flag}")
