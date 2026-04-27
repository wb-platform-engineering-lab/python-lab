"""Exercise 1 — for loop + counter.

Implement `count_pending` so it counts orders with status "pending"
using a for loop and a counter variable.

Rules:
  - Loop over `orders` with a for loop
  - Use an if statement to check each order's status
  - Increment a counter variable when the condition is True
  - Return the final count

Do NOT use built-ins like sum() or list.count() — write the loop yourself.

Run:
    python3 src/02_ex1_count_pending.py
"""


def count_pending(orders):
    """Return the number of orders with status "pending"."""
    pass   # replace with your code


# ─── assertions ───────────────────────────────────────────────────────────────
orders = [
    {"order_id": "A-001", "status": "pending"},
    {"order_id": "A-002", "status": "cancelled"},
    {"order_id": "A-003", "status": "pending"},
    {"order_id": "A-004", "status": "shipped"},
    {"order_id": "A-005", "status": "pending"},
]

result = count_pending(orders)
assert result == 3,                                              f"expected 3, got {result}"
assert count_pending([]) == 0,                                   "empty list should return 0"
assert count_pending([{"status": "cancelled"}]) == 0,           "no pending → 0"
assert count_pending([{"status": "pending"}])   == 1,           "one pending → 1"

print(f"Exercise 1 passed — pending orders: {result}")
