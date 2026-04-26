"""Challenge 1 — *args and **kwargs.

Flexible function signatures for batch operations and logging.
"""

# --- *args: variable positional arguments ---

def batch_value(*amounts):
    """Return the sum of any number of order values."""
    return sum(amounts)


values = [179.98, 149.99, 299.95, 959.92, 239.98, 89.99, 1079.88]

print("=== *args ===")
print(f"batch_value(179.98)                    → ${batch_value(179.98):.2f}")
print(f"batch_value(179.98, 149.99, 299.95)   → ${batch_value(179.98, 149.99, 299.95):.2f}")
print(f"batch_value(*values)                   → ${batch_value(*values):,.2f}")


# --- **kwargs: variable keyword arguments ---

def create_order(**fields):
    """Build an order dict from keyword arguments."""
    required = {"order_id", "sku", "quantity"}
    missing  = required - fields.keys()
    if missing:
        raise ValueError(f"missing required fields: {missing}")
    fields.setdefault("warehouse", "north")
    fields.setdefault("status",    "pending")
    return fields


print()
print("=== **kwargs ===")
order = create_order(order_id="ORD-001", sku="TENT-3P-GRN", quantity=2, warehouse="north")
print(f"create_order(...)  → {order}")


# --- keyword-only parameters (after *) ---

def dispatch(sku, quantity, *, dry_run=False, warehouse="north"):
    """Dispatch an order. dry_run and warehouse are keyword-only."""
    if dry_run:
        print(f"dispatch {sku} qty={quantity} warehouse={warehouse} dry_run=True  [DRY RUN — no stock change]")
    else:
        print(f"dispatch {sku} qty={quantity} warehouse={warehouse} dry_run=False")


print()
print("=== keyword-only ===")
dispatch("TENT-3P-GRN", 2)
dispatch("TENT-3P-GRN", 2, warehouse="south", dry_run=True)

try:
    dispatch("TENT-3P-GRN", 2, True)   # dry_run is keyword-only — cannot be positional
except TypeError as e:
    print(f"TypeError (expected): {e}")


# --- combining *args, **kwargs, and keyword-only ---

def log(message, *tags, level="INFO", **context):
    """Flexible logger: log(msg, tag1, tag2, level=..., key=val, ...)"""
    tag_str = " ".join(f"[{t}]" for t in tags)
    ctx_str = " ".join(f"{k}={v}" for k, v in context.items())
    print(f"[{level:<7}] {tag_str:<15} {message} {ctx_str}")


print()
print("=== log ===")
log("dispatched", "orders", "north", order_id="ORD-001", value=179.98)
log("low stock",  "stock",           level="WARNING", sku="SLEEP-REG-BLU", remaining=4)
