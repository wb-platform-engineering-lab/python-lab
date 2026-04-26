# Phase 1 — Core Python

> **Concepts introduced:** `if/elif/else`, logical operators, `for`, `while`, `break`, `continue`, `range()`, `enumerate()`, `zip()`, functions, scope, multiple return values, `None`, truthiness | **Difficulty:** Beginner | **Cost:** Free

---

## The problem

Meridian receives 2,400 orders per day across three warehouses. Right now, every order lands in one queue and someone manually decides:

- Is this order valid?
- Which warehouse should fulfil it?
- Is stock available, or does it need to be flagged?
- What is the end-of-day summary?

These decisions follow rules. Rules are `if` statements. Repeated decisions are loops. Reusable logic is functions. By the end of this phase you will have a script that processes a full day's orders automatically.

---

## How Python makes decisions

```
An order arrives
      │
      ▼
  if order["status"] == "cancelled":
      skip it
  elif order["quantity"] > stock:
      flag as unfulfillable
  else:
      route to warehouse
      │
      ▼
  Result recorded
```

Python evaluates conditions top to bottom and executes the first branch that is `True`. Everything else is skipped.

---

## Challenge 1 — Control flow

**Goal:** Use `if/elif/else` to route orders based on their status and priority.

### Step 1: Read `src/01_control_flow.py`

```python
order = {
    "order_id": "ORD-00142",
    "status": "pending",
    "customer_tier": "enterprise",
    "quantity": 5,
}

if order["status"] == "cancelled":
    print(f"{order['order_id']} — skipped (cancelled)")
elif order["status"] == "shipped":
    print(f"{order['order_id']} — already shipped, archive it")
elif order["status"] == "pending":
    print(f"{order['order_id']} — needs processing")
else:
    print(f"{order['order_id']} — unknown status: {order['status']}")
```

### Step 2: Run it

```bash
python3 src/01_control_flow.py
```

Expected output:
```
ORD-00142 — needs processing
enterprise order: flag for priority handling
quantity 5 is within single-pallet limit
```

### Step 3: Logical operators

Combine conditions with `and`, `or`, `not`:

```python
tier     = order["customer_tier"]
quantity = order["quantity"]

# and — both must be True
if tier == "enterprise" and quantity > 100:
    print("large enterprise order — escalate")

# or — at least one must be True
if tier == "enterprise" or tier == "pro":
    print("paid customer — prioritise")

# not — invert a condition
if not order["status"] == "cancelled":
    print("order is active")
```

### Step 4: Chained comparisons

Python lets you chain comparisons naturally:

```python
quantity = 45

if 10 <= quantity <= 100:
    print("standard order")          # True for quantities 10–100

if 0 < quantity < 10:
    print("small order — combine with next batch")
```

### Step 5: The ternary expression

Assign a value based on a condition in one line:

```python
label = "priority" if tier == "enterprise" else "standard"
print(f"Handling: {label}")
```

---

## Challenge 2 — Loops

**Goal:** Process every order in a batch using `for` and `while`.

### Step 1: The `for` loop

```python
orders = ["ORD-001", "ORD-002", "ORD-003"]

for order_id in orders:
    print(f"Processing {order_id}")
```

A `for` loop runs the indented block once per item. `order_id` takes each value in turn.

### Step 2: `range()`

When you need to repeat something N times or iterate over a sequence of numbers:

```python
for i in range(5):          # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 6):       # 1, 2, 3, 4, 5
    print(i)

for i in range(0, 100, 10): # 0, 10, 20, ... 90
    print(i)
```

### Step 3: `enumerate()` — loop with an index

```python
warehouses = ["north", "south", "west"]

for index, name in enumerate(warehouses):
    print(f"{index + 1}. {name}")
```

Output:
```
1. north
2. south
3. west
```

Use `enumerate()` any time you need both the item and its position. Never write `range(len(x))`.

### Step 4: `zip()` — loop over two lists together

```python
skus       = ["TENT-3P-GRN", "PACK-45L-BLK", "SLEEP-REG-BLU"]
quantities = [2, 1, 3]

for sku, qty in zip(skus, quantities):
    print(f"  {sku}: {qty} units")
```

### Step 5: `break` and `continue`

```python
orders = ["ORD-001", "ORD-002", "CANCELLED", "ORD-004", "ORD-005"]

for order_id in orders:
    if order_id == "CANCELLED":
        continue                  # skip this iteration, keep looping
    if order_id == "ORD-004":
        break                     # stop the loop entirely
    print(f"Processing {order_id}")
```

Output:
```
Processing ORD-001
Processing ORD-002
```

### Step 6: The `while` loop

`while` repeats as long as a condition is `True`:

```python
retries = 0
max_retries = 3
success = False

while not success and retries < max_retries:
    print(f"Attempt {retries + 1}: calling warehouse API...")
    retries += 1
    if retries == 2:        # simulate success on attempt 2
        success = True

if success:
    print("Connected.")
else:
    print("Failed after 3 attempts.")
```

Use `while` when you don't know in advance how many iterations you need. Use `for` when you're iterating over a known sequence.

### Step 7: Run the full loop script

```bash
python3 src/02_loops.py
```

Expected output:
```
=== Batch Processing 5 orders ===
[1/5] ORD-001  pending     north   qty=2   → dispatched
[2/5] ORD-002  cancelled   south   qty=1   → skipped
[3/5] ORD-003  pending     west    qty=5   → dispatched
[4/5] ORD-004  pending     north   qty=12  → dispatched
[5/5] ORD-005  shipped     south   qty=3   → already shipped

Dispatched : 3
Skipped    : 1
Archived   : 1
```

---

## Challenge 3 — Functions and scope

**Goal:** Write functions that return values, handle edge cases with early returns, and understand where variables live.

### Scope — where variables exist

```python
threshold = 100          # module-level variable — visible everywhere in this file

def check_stock(available):
    message = "low stock"    # local variable — only exists inside check_stock
    return available < threshold

print(check_stock(50))   # True
print(message)           # NameError — message doesn't exist here
```

Variables created inside a function are **local** — they disappear when the function returns. Variables at the top of the file are **module-level** — visible to all functions in the file.

### Early returns

Return as soon as you have the answer. Avoid deep nesting:

```python
# hard to read — three levels of nesting
def route_order(order):
    if order["status"] == "pending":
        if order["quantity"] > 0:
            if order["warehouse"] in VALID_WAREHOUSES:
                return order["warehouse"]

# easier to read — early returns flatten the logic
def route_order(order):
    if order["status"] != "pending":
        return None
    if order["quantity"] <= 0:
        return None
    if order["warehouse"] not in VALID_WAREHOUSES:
        return None
    return order["warehouse"]
```

### Multiple return values

Python functions can return more than one value — they come back as a tuple you can unpack:

```python
def summarise_batch(orders):
    """Return (dispatched_count, skipped_count, total_value)."""
    dispatched = 0
    skipped    = 0
    total      = 0.0

    for order in orders:
        if order["status"] == "cancelled":
            skipped += 1
        else:
            dispatched += 1
            total += order["quantity"] * order["unit_price"]

    return dispatched, skipped, total   # returns a tuple


dispatched, skipped, value = summarise_batch(orders)   # unpack immediately
print(f"Dispatched: {dispatched}, Skipped: {skipped}, Value: ${value:,.2f}")
```

### Step 1: Run `src/03_functions.py`

```bash
python3 src/03_functions.py
```

Expected output:
```
=== Order Routing ===
ORD-001 → north     (enterprise, qty=2)
ORD-002 → None      (cancelled)
ORD-003 → west      (pro, qty=5)
ORD-004 → north     (free, qty=12)
ORD-005 → None      (already shipped)

=== Batch Summary ===
Dispatched : 3 orders
Skipped    : 2 orders
Batch value: $2,847.50
```

---

## Challenge 4 — None and truthiness

**Goal:** Understand Python's concept of "nothing" and how to write clean conditional checks.

### `None` — the absence of a value

`None` is Python's way of saying "there is no value here". It is not zero. It is not an empty string. It is the explicit absence of a value.

```python
draft_response = None      # no draft yet

if draft_response is None:
    print("no draft — generate one")
else:
    print(f"draft ready: {draft_response}")
```

Always use `is None` / `is not None` to check for None — not `== None`.

### Truthiness — what counts as True or False

Python evaluates these as `False` in an `if` statement:

| Value | Truthiness |
|---|---|
| `None` | False |
| `0` | False |
| `0.0` | False |
| `""` (empty string) | False |
| `[]` (empty list) | False |
| `{}` (empty dict) | False |
| Everything else | True |

```python
orders = []
if orders:
    print("process orders")
else:
    print("no orders today")    # prints this — empty list is falsy

stock = 0
if not stock:
    print("out of stock")       # prints this — 0 is falsy
```

### The trap: `if x` vs `if x is not None`

```python
quantity = 0

if quantity:                    # False — 0 is falsy
    print("has quantity")       # never prints

if quantity is not None:        # True — 0 is not None
    print("quantity was set")   # prints this
```

Use `if x is not None` when `0` or `""` are valid values you want to keep. Use `if x` when any falsy value should be treated as "nothing".

### Step 1: Run `src/04_none_truthiness.py`

```bash
python3 src/04_none_truthiness.py
```

Expected output:
```
=== Order Validation ===
ORD-001: valid   — 2 units, warehouse=north
ORD-002: invalid — missing warehouse
ORD-003: invalid — quantity is 0
ORD-004: valid   — 8 units, warehouse=west
ORD-005: invalid — cancelled

Valid orders   : 2
Invalid orders : 3
```

---

## Challenge 5 — Mini order processor

**Goal:** Combine everything from this phase into a script that processes a full batch of orders and prints a report.

This is the payoff. No new syntax — just everything working together.

### What it does

1. Loops over a list of orders
2. Validates each order (checks for missing fields, cancelled status, zero quantity)
3. Routes valid orders to the correct warehouse
4. Calculates the value of each dispatched order
5. Prints a per-order log and an end-of-batch summary

### Step 1: Run it

```bash
python3 src/05_order_processor.py
```

Expected output:
```
=== Meridian Order Processor ===
Processing batch of 8 orders...

ORD-001  enterprise  north   TENT-3P-GRN      qty=2   $179.98   → dispatched
ORD-002  pro         south   PACK-45L-BLK     qty=1   $149.99   → dispatched
ORD-003  free        west    SLEEP-REG-BLU    qty=0   $0.00     → rejected (zero quantity)
ORD-004  enterprise  north   JACKET-M-RED     qty=4   $599.96   → dispatched
ORD-005  pro         —       BOOT-42-BRN      qty=2   —         → rejected (missing warehouse)
ORD-006  free        west    TENT-3P-GRN      qty=1   $89.99    → dispatched
ORD-007  enterprise  south   PACK-45L-BLK     qty=3   $449.97   → dispatched (cancelled order skipped)
ORD-008  pro         north   SLEEP-REG-BLU    qty=6   $359.94   → dispatched

=== End of Batch Summary ===
Total orders    : 8
Dispatched      : 6
Rejected        : 2
Batch value     : $1,829.84
By warehouse    : north=$779.94  south=$599.96  west=$449.98
Fill rate       : 75.0%
```

### Step 2: Trace through the code

Open `src/05_order_processor.py` and follow one order through every function call:

1. `process_batch(orders)` — loops over orders, calls `process_order()` for each
2. `process_order(order, prices)` — validates, routes, calculates value
3. `validate_order(order)` — returns `(True, None)` or `(False, reason)`
4. `calculate_value(order, prices)` — returns a float
5. `print_summary(results)` — aggregates and formats the final report

Every function does one thing. Each one is testable on its own. This is the pattern you will use in every phase from here on.

---

## What you built

| Before | After |
|---|---|
| Manual triage of every order | Every order classified in one loop |
| "Is this order valid?" answered by a human | `validate_order()` answers it in microseconds |
| Warehouse routing done from memory | `route_order()` applies the rules consistently |
| End-of-day summary built from a spreadsheet | `print_summary()` generates it from the processed data |

The processor handles 8 orders here. In Phase 3 (Files) you will feed it real CSV data — thousands of rows, same code.

---

## Key things to remember

- `if/elif/else` — Python executes the **first** matching branch only
- `for` for known sequences, `while` when you don't know how many iterations
- Use `enumerate()` instead of `range(len(x))` when you need the index
- Use `zip()` to loop over two lists in parallel
- `break` exits the loop; `continue` skips to the next iteration
- Variables created inside a function are **local** — they don't leak out
- Use **early returns** to flatten nested logic
- Functions can return multiple values — unpack them immediately
- Use `is None` / `is not None` for None checks, never `== None`
- Empty list, `0`, `""`, and `None` are all **falsy** — know when that matters

---

## Files in this phase

```
phase-1-core-python/
├── README.md
└── src/
    ├── 01_control_flow.py     — Challenge 1: if/elif/else, logical operators
    ├── 02_loops.py            — Challenge 2: for, while, break, continue, enumerate, zip
    ├── 03_functions.py        — Challenge 3: scope, early returns, multiple return values
    ├── 04_none_truthiness.py  — Challenge 4: None, is/is not, truthiness
    └── 05_order_processor.py  — Challenge 5: full mini processor combining all concepts
```

---

→ **Next: [Phase 2 — Data Structures](../phase-2-data-structures/README.md)**
