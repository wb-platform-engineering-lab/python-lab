"""Challenge 2 — Loops.

Process a batch of orders using for, while, break, continue,
enumerate, and zip.
"""

orders = [
    {"order_id": "ORD-001", "status": "pending",   "warehouse": "north", "quantity": 2},
    {"order_id": "ORD-002", "status": "cancelled", "warehouse": "south", "quantity": 1},
    {"order_id": "ORD-003", "status": "pending",   "warehouse": "west",  "quantity": 5},
    {"order_id": "ORD-004", "status": "pending",   "warehouse": "north", "quantity": 12},
    {"order_id": "ORD-005", "status": "shipped",   "warehouse": "south", "quantity": 3},
]

# --- for loop over a list ---
print(f"=== Batch Processing {len(orders)} orders ===")

dispatched = 0
skipped    = 0
archived   = 0

for index, order in enumerate(orders):
    order_id  = order["order_id"]
    status    = order["status"]
    warehouse = order["warehouse"]
    qty       = order["quantity"]
    position  = f"[{index + 1}/{len(orders)}]"

    if status == "cancelled":
        result = "skipped"
        skipped += 1
    elif status == "shipped":
        result = "already shipped"
        archived += 1
    else:
        result = "dispatched"
        dispatched += 1

    print(f"{position} {order_id:<8} {status:<10} {warehouse:<7} qty={qty:<3} → {result}")

print()
print(f"Dispatched : {dispatched}")
print(f"Skipped    : {skipped}")
print(f"Archived   : {archived}")

# --- range() ---
print()
print("--- range() examples ---")
print("range(5)         :", list(range(5)))
print("range(1, 6)      :", list(range(1, 6)))
print("range(0, 50, 10) :", list(range(0, 50, 10)))

# --- zip() — two lists in parallel ---
print()
print("--- zip() ---")
skus       = ["TENT-3P-GRN", "PACK-45L-BLK", "SLEEP-REG-BLU"]
quantities = [2, 1, 3]

for sku, qty in zip(skus, quantities):
    print(f"  {sku:<22} qty={qty}")

# --- while loop: retry logic ---
print()
print("--- while: warehouse API retry ---")

retries     = 0
max_retries = 3
connected   = False

while not connected and retries < max_retries:
    retries += 1
    print(f"  Attempt {retries}: connecting to warehouse API...")
    if retries == 2:
        connected = True

print(f"  {'Connected.' if connected else 'Failed after ' + str(max_retries) + ' attempts.'}")

# --- break and continue ---
print()
print("--- break and continue ---")
batch = ["ORD-010", "ORD-011", "ORD-012", "STOP", "ORD-014"]

for order_id in batch:
    if order_id.startswith("ORD-01") and order_id == "ORD-011":
        print(f"  {order_id} — skipping (on hold)")
        continue
    if order_id == "STOP":
        print(f"  Stop signal received — halting batch")
        break
    print(f"  {order_id} — processed")


# ─── YOUR TURN ───────────────────────────────────────────────────────────────
#
# Four exercises below. Work through them in order.
# Run `python3 src/02_loops.py` after each one to verify.
# ─────────────────────────────────────────────────────────────────────────────

# Exercise 1 — for loop + counter
# --------------------------------
# Loop over `ex1_orders` using a for loop.
# Count how many have status "pending" using an if statement and a counter.
# At the end, print: "Pending orders: 3"
#
# Do NOT use built-ins like sum() or list.count() — write the loop yourself.
#
# Expected output:
#   Pending orders: 3

ex1_orders = [
    {"order_id": "A-001", "status": "pending"},
    {"order_id": "A-002", "status": "cancelled"},
    {"order_id": "A-003", "status": "pending"},
    {"order_id": "A-004", "status": "shipped"},
    {"order_id": "A-005", "status": "pending"},
]

# write your code here


# Exercise 2 — enumerate()
# -------------------------
# Print each warehouse with a 1-based position number.
# Use enumerate() — do not use range(len(...)).
#
# Expected output:
#   1. north
#   2. south
#   3. west

ex2_warehouses = ["north", "south", "west"]

# write your code here


# Exercise 3 — zip()
# -------------------
# Use zip() to print each SKU paired with its restock quantity.
# Expected output:
#   TENT-3P-GRN: restock 50 units
#   PACK-45L-BLK: restock 30 units
#   SLEEP-REG-BLU: restock 75 units

ex3_skus            = ["TENT-3P-GRN", "PACK-45L-BLK", "SLEEP-REG-BLU"]
ex3_restock_amounts = [50, 30, 75]

# write your code here


# Exercise 4 — while loop
# ------------------------
# Simulate polling for a shipment confirmation.
# Rules:
#   - Start: arrived=False, checks=0, max_checks=4
#   - Each iteration: increment checks, print "Check N: not yet..."
#   - On check 3: set arrived=True and break out of the loop
#   - After the loop: print "Shipment confirmed." or "Shipment not found."
#
# Expected output:
#   Check 1: not yet...
#   Check 2: not yet...
#   Check 3: not yet...
#   Shipment confirmed.

arrived    = False
checks     = 0
max_checks = 4

# write your code here
