"""Challenge 3 — Functions and scope.

Routing logic extracted into clean, single-purpose functions.
Demonstrates scope, early returns, and multiple return values.
"""

VALID_WAREHOUSES = {"north", "south", "west"}

PRICES = {
    "TENT-3P-GRN":   89.99,
    "PACK-45L-BLK":  149.99,
    "SLEEP-REG-BLU": 59.99,
}


def route_order(order):
    """Return the warehouse name for a pending order, or None if not routable.

    Uses early returns to avoid nesting — each invalid case exits immediately.
    """
    if order["status"] != "pending":
        return None
    if order["quantity"] <= 0:
        return None
    if order["warehouse"] not in VALID_WAREHOUSES:
        return None
    return order["warehouse"]


def calculate_value(order, prices):
    """Return the total value of the order in dollars.

    Returns 0.0 if the SKU is not in the price list.
    """
    unit_price = prices.get(order["sku"], 0.0)
    return unit_price * order["quantity"]


def summarise_batch(orders, prices):
    """Return (dispatched_count, skipped_count, total_value) for a batch.

    Multiple return values — unpack on the calling side.
    """
    dispatched = 0
    skipped    = 0
    total      = 0.0

    for order in orders:
        warehouse = route_order(order)
        if warehouse is None:
            skipped += 1
        else:
            dispatched += 1
            total += calculate_value(order, prices)

    return dispatched, skipped, total   # returned as a tuple


# --- run the demo ---
orders = [
    {"order_id": "ORD-001", "status": "pending",   "warehouse": "north",  "sku": "TENT-3P-GRN",   "quantity": 2, "customer_tier": "enterprise"},
    {"order_id": "ORD-002", "status": "cancelled", "warehouse": "south",  "sku": "PACK-45L-BLK",  "quantity": 1, "customer_tier": "pro"},
    {"order_id": "ORD-003", "status": "pending",   "warehouse": "west",   "sku": "SLEEP-REG-BLU", "quantity": 5, "customer_tier": "pro"},
    {"order_id": "ORD-004", "status": "pending",   "warehouse": "north",  "sku": "TENT-3P-GRN",   "quantity": 12, "customer_tier": "free"},
    {"order_id": "ORD-005", "status": "shipped",   "warehouse": "south",  "sku": "PACK-45L-BLK",  "quantity": 3, "customer_tier": "enterprise"},
]

print("=== Order Routing ===")
for order in orders:
    warehouse = route_order(order)
    tier      = order["customer_tier"]
    qty       = order["quantity"]
    print(f"{order['order_id']} → {str(warehouse):<8} ({tier}, qty={qty})")

print()
print("=== Batch Summary ===")
dispatched, skipped, value = summarise_batch(orders, PRICES)
print(f"Dispatched : {dispatched} orders")
print(f"Skipped    : {skipped} orders")
print(f"Batch value: ${value:,.2f}")

# --- scope demonstration ---
print()
print("--- Scope ---")
threshold = 100   # module-level — visible to all functions below

def is_low_stock(available):
    """Local variable 'message' only exists inside this function."""
    message = "low stock" if available < threshold else "ok"
    return message

print(f"stock=50  → {is_low_stock(50)}")
print(f"stock=200 → {is_low_stock(200)}")
# print(message)   # would raise NameError — message is local to is_low_stock
