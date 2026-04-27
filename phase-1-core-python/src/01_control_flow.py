"""Challenge 1 — Control flow.

Route and prioritise orders using if/elif/else, logical operators,
and the ternary expression.
"""

VALID_WAREHOUSES = {"north", "south", "west"}

order = {
    "order_id": "ORD-00142",
    "status": "pending",
    "customer_tier": "enterprise",
    "quantity": 5,
    "warehouse": "north",
}

# --- if / elif / else ---
if order["status"] == "cancelled":
    print(f"{order['order_id']} — skipped (cancelled)")
elif order["status"] == "shipped":
    print(f"{order['order_id']} — already shipped, archive it")
elif order["status"] == "pending":
    print(f"{order['order_id']} — needs processing")
else:
    print(f"{order['order_id']} — unknown status: {order['status']}")

# --- logical operators: and, or, not ---
tier     = order["customer_tier"]
quantity = order["quantity"]

if tier == "enterprise" or tier == "pro":
    print(f"{tier} order: flag for priority handling")

if order["warehouse"] not in VALID_WAREHOUSES:
    print(f"warning: unknown warehouse '{order['warehouse']}'")
else:
    pass   # warehouse is valid — nothing to do

# --- chained comparisons ---
if 1 <= quantity <= 12:
    print(f"quantity {quantity} is within single-pallet limit")
elif quantity > 12:
    print(f"quantity {quantity} needs multi-pallet handling")

# --- ternary expression ---
label = "priority" if tier == "enterprise" else "standard"
print(f"Handling: {label}")

# --- nested conditions (flattened with early logic) ---
print()
print("--- Warehouse routing check ---")
for status, wh, qty in [
    ("pending",   "north",   5),
    ("cancelled", "south",   1),
    ("pending",   "unknown", 3),
    ("pending",   "west",    0),
    ("pending",   "west",   10),
]:
    if status == "cancelled":
        print(f"  skip  — cancelled")
        continue
    if wh not in VALID_WAREHOUSES:
        print(f"  error — invalid warehouse '{wh}'")
        continue
    if qty <= 0:
        print(f"  error — zero quantity")
        continue
    print(f"  route to {wh} (qty={qty})")


# ─── YOUR TURN ───────────────────────────────────────────────────────────────
#
# Three exercises below. Write your code in the marked sections.
# Run `python3 src/01_control_flow.py` after each exercise to verify.
# Try writing from memory — look at the demo above only if you're stuck.
# ─────────────────────────────────────────────────────────────────────────────

# Exercise 1 — if/elif/else
# --------------------------
# Write an if/elif/else block for `ex1_tier` that prints:
#   "priority queue"  when tier is "enterprise"
#   "standard queue"  when tier is "pro"
#   "self-service"    for any other tier
#
# Expected output:
#   priority queue

ex1_tier = "enterprise"

# write your code here


# Exercise 2 — Logical operators
# --------------------------------
# Using `ex2_tier` and `ex2_quantity`, write:
#   a) An `if` with `and` that prints "bulk enterprise — escalate" only
#      when tier is "enterprise" AND quantity is greater than 10.
#   b) An `if` with `or` that prints "paid customer" when tier is
#      "enterprise" or "pro".
#
# Expected output:
#   bulk enterprise — escalate
#   paid customer

ex2_tier     = "enterprise"
ex2_quantity = 15

# write your code here


# Exercise 3 — Ternary expression + chained comparison
# -----------------------------------------------------
# a) Use a ternary expression to set `urgency` to "urgent" if
#    ex3_quantity > 10, else "normal". Print: f"urgency: {urgency}"
# b) Use a chained comparison to check if ex3_quantity is between
#    1 and 20 inclusive. If True, print "standard pallet".
#
# Expected output:
#   urgency: urgent
#   standard pallet

ex3_quantity = 15

# write your code here
