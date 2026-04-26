"""Challenge 1 — Control flow.

Route and prioritise orders using if/elif/else, logical operators,
and the ternary expression.
"""

VALID_WAREHOUSES = {"north", "south", "west"}

order = {
    "order_id": "ORD-00142",
    "status": "pending",
    "customer_tier": "enterprise",
    "quantity": 5,
    "warehouse": "north",
}

# --- if / elif / else ---
if order["status"] == "cancelled":
    print(f"{order['order_id']} — skipped (cancelled)")
elif order["status"] == "shipped":
    print(f"{order['order_id']} — already shipped, archive it")
elif order["status"] == "pending":
    print(f"{order['order_id']} — needs processing")
else:
    print(f"{order['order_id']} — unknown status: {order['status']}")

# --- logical operators: and, or, not ---
tier     = order["customer_tier"]
quantity = order["quantity"]

if tier == "enterprise" or tier == "pro":
    print(f"{tier} order: flag for priority handling")

if not order["warehouse"] not in VALID_WAREHOUSES:
    pass   # warehouse is valid — nothing to do

# --- chained comparisons ---
if 1 <= quantity <= 12:
    print(f"quantity {quantity} is within single-pallet limit")
elif quantity > 12:
    print(f"quantity {quantity} needs multi-pallet handling")

# --- ternary expression ---
label = "priority" if tier == "enterprise" else "standard"
print(f"Handling: {label}")

# --- nested conditions (flattened with early logic) ---
print()
print("--- Warehouse routing check ---")
for status, wh, qty in [
    ("pending",   "north",   5),
    ("cancelled", "south",   1),
    ("pending",   "unknown", 3),
    ("pending",   "west",    0),
    ("pending",   "west",   10),
]:
    if status == "cancelled":
        print(f"  skip  — cancelled")
        continue
    if wh not in VALID_WAREHOUSES:
        print(f"  error — invalid warehouse '{wh}'")
        continue
    if qty <= 0:
        print(f"  error — zero quantity")
        continue
    print(f"  route to {wh} (qty={qty})")
