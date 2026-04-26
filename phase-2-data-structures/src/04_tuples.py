"""Challenge 4 — Tuples.

Fixed records, unpacking, and composite dict keys.
"""

# --- tuples as fixed records ---
warehouses = [
    ("north", 53.4808, -2.2426),
    ("south", 51.5074, -0.1278),
    ("west",  53.8008, -1.5491),
]

print("=== Warehouse Locations ===")
for name, lat, lon in warehouses:          # unpack in the loop header
    print(f"{name:<6} lat={lat:.2f}  lon={lon:.2f}")

# --- tuple as composite dict key ---
# (warehouse, sku) → stock level
stock = {
    ("north", "TENT-3P-GRN"):  100,
    ("south", "TENT-3P-GRN"):   80,
    ("north", "PACK-45L-BLK"):  50,
    ("west",  "PACK-45L-BLK"):  38,
}

print()
print("=== Composite Stock Lookup ===")
for (wh, sku), qty in stock.items():
    print(f"({wh}, {sku:<20}) : {qty} units")

# --- unpacking patterns ---
print()
print("=== Unpacking examples ===")

# swap without a temp variable
a, b = 1, 2
a, b = b, a
print(f"Swap    : a={a}, b={b}")

# capture first + rest
order_ids = ["ORD-001", "ORD-002", "ORD-003", "ORD-004"]
first, *rest = order_ids
print(f"Rest    : first={first}, rest={rest}")

# discard fields you don't need with _
sku, _, price = ("TENT-3P-GRN", "tent", 89.99)
print(f"Discard : sku={sku}, price={price}")

# --- tuples are immutable ---
coords = (53.4808, -2.2426)
try:
    coords[0] = 0.0
except TypeError as e:
    print(f"\nImmutability : {e}")
