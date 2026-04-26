"""Challenge 5 — Dunder methods.

Making Order and Inventory work naturally with Python's built-in
operators, functions, and iteration protocols.
"""


class Order:
    """A customer order with full dunder support."""

    def __init__(self, order_id, sku, quantity, warehouse, status="pending"):
        self.order_id  = order_id
        self.sku       = sku
        self.quantity  = quantity
        self.warehouse = warehouse
        self.status    = status

    def __str__(self):
        """Human-readable: used by print() and str()."""
        return f"Order({self.order_id}, {self.sku}, qty={self.quantity}) @ {self.warehouse} [{self.status}]"

    def __repr__(self):
        """Unambiguous: used by repr(), the REPL, and debuggers."""
        return (f"Order(order_id={self.order_id!r}, sku={self.sku!r}, "
                f"quantity={self.quantity!r}, warehouse={self.warehouse!r}, "
                f"status={self.status!r})")

    def __eq__(self, other):
        """order1 == order2 — two orders are equal if they share an order_id."""
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_id == other.order_id

    def __lt__(self, other):
        """order1 < order2 — enables sorted(list_of_orders)."""
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_id < other.order_id

    def __hash__(self):
        """Needed when __eq__ is defined — allows use in sets and as dict keys."""
        return hash(self.order_id)


class Inventory:
    """A collection of inventory items with container dunder methods."""

    def __init__(self, items):
        # items: dict of sku → {"stock": int, "reorder_threshold": int}
        self._items = dict(items)

    def __len__(self):
        """len(inventory) — number of distinct SKUs."""
        return len(self._items)

    def __contains__(self, sku):
        """'TENT-3P-GRN' in inventory"""
        return sku in self._items

    def __iter__(self):
        """for sku, info in inventory — iterates over (sku, info) pairs."""
        return iter(self._items.items())

    def __getitem__(self, sku):
        """inventory['TENT-3P-GRN'] — direct access by SKU."""
        return self._items[sku]


# --- Order dunders ---
orders = [
    Order("ORD-003", "SLEEP-REG-BLU", 5, "west"),
    Order("ORD-001", "TENT-3P-GRN",   2, "north"),
    Order("ORD-005", "BOOT-42-BRN",   2, "south", status="cancelled"),
    Order("ORD-002", "PACK-45L-BLK",  1, "south"),
    Order("ORD-004", "JACKET-M-RED",  4, "north"),
]

print("=== __str__ and __repr__ ===")
o = orders[1]
print(f"str  : {str(o)}")
print(f"repr : {repr(o)}")

print()
print("=== __eq__ and __lt__ ===")
a = Order("ORD-001", "TENT-3P-GRN", 2, "north")
b = Order("ORD-001", "TENT-3P-GRN", 2, "north")
c = Order("ORD-002", "PACK-45L-BLK", 1, "south")
print(f"ORD-001 == ORD-001 : {a == b}")
print(f"ORD-001 == ORD-002 : {a == c}")
print(f"sorted orders: {[o.order_id for o in sorted(orders)]}")

print()
print("=== Order in a set (requires __hash__) ===")
seen = {a, b, c}           # b is a duplicate of a
print(f"{{a, b, c}} has {len(seen)} unique orders (a and b are equal)")

# --- Inventory dunders ---
inventory = Inventory({
    "TENT-3P-GRN":   {"stock": 312, "reorder_threshold": 50},
    "PACK-45L-BLK":  {"stock":  88, "reorder_threshold": 30},
    "SLEEP-REG-BLU": {"stock":  14, "reorder_threshold": 20},
    "JACKET-M-RED":  {"stock":   0, "reorder_threshold": 25},
    "BOOT-42-BRN":   {"stock": 203, "reorder_threshold": 40},
})

print()
print("=== Inventory dunders ===")
print(f"len(inventory)              : {len(inventory)}")
print(f"'TENT-3P-GRN' in inventory  : {'TENT-3P-GRN' in inventory}")
print(f"'CRAMPONS-S' in inventory   : {'CRAMPONS-S' in inventory}")

print("Iterating:")
for sku, info in inventory:
    print(f"  {sku:<20} stock={info['stock']:>3}")

print(f"inventory['TENT-3P-GRN']    : {inventory['TENT-3P-GRN']}")
