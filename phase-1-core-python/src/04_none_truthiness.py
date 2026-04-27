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


# ─── YOUR TURN ───────────────────────────────────────────────────────────────
#
# Two exercises. Read validate_order() above first — your exercise follows
# the same pattern.
# Run `python3 src/04_none_truthiness.py` to verify your output.
# ─────────────────────────────────────────────────────────────────────────────

# Exercise 1 — implement validate_shipment()
# -------------------------------------------
# A shipment dict has these fields: tracking_number, carrier, weight_kg
#
# Rules (check in this order, use early returns):
#   1. tracking_number is None or ""  → invalid, "missing tracking number"
#   2. carrier is None or ""          → invalid, "missing carrier"
#   3. weight_kg is None              → invalid, "missing weight"
#   4. weight_kg <= 0                 → invalid, "invalid weight"
#   5. Otherwise                      → valid, None
#
# Key distinction (same trap as in the demo above):
#   `if not weight_kg`  catches both None AND 0 — too broad for rule 3 vs 4.
#   Use `if weight_kg is None` for rule 3 so that 0 is handled separately.
#
# Return (is_valid, reason) — same shape as validate_order().

def validate_shipment(shipment):
    # write your code here
    pass


ex_shipments = [
    {"tracking_number": "TRK-001", "carrier": "FedEx", "weight_kg": 5.2},
    {"tracking_number": "",         "carrier": "UPS",   "weight_kg": 2.1},
    {"tracking_number": "TRK-003", "carrier": None,    "weight_kg": 8.0},
    {"tracking_number": "TRK-004", "carrier": "DHL",   "weight_kg": 0},
    {"tracking_number": "TRK-005", "carrier": "FedEx", "weight_kg": None},
]

print()
print("--- Your validate_shipment ---")
for s in ex_shipments:
    result = validate_shipment(s)
    if result is None:
        print("  (not implemented yet — validate_shipment returned None)")
        break
    is_valid, reason = result
    tn = s["tracking_number"] or "(empty)"
    status = "valid" if is_valid else f"invalid — {reason}"
    print(f"  {tn}: {status}")
# Expected:
#   TRK-001: valid
#   (empty): invalid — missing tracking number
#   TRK-003: invalid — missing carrier
#   TRK-004: invalid — invalid weight
#   TRK-005: invalid — missing weight


# Exercise 2 — fix the bugs
# --------------------------
# The function below has three bugs related to None checks and truthiness.
# Find and fix each one. The comment next to each bug describes what it
# should actually do.
#
# Hint: review the "trap" section above — the fixes all come from that concept.

def buggy_validate(order):
    if order["status"] == None:       # Bug 1: wrong way to check for None
        return False, "missing status"

    quantity = order.get("quantity")
    if quantity == False:             # Bug 2: catches False but not 0 or None
        return False, "no quantity"   #        should catch: quantity is None OR quantity <= 0

    warehouse = order.get("warehouse")
    if warehouse == "":               # Bug 3: misses the case where warehouse is None
        return False, "missing warehouse"

    return True, None


ex_bug_tests = [
    {"status": None,      "quantity": 5,    "warehouse": "north"},   # Bug 1 fires
    {"status": "pending", "quantity": 0,    "warehouse": "north"},   # Bug 2 fires (0)
    {"status": "pending", "quantity": None, "warehouse": "north"},   # Bug 2 fires (None)
    {"status": "pending", "quantity": 3,    "warehouse": ""},        # Bug 3 fires ("")
    {"status": "pending", "quantity": 3,    "warehouse": None},      # Bug 3 fires (None)
    {"status": "pending", "quantity": 3,    "warehouse": "north"},   # all valid
]

print()
print("--- Your fixed buggy_validate ---")
for t in ex_bug_tests:
    is_valid, reason = buggy_validate(t)
    result = "valid" if is_valid else f"invalid — {reason}"
    print(f"  status={str(t['status']):<8} qty={str(t['quantity']):<5} wh={str(t['warehouse']):<6} → {result}")
# Expected (all invalid except the last):
#   status=None     qty=5     wh=north  → invalid — missing status
#   status=pending  qty=0     wh=north  → invalid — no quantity
#   status=pending  qty=None  wh=north  → invalid — no quantity
#   status=pending  qty=3     wh=       → invalid — missing warehouse
#   status=pending  qty=3     wh=None   → invalid — missing warehouse
#   status=pending  qty=3     wh=north  → valid
