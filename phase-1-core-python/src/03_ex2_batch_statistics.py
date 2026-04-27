"""Exercise 2 — batch_statistics with multiple return values.

Implement `batch_statistics` so it returns three values as a tuple.

Definitions:
  total_orders — count of orders where status != "cancelled"
  total_value  — sum of (unit_price × quantity) for each non-cancelled order
  avg_value    — total_value / total_orders  (return 0.0 when total_orders is 0)

Use PRICES.get(order["sku"], 0.0) to look up the unit price safely.

Return all three with a single return line:
    return total_orders, total_value, avg_value

The caller unpacks them immediately:
    total, value, avg = batch_statistics(orders, PRICES)

Run:
    python3 src/03_ex2_batch_statistics.py
"""

PRICES = {
    "TENT-3P-GRN":   89.99,
    "PACK-45L-BLK":  149.99,
    "SLEEP-REG-BLU": 59.99,
}


def batch_statistics(orders, prices):
    """Return (total_orders, total_value, avg_value) for non-cancelled orders."""
    pass   # replace with your code


# ─── data ─────────────────────────────────────────────────────────────────────
orders = [
    # non-cancelled: TENT-3P-GRN × 2 = $179.98
    {"order_id": "T-001", "status": "pending",   "sku": "TENT-3P-GRN",   "quantity": 2},
    # cancelled → skipped
    {"order_id": "T-002", "status": "cancelled", "sku": "PACK-45L-BLK",  "quantity": 1},
    # non-cancelled: SLEEP-REG-BLU × 0 = $0.00
    {"order_id": "T-003", "status": "pending",   "sku": "SLEEP-REG-BLU", "quantity": 0},
    # non-cancelled: PACK-45L-BLK × 1 = $149.99
    {"order_id": "T-004", "status": "shipped",   "sku": "PACK-45L-BLK",  "quantity": 1},
    # cancelled → skipped
    {"order_id": "T-005", "status": "cancelled", "sku": "TENT-3P-GRN",   "quantity": 3},
]

# ─── assertions ───────────────────────────────────────────────────────────────
# non-cancelled: T-001 ($179.98), T-003 ($0.00), T-004 ($149.99) → 3 orders, $329.97, avg $109.99
result = batch_statistics(orders, PRICES)
assert result is not None, "function returned None — did you forget to return?"

total, value, avg = result
assert total == 3,                     f"expected total=3, got {total}"
assert abs(value - 329.97) < 0.01,    f"expected value≈329.97, got {value}"
assert abs(avg   - 109.99) < 0.01,    f"expected avg≈109.99, got {avg}"

# edge case: all cancelled → no division by zero
all_cancelled = [{"status": "cancelled", "sku": "TENT-3P-GRN", "quantity": 1}]
t2, v2, a2 = batch_statistics(all_cancelled, PRICES)
assert t2 == 0   and v2 == 0.0 and a2 == 0.0, "all cancelled: expected (0, 0.0, 0.0)"

print(f"Exercise 2 passed — {total} orders, ${value:.2f} total, ${avg:.2f} avg")
