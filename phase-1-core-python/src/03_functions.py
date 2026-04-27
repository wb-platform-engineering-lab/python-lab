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


# ─── YOUR TURN ───────────────────────────────────────────────────────────────
#
# Implement two functions below. The complete examples above show the pattern:
#   - route_order()     → early returns to flatten logic
#   - calculate_value() → simple lookup + arithmetic
#   - summarise_batch() → loop, accumulate, return multiple values
#
# Read those implementations carefully, then close the file and write yours.
# Run `python3 src/03_functions.py` to check the verification output.
# ─────────────────────────────────────────────────────────────────────────────


def classify_order(order):
    """Return a string classifying the order. Use early returns.

    Rules (check in this order — return as soon as one matches):
      1. status == "cancelled"               → return "cancelled"
      2. status == "shipped"                 → return "archived"
      3. quantity == 0                       → return "rejected"
      4. warehouse not in VALID_WAREHOUSES   → return "unroutable"
      5. Otherwise                           → return "dispatchable"

    This is the early-return pattern: each invalid case exits immediately,
    so the final return only runs when everything is fine.
    """
    # write your code here
    pass


def batch_statistics(orders, prices):
    """Return (total_orders, total_value, avg_value) for non-cancelled orders.

    Definitions:
      total_orders — count of orders where status != "cancelled"
      total_value  — sum of calculate_value(order, prices) for each counted order
      avg_value    — total_value / total_orders  (return 0.0 when total_orders is 0)

    Return all three values as a tuple so the caller can unpack them:
        total, value, avg = batch_statistics(orders, prices)

    Hint: call calculate_value() (already defined above) inside your loop.
    """
    # write your code here
    pass


# ─── verification ─────────────────────────────────────────────────────────────

ex_orders = [
    # pending + valid warehouse + qty > 0  → dispatchable, value = $89.99 × 2 = $179.98
    {"order_id": "T-001", "status": "pending",   "warehouse": "north", "sku": "TENT-3P-GRN",   "quantity": 2, "customer_tier": "pro"},
    # cancelled                             → skipped by batch_statistics
    {"order_id": "T-002", "status": "cancelled", "warehouse": "south", "sku": "PACK-45L-BLK",  "quantity": 1, "customer_tier": "free"},
    # pending + qty == 0                   → rejected, value = $0.00
    {"order_id": "T-003", "status": "pending",   "warehouse": "west",  "sku": "SLEEP-REG-BLU", "quantity": 0, "customer_tier": "enterprise"},
    # shipped                              → archived, value = $149.99 × 1 = $149.99
    {"order_id": "T-004", "status": "shipped",   "warehouse": "north", "sku": "PACK-45L-BLK",  "quantity": 1, "customer_tier": "enterprise"},
    # cancelled                            → skipped by batch_statistics
    {"order_id": "T-005", "status": "cancelled", "warehouse": "west",  "sku": "TENT-3P-GRN",   "quantity": 3, "customer_tier": "pro"},
]

print()
print("--- Your classify_order ---")
for o in ex_orders:
    result = classify_order(o)
    print(f"  {o['order_id']} → {result}")
# Expected:
#   T-001 → dispatchable
#   T-002 → cancelled
#   T-003 → rejected
#   T-004 → archived
#   T-005 → cancelled

print()
print("--- Your batch_statistics ---")
stats = batch_statistics(ex_orders, PRICES)
if stats is None:
    print("  (not implemented yet — batch_statistics returned None)")
else:
    total, value, avg = stats
    print(f"  Total orders : {total}")
    print(f"  Total value  : ${value:.2f}")
    print(f"  Avg value    : ${avg:.2f}")
# Non-cancelled orders: T-001, T-003, T-004 → 3 orders
# Values: $179.98 + $0.00 + $149.99 = $329.97, avg = $329.97 / 3 = $109.99
# Expected:
#   Total orders : 3
#   Total value  : $329.97
#   Avg value    : $109.99
