"""Solution — Mini order processor capstone (05_order_processor.py).

Do not open this file until you have implemented all five functions yourself.
The value of the capstone comes from writing the complete processor from scratch.
"""

VALID_WAREHOUSES = {"north", "south", "west"}

PRICES = {
    "TENT-3P-GRN":   89.99,
    "PACK-45L-BLK":  149.99,
    "SLEEP-REG-BLU": 59.99,
    "JACKET-M-RED":  149.99,
    "BOOT-42-BRN":   119.99,
}


def validate_order(order):
    """Return (is_valid, reason). Reason is None when valid."""
    if order.get("status") == "cancelled":
        return False, "cancelled"
    if not order.get("warehouse"):
        return False, "missing warehouse"
    if order.get("warehouse") not in VALID_WAREHOUSES:
        return False, f"unknown warehouse '{order['warehouse']}'"
    quantity = order.get("quantity")
    if quantity is None:
        return False, "missing quantity"
    if quantity <= 0:
        return False, "zero quantity"
    return True, None


def calculate_value(order, prices):
    """Return the total order value in dollars."""
    unit_price = prices.get(order["sku"], 0.0)
    return unit_price * order["quantity"]


def process_order(order, prices):
    """Validate and process a single order. Return a result dict."""
    is_valid, reason = validate_order(order)

    if not is_valid:
        return {
            "order_id":  order.get("order_id", "?"),
            "sku":       order.get("sku", "?"),
            "tier":      order.get("customer_tier", "?"),
            "warehouse": order.get("warehouse") or "—",
            "quantity":  order.get("quantity", 0),
            "value":     None,
            "status":    "rejected",
            "reason":    reason,
        }

    return {
        "order_id":  order["order_id"],
        "sku":       order["sku"],
        "tier":      order["customer_tier"],
        "warehouse": order["warehouse"],
        "quantity":  order["quantity"],
        "value":     calculate_value(order, prices),
        "status":    "dispatched",
        "reason":    None,
    }


def process_batch(orders, prices):
    """Process all orders and return a list of result dicts."""
    results = []
    for order in orders:
        results.append(process_order(order, prices))
    return results


def print_summary(results):
    """Print the end-of-batch summary report."""
    dispatched = [r for r in results if r["status"] == "dispatched"]
    rejected   = [r for r in results if r["status"] == "rejected"]

    total_value  = sum(r["value"] for r in dispatched)

    by_warehouse = {}
    for r in dispatched:
        wh = r["warehouse"]
        by_warehouse[wh] = by_warehouse.get(wh, 0.0) + r["value"]

    fill_rate = len(dispatched) / len(results) if results else 0.0

    print()
    print("=== End of Batch Summary ===")
    print(f"Total orders    : {len(results)}")
    print(f"Dispatched      : {len(dispatched)}")
    print(f"Rejected        : {len(rejected)}")
    print(f"Batch value     : ${total_value:,.2f}")

    wh_parts = "  ".join(f"{wh}=${v:,.2f}" for wh, v in sorted(by_warehouse.items()))
    print(f"By warehouse    : {wh_parts}")
    print(f"Fill rate       : {fill_rate:.1%}")


# ─── run with the same batch as the exercise ──────────────────────────────────

orders = [
    {"order_id": "ORD-001", "status": "pending",   "customer_tier": "enterprise", "warehouse": "north", "sku": "TENT-3P-GRN",   "quantity": 2},
    {"order_id": "ORD-002", "status": "pending",   "customer_tier": "pro",        "warehouse": "south", "sku": "PACK-45L-BLK",  "quantity": 1},
    {"order_id": "ORD-003", "status": "pending",   "customer_tier": "free",       "warehouse": "west",  "sku": "SLEEP-REG-BLU", "quantity": 0},
    {"order_id": "ORD-004", "status": "pending",   "customer_tier": "enterprise", "warehouse": "north", "sku": "JACKET-M-RED",  "quantity": 4},
    {"order_id": "ORD-005", "status": "pending",   "customer_tier": "pro",        "warehouse": None,    "sku": "BOOT-42-BRN",   "quantity": 2},
    {"order_id": "ORD-006", "status": "pending",   "customer_tier": "free",       "warehouse": "west",  "sku": "TENT-3P-GRN",   "quantity": 1},
    {"order_id": "ORD-007", "status": "cancelled", "customer_tier": "enterprise", "warehouse": "south", "sku": "PACK-45L-BLK",  "quantity": 3},
    {"order_id": "ORD-008", "status": "pending",   "customer_tier": "pro",        "warehouse": "north", "sku": "SLEEP-REG-BLU", "quantity": 6},
]

print("=== Meridian Order Processor ===")
print(f"Processing batch of {len(orders)} orders...")
print()

results = process_batch(orders, PRICES)

for r in results:
    oid   = r["order_id"]
    tier  = r["tier"]
    wh    = r["warehouse"]
    sku   = r["sku"]
    qty   = r["quantity"]
    value = f"${r['value']:,.2f}" if r["value"] is not None else "—"
    note  = f"({r['reason']})" if r["reason"] else ""
    print(f"{oid}  {tier:<12} {wh:<7} {sku:<20} qty={qty}  {value:<10} → {r['status']} {note}")

print_summary(results)
