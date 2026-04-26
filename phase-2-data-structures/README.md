# Phase 2 — Data Structures

> **Concepts introduced:** `list`, `dict`, `set`, `tuple`, list/dict comprehensions, slicing, unpacking, common built-ins (`sorted`, `min`, `max`, `sum`, `any`, `all`) | **Difficulty:** Beginner–Intermediate | **Cost:** Free

---

## The problem

Meridian's order processor from Phase 1 works — but it handles one batch of hardcoded orders. Real data is messier: thousands of rows, repeated SKUs, orders referencing warehouses that may or may not exist, inventory that changes with every shipment.

To manage that, you need the right containers. Python's built-in data structures — `list`, `dict`, `set`, `tuple` — each have different strengths. Choosing the wrong one makes code slow and hard to read. Choosing the right one makes it obvious.

---

## The four containers at a glance

| Container | Ordered | Mutable | Duplicates | Key use case |
|---|---|---|---|---|
| `list` | Yes | Yes | Yes | Ordered sequences, stacks, queues |
| `dict` | Yes (3.7+) | Yes | Keys: No | Lookup by key, structured records |
| `set` | No | Yes | No | Membership testing, deduplication |
| `tuple` | Yes | No | Yes | Fixed records, multiple return values |

---

## Challenge 1 — Lists

**Goal:** Store and manipulate ordered sequences of orders and SKUs.

### Creating lists

```python
warehouse_names = ["north", "south", "west"]
order_ids       = ["ORD-001", "ORD-002", "ORD-003"]
empty           = []
mixed           = ["ORD-001", 5, True]   # valid but avoid — keep types consistent
```

### Indexing and slicing

```python
skus = ["TENT-3P-GRN", "PACK-45L-BLK", "SLEEP-REG-BLU", "JACKET-M-RED", "BOOT-42-BRN"]

print(skus[0])      # "TENT-3P-GRN"    — first item
print(skus[-1])     # "BOOT-42-BRN"    — last item
print(skus[1:3])    # ["PACK-45L-BLK", "SLEEP-REG-BLU"]  — items 1 and 2
print(skus[:2])     # first two items
print(skus[2:])     # everything from index 2 onward
print(skus[::-1])   # reversed copy
```

### Common list methods

```python
orders = ["ORD-001", "ORD-002"]

orders.append("ORD-003")         # add one item to the end
orders.extend(["ORD-004", "ORD-005"])  # add multiple items
orders.insert(0, "ORD-000")      # insert at index 0

orders.pop()                      # remove and return the last item
orders.pop(0)                     # remove and return item at index 0
orders.remove("ORD-002")         # remove first occurrence of a value

print(len(orders))                # number of items
print("ORD-003" in orders)        # True — membership test
```

### Sorting

```python
quantities = [12, 3, 45, 1, 8]

print(sorted(quantities))         # [1, 3, 8, 12, 45]  — returns new list
quantities.sort()                  # sorts in place — modifies the original
quantities.sort(reverse=True)      # descending

# Sort a list of dicts by a field
orders = [
    {"order_id": "ORD-003", "quantity": 12},
    {"order_id": "ORD-001", "quantity": 3},
    {"order_id": "ORD-002", "quantity": 45},
]
by_qty = sorted(orders, key=lambda o: o["quantity"])
```

### Step 1: Run `src/01_lists.py`

```bash
python3 src/01_lists.py
```

Expected output:
```
=== SKU Catalogue (5 items) ===
[0] TENT-3P-GRN
[1] PACK-45L-BLK
[2] SLEEP-REG-BLU
[3] JACKET-M-RED
[4] BOOT-42-BRN

Last SKU    : BOOT-42-BRN
First two   : ['TENT-3P-GRN', 'PACK-45L-BLK']
Reversed    : ['BOOT-42-BRN', 'JACKET-M-RED', 'SLEEP-REG-BLU', 'PACK-45L-BLK', 'TENT-3P-GRN']

=== Orders by quantity (ascending) ===
ORD-001   qty=1
ORD-003   qty=3
ORD-002   qty=12
ORD-005   qty=45
ORD-004   qty=100

Total quantity : 161
Max quantity   : 100
Min quantity   : 1
```

---

## Challenge 2 — Dictionaries

**Goal:** Look up inventory levels and product details by SKU in O(1) time.

### Why dict instead of list?

```python
# list — you have to loop through every item to find one
for item in inventory:
    if item["sku"] == "TENT-3P-GRN":
        print(item["stock"])          # O(n) — gets slower as inventory grows

# dict — jump directly to the value by key
inventory = {"TENT-3P-GRN": 312, "PACK-45L-BLK": 88}
print(inventory["TENT-3P-GRN"])       # O(1) — instant, regardless of size
```

### Creating and accessing dicts

```python
product = {
    "sku":      "TENT-3P-GRN",
    "name":     "3-Person Tent (Green)",
    "category": "tent",
    "price":    89.99,
}

print(product["sku"])               # direct access — KeyError if missing
print(product.get("sku"))           # safe access — returns None if missing
print(product.get("weight", 0.0))   # safe access with a default
```

### Modifying dicts

```python
inventory = {"TENT-3P-GRN": 312}

inventory["PACK-45L-BLK"] = 88      # add a new key
inventory["TENT-3P-GRN"] = 300      # update an existing key
inventory["TENT-3P-GRN"] -= 5       # decrement stock

del inventory["PACK-45L-BLK"]       # remove a key (KeyError if missing)
inventory.pop("TENT-3P-GRN", 0)     # remove with a default if missing
```

### Iterating

```python
for sku, stock in inventory.items():     # key–value pairs
    print(f"  {sku}: {stock}")

for sku in inventory.keys():            # keys only
    print(sku)

for stock in inventory.values():        # values only
    print(stock)
```

### Nested dicts

```python
warehouse_stock = {
    "north": {"TENT-3P-GRN": 100, "PACK-45L-BLK": 50},
    "south": {"TENT-3P-GRN":  80, "SLEEP-REG-BLU": 200},
}

print(warehouse_stock["north"]["TENT-3P-GRN"])   # 100
```

### Step 1: Run `src/02_dicts.py`

```bash
python3 src/02_dicts.py
```

Expected output:
```
=== Inventory Lookup ===
TENT-3P-GRN    : 312 units  @ $89.99   → OK
PACK-45L-BLK   : 88 units   @ $149.99  → OK
SLEEP-REG-BLU  : 14 units   @ $59.99   → REORDER
JACKET-M-RED   : 0 units    @ $149.99  → OUT OF STOCK
BOOT-42-BRN    : 203 units  @ $119.99  → OK

=== Warehouse Stock: north ===
  TENT-3P-GRN   : 100
  PACK-45L-BLK  : 50
  JACKET-M-RED  : 75

Total SKUs tracked : 5
Total units        : 617
```

---

## Challenge 3 — Sets

**Goal:** Deduplicate SKUs and do fast membership testing across warehouses.

### What makes a set different

A set stores **unique** values with no order. Membership testing (`in`) is O(1) — as fast as a dict lookup, regardless of how many items the set contains.

```python
# list membership — scans every item
"TENT-3P-GRN" in ["TENT-3P-GRN", "PACK-45L-BLK", "SLEEP-REG-BLU"]   # O(n)

# set membership — instant hash lookup
"TENT-3P-GRN" in {"TENT-3P-GRN", "PACK-45L-BLK", "SLEEP-REG-BLU"}   # O(1)
```

### Creating and modifying sets

```python
active_skus = {"TENT-3P-GRN", "PACK-45L-BLK", "SLEEP-REG-BLU"}
active_skus.add("JACKET-M-RED")         # add one item
active_skus.discard("MISSING-SKU")      # remove if present — no error if missing
active_skus.remove("PACK-45L-BLK")      # remove — KeyError if missing
```

### Set operations

```python
north_skus = {"TENT-3P-GRN", "PACK-45L-BLK", "JACKET-M-RED"}
south_skus = {"TENT-3P-GRN", "SLEEP-REG-BLU", "BOOT-42-BRN"}

# union — all SKUs stocked anywhere
all_skus = north_skus | south_skus

# intersection — SKUs stocked in both warehouses
in_both  = north_skus & south_skus

# difference — SKUs in north but not south
only_north = north_skus - south_skus

# symmetric difference — SKUs in one but not both
exclusive = north_skus ^ south_skus
```

### Deduplication

```python
raw_order_skus = ["TENT-3P-GRN", "PACK-45L-BLK", "TENT-3P-GRN", "BOOT-42-BRN", "PACK-45L-BLK"]
unique_skus = list(set(raw_order_skus))   # remove duplicates — order not preserved
```

### Step 1: Run `src/03_sets.py`

```bash
python3 src/03_sets.py
```

Expected output:
```
=== Warehouse SKU Coverage ===
north stocks : 4 SKUs
south stocks : 4 SKUs
west  stocks : 3 SKUs

Stocked everywhere    : {'TENT-3P-GRN'}
Stocked in north only : {'JACKET-M-RED'}
All unique SKUs        : 6 SKUs

=== Fulfilment Check ===
TENT-3P-GRN    → can fulfil (in stock somewhere)
CRAMPONS-S     → cannot fulfil (unknown SKU)
PACK-45L-BLK   → can fulfil (in stock somewhere)
TARP-3X4-GRN   → cannot fulfil (unknown SKU)

=== Deduplication ===
Raw SKUs in today's orders : 12 (with duplicates)
Unique SKUs ordered        : 5
```

---

## Challenge 4 — Tuples

**Goal:** Use tuples for fixed records and safe multiple return values.

### Tuples are immutable lists

```python
point     = (10, 20)          # a fixed (x, y) pair
rgb       = (255, 128, 0)     # a colour — never changes
warehouse = ("north", "GB", True)  # a record — fields have positional meaning
```

Once created, a tuple cannot be changed:

```python
point[0] = 99    # TypeError — tuples are immutable
```

### When to use a tuple vs a list

| Situation | Use |
|---|---|
| A sequence that will be modified (add, remove items) | `list` |
| A fixed record where position has meaning | `tuple` |
| Multiple return values from a function | `tuple` (unpacked on return) |
| Dictionary key (must be hashable) | `tuple` — lists cannot be dict keys |

### Unpacking

```python
location = ("north", 53.4808, -2.2426)
name, lat, lon = location     # unpack into three variables

# swap two variables without a temp variable
a, b = 1, 2
a, b = b, a

# ignore values you don't need
sku, _, price = ("TENT-3P-GRN", "tent", 89.99)

# capture the rest with *
first, *rest = [1, 2, 3, 4, 5]   # first=1, rest=[2, 3, 4, 5]
*init, last  = [1, 2, 3, 4, 5]   # init=[1,2,3,4], last=5
```

### Tuples as dict keys

```python
# (warehouse, sku) as a composite key
stock = {
    ("north", "TENT-3P-GRN"): 100,
    ("south", "TENT-3P-GRN"): 80,
    ("north", "PACK-45L-BLK"): 50,
}

print(stock[("north", "TENT-3P-GRN")])   # 100
```

### Step 1: Run `src/04_tuples.py`

```bash
python3 src/04_tuples.py
```

Expected output:
```
=== Warehouse Locations ===
north  lat=53.48  lon=-2.24
south  lat=51.51  lon=-0.13
west   lat=53.80  lon=-1.55

=== Composite Stock Lookup ===
(north, TENT-3P-GRN)   : 100 units
(south, TENT-3P-GRN)   : 80 units
(north, PACK-45L-BLK)  : 50 units

=== Unpacking examples ===
Swap    : a=2, b=1
Rest    : first=ORD-001, rest=['ORD-002', 'ORD-003', 'ORD-004']
Discard : sku=TENT-3P-GRN, price=89.99
```

---

## Challenge 5 — Comprehensions

**Goal:** Transform and filter collections in one readable line instead of five.

### List comprehensions

The pattern: `[expression for item in iterable if condition]`

```python
# without comprehension
low_stock = []
for sku, qty in inventory.items():
    if qty < 50:
        low_stock.append(sku)

# with comprehension — identical result, one line
low_stock = [sku for sku, qty in inventory.items() if qty < 50]
```

### Dict comprehensions

```python
prices = {"TENT-3P-GRN": 89.99, "PACK-45L-BLK": 149.99, "SLEEP-REG-BLU": 59.99}

# apply a 10% discount to all prices
discounted = {sku: round(price * 0.9, 2) for sku, price in prices.items()}

# flip keys and values
by_price = {price: sku for sku, price in prices.items()}
```

### Filtering with comprehensions

```python
orders = [
    {"order_id": "ORD-001", "status": "pending",   "quantity": 5},
    {"order_id": "ORD-002", "status": "cancelled", "quantity": 2},
    {"order_id": "ORD-003", "status": "pending",   "quantity": 12},
]

pending   = [o for o in orders if o["status"] == "pending"]
order_ids = [o["order_id"] for o in orders]
large     = [o for o in orders if o["quantity"] > 10 and o["status"] == "pending"]
```

### Built-ins that work with any iterable

```python
quantities = [5, 2, 12, 0, 8]

print(sum(quantities))                  # 27
print(max(quantities))                  # 12
print(min(quantities))                  # 0
print(any(q > 10 for q in quantities))  # True — at least one > 10
print(all(q > 0  for q in quantities))  # False — 0 is not > 0
```

### When NOT to use a comprehension

If the logic requires more than a simple expression or condition, a plain `for` loop is clearer:

```python
# too complex for a comprehension — use a loop
results = []
for order in orders:
    value = calculate_value(order, prices)
    if value > 100 and order["status"] == "pending":
        results.append({"order_id": order["order_id"], "value": value})
```

### Step 1: Run `src/05_comprehensions.py`

```bash
python3 src/05_comprehensions.py
```

Expected output:
```
=== Inventory Alerts ===
Low stock  (< 50 units) : ['SLEEP-REG-BLU', 'JACKET-M-RED']
Out of stock            : ['JACKET-M-RED']
Reorder list            : ['SLEEP-REG-BLU', 'JACKET-M-RED']

=== Pricing ===
Original prices  : {'TENT-3P-GRN': 89.99, 'PACK-45L-BLK': 149.99, 'SLEEP-REG-BLU': 59.99, 'JACKET-M-RED': 149.99, 'BOOT-42-BRN': 119.99}
After 10% sale   : {'TENT-3P-GRN': 81.0, 'PACK-45L-BLK': 135.0, 'SLEEP-REG-BLU': 54.0, 'JACKET-M-RED': 135.0, 'BOOT-42-BRN': 108.0}

=== Order Stats ===
Total orders    : 6
Pending         : 4
Total quantity  : 29
Any over 10?    : True
All positive?   : True
```

---

## Challenge 6 — Inventory manager

**Goal:** A working in-memory inventory manager that combines all four data structures.

This is the Phase 2 capstone. The `InventoryManager` is not a class yet (that's Phase 5) — it is a dict acting as the central store, with functions operating on it.

### What it does

- Tracks stock levels per SKU in a `dict`
- Maintains a `set` of SKUs flagged for reorder
- Processes a `list` of incoming orders, adjusting stock on each dispatch
- Returns summaries built with comprehensions
- Uses tuples as composite keys for per-warehouse stock

### Step 1: Run `src/06_inventory_manager.py`

```bash
python3 src/06_inventory_manager.py
```

Expected output:
```
=== Meridian Inventory Manager ===

Processing 8 orders...
ORD-001  TENT-3P-GRN      qty=2   stock: 312 → 310   ✓
ORD-002  PACK-45L-BLK     qty=1   stock:  88 →  87   ✓
ORD-003  SLEEP-REG-BLU    qty=5   stock:  14 →   9   ✓ (low stock flagged)
ORD-004  JACKET-M-RED     qty=4   stock:   0 →   —   ✗ out of stock
ORD-005  TENT-3P-GRN      qty=10  stock: 310 → 300   ✓
ORD-006  BOOT-42-BRN      qty=2   stock: 203 → 201   ✓
ORD-007  SLEEP-REG-BLU    qty=12  stock:   9 →   —   ✗ insufficient stock (need 12, have 9)
ORD-008  PACK-45L-BLK     qty=3   stock:  87 →  84   ✓

=== End of Run ===
Dispatched : 6 orders
Rejected   : 2 orders

Current stock:
  BOOT-42-BRN      :  201
  JACKET-M-RED     :    0  ← REORDER
  PACK-45L-BLK     :   84
  SLEEP-REG-BLU    :    9  ← REORDER
  TENT-3P-GRN      :  300

SKUs needing reorder : ['JACKET-M-RED', 'SLEEP-REG-BLU']
```

---

## What you built

| Before | After |
|---|---|
| Orders stored as a list of dicts with no fast lookup | Inventory in a `dict` — O(1) stock check per SKU |
| Manually scanning for duplicates | `set` deduplication in one line |
| Functions returning one value | Tuples for composite dict keys and clean multi-value returns |
| Multi-line filter loops | Comprehensions that read like plain English |

In Phase 3 (Files & Exceptions) the hardcoded data is replaced by real CSV files. The data structures stay the same — you just load them from disk.

---

## Key things to remember

- `list` for ordered, mutable sequences; `dict` for key→value lookups; `set` for unique membership; `tuple` for fixed records
- Use `dict.get(key, default)` instead of direct access when a key might be missing
- `in` on a `set` or `dict` is O(1); `in` on a `list` is O(n)
- Comprehensions: `[expr for x in iterable if condition]` — keep them simple
- `sorted()` returns a new list; `.sort()` modifies in place
- `sum()`, `min()`, `max()`, `any()`, `all()` work on any iterable
- Tuples are immutable — use them as dict keys, for fixed records, and for multiple return values

---

## Files in this phase

```
phase-2-data-structures/
├── README.md
└── src/
    ├── 01_lists.py              — indexing, slicing, methods, sorting
    ├── 02_dicts.py              — lookup, iteration, nested dicts
    ├── 03_sets.py               — membership, set operations, deduplication
    ├── 04_tuples.py             — immutability, unpacking, composite keys
    ├── 05_comprehensions.py     — list/dict comprehensions, built-in aggregates
    └── 06_inventory_manager.py  — capstone: all four structures working together
```

---

→ **Next: [Phase 3 — Files & Exceptions](../phase-3-files-exceptions/README.md)**
