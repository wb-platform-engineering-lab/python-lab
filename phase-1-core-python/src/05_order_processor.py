"""Challenge 5 — Mini order processor (your implementation).

This is the capstone for Phase 1. There is no demo code to read first —
your task is to implement all five functions below using only what you
have learned across challenges 1–4.

Strategy:
  1. Read each function's docstring carefully — the rules are all there.
  2. Implement one function at a time, starting from the top.
  3. Run `python3 src/05_order_processor.py` after each function.
     The output will be incomplete until all five are done, but running
     early helps you spot mistakes before they compound.
  4. Your final output must match the expected output in README.md exactly.

You can look back at 01_control_flow.py through 04_none_truthiness.py —
they each contain a complete worked example of the patterns you need here.
"""

VALID_WAREHOUSES = {"north", "south", "west"}

PRICES = {
    "TENT-3P-GRN":   89.99,
    "PACK-45L-BLK":  149.99,
    "SLEEP-REG-BLU": 59.99,
    "JACKET-M-RED":  149.99,
    "BOOT-42-BRN":   119.99,
}


# ── Function 1 of 5 ───────────────────────────────────────────────────────────

def validate_order(order):
    """Return (is_valid, reason). Reason is None when valid.

    Check each rule in order and return early on the first failure.

    Rules:
      1. status == "cancelled"                    → False, "cancelled"
      2. warehouse is missing or empty string     → False, "missing warehouse"
      3. warehouse not in VALID_WAREHOUSES        → False, f"unknown warehouse '{wh}'"
      4. quantity is None                         → False, "missing quantity"
      5. quantity <= 0                            → False, "zero quantity"
      6. all good                                 → True, None

    Hints:
      - Use order.get("field") to safely read a key — returns None if absent.
      - `if not warehouse` is True for both None and "" (empty string).
      - Use `if quantity is None` for rule 4 so that 0 is caught separately
        by rule 5 and not silently skipped by the truthiness check.
    """
    # write your code here
    pass


# ── Function 2 of 5 ───────────────────────────────────────────────────────────

def calculate_value(order, prices):
    """Return the total order value in dollars: unit_price × quantity.

    If the SKU is not in the prices dict, treat unit_price as 0.0.

    Hint: dict.get(key, default) returns `default` when the key is missing.
    """
    # write your code here
    pass


# ── Function 3 of 5 ───────────────────────────────────────────────────────────

def process_order(order, prices):
    """Validate and process a single order. Return a result dict.

    Steps:
      1. Call validate_order(order) to get (is_valid, reason).
      2. Build and return a dict with these keys:
           order_id, sku, tier, warehouse, quantity, value, status, reason

         When invalid:
           - status = "rejected"
           - value  = None
           - Use order.get() for all fields — some may be missing.
           - For warehouse: use `order.get("warehouse") or "—"` so that
             a missing/None warehouse shows up as "—" in the output.

         When valid:
           - status = "dispatched"
           - reason = None
           - value  = calculate_value(order, prices)
           - All fields are guaranteed to exist (validation passed).

    Hint: a dict literal looks like {"key": value, "key2": value2, ...}
    """
    # write your code here
    pass


# ── Function 4 of 5 ───────────────────────────────────────────────────────────

def process_batch(orders, prices):
    """Process every order and return a list of result dicts.

    Loop over orders, call process_order() for each, collect the results.

    Hint: start with an empty list and use .append() inside the loop.
    """
    # write your code here
    pass


# ── Function 5 of 5 ───────────────────────────────────────────────────────────

def print_summary(results):
    """Print the end-of-batch summary report.

    You need to calculate:
      dispatched  — list of results where status == "dispatched"
      rejected    — list of results where status == "rejected"
      total_value — sum of `value` for all dispatched results
      by_warehouse — dict mapping warehouse name → total dispatched value
      fill_rate   — len(dispatched) / len(results), or 0.0 if results is empty

    Then print in this format (spacing must match for the output to align):
      === End of Batch Summary ===
      Total orders    : 8
      Dispatched      : 6
      Rejected        : 2
      Batch value     : $1,829.84
      By warehouse    : north=$779.94  south=$599.96  west=$449.98
      Fill rate       : 75.0%

    Hints:
      - List comprehension: [r for r in results if r["status"] == "dispatched"]
      - Accumulate warehouse totals:
            by_warehouse[wh] = by_warehouse.get(wh, 0.0) + r["value"]
      - Sort warehouses: sorted(by_warehouse.items())
      - Format currency: f"${value:,.2f}"
      - Format percentage: f"{fill_rate:.1%}"
    """
    # write your code here
    pass


# ─── main script — do not modify below this line ─────────────────────────────

orders = [
    {"order_id": "ORD-001", "status": "pending",   "customer_tier": "enterprise", "warehouse": "north", "sku": "TENT-3P-GRN",   "quantity": 2},
    {"order_id": "ORD-002", "status": "pending",   "customer_tier": "pro",        "warehouse": "south", "sku": "PACK-45L-BLK",  "quantity": 1},
    {"order_id": "ORD-003", "status": "pending",   "customer_tier": "free",       "warehouse": "west",  "sku": "SLEEP-REG-BLU", "quantity": 0},
    {"order_id": "ORD-004", "status": "pending",   "customer_tier": "enterprise", "warehouse": "north", "sku": "JACKET-M-RED",  "quantity": 4},
    {"order_id": "ORD-005", "status": "pending",   "customer_tier": "pro",        "warehouse": None,    "sku": "BOOT-42-BRN",   "quantity": 2},
    {"order_id": "ORD-006", "status": "pending",   "customer_tier": "free",       "warehouse": "west",  "sku": "TENT-3P-GRN",   "quantity": 1},
    {"order_id": "ORD-007", "status": "cancelled", "customer_tier": "enterprise", "warehouse": "south", "sku": "PACK-45L-BLK",  "quantity": 3},
    {"order_id": "ORD-008", "status": "pending",   "customer_tier": "pro",        "warehouse": "north", "sku": "SLEEP-REG-BLU", "quantity": 6},
]

print("=== Meridian Order Processor ===")
print(f"Processing batch of {len(orders)} orders...")
print()

results = process_batch(orders, PRICES)

if results is None:
    print("(process_batch not implemented yet — implement all five functions and re-run)")
    raise SystemExit(0)

for r in results:
    oid   = r["order_id"]
    tier  = r["tier"]
    wh    = r["warehouse"]
    sku   = r["sku"]
    qty   = r["quantity"]
    value = f"${r['value']:,.2f}" if r["value"] is not None else "—"
    note  = f"({r['reason']})" if r["reason"] else ""
    print(f"{oid}  {tier:<12} {wh:<7} {sku:<20} qty={qty}  {value:<10} → {r['status']} {note}")

print_summary(results)
