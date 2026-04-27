"""Solutions — None and truthiness exercises (04_ex1 and 04_ex2).

Do not open this file until you have attempted both exercises yourself.
"""


# ── Exercise 1 ────────────────────────────────────────────────────────────────

def validate_shipment(shipment):
    if not shipment.get("tracking_number"):   # catches None and "" — both mean "missing"
        return False, "missing tracking number"
    if not shipment.get("carrier"):           # catches None and "" — both mean "missing"
        return False, "missing carrier"
    weight_kg = shipment.get("weight_kg")
    if weight_kg is None:                     # None means "not provided" — separate from 0
        return False, "missing weight"
    if weight_kg <= 0:                        # 0 and negative are invalid values
        return False, "invalid weight"
    return True, None


# ── Exercise 2 ────────────────────────────────────────────────────────────────

def fixed_validate(order):
    if order["status"] is None:               # Bug 1 fixed: `is None` not `== "None"`
        return False, "missing status"

    quantity = order.get("quantity")
    if quantity is None or quantity <= 0:     # Bug 2 fixed: catches None, 0, and negatives
        return False, "no quantity"

    warehouse = order.get("warehouse")
    if not warehouse:                         # Bug 3 fixed: `not warehouse` catches None and ""
        return False, "missing warehouse"

    return True, None


# ─── verify all solutions ─────────────────────────────────────────────────────

assert validate_shipment({"tracking_number": "TRK-001", "carrier": "FedEx", "weight_kg": 5.2})  == (True,  None)
assert validate_shipment({"tracking_number": "",         "carrier": "UPS",   "weight_kg": 2.1})  == (False, "missing tracking number")
assert validate_shipment({"tracking_number": None,       "carrier": "UPS",   "weight_kg": 2.1})  == (False, "missing tracking number")
assert validate_shipment({"tracking_number": "TRK-003", "carrier": None,    "weight_kg": 8.0})  == (False, "missing carrier")
assert validate_shipment({"tracking_number": "TRK-004", "carrier": "",      "weight_kg": 8.0})  == (False, "missing carrier")
assert validate_shipment({"tracking_number": "TRK-005", "carrier": "FedEx", "weight_kg": None}) == (False, "missing weight")
assert validate_shipment({"tracking_number": "TRK-006", "carrier": "DHL",   "weight_kg": 0})    == (False, "invalid weight")
assert validate_shipment({"tracking_number": "TRK-007", "carrier": "DHL",   "weight_kg": -1})   == (False, "invalid weight")

assert fixed_validate({"status": None,      "quantity": 5,    "warehouse": "north"}) == (False, "missing status")
assert fixed_validate({"status": "pending", "quantity": None, "warehouse": "north"}) == (False, "no quantity")
assert fixed_validate({"status": "pending", "quantity": -1,   "warehouse": "north"}) == (False, "no quantity")
assert fixed_validate({"status": "pending", "quantity": 0,    "warehouse": "north"}) == (False, "no quantity")
assert fixed_validate({"status": "pending", "quantity": 3,    "warehouse": ""})      == (False, "missing warehouse")
assert fixed_validate({"status": "pending", "quantity": 3,    "warehouse": None})    == (False, "missing warehouse")
assert fixed_validate({"status": "pending", "quantity": 3,    "warehouse": "north"}) == (True,  None)

print("All solutions verified.")
