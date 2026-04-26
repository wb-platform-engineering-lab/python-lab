"""Challenge 4 — Exceptions.

Process orders with full error handling so one bad row never
crashes the pipeline. Demonstrates try/except/else/finally,
specific exception types, and raising.
"""
import csv
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def load_inventory(path):
    """Load inventory JSON. Raises FileNotFoundError if path is missing."""
    if not path.exists():
        raise FileNotFoundError(f"inventory file not found: {path}")
    with open(path) as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"invalid JSON in {path}: {e}") from e


def validate_and_dispatch(order, inventory):
    """Validate an order and update inventory.

    Returns the unit_price of the dispatched order.
    Raises ValueError or KeyError on invalid input.
    """
    status = order.get("status")
    if status == "cancelled":
        return None   # signal to skip — not an error

    quantity = order["quantity"]
    if quantity <= 0:
        raise ValueError("zero quantity")

    sku = order["sku"]
    if sku not in inventory:
        raise KeyError(f"unknown SKU")

    stock = inventory[sku]["stock"]
    if stock == 0:
        raise ValueError("out of stock")
    if stock < quantity:
        raise ValueError(f"insufficient stock (need {quantity}, have {stock})")

    inventory[sku]["stock"] -= quantity
    return True


# --- load inventory (with error handling) ---
try:
    inventory = load_inventory(DATA_DIR / "inventory.json")
except FileNotFoundError as e:
    print(f"Fatal: {e}")
    raise SystemExit(1)
except ValueError as e:
    print(f"Fatal: {e}")
    raise SystemExit(1)

# --- process orders ---
processed = 0
skipped   = 0
errors    = 0

print("=== Processing orders with error handling ===")

with open(DATA_DIR / "orders.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        order_id = row["order_id"]
        sku      = row["sku"]
        qty_raw  = row["quantity"]

        try:
            row["quantity"] = int(qty_raw)   # CSV values are strings
            result = validate_and_dispatch(row, inventory)
        except ValueError as e:
            status = f"error: {e} (ValueError)"
            errors += 1
        except KeyError as e:
            status = f"error: {e} (KeyError)"
            errors += 1
        else:
            if result is None:
                status = "skipped (cancelled)"
                skipped += 1
            else:
                status = "ok"
                processed += 1

        qty_display = qty_raw.strip()
        print(f"{order_id:<10} {sku:<20} qty={qty_display:<4} → {status}")

print()
print(f"Processed : {processed}")
print(f"Skipped   : {skipped}")
print(f"Errors    : {errors}")

# --- finally example ---
print()
print("--- finally always runs ---")
try:
    x = 1 / 0
except ZeroDivisionError:
    print("caught division by zero")
finally:
    print("finally block ran")
