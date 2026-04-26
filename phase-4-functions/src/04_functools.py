"""Challenge 4 — functools.

partial for pre-filled arguments, lru_cache for memoisation,
reduce for custom accumulation.
"""
import functools

# --- functools.partial ---

def dispatch(sku, quantity, warehouse, *, dry_run=False):
    """Dispatch units of a SKU to a warehouse."""
    action = "[DRY RUN] would dispatch" if dry_run else "dispatched"
    print(f"  {action} {sku} qty={quantity} to {warehouse}")
    return not dry_run


# Pre-fill warehouse — caller only provides sku and quantity
dispatch_north = functools.partial(dispatch, warehouse="north")
dispatch_south = functools.partial(dispatch, warehouse="south")

# Pre-fill dry_run=True for safe testing
dry_dispatch = functools.partial(dispatch, warehouse="north", dry_run=True)

print("=== partial ===")
dispatch_north("TENT-3P-GRN",  2)
dispatch_south("PACK-45L-BLK", 1)
dry_dispatch("BOOT-42-BRN",    5)


# --- functools.lru_cache ---

CATALOGUE = {
    "TENT-3P-GRN":   {"name": "3-Person Tent",        "price": 89.99},
    "PACK-45L-BLK":  {"name": "45L Backpack",          "price": 149.99},
    "SLEEP-REG-BLU": {"name": "Regular Sleeping Bag",  "price": 59.99},
    "JACKET-M-RED":  {"name": "Mountain Jacket",       "price": 149.99},
    "BOOT-42-BRN":   {"name": "Hiking Boot Size 42",   "price": 119.99},
}

@functools.lru_cache(maxsize=128)
def get_product(sku):
    """Look up a product by SKU. Result is cached after the first call."""
    print(f"  loading {sku} from catalogue...")
    return CATALOGUE.get(sku)


print()
print("=== lru_cache ===")

# First calls — cache misses
skus_to_lookup = [
    "TENT-3P-GRN", "PACK-45L-BLK",
    "TENT-3P-GRN",                  # cache hit
    "PACK-45L-BLK",                 # cache hit
    "TENT-3P-GRN",                  # cache hit
    "PACK-45L-BLK",                 # cache hit
]

for sku in skus_to_lookup:
    product = get_product(sku)
    print(f"  {sku:<22} → ${product['price']:.2f}")

print(f"  {get_product.cache_info()}")


# --- functools.reduce ---

from functools import reduce

order_values = [179.98, 149.99, 299.95, 239.98]

total = reduce(lambda acc, x: acc + x, order_values, 0)
max_v = reduce(lambda a, b: a if a > b else b, order_values)

print()
print("=== reduce ===")
print(f"Batch total : ${total:.2f}")
print(f"Max value   : ${max_v:.2f}")
