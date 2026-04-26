"""Challenge 4 — None and truthiness.

Validate orders using None checks and Python's truthiness rules.
Demonstrates the difference between `if x` and `if x is not None`.
"""


def validate_order(order):
    """Return (is_valid, reason) for the given order dict.

    Returns (True, None) if valid, (False, reason_string) if not.
    """
    if order.get("status") == "cancelled":
        return False, "cancelled"

    warehouse = order.get("warehouse")
    if not warehouse:                        # catches None and ""
        return False, "missing warehouse"

    quantity = order.get("quantity")
    if quantity is None:                     # None means "not provided"
        return False, "missing quantity"
    if quantity == 0:                        # 0 is a valid int but means nothing to ship
        return False, "quantity is 0"
    if quantity < 0:
        return False, "negative quantity"

    return True, None


# --- run the validation ---
orders = [
    {"order_id": "ORD-001", "status": "pending",   "warehouse": "north", "quantity": 2},
    {"order_id": "ORD-002", "status": "pending",   "warehouse": "",      "quantity": 1},
    {"order_id": "ORD-003", "status": "pending",   "warehouse": "west",  "quantity": 0},
    {"order_id": "ORD-004", "status": "pending",   "warehouse": "west",  "quantity": 8},
    {"order_id": "ORD-005", "status": "cancelled", "warehouse": "south", "quantity": 3},
]

print("=== Order Validation ===")
valid_count   = 0
invalid_count = 0

for order in orders:
    is_valid, reason = validate_order(order)
    oid = order["order_id"]

    if is_valid:
        valid_count += 1
        wh  = order["warehouse"]
        qty = order["quantity"]
        print(f"{oid}: valid   — {qty} units, warehouse={wh}")
    else:
        invalid_count += 1
        print(f"{oid}: invalid — {reason}")

print()
print(f"Valid orders   : {valid_count}")
print(f"Invalid orders : {invalid_count}")

# --- truthiness table ---
print()
print("--- Truthiness of common values ---")
values = [None, 0, 0.0, "", [], {}, "north", 1, [1], {"a": 1}]
for v in values:
    label = "truthy" if v else "falsy "
    print(f"  {label}  {repr(v)}")

# --- the trap: 0 is falsy but is not None ---
print()
print("--- The 0 trap ---")
quantity = 0

print(f"quantity = {quantity}")
print(f"  if quantity           → {'enters' if quantity else 'skips'} (0 is falsy)")
print(f"  if quantity is None   → {'enters' if quantity is None else 'skips'} (0 is not None)")
print(f"  if quantity is not None → {'enters' if quantity is not None else 'skips'}")
