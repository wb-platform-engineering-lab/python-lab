"""Challenge 2 — Dictionaries.

O(1) inventory lookups by SKU.
Demonstrates creation, access, iteration, and nested dicts.
"""

REORDER_THRESHOLD = 20

inventory = {
    "TENT-3P-GRN":   312,
    "PACK-45L-BLK":   88,
    "SLEEP-REG-BLU":  14,
    "JACKET-M-RED":    0,
    "BOOT-42-BRN":   203,
}

prices = {
    "TENT-3P-GRN":   89.99,
    "PACK-45L-BLK":  149.99,
    "SLEEP-REG-BLU":  59.99,
    "JACKET-M-RED":  149.99,
    "BOOT-42-BRN":   119.99,
}

# --- access and status ---
print("=== Inventory Lookup ===")
for sku, stock in inventory.items():
    price = prices.get(sku, 0.0)

    if stock == 0:
        status = "OUT OF STOCK"
    elif stock < REORDER_THRESHOLD:
        status = "REORDER"
    else:
        status = "OK"

    print(f"{sku:<22} : {stock:>3} units  @ ${price:<7.2f} → {status}")

print()
print(f"Total SKUs tracked : {len(inventory)}")
print(f"Total units        : {sum(inventory.values())}")

# --- safe access with .get() ---
print()
print("--- .get() with defaults ---")
print(f"Known SKU   : {inventory.get('TENT-3P-GRN', 0)}")
print(f"Unknown SKU : {inventory.get('CRAMPONS-S', 0)}")   # returns 0, no KeyError

# --- updating ---
inventory["TENT-3P-GRN"] -= 5        # dispatch 5 units
inventory["CRAMPONS-S"] = 50         # add a new SKU
del inventory["CRAMPONS-S"]          # remove it

# --- nested dict: per-warehouse stock ---
warehouse_stock = {
    "north": {"TENT-3P-GRN": 100, "PACK-45L-BLK": 50, "JACKET-M-RED": 75},
    "south": {"TENT-3P-GRN": 80,  "SLEEP-REG-BLU": 200, "BOOT-42-BRN": 120},
    "west":  {"PACK-45L-BLK": 38, "SLEEP-REG-BLU": 14,  "BOOT-42-BRN": 83},
}

print()
print("=== Warehouse Stock: north ===")
for sku, qty in warehouse_stock["north"].items():
    print(f"  {sku:<22} : {qty}")

# safe nested access
west_tent = warehouse_stock.get("west", {}).get("TENT-3P-GRN", 0)
print(f"\nTENT-3P-GRN in west : {west_tent} units")
