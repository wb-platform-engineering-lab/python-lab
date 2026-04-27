"""Solutions — Loops exercises (02_ex1 through 02_ex4).

Do not open this file until you have attempted all four exercises yourself.
"""


# ── Exercise 1 ────────────────────────────────────────────────────────────────

def count_pending(orders):
    count = 0
    for order in orders:
        if order["status"] == "pending":
            count += 1
    return count


# ── Exercise 2 ────────────────────────────────────────────────────────────────

def format_warehouses(warehouses):
    result = []
    for index, name in enumerate(warehouses):
        result.append(f"{index + 1}. {name}")
    return result


# ── Exercise 3 ────────────────────────────────────────────────────────────────

def format_restock(skus, amounts):
    result = []
    for sku, amount in zip(skus, amounts):
        result.append(f"{sku}: restock {amount} units")
    return result


# ── Exercise 4 ────────────────────────────────────────────────────────────────

def poll_shipment(max_checks, success_on_check):
    arrived = False
    checks  = 0
    while not arrived and checks < max_checks:
        checks += 1
        if checks == success_on_check:
            arrived = True
            break
    return arrived, checks


# ─── verify all solutions ─────────────────────────────────────────────────────

orders = [
    {"order_id": "A-001", "status": "pending"},
    {"order_id": "A-002", "status": "cancelled"},
    {"order_id": "A-003", "status": "pending"},
    {"order_id": "A-004", "status": "shipped"},
    {"order_id": "A-005", "status": "pending"},
]
assert count_pending(orders)                      == 3
assert count_pending([])                          == 0
assert count_pending([{"status": "cancelled"}])   == 0
assert count_pending([{"status": "pending"}])     == 1

warehouses = ["north", "south", "west"]
assert format_warehouses(warehouses) == ["1. north", "2. south", "3. west"]
assert format_warehouses([])         == []
assert format_warehouses(["east"])   == ["1. east"]

skus    = ["TENT-3P-GRN", "PACK-45L-BLK", "SLEEP-REG-BLU"]
amounts = [50, 30, 75]
assert format_restock(skus, amounts) == [
    "TENT-3P-GRN: restock 50 units",
    "PACK-45L-BLK: restock 30 units",
    "SLEEP-REG-BLU: restock 75 units",
]
assert format_restock([], []) == []

arrived, checks = poll_shipment(max_checks=4, success_on_check=3)
assert arrived is True and checks == 3

arrived, checks = poll_shipment(max_checks=3, success_on_check=10)
assert arrived is False and checks == 3

arrived, checks = poll_shipment(max_checks=5, success_on_check=1)
assert arrived is True and checks == 1

print("All solutions verified.")
