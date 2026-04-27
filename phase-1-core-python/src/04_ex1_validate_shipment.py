"""Exercise 1 — validate_shipment with None and truthiness checks.

Implement `validate_shipment` using early returns.

Rules (check in this order):
  1. tracking_number is None or ""  → False, "missing tracking number"
  2. carrier is None or ""          → False, "missing carrier"
  3. weight_kg is None              → False, "missing weight"
  4. weight_kg <= 0                 → False, "invalid weight"
  5. otherwise                      → True, None

Return (is_valid, reason) as a tuple. Reason is None when valid.

Key distinction — this is the None trap:
  `if not weight_kg` catches None AND 0 — too broad for rules 3 vs 4.
  Use `if weight_kg is None` for rule 3 so that 0 is handled separately by rule 4.

  For rules 1 and 2 (strings), `if not value` is fine because both None
  and "" mean "nothing useful is here" — no need to distinguish them.

Run:
    python3 src/04_ex1_validate_shipment.py
"""


def validate_shipment(shipment):
    """Return (is_valid, reason). Reason is None when valid."""
    pass   # replace with your code


# ─── assertions ───────────────────────────────────────────────────────────────
assert validate_shipment({"tracking_number": "TRK-001", "carrier": "FedEx", "weight_kg": 5.2})  == (True,  None),                "valid shipment"
assert validate_shipment({"tracking_number": "",         "carrier": "UPS",   "weight_kg": 2.1})  == (False, "missing tracking number"), "empty tracking number"
assert validate_shipment({"tracking_number": None,       "carrier": "UPS",   "weight_kg": 2.1})  == (False, "missing tracking number"), "None tracking number"
assert validate_shipment({"tracking_number": "TRK-003", "carrier": None,    "weight_kg": 8.0})  == (False, "missing carrier"),    "None carrier"
assert validate_shipment({"tracking_number": "TRK-004", "carrier": "",      "weight_kg": 8.0})  == (False, "missing carrier"),    "empty carrier"
assert validate_shipment({"tracking_number": "TRK-005", "carrier": "FedEx", "weight_kg": None}) == (False, "missing weight"),     "None weight"
assert validate_shipment({"tracking_number": "TRK-006", "carrier": "DHL",   "weight_kg": 0})    == (False, "invalid weight"),     "zero weight"
assert validate_shipment({"tracking_number": "TRK-007", "carrier": "DHL",   "weight_kg": -1})   == (False, "invalid weight"),     "negative weight"

print("Exercise 1 passed.")
