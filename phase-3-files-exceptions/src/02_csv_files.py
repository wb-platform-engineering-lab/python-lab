"""Challenge 2 — CSV files.

Loading orders and products with csv.DictReader.
Writing results with csv.DictWriter.
"""
import csv
from pathlib import Path

DATA_DIR   = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def load_orders(path):
    """Return a list of order dicts loaded from a CSV file."""
    orders = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["quantity"] = int(row["quantity"])   # CSV values are always strings
            orders.append(row)
    return orders


def load_products(path):
    """Return a dict of sku → product info loaded from a CSV file."""
    products = {}
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["unit_price"] = float(row["unit_price"])
            products[row["sku"]] = row
    return products


def write_results(path, results):
    """Write a list of result dicts to a CSV file."""
    if not results:
        return
    fieldnames = list(results[0].keys())
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


# --- load ---
orders   = load_orders(DATA_DIR / "orders.csv")
products = load_products(DATA_DIR / "products.csv")

print("=== Orders loaded from CSV ===")
print(f"Loaded {len(orders)} orders\n")

print(f"{'order_id':<10} {'sku':<20} {'qty':<4} {'warehouse':<10} {'tier':<11} {'status'}")
for o in orders:
    print(f"{o['order_id']:<10} {o['sku']:<20} {o['quantity']:<4} {o['warehouse']:<10} {o['customer_tier']:<11} {o['status']}")

print(f"\nProducts loaded: {len(products)}")

# --- write results ---
results = [
    {"order_id": o["order_id"], "sku": o["sku"], "status": "processed"}
    for o in orders
]
out_path = OUTPUT_DIR / "results.csv"
write_results(out_path, results)
print(f"\nResults written to {out_path} ({len(results)} rows)")
