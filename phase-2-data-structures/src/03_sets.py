"""Challenge 3 — Sets.

Fast membership testing and SKU coverage analysis across warehouses.
Demonstrates set operations, deduplication, and O(1) lookup.
"""

north_skus = {"TENT-3P-GRN", "PACK-45L-BLK", "JACKET-M-RED", "BOOT-42-BRN"}
south_skus = {"TENT-3P-GRN", "SLEEP-REG-BLU", "BOOT-42-BRN", "PACK-45L-BLK"}
west_skus  = {"PACK-45L-BLK", "SLEEP-REG-BLU", "BOOT-42-BRN"}

# --- set operations ---
all_skus        = north_skus | south_skus | west_skus       # union
stocked_everywhere = north_skus & south_skus & west_skus    # intersection
only_north      = north_skus - south_skus - west_skus       # difference

print("=== Warehouse SKU Coverage ===")
print(f"north stocks : {len(north_skus)} SKUs")
print(f"south stocks : {len(south_skus)} SKUs")
print(f"west  stocks : {len(west_skus)} SKUs")
print()
print(f"Stocked everywhere    : {stocked_everywhere}")
print(f"Stocked in north only : {only_north}")
print(f"All unique SKUs        : {len(all_skus)} SKUs")

# --- O(1) membership testing ---
catalogue_skus = all_skus  # treat our known SKUs as the catalogue

incoming_requests = ["TENT-3P-GRN", "CRAMPONS-S", "PACK-45L-BLK", "TARP-3X4-GRN"]

print()
print("=== Fulfilment Check ===")
for sku in incoming_requests:
    if sku in catalogue_skus:
        print(f"{sku:<22} → can fulfil (in stock somewhere)")
    else:
        print(f"{sku:<22} → cannot fulfil (unknown SKU)")

# --- deduplication ---
raw_order_skus = [
    "TENT-3P-GRN", "PACK-45L-BLK", "TENT-3P-GRN",
    "BOOT-42-BRN", "PACK-45L-BLK", "SLEEP-REG-BLU",
    "TENT-3P-GRN", "BOOT-42-BRN", "PACK-45L-BLK",
    "SLEEP-REG-BLU", "JACKET-M-RED", "TENT-3P-GRN",
]

unique_skus = set(raw_order_skus)

print()
print("=== Deduplication ===")
print(f"Raw SKUs in today's orders : {len(raw_order_skus)} (with duplicates)")
print(f"Unique SKUs ordered        : {len(unique_skus)}")

# --- add and discard ---
unique_skus.add("CRAMPONS-S")      # add a new SKU
unique_skus.discard("CRAMPONS-S")  # remove — no error if not present
unique_skus.discard("MISSING")     # safe — no KeyError
