"""Challenge 5 — Lambdas and higher-order functions.

Using lambda with sorted, map, and filter to transform
order and inventory data concisely.
"""

orders = [
    {"order_id": "ORD-001", "sku": "TENT-3P-GRN",   "warehouse": "north", "quantity": 2,  "value": 179.98,  "status": "pending"},
    {"order_id": "ORD-002", "sku": "PACK-45L-BLK",   "warehouse": "south", "quantity": 1,  "value": 149.99,  "status": "pending"},
    {"order_id": "ORD-003", "sku": "SLEEP-REG-BLU",  "warehouse": "west",  "quantity": 5,  "value": 299.95,  "status": "pending"},
    {"order_id": "ORD-004", "sku": "JACKET-M-RED",   "warehouse": "north", "quantity": 4,  "value": 599.96,  "status": "pending"},
    {"order_id": "ORD-005", "sku": "BOOT-42-BRN",    "warehouse": "south", "quantity": 2,  "value": 239.98,  "status": "cancelled"},
    {"order_id": "ORD-008", "sku": "SLEEP-REG-BLU",  "warehouse": "north", "quantity": 6,  "value": 359.94,  "status": "pending"},
    {"order_id": "ORD-010", "sku": "BOOT-42-BRN",    "warehouse": "west",  "quantity": 8,  "value": 959.92,  "status": "pending"},
    {"order_id": "ORD-011", "sku": "TENT-3P-GRN",    "warehouse": "north", "quantity": 12, "value": 1079.88, "status": "pending"},
]

# --- sorted with lambda ---

by_value    = sorted(orders, key=lambda o: o["value"], reverse=True)
by_wh_value = sorted(orders, key=lambda o: (o["warehouse"], -o["value"]))

print("=== sorted with lambda ===")
print("By value (desc):")
for o in by_value[:4]:
    print(f"  {o['order_id']}  ${o['value']:<9.2f} qty={o['quantity']}")

print("By warehouse then value (desc):")
for o in by_wh_value:
    print(f"  {o['order_id']}  {o['warehouse']:<6} ${o['value']:.2f}")


# --- map ---

skus        = ["tent-3p-grn", "pack-45l-blk", "sleep-reg-blu"]
upper_skus  = list(map(str.upper, skus))     # use existing method as key fn

prices      = {"TENT-3P-GRN": 89.99, "PACK-45L-BLK": 149.99, "SLEEP-REG-BLU": 59.99}
discounted  = {sku: round(p * 0.9, 2) for sku, p in prices.items()}  # comprehension clearer here

print()
print("=== map ===")
print(f"SKUs upper-cased : {upper_skus}")
print(f"Discounted prices: {discounted}")


# --- filter ---

pending    = list(filter(lambda o: o["status"] == "pending", orders))
enterprise = list(filter(lambda o: o["warehouse"] == "north" and o["quantity"] > 3, orders))
high_value = list(filter(lambda o: o["value"] > 500, orders))

print()
print("=== filter ===")
print(f"Pending orders          : {len(pending)}")
print(f"Large north orders      : {len(enterprise)}")
print(f"High-value orders >$500 : {len(high_value)}")
for o in high_value:
    print(f"  {o['order_id']}  ${o['value']:.2f}")


# --- lambda limitations: use def when logic is not trivial ---

# Good use of lambda: short key function passed inline
top_sku = max(orders, key=lambda o: o["value"])
print()
print(f"Highest-value order: {top_sku['order_id']} (${top_sku['value']:.2f})")

# Bad use of lambda: complex logic belongs in a def
# value_category = lambda o: "high" if o["value"] > 500 else "medium" if o["value"] > 200 else "low"
# Use a named function instead:
def value_category(order):
    if order["value"] > 500:
        return "high"
    if order["value"] > 200:
        return "medium"
    return "low"

print()
print("Order value categories:")
for o in sorted(orders, key=lambda o: o["value"], reverse=True)[:4]:
    print(f"  {o['order_id']}  ${o['value']:<9.2f} → {value_category(o)}")
