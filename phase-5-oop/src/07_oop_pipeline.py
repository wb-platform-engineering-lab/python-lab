"""Challenge 7 — OOP pipeline (capstone).

The Meridian pipeline rebuilt with a full object-oriented design:
  Order          — @dataclass with validation and a classmethod constructor
  Product        — @dataclass with value_of() method
  Inventory      — class with @property, dispatch(), and reorder reporting
  OrderProcessor — orchestrates the pipeline; no raw dicts anywhere
"""
from dataclasses import dataclass, field
from typing import Optional


# ── Order ─────────────────────────────────────────────────────────────────────

@dataclass
class Order:
    order_id:      str
    sku:           str
    quantity:      int
    warehouse:     str
    customer_tier: str
    status:        str = "pending"

    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError(f"{self.order_id}: quantity cannot be negative")

    @classmethod
    def from_dict(cls, data):
        return cls(
            order_id      = data["order_id"],
            sku           = data["sku"],
            quantity      = int(data["quantity"]),
            warehouse     = data["warehouse"],
            customer_tier = data.get("customer_tier", "free"),
            status        = data.get("status", "pending"),
        )

    def is_pending(self):
        return self.status == "pending"


# ── Product ───────────────────────────────────────────────────────────────────

@dataclass
class Product:
    sku:        str
    name:       str
    unit_price: float

    def value_of(self, quantity):
        return self.unit_price * quantity


# ── Inventory ─────────────────────────────────────────────────────────────────

class OrderError(Exception):
    pass


class Inventory:
    """Tracks stock levels and handles dispatch."""

    def __init__(self, stock_data, products):
        # stock_data: dict of sku → {"stock": int, "reorder_threshold": int}
        self._stock     = {sku: info["stock"] for sku, info in stock_data.items()}
        self._threshold = {sku: info["reorder_threshold"] for sku, info in stock_data.items()}
        self._products  = {p.sku: p for p in products}

    @property
    def sku_count(self):
        return len(self._stock)

    @property
    def total_units(self):
        return sum(self._stock.values())

    def stock(self, sku):
        return self._stock.get(sku, 0)

    def dispatch(self, order):
        """Dispatch an order. Returns the order value on success.

        Returns None for cancelled orders.
        Raises OrderError on any failure.
        """
        if order.status == "cancelled":
            return None

        sku = order.sku
        qty = order.quantity

        if qty <= 0:
            raise OrderError("zero quantity")
        if sku not in self._stock:
            raise OrderError(f"unknown SKU: {sku}")

        current = self._stock[sku]
        if current == 0:
            raise OrderError("out of stock")
        if current < qty:
            raise OrderError(f"insufficient stock (need {qty}, have {current})")

        self._stock[sku] -= qty
        product = self._products.get(sku)
        return product.value_of(qty) if product else 0.0

    def reorder_report(self):
        """Return list of (sku, stock, threshold) for items needing reorder."""
        return [
            (sku, self._stock[sku], self._threshold[sku])
            for sku in sorted(self._stock)
            if self._stock[sku] <= self._threshold[sku]
        ]


# ── OrderProcessor ────────────────────────────────────────────────────────────

@dataclass
class DispatchResult:
    order:  Order
    value:  Optional[float]   # None if rejected
    reason: Optional[str]     # None if dispatched

    @property
    def dispatched(self):
        return self.value is not None


class OrderProcessor:
    """Processes a batch of orders against an inventory."""

    def __init__(self, inventory):
        self._inventory = inventory
        self._results   = []

    def process(self, orders):
        for order in orders:
            try:
                value = self._inventory.dispatch(order)
            except OrderError as e:
                self._results.append(DispatchResult(order, value=None, reason=str(e)))
                continue

            if value is None:
                self._results.append(DispatchResult(order, value=None, reason="cancelled"))
            else:
                self._results.append(DispatchResult(order, value=value, reason=None))

    def print_log(self):
        for r in self._results:
            oid   = r.order.order_id
            sku   = r.order.sku
            qty   = r.order.quantity
            value = f"${r.value:<9.2f}" if r.dispatched else f"{'—':<10}"
            status = "dispatched" if r.dispatched else f"rejected: {r.reason}"
            print(f"{oid}  {sku:<20} qty={qty}   {value} {status}")

    def print_summary(self):
        dispatched = [r for r in self._results if r.dispatched]
        rejected   = [r for r in self._results if not r.dispatched]
        total      = sum(r.value for r in dispatched)
        fill_rate  = len(dispatched) / len(self._results) if self._results else 0

        print(f"\n=== Results ===")
        print(f"Dispatched : {len(dispatched)}  (${total:.2f})")
        print(f"Rejected   : {len(rejected)}")
        print(f"Fill rate  : {fill_rate:.1%}")


# ── run ───────────────────────────────────────────────────────────────────────

products = [
    Product("TENT-3P-GRN",   "3-Person Tent",       89.99),
    Product("PACK-45L-BLK",  "45L Backpack",        149.99),
    Product("SLEEP-REG-BLU", "Regular Sleeping Bag", 59.99),
    Product("JACKET-M-RED",  "Mountain Jacket",     149.99),
    Product("BOOT-42-BRN",   "Hiking Boot",         119.99),
]

stock_data = {
    "TENT-3P-GRN":   {"stock": 312, "reorder_threshold": 50},
    "PACK-45L-BLK":  {"stock":  88, "reorder_threshold": 30},
    "SLEEP-REG-BLU": {"stock":  14, "reorder_threshold": 20},
    "JACKET-M-RED":  {"stock":   0, "reorder_threshold": 25},
    "BOOT-42-BRN":   {"stock": 203, "reorder_threshold": 40},
}

order_data = [
    {"order_id": "ORD-001", "sku": "TENT-3P-GRN",   "quantity": "2", "warehouse": "north", "customer_tier": "enterprise"},
    {"order_id": "ORD-002", "sku": "PACK-45L-BLK",  "quantity": "1", "warehouse": "south", "customer_tier": "pro"},
    {"order_id": "ORD-003", "sku": "SLEEP-REG-BLU", "quantity": "5", "warehouse": "west",  "customer_tier": "free"},
    {"order_id": "ORD-004", "sku": "JACKET-M-RED",  "quantity": "4", "warehouse": "north", "customer_tier": "enterprise"},
    {"order_id": "ORD-005", "sku": "BOOT-42-BRN",   "quantity": "2", "warehouse": "south", "customer_tier": "pro"},
    {"order_id": "ORD-006", "sku": "TENT-3P-GRN",   "quantity": "1", "warehouse": "west",  "customer_tier": "free"},
    {"order_id": "ORD-007", "sku": "PACK-45L-BLK",  "quantity": "3", "warehouse": "south", "customer_tier": "enterprise", "status": "cancelled"},
    {"order_id": "ORD-008", "sku": "SLEEP-REG-BLU", "quantity": "6", "warehouse": "north", "customer_tier": "pro"},
]

inventory = Inventory(stock_data, products)
orders    = [Order.from_dict(d) for d in order_data]
processor = OrderProcessor(inventory)

print("=== Meridian OOP Pipeline ===")
print(f"Inventory: {inventory.sku_count} SKUs, {inventory.total_units} total units")
print(f"\nProcessing {len(orders)} orders...\n")

processor.process(orders)
processor.print_log()
processor.print_summary()

print("\n=== Reorder Report ===")
for sku, stock, threshold in inventory.reorder_report():
    print(f"{sku:<20} stock={stock:<4} threshold={threshold:<4} ← REORDER")
