"""Challenge 1 — Lists.

Ordered sequences of SKUs and orders.
Demonstrates indexing, slicing, common methods, and sorting.
"""

# --- creating and inspecting ---
skus = ["TENT-3P-GRN", "PACK-45L-BLK", "SLEEP-REG-BLU", "JACKET-M-RED", "BOOT-42-BRN"]

print(f"=== SKU Catalogue ({len(skus)} items) ===")
for i, sku in enumerate(skus):
    print(f"[{i}] {sku}")

# --- indexing and slicing ---
print()
print(f"Last SKU    : {skus[-1]}")
print(f"First two   : {skus[:2]}")
print(f"Reversed    : {skus[::-1]}")

# --- modifying lists ---
catalogue = skus.copy()           # work on a copy so we don't mutate the original
catalogue.append("TARP-3X4-GRN")
catalogue.insert(0, "CRAMPONS-S")
catalogue.remove("TARP-3X4-GRN")
popped = catalogue.pop()
# catalogue is back to original length with CRAMPONS-S prepended

# --- sorting ---
orders = [
    {"order_id": "ORD-001", "quantity": 1},
    {"order_id": "ORD-002", "quantity": 12},
    {"order_id": "ORD-003", "quantity": 3},
    {"order_id": "ORD-004", "quantity": 100},
    {"order_id": "ORD-005", "quantity": 45},
]

by_qty = sorted(orders, key=lambda o: o["quantity"])

print()
print("=== Orders by quantity (ascending) ===")
for o in by_qty:
    print(f"{o['order_id']}   qty={o['quantity']}")

quantities = [o["quantity"] for o in orders]
print()
print(f"Total quantity : {sum(quantities)}")
print(f"Max quantity   : {max(quantities)}")
print(f"Min quantity   : {min(quantities)}")

# --- membership test ---
print()
print(f"'TENT-3P-GRN' in skus : {'TENT-3P-GRN' in skus}")
print(f"'CRAMPONS-S' in skus  : {'CRAMPONS-S' in skus}")
