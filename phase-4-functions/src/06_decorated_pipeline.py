"""Challenge 6 — Decorated pipeline (capstone).

The dispatch function from Phase 3 is unchanged.
Timing and logging are added as decorators.
A closure pre-binds inventory and prices so callers pass only the order.
"""
import time
import functools

# --- decorators ---

def timed(func):
    """Record how long each call takes and attach it to the result."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        wrapper.last_ms = elapsed
        return result
    wrapper.last_ms = 0.0
    return wrapper


def logged(func):
    """Print an entry/exit line for every call."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract order_id, sku, qty from the first positional arg (the order dict)
        order = args[0] if args else {}
        oid   = order.get("order_id", "?")
        sku   = order.get("sku", "?")
        qty   = order.get("quantity", "?")
        print(f"→ dispatch({oid}, {sku}, qty={qty})")
        try:
            result = func(*args, **kwargs)
            ms = getattr(func, "last_ms", 0.0)
            if result is None:
                print(f"← dispatch OK  (cancelled)  [{ms:.1f}ms]")
            else:
                print(f"← dispatch OK  ${result:<9.2f} [{ms:.1f}ms]")
            return result
        except Exception as e:
            ms = getattr(func, "last_ms", 0.0)
            print(f"← dispatch ERR {e}  [{ms:.1f}ms]")
            return None
    return wrapper


# --- core dispatch (unchanged from Phase 3 logic) ---

class OrderError(Exception):
    pass


@timed
def _dispatch_core(order, inventory, prices):
    """Dispatch one order. Returns total value or None for cancelled."""
    if order.get("status") == "cancelled":
        return None

    sku      = order["sku"]
    quantity = order["quantity"]

    if quantity <= 0:
        raise OrderError("zero quantity")
    if sku not in inventory:
        raise OrderError(f"unknown SKU: {sku}")

    stock = inventory[sku]["stock"]
    if stock == 0:
        raise OrderError("out of stock")
    if stock < quantity:
        raise OrderError(f"insufficient stock (need {quantity}, have {stock})")

    inventory[sku]["stock"] -= quantity
    return prices.get(sku, 0.0) * quantity


# --- factory: pre-bind inventory and prices via closure ---

def make_dispatcher(inventory, prices):
    """Return a logged dispatch function pre-bound to inventory and prices."""
    @logged
    def dispatch(order):
        return _dispatch_core(order, inventory, prices)
    return dispatch


# --- run ---

inventory = {
    "TENT-3P-GRN":   {"stock": 312, "reorder_threshold": 50},
    "PACK-45L-BLK":  {"stock":  88, "reorder_threshold": 30},
    "SLEEP-REG-BLU": {"stock":  14, "reorder_threshold": 20},
    "JACKET-M-RED":  {"stock":   0, "reorder_threshold": 25},
    "BOOT-42-BRN":   {"stock": 203, "reorder_threshold": 40},
}

prices = {
    "TENT-3P-GRN":   89.99,
    "PACK-45L-BLK":  149.99,
    "SLEEP-REG-BLU":  59.99,
    "JACKET-M-RED":  149.99,
    "BOOT-42-BRN":   119.99,
}

dispatch = make_dispatcher(inventory, prices)

orders = [
    {"order_id": "ORD-001", "sku": "TENT-3P-GRN",  "quantity": 2, "status": "pending"},
    {"order_id": "ORD-002", "sku": "PACK-45L-BLK",  "quantity": 1, "status": "pending"},
    {"order_id": "ORD-003", "sku": "SLEEP-REG-BLU", "quantity": 5, "status": "pending"},
    {"order_id": "ORD-004", "sku": "JACKET-M-RED",  "quantity": 4, "status": "pending"},
    {"order_id": "ORD-005", "sku": "BOOT-42-BRN",   "quantity": 2, "status": "pending"},
]

print("=== Decorated Pipeline ===")
print()

results     = [dispatch(o) for o in orders]
dispatched  = [v for v in results if v is not None and v > 0]
rejected    = [v for v in results if v is None or v == 0]
total_value = sum(dispatched)

print()
print("=== Summary ===")
print(f"Dispatched : {len(dispatched)}")
print(f"Rejected   : {len(orders) - len(dispatched)}")
print(f"Total value: ${total_value:,.2f}")
