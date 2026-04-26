"""Challenge 6 — File pipeline (capstone).

Reads from files, processes every order, handles every error,
writes results to output files. No order crashes the pipeline.
"""
import csv
import json
from datetime import datetime
from pathlib import Path

DATA_DIR   = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


# --- custom exceptions (inline for self-contained capstone) ---

class OrderError(Exception):
    pass

class UnknownSKUError(OrderError):
    def __init__(self, sku):
        super().__init__(f"unknown SKU: {sku}")

class ZeroQuantityError(OrderError):
    def __init__(self):
        super().__init__("zero quantity")

class OutOfStockError(OrderError):
    def __init__(self, sku):
        super().__init__(f"out of stock")

class InsufficientStockError(OrderError):
    def __init__(self, needed, have):
        super().__init__(f"insufficient stock (need {needed}, have {have})")


# --- loaders ---

def load_inventory(path):
    with open(path) as f:
        return json.load(f)

def load_products(path):
    products = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            row["unit_price"] = float(row["unit_price"])
            products[row["sku"]] = row
    return products

def load_orders(path):
    orders = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            row["quantity"] = int(row["quantity"])
            orders.append(row)
    return orders


# --- dispatch logic ---

def dispatch(order, inventory, products):
    """Attempt to dispatch an order. Returns unit value on success.

    Returns None for cancelled orders.
    Raises OrderError subclasses on failure.
    """
    if order["status"] == "cancelled":
        return None

    sku      = order["sku"]
    quantity = order["quantity"]

    if quantity <= 0:
        raise ZeroQuantityError()
    if sku not in inventory:
        raise UnknownSKUError(sku)

    stock = inventory[sku]["stock"]
    if stock == 0:
        raise OutOfStockError(sku)
    if stock < quantity:
        raise InsufficientStockError(quantity, stock)

    inventory[sku]["stock"] -= quantity
    unit_price = products[sku]["unit_price"] if sku in products else 0.0
    return unit_price * quantity


# --- writers ---

def write_csv(path, rows):
    if not rows:
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def append_log(path, message):
    with open(path, "a") as f:
        f.write(message + "\n")


# --- main pipeline ---

def run_pipeline():
    print("=== Meridian File Pipeline ===")

    inventory = load_inventory(DATA_DIR / "inventory.json")
    products  = load_products(DATA_DIR / "products.csv")
    orders    = load_orders(DATA_DIR / "orders.csv")

    print(f"Loaded {len(inventory)} SKUs from {DATA_DIR / 'inventory.json'}")
    print(f"Loaded {len(products)} products from {DATA_DIR / 'products.csv'}")
    print(f"Processing {DATA_DIR / 'orders.csv'}...")
    print()

    dispatched_rows = []
    rejected_rows   = []
    total_value     = 0.0

    for order in orders:
        oid = order["order_id"]
        sku = order["sku"]
        qty = order["quantity"]

        try:
            value = dispatch(order, inventory, products)
        except OrderError as e:
            reason = str(e)
            rejected_rows.append({"order_id": oid, "sku": sku, "quantity": qty, "reason": reason})
            print(f"{oid:<10} {sku:<20} qty={qty:<4} {'—':<10} → rejected: {reason}")
            continue

        if value is None:
            reason = "cancelled"
            rejected_rows.append({"order_id": oid, "sku": sku, "quantity": qty, "reason": reason})
            print(f"{oid:<10} {sku:<20} qty={qty:<4} {'—':<10} → rejected: {reason}")
        else:
            total_value += value
            dispatched_rows.append({
                "order_id": oid, "sku": sku, "quantity": qty,
                "value": round(value, 2), "warehouse": order["warehouse"],
            })
            print(f"{oid:<10} {sku:<20} qty={qty:<4} ${value:<9.2f} → dispatched")

    # --- write outputs ---
    dispatched_path = OUTPUT_DIR / "dispatched.csv"
    rejected_path   = OUTPUT_DIR / "rejected.csv"
    inv_path        = OUTPUT_DIR / "inventory_updated.json"
    log_path        = OUTPUT_DIR / "run_log.txt"

    write_csv(dispatched_path, dispatched_rows)
    write_csv(rejected_path, rejected_rows)

    with open(inv_path, "w") as f:
        json.dump(inventory, f, indent=2)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"[{timestamp}] dispatched={len(dispatched_rows)} "
        f"rejected={len(rejected_rows)} value=${total_value:.2f}"
    )
    append_log(log_path, log_entry)

    print()
    print("=== Run Complete ===")
    print(f"Dispatched : {len(dispatched_rows):<4} →  {dispatched_path}")
    print(f"Rejected   : {len(rejected_rows):<4} →  {rejected_path}")
    print(f"Batch value: ${total_value:,.2f}")
    print(f"Updated inventory → {inv_path}")
    print(f"Run log appended  → {log_path}")


if __name__ == "__main__":
    run_pipeline()
