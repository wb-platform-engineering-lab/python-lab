"""Challenge 5 — Custom exceptions.

A typed exception hierarchy for Meridian order processing.
Callers can catch MeridianError for anything, OrderError for
order-specific problems, or the specific leaf class for precise handling.
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


# --- exception hierarchy ---

class MeridianError(Exception):
    """Base class for all Meridian application errors."""


class OrderError(MeridianError):
    """Raised when an order cannot be processed."""


class UnknownSKUError(OrderError):
    def __init__(self, sku):
        self.sku = sku
        super().__init__(f"unknown SKU: {sku}")


class ZeroQuantityError(OrderError):
    def __init__(self, order_id):
        self.order_id = order_id
        super().__init__(f"{order_id}: zero quantity")


class OutOfStockError(OrderError):
    def __init__(self, sku):
        self.sku = sku
        super().__init__(f"{sku}: out of stock")


class InsufficientStockError(OrderError):
    def __init__(self, sku, requested, available):
        self.sku       = sku
        self.requested = requested
        self.available = available
        super().__init__(f"{sku}: requested {requested}, only {available} available")


# --- dispatch using custom exceptions ---

def load_inventory(path):
    with open(path) as f:
        return json.load(f)


def dispatch(order, inventory, prices):
    """Dispatch an order. Returns total value on success. Raises OrderError on failure."""
    if order["status"] == "cancelled":
        return None

    order_id = order["order_id"]
    sku      = order["sku"]
    quantity = order["quantity"]

    if quantity <= 0:
        raise ZeroQuantityError(order_id)
    if sku not in inventory:
        raise UnknownSKUError(sku)

    stock = inventory[sku]["stock"]
    if stock == 0:
        raise OutOfStockError(sku)
    if stock < quantity:
        raise InsufficientStockError(sku, quantity, stock)

    inventory[sku]["stock"] -= quantity
    unit_price = prices.get(sku, 0.0)
    return unit_price * quantity


# --- demo ---
inventory = load_inventory(DATA_DIR / "inventory.json")

prices = {
    "TENT-3P-GRN":   89.99,
    "PACK-45L-BLK":  149.99,
    "SLEEP-REG-BLU":  59.99,
    "JACKET-M-RED":  149.99,
    "BOOT-42-BRN":   119.99,
}

test_orders = [
    {"order_id": "ORD-001", "sku": "TENT-3P-GRN",   "quantity": 2,  "status": "pending"},
    {"order_id": "ORD-004", "sku": "JACKET-M-RED",  "quantity": 4,  "status": "pending"},
    {"order_id": "ORD-009", "sku": "JACKET-M-RED",  "quantity": 0,  "status": "pending"},
    {"order_id": "ORD-011", "sku": "TENT-3P-GRN",   "quantity": 50, "status": "pending"},
    {"order_id": "ORD-012", "sku": "UNKNOWN-SKU",   "quantity": 2,  "status": "pending"},
]

print("=== Dispatch with custom exceptions ===")
for order in test_orders:
    oid = order["order_id"]
    sku = order["sku"]
    qty = order["quantity"]
    try:
        value = dispatch(order, inventory, prices)
        if value is None:
            print(f"{oid}  {sku:<20} qty={qty:<3} → cancelled")
        else:
            print(f"{oid}  {sku:<20} qty={qty:<3} → dispatched (${value:.2f})")
    except OrderError as e:
        print(f"{oid}  {sku:<20} qty={qty:<3} → OrderError: {e}")

# --- catching by specific type ---
# Use a tight inventory to guarantee InsufficientStockError
print()
print("Catching by specific type:")
tight_inventory = {"TENT-3P-GRN": {"stock": 5, "reorder_threshold": 10}}
order = {"order_id": "ORD-011", "sku": "TENT-3P-GRN", "quantity": 50, "status": "pending"}
try:
    dispatch(order, tight_inventory, prices)
except InsufficientStockError as e:
    print(f"  InsufficientStockError on {order['order_id']}: sku={e.sku} requested={e.requested} available={e.available}")
except OrderError as e:
    print(f"  OrderError: {e}")
