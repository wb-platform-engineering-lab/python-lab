"""Challenge 3 — JSON files.

Loading inventory from JSON, updating it, and saving back to disk.
Demonstrates json.load/dump and json.loads/dumps.
"""
import json
from pathlib import Path

DATA_DIR   = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def load_inventory(path):
    """Return inventory dict loaded from a JSON file."""
    with open(path) as f:
        return json.load(f)


def save_inventory(inventory, path):
    """Save inventory dict to a JSON file."""
    with open(path, "w") as f:
        json.dump(inventory, f, indent=2)


# --- load ---
inventory = load_inventory(DATA_DIR / "inventory.json")

print("=== Inventory loaded from JSON ===")
for sku, info in inventory.items():
    stock     = info["stock"]
    threshold = info["reorder_threshold"]
    if stock == 0:
        status = "OUT OF STOCK"
    elif stock <= threshold:
        status = "REORDER"
    else:
        status = "OK"
    print(f"{sku:<20} stock={stock:>3}  threshold={threshold:>2}   {status}")

# --- update ---
sku_to_dispatch = "TENT-3P-GRN"
qty_to_dispatch = 10

print(f"\nDispatching {qty_to_dispatch} units of {sku_to_dispatch}...")
before = inventory[sku_to_dispatch]["stock"]
inventory[sku_to_dispatch]["stock"] -= qty_to_dispatch
after  = inventory[sku_to_dispatch]["stock"]
print(f"Stock updated: {before} → {after}")

# --- save updated inventory ---
out_path = OUTPUT_DIR / "inventory_updated.json"
save_inventory(inventory, out_path)
print(f"\nUpdated inventory saved to {out_path}")

# --- json.loads / json.dumps (for strings, not files) ---
print()
print("--- json.loads / json.dumps ---")
raw_string = '{"order_id": "ORD-001", "sku": "TENT-3P-GRN", "quantity": 2}'
order = json.loads(raw_string)
print(f"Parsed : {order}")
print(f"Type   : {type(order)}")

back_to_string = json.dumps(order, indent=2)
print(f"Serialised:\n{back_to_string}")
