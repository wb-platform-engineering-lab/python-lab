"""Solutions — Functions exercises (03_ex1 and 03_ex2).

Do not open this file until you have attempted both exercises yourself.
"""

VALID_WAREHOUSES = {"north", "south", "west"}

PRICES = {
    "TENT-3P-GRN":   89.99,
    "PACK-45L-BLK":  149.99,
    "SLEEP-REG-BLU": 59.99,
}


# ── Exercise 1 ────────────────────────────────────────────────────────────────

def classify_order(order):
    if order["status"] == "cancelled":
        return "cancelled"
    if order["status"] == "shipped":
        return "archived"
    if order["quantity"] == 0:
        return "rejected"
    if order["warehouse"] not in VALID_WAREHOUSES:
        return "unroutable"
    return "dispatchable"


# ── Exercise 2 ────────────────────────────────────────────────────────────────

def batch_statistics(orders, prices):
    total_orders = 0
    total_value  = 0.0

    for order in orders:
        if order["status"] == "cancelled":
            continue
        total_orders += 1
        total_value  += prices.get(order["sku"], 0.0) * order["quantity"]

    avg_value = total_value / total_orders if total_orders > 0 else 0.0
    return total_orders, total_value, avg_value


# ─── verify all solutions ─────────────────────────────────────────────────────

assert classify_order({"status": "cancelled", "warehouse": "north", "quantity": 2}) == "cancelled"
assert classify_order({"status": "shipped",   "warehouse": "north", "quantity": 2}) == "archived"
assert classify_order({"status": "pending",   "warehouse": "west",  "quantity": 0}) == "rejected"
assert classify_order({"status": "pending",   "warehouse": "east",  "quantity": 3}) == "unroutable"
assert classify_order({"status": "pending",   "warehouse": "north", "quantity": 2}) == "dispatchable"
assert classify_order({"status": "pending",   "warehouse": "south", "quantity": 1}) == "dispatchable"

orders = [
    {"order_id": "T-001", "status": "pending",   "sku": "TENT-3P-GRN",   "quantity": 2},
    {"order_id": "T-002", "status": "cancelled", "sku": "PACK-45L-BLK",  "quantity": 1},
    {"order_id": "T-003", "status": "pending",   "sku": "SLEEP-REG-BLU", "quantity": 0},
    {"order_id": "T-004", "status": "shipped",   "sku": "PACK-45L-BLK",  "quantity": 1},
    {"order_id": "T-005", "status": "cancelled", "sku": "TENT-3P-GRN",   "quantity": 3},
]

total, value, avg = batch_statistics(orders, PRICES)
assert total == 3
assert abs(value - 329.97) < 0.01
assert abs(avg   - 109.99) < 0.01

t2, v2, a2 = batch_statistics([{"status": "cancelled", "sku": "TENT-3P-GRN", "quantity": 1}], PRICES)
assert t2 == 0 and v2 == 0.0 and a2 == 0.0

print("All solutions verified.")
