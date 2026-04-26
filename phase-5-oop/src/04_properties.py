"""Challenge 4 — Properties.

@property and setter to validate stock changes.
Read-only computed properties for derived values.
"""


class InventoryItem:
    """An inventory item with validated stock access."""

    def __init__(self, sku, stock, reorder_threshold, unit_price):
        self.sku               = sku
        self.reorder_threshold = reorder_threshold
        self.unit_price        = unit_price
        self._stock            = stock    # private backing variable

    # --- @property: getter ---
    @property
    def stock(self):
        """Current stock level."""
        return self._stock

    # --- @stock.setter: validated write ---
    @stock.setter
    def stock(self, value):
        if not isinstance(value, int):
            raise TypeError(f"stock must be an int, got {type(value).__name__}")
        if value < 0:
            raise ValueError(f"stock cannot be negative (got {value})")
        self._stock = value

    # --- read-only computed properties (no setter) ---

    @property
    def needs_reorder(self):
        """True when stock is at or below the reorder threshold."""
        return self._stock <= self.reorder_threshold

    @property
    def status(self):
        """Human-readable stock status."""
        if self._stock == 0:
            return "OUT OF STOCK"
        if self.needs_reorder:
            return "REORDER"
        return "OK"

    @property
    def total_value(self):
        """Monetary value of all units currently in stock."""
        return self._stock * self.unit_price

    def dispatch(self, quantity):
        """Remove `quantity` units from stock."""
        if quantity > self._stock:
            raise ValueError(
                f"cannot dispatch {quantity} units — only {self._stock} available"
            )
        self.stock = self._stock - quantity   # goes through the setter

    def __str__(self):
        return (f"{self.sku:<20} stock={self.stock:<4} "
                f"needs_reorder={self.needs_reorder}   status={self.status}")


# --- demo ---
item = InventoryItem("TENT-3P-GRN", stock=312, reorder_threshold=50, unit_price=89.99)

print("=== Properties ===")
print(item)

print("\nDispatching 300 units...")
item.dispatch(300)
print(item)

# --- validation ---
print()
print("=== Validation ===")
try:
    item.stock = -5
except ValueError as e:
    print(f"Setting stock to -5: ValueError: {e}")

item.stock = 50
print(f"Setting stock to 50: stock={item.stock}")

# --- read-only property ---
print()
print("=== Read-only ===")
try:
    item.needs_reorder = True
except AttributeError as e:
    print(f"AttributeError: {e}")

# --- computed total_value ---
print()
print("=== Computed properties ===")
items = [
    InventoryItem("TENT-3P-GRN",   312, 50,  89.99),
    InventoryItem("PACK-45L-BLK",   88, 30, 149.99),
    InventoryItem("SLEEP-REG-BLU",  14, 20,  59.99),
    InventoryItem("JACKET-M-RED",    0, 25, 149.99),
]
total_stock_value = sum(i.total_value for i in items)
print(f"Total inventory value: ${total_stock_value:,.2f}")
for i in items:
    print(f"  {i.sku:<22} ${i.total_value:>8,.2f}")
