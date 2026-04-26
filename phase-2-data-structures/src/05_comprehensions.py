"""Challenge 5 — Comprehensions.

Transform and filter inventory and order data in one readable line.
"""

inventory = {
    "TENT-3P-GRN":   312,
    "PACK-45L-BLK":   88,
    "SLEEP-REG-BLU":  14,
    "JACKET-M-RED":    0,
    "BOOT-42-BRN":   203,
}

prices = {
    "TENT-3P-GRN":   89.99,
    "PACK-45L-BLK":  149.99,
    "SLEEP-REG-BLU":  59.99,
    "JACKET-M-RED":  149.99,
    "BOOT-42-BRN":   119.99,
}

# --- list comprehensions ---
low_stock    = [sku for sku, qty in inventory.items() if qty < 50]
out_of_stock = [sku for sku, qty in inventory.items() if qty == 0]
reorder_list = sorted([sku for sku, qty in inventory.items() if qty < 50])

print("=== Inventory Alerts ===")
print(f"Low stock  (< 50 units) : {low_stock}")
print(f"Out of stock            : {out_of_stock}")
print(f"Reorder list            : {reorder_list}")

# --- dict comprehensions ---
discounted = {sku: round(price * 0.9, 2) for sku, price in prices.items()}

print()
print("=== Pricing ===")
print(f"Original prices  : {prices}")
print(f"After 10% sale   : {discounted}")

# --- built-in aggregates on comprehensions ---
orders = [
    {"order_id": "ORD-001", "status": "pending",   "quantity": 5},
    {"order_id": "ORD-002", "status": "cancelled", "quantity": 2},
    {"order_id": "ORD-003", "status": "pending",   "quantity": 12},
    {"order_id": "ORD-004", "status": "pending",   "quantity": 1},
    {"order_id": "ORD-005", "status": "shipped",   "quantity": 3},
    {"order_id": "ORD-006", "status": "pending",   "quantity": 6},
]

pending_orders  = [o for o in orders if o["status"] == "pending"]
total_qty       = sum(o["quantity"] for o in orders)
any_large       = any(o["quantity"] > 10 for o in orders)
all_positive    = all(o["quantity"] > 0  for o in orders)

print()
print("=== Order Stats ===")
print(f"Total orders    : {len(orders)}")
print(f"Pending         : {len(pending_orders)}")
print(f"Total quantity  : {total_qty}")
print(f"Any over 10?    : {any_large}")
print(f"All positive?   : {all_positive}")

# --- when a plain loop is clearer ---
# This is too complex for a readable comprehension — use a loop
valued_orders = []
for o in orders:
    sku_price = prices.get("TENT-3P-GRN", 0.0)   # simplified: assume same SKU
    value = o["quantity"] * sku_price
    if value > 100 and o["status"] == "pending":
        valued_orders.append({"order_id": o["order_id"], "value": value})

print()
print("=== High-value pending orders (> $100) ===")
for o in valued_orders:
    print(f"  {o['order_id']}  ${o['value']:.2f}")
