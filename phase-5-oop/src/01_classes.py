"""Challenge 1 — Classes and instances.

Defining the Order class with __init__, instance variables, and methods.
"""

PRICES = {
    "TENT-3P-GRN":   89.99,
    "PACK-45L-BLK":  149.99,
    "SLEEP-REG-BLU":  59.99,
    "JACKET-M-RED":  149.99,
    "BOOT-42-BRN":   119.99,
}


class Order:
    """A single customer order."""

    def __init__(self, order_id, sku, quantity, warehouse, status="pending"):
        self.order_id  = order_id
        self.sku       = sku
        self.quantity  = quantity
        self.warehouse = warehouse
        self.status    = status

    # --- instance methods ---

    def is_pending(self):
        """Return True if the order has not yet been processed."""
        return self.status == "pending"

    def total_value(self, prices):
        """Return the total monetary value of this order."""
        unit_price = prices.get(self.sku, 0.0)
        return unit_price * self.quantity

    def dispatch(self):
        """Mark the order as shipped."""
        self.status = "shipped"

    def __str__(self):
        return (f"{self.order_id}  {self.sku:<20} qty={self.quantity}"
                f"   {self.warehouse}   {self.status}")


# --- create instances ---
orders = [
    Order("ORD-001", "TENT-3P-GRN",   2, "north"),
    Order("ORD-002", "PACK-45L-BLK",  1, "south"),
    Order("ORD-003", "SLEEP-REG-BLU", 5, "west"),
    Order("ORD-004", "JACKET-M-RED",  4, "north", status="cancelled"),
]

print("=== Order instances ===")
for o in orders:
    print(o)

pending = [o for o in orders if o.is_pending()]
total   = sum(o.total_value(PRICES) for o in pending)

print(f"\nPending orders : {len(pending)}")
print(f"Total value    : ${total:.2f}")

# --- mutation ---
print()
print("=== Mutation ===")
target = orders[0]
print(f"Before: {target.order_id} status={target.status}")
target.dispatch()
print(f"After : {target.order_id} status={target.status}")
