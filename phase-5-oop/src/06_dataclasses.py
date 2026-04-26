"""Challenge 6 — Dataclasses.

@dataclass eliminates __init__ boilerplate.
__post_init__ adds validation.
frozen=True creates immutable, hashable records.
order=True enables sorting.
"""
from dataclasses import dataclass, field


# --- basic @dataclass ---

@dataclass
class Order:
    order_id:  str
    sku:       str
    quantity:  int
    warehouse: str
    status:    str  = "pending"
    tags:      list = field(default_factory=list)   # mutable default must use field()

    def __post_init__(self):
        """Runs automatically after __init__. Use for validation."""
        if self.quantity < 0:
            raise ValueError(f"quantity cannot be negative: {self.quantity}")
        if not self.order_id.startswith("ORD-"):
            raise ValueError(f"order_id must start with 'ORD-': {self.order_id}")


print("=== @dataclass ===")
o1 = Order("ORD-001", "TENT-3P-GRN",   2, "north")
o2 = Order("ORD-002", "PACK-45L-BLK",  1, "south", tags=["fragile"])
print(o1)
print(o2)

# __eq__ is generated automatically
o1_copy = Order("ORD-001", "TENT-3P-GRN", 2, "north")
print(f"\no1 == o1_copy : {o1 == o1_copy}")   # True — same field values

# --- __post_init__ validation ---
print()
print("=== __post_init__ validation ===")
try:
    o3 = Order("ORD-003", "SLEEP-REG-BLU", 5, "west")
    print(f"Created: {o3}")
except ValueError as e:
    print(f"ValueError: {e}")

try:
    Order("ORD-004", "BOOT-42-BRN", -1, "north")
except ValueError as e:
    print(f"ValueError: {e}")


# --- frozen=True: immutable and hashable ---

@dataclass(frozen=True)
class ProductKey:
    """A composite key identifying a SKU at a specific warehouse."""
    sku:       str
    warehouse: str


print()
print("=== frozen dataclass ===")
key = ProductKey(sku="TENT-3P-GRN", warehouse="north")
print(f"key = {key}")

stock_by_key = {
    ProductKey("TENT-3P-GRN", "north"): 100,
    ProductKey("TENT-3P-GRN", "south"): 80,
    ProductKey("PACK-45L-BLK", "north"): 50,
}
print(f"Hashable — can be dict key: stock={stock_by_key[key]}")

try:
    key.sku = "OTHER"
except Exception as e:
    print(f"FrozenInstanceError on mutation: {type(e).__name__}")


# --- order=True: automatic comparison for sorting ---

@dataclass(order=True)
class StockLevel:
    stock: int
    sku:   str   # secondary sort key when stocks are equal


print()
print("=== order=True ===")
levels = [
    StockLevel(88,  "PACK-45L-BLK"),
    StockLevel(312, "TENT-3P-GRN"),
    StockLevel(0,   "JACKET-M-RED"),
    StockLevel(14,  "SLEEP-REG-BLU"),
    StockLevel(203, "BOOT-42-BRN"),
]
print("Sorted by stock:")
for s in sorted(levels):
    print(f"  {s}")
