"""Challenge 5 — Your first function.

Reusable functions for Meridian's inventory reporting.
Write each function once; call it for all 12,000 SKUs.
"""


def check_stock(available, threshold=100):
    """Return True if stock is at or below the reorder threshold."""
    return available <= threshold


def fill_rate(shipped, total):
    """Return fill rate as a float between 0 and 1.

    Returns 0.0 if total is zero to avoid division by zero.
    """
    if total == 0:
        return 0.0
    return shipped / total


def format_report_line(sku, available, threshold):
    """Return a formatted inventory status line for a single SKU."""
    status = "REORDER" if check_stock(available, threshold) else "OK"
    return f"{sku:<22} stock={available:>5}  threshold={threshold:>5}  [{status}]"


# --- run the report ---
inventory = [
    ("TENT-3P-GRN",     48, 100),
    ("PACK-45L-BLK",   312,  50),
    ("SLEEP-REG-BLU",    3,  20),
    ("JACKET-M-RED",   225, 200),
    ("BOOT-42-BRN",      0,  30),
]

print("=== Inventory Status ===")
for sku, available, threshold in inventory:
    print(format_report_line(sku, available, threshold))

# --- fill rate summary ---
rate = fill_rate(shipped=2350, total=2400)
print(f"\nFill rate today : {rate:.1%}")
print(f"Target          : 95.0%")
print(f"Status          : {'ON TRACK' if rate >= 0.95 else 'AT RISK'}")

# --- explore default parameters ---
print()
print("check_stock(48)         →", check_stock(48))           # uses default threshold=100
print("check_stock(48, 50)     →", check_stock(48, 50))       # overrides to 50
print("check_stock(48, 20)     →", check_stock(48, 20))       # 48 > 20, so False
