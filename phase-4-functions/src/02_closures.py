"""Challenge 2 — Closures.

Inner functions that capture enclosing scope.
Factory functions that return pre-configured behaviour.
"""

# --- basic closure: multiplier factory ---

def make_multiplier(factor):
    """Return a function that multiplies its argument by factor."""
    def multiply(x):
        return x * factor    # factor is captured from make_multiplier's scope
    return multiply


double = make_multiplier(2)
triple = make_multiplier(3)

print("=== Multiplier factory ===")
print(f"double(50)  = {double(50)}")
print(f"triple(50)  = {triple(50)}")


# --- factory function: pre-configured validator ---

def make_validator(valid_warehouses, max_quantity):
    """Return a validation function configured with the given rules."""
    def validate(order):
        if order["status"] == "cancelled":
            return False, "cancelled"
        if order["warehouse"] not in valid_warehouses:
            return False, f"unknown warehouse: {order['warehouse']}"
        if order["quantity"] <= 0:
            return False, "zero quantity"
        if order["quantity"] > max_quantity:
            return False, f"quantity {order['quantity']} exceeds limit {max_quantity}"
        return True, None
    return validate


standard_validator   = make_validator({"north", "south", "west"}, max_quantity=50)
enterprise_validator = make_validator({"north", "south", "west"}, max_quantity=500)

test_orders = [
    {"order_id": "ORD-001", "sku": "TENT-3P-GRN",  "quantity": 2,  "warehouse": "north",   "status": "pending",   "tier": "standard"},
    {"order_id": "ORD-002", "sku": "PACK-45L-BLK",  "quantity": 75, "warehouse": "north",   "status": "pending",   "tier": "standard"},
    {"order_id": "ORD-003", "sku": "BOOT-42-BRN",   "quantity": 75, "warehouse": "north",   "status": "pending",   "tier": "enterprise"},
    {"order_id": "ORD-004", "sku": "SLEEP-REG-BLU", "quantity": 1,  "warehouse": "unknown", "status": "pending",   "tier": "standard"},
]

print()
print("=== Validator factory ===")
for o in test_orders:
    validator = enterprise_validator if o["tier"] == "enterprise" else standard_validator
    valid, reason = validator(o)
    result = "valid" if valid else f"invalid: {reason}"
    print(f"{o['order_id']}  {o['tier']:<11} {o['warehouse']:<7} qty={o['quantity']:<3} → {result}")


# --- counter closure with nonlocal ---

def make_counter(name):
    """Return an increment function that tracks its own count."""
    count = 0

    def increment(amount=1):
        nonlocal count      # reassign the enclosing variable
        count += amount
        return count

    def reset():
        nonlocal count
        count = 0

    increment.reset = reset
    increment.name  = name
    return increment


dispatched = make_counter("dispatched")
rejected   = make_counter("rejected")

dispatched()    # 1
dispatched()    # 2
dispatched(3)   # 5
rejected()      # 1
rejected()      # 2

print()
print("=== Counters ===")
print(f"dispatched: {dispatched()}   rejected: {rejected()}")

dispatched.reset()
print(f"After reset — dispatched: {dispatched()}")
