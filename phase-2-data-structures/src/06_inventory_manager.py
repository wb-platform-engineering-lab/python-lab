"""Challenge 6 — Inventory manager (capstone).

All four data structures working together:
  - dict  : stock levels per SKU (O(1) lookup and update)
  - set   : SKUs flagged for reorder (O(1) membership)
  - list  : incoming orders to process in sequence
  - tuple : composite (warehouse, sku) keys for per-warehouse stock
"""

REORDER_THRESHOLD = 20


def dispatch(stock, reorder_flags, sku, quantity):
    """Attempt to dispatch `quantity` units of `sku`.

    Updates stock dict and reorder_flags set in place.
    Returns (success, message).
    """
    current = stock.get(sku)

    if current is None:
        return False, "unknown SKU"
    if current == 0:
        return False, "out of stock"
    if current < quantity:
        return False, f"insufficient stock (need {quantity}, have {current})"

    stock[sku] -= quantity

    if stock[sku] <= REORDER_THRESHOLD:
        reorder_flags.add(sku)

    return True, None


def stock_report(stock, reorder_flags):
    """Print current stock levels sorted by SKU name."""
    print()
    print("Current stock:")
    for sku in sorted(stock):
        qty   = stock[sku]
        flag  = "  ← REORDER" if sku in reorder_flags else ""
        print(f"  {sku:<22} : {qty:>4}{flag}")

    flagged = sorted(reorder_flags)
    print(f"\nSKUs needing reorder : {flagged}")


# --- initial stock ---
stock = {
    "TENT-3P-GRN":   312,
    "PACK-45L-BLK":   88,
    "SLEEP-REG-BLU":  14,
    "JACKET-M-RED":    0,
    "BOOT-42-BRN":   203,
}

# pre-populate reorder flags for anything already below threshold
reorder_flags = {sku for sku, qty in stock.items() if qty <= REORDER_THRESHOLD}

# --- orders to process (list of tuples: order_id, sku, quantity) ---
orders = [
    ("ORD-001", "TENT-3P-GRN",   2),
    ("ORD-002", "PACK-45L-BLK",  1),
    ("ORD-003", "SLEEP-REG-BLU", 5),
    ("ORD-004", "JACKET-M-RED",  4),
    ("ORD-005", "TENT-3P-GRN",  10),
    ("ORD-006", "BOOT-42-BRN",   2),
    ("ORD-007", "SLEEP-REG-BLU",12),
    ("ORD-008", "PACK-45L-BLK",  3),
]

print("=== Meridian Inventory Manager ===")
print(f"\nProcessing {len(orders)} orders...")

dispatched_count = 0
rejected_count   = 0

for order_id, sku, qty in orders:
    stock_before = stock.get(sku, 0)
    success, reason = dispatch(stock, reorder_flags, sku, qty)

    if success:
        stock_after = stock[sku]
        low_flag    = "  (low stock flagged)" if sku in reorder_flags else ""
        print(f"{order_id}  {sku:<20} qty={qty:<3} stock: {stock_before:>3} → {stock_after:>3}   ✓{low_flag}")
        dispatched_count += 1
    else:
        print(f"{order_id}  {sku:<20} qty={qty:<3} stock: {stock_before:>3} →   —   ✗ {reason}")
        rejected_count += 1

print()
print("=== End of Run ===")
print(f"Dispatched : {dispatched_count} orders")
print(f"Rejected   : {rejected_count} orders")

stock_report(stock, reorder_flags)
