"""Challenge 2 — Class methods and static methods.

@classmethod for alternative constructors.
@staticmethod for utility functions.
Class variables shared across all instances.
"""


class Order:
    """A single customer order."""

    VALID_WAREHOUSES = {"north", "south", "west"}
    _total_created   = 0    # class variable — shared by all instances

    def __init__(self, order_id, sku, quantity, warehouse, status="pending"):
        self.order_id  = order_id
        self.sku       = sku
        self.quantity  = int(quantity)
        self.warehouse = warehouse
        self.status    = status
        Order._total_created += 1

    def __str__(self):
        return (f"{self.order_id}  {self.sku:<20} qty={self.quantity}"
                f"  {self.warehouse}  {self.status}")

    # --- @classmethod: alternative constructors ---

    @classmethod
    def from_dict(cls, data):
        """Create an Order from a plain dict."""
        return cls(
            order_id  = data["order_id"],
            sku       = data["sku"],
            quantity  = int(data["quantity"]),
            warehouse = data["warehouse"],
            status    = data.get("status", "pending"),
        )

    @classmethod
    def from_csv_row(cls, row):
        """Create an Order from a csv.DictReader row (all values are strings)."""
        return cls.from_dict(row)    # reuse from_dict — csv rows are dicts

    @classmethod
    def total_created(cls):
        """Return the total number of Order instances ever created."""
        return cls._total_created

    # --- @staticmethod: utility with no need for self or cls ---

    @staticmethod
    def is_valid_warehouse(name):
        """Return True if the warehouse name is recognised."""
        return name in Order.VALID_WAREHOUSES

    @staticmethod
    def parse_order_id(raw):
        """Normalise an order ID string (strip whitespace, uppercase)."""
        return raw.strip().upper()


# --- from_dict ---
print("=== from_dict constructor ===")
data = {"order_id": "ORD-001", "sku": "TENT-3P-GRN", "quantity": "2", "warehouse": "north"}
o = Order.from_dict(data)
print(o)

# --- from_csv_rows ---
print()
print("=== from_csv_rows ===")
csv_rows = [
    {"order_id": "ORD-001", "sku": "TENT-3P-GRN",   "quantity": "2", "warehouse": "north"},
    {"order_id": "ORD-002", "sku": "PACK-45L-BLK",   "quantity": "1", "warehouse": "south"},
    {"order_id": "ORD-003", "sku": "SLEEP-REG-BLU",  "quantity": "5", "warehouse": "west"},
    {"order_id": "ORD-004", "sku": "JACKET-M-RED",   "quantity": "4", "warehouse": "north", "status": "cancelled"},
]
orders = [Order.from_csv_row(row) for row in csv_rows]
print(f"Loaded {len(orders)} orders from dicts")

# --- static method ---
print()
print("=== static method ===")
print(f'is_valid_warehouse("north")   → {Order.is_valid_warehouse("north")}')
print(f'is_valid_warehouse("unknown") → {Order.is_valid_warehouse("unknown")}')
print(f'parse_order_id("  ord-001 ") → {Order.parse_order_id("  ord-001 ")}')

# --- class variable ---
print()
print("=== class variable ===")
print(f"Total orders created: {Order.total_created()}")
