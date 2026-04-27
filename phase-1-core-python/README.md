# Phase 1 — Core Python

> **Concepts introduced:** `if/elif/else`, logical operators, `for`, `while`, `break`, `continue`, `range()`, `enumerate()`, `zip()`, functions, scope, multiple return values, `None`, truthiness | **Difficulty:** Beginner | **Cost:** Free

---

## The problem

Meridian receives 2,400 orders per day across three warehouses. Right now, every order lands in one queue and someone manually decides:

- Is this order valid?
- Which warehouse should fulfil it?
- Is stock available, or does it need to be flagged?
- What is the end-of-day summary?

These decisions follow rules. Rules are `if` statements. Repeated decisions are loops. Reusable logic is functions. By the end of this phase you will have written a script that processes a full day's orders automatically.

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

### Concept: if / elif / else

Every `if` block has three parts:
- `if` — the condition that is checked first
- `elif` — checked only when the `if` above was `False` (you can have as many as you need)
- `else` — runs when nothing above matched (optional)

Python stops at the **first** matching branch — branches below it are not checked.

```python
order = {"order_id": "ORD-00142", "status": "pending"}

if order["status"] == "cancelled":
    print(f"{order['order_id']} — skipped")         # runs if status is "cancelled"
elif order["status"] == "shipped":
    print(f"{order['order_id']} — archive it")      # runs if status is "shipped"
elif order["status"] == "pending":
    print(f"{order['order_id']} — needs processing") # runs if status is "pending"
else:
    print(f"{order['order_id']} — unknown status")  # runs for anything else
```

### Concept: logical operators

Combine conditions with `and`, `or`, `not`:

```python
tier     = "enterprise"
quantity = 150

# and — BOTH conditions must be True
if tier == "enterprise" and quantity > 100:
    print("large enterprise order — escalate")

# or — AT LEAST ONE condition must be True
if tier == "enterprise" or tier == "pro":
    print("paid customer — prioritise")

# not — inverts a condition
if not order["status"] == "cancelled":
    print("order is active")
```

### Concept: chained comparisons

Python lets you chain comparisons the way you would write them in maths:

```python
quantity = 45

if 10 <= quantity <= 100:
    print("standard order")   # True when quantity is 10, 11, ..., 100

if 0 < quantity < 10:
    print("small order")      # True when quantity is 1, 2, ..., 9
```

This is cleaner than writing `quantity >= 10 and quantity <= 100`.

### Concept: the ternary expression

Assign a value based on a condition in one line:

```python
# pattern: value_if_true  if  condition  else  value_if_false
label = "priority" if tier == "enterprise" else "standard"
print(f"Handling: {label}")
```

Use this only when both branches fit on one readable line. For anything more complex, use a full `if/else` block.

### Step 1: Run the demo

```bash
python3 src/01_control_flow.py
```

Read through the file and the output. Notice how each case is handled separately, how the loop at the bottom uses `continue` to skip early, and how the early returns keep the logic flat.

### Your turn — exercises

**Option A — interactive exercises (file with assertions)**

```bash
python3 src/01_control_flow_test.py
```

Open `src/01_control_flow_test.py`. Replace each `pass` with your implementation. The `assert` statements at the bottom verify your code automatically — a passing run prints `"All checks passed."`. Work through the four functions one at a time.

**Option B — open-ended exercises**

Scroll to the `# YOUR TURN` section at the bottom of `src/01_control_flow.py`. Complete the three exercises there. Run the file after each one to see your output.

---

## Challenge 2 — Loops

**Goal:** Process every order in a batch using `for` and `while`.

### Concept: for loop

A `for` loop runs the indented block once per item. The variable before `in` takes each value in turn:

```python
orders = ["ORD-001", "ORD-002", "ORD-003"]

for order_id in orders:
    print(f"Processing {order_id}")
```

You do not need to track an index or call `next()` yourself — Python does it.

### Concept: range()

When you need to repeat something N times or work with a sequence of numbers:

```python
for i in range(5):          # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 6):       # 1, 2, 3, 4, 5
    print(i)

for i in range(0, 100, 10): # 0, 10, 20, ... 90
    print(i)
```

`range(start, stop, step)` — stop is **not** included.

### Concept: enumerate() — loop with a position

When you need both the item **and** its index, use `enumerate()`:

```python
warehouses = ["north", "south", "west"]

for index, name in enumerate(warehouses):
    print(f"{index + 1}. {name}")
# 1. north
# 2. south
# 3. west
```

`enumerate()` returns `(index, item)` pairs. Unpack them directly in the `for` line.

> **Rule:** never write `for i in range(len(x))` when you need an index — use `enumerate(x)` instead.

### Concept: zip() — loop over two lists together

When you need to pair items from two lists:

```python
skus       = ["TENT-3P-GRN", "PACK-45L-BLK", "SLEEP-REG-BLU"]
quantities = [2, 1, 3]

for sku, qty in zip(skus, quantities):
    print(f"  {sku}: {qty} units")
```

`zip()` stops at the shorter list. If the lists may be different lengths, you will need `itertools.zip_longest` — but for now, assume they match.

### Concept: break and continue

```python
orders = ["ORD-001", "ORD-002", "CANCELLED", "ORD-004", "ORD-005"]

for order_id in orders:
    if order_id == "CANCELLED":
        continue     # skip THIS iteration and move to the next one
    if order_id == "ORD-004":
        break        # exit the loop entirely — nothing after this runs
    print(f"Processing {order_id}")
# Processing ORD-001
# Processing ORD-002
```

`continue` jumps to the next iteration. `break` ends the loop.

### Concept: while loop

`while` repeats as long as a condition is `True`. Use it when you do not know in advance how many iterations you need:

```python
retries = 0
max_retries = 3
success = False

while not success and retries < max_retries:
    print(f"Attempt {retries + 1}: calling warehouse API...")
    retries += 1
    if retries == 2:
        success = True   # simulate success on attempt 2

if success:
    print("Connected.")
else:
    print("Failed after 3 attempts.")
```

> Use `for` when iterating over a known sequence. Use `while` when the stop condition depends on something that changes during the loop.

### Step 1: Run the demo

```bash
python3 src/02_loops.py
```

Expected output:
```
=== Batch Processing 5 orders ===
[1/5] ORD-001  pending    north   qty=2   → dispatched
[2/5] ORD-002  cancelled  south   qty=1   → skipped
[3/5] ORD-003  pending    west    qty=5   → dispatched
[4/5] ORD-004  pending    north   qty=12  → dispatched
[5/5] ORD-005  shipped    south   qty=3   → already shipped

Dispatched : 3
Skipped    : 1
Archived   : 1
```

### Your turn — exercises

Scroll to the `# YOUR TURN` section at the bottom of `src/02_loops.py`. Complete the four exercises there. Each one practises a different loop tool — work through them in order.

```bash
python3 src/02_loops.py
```

---

## Challenge 3 — Functions and scope

**Goal:** Write functions that return values, handle edge cases with early returns, and understand where variables live.

### Concept: scope — where variables exist

Variables created inside a function are **local** — they only exist while that function is running and disappear when it returns. Variables at the top of a file are **module-level** — visible to all code in that file.

```python
threshold = 100          # module-level — visible everywhere in this file

def check_stock(available):
    message = "low stock"    # local — only exists inside check_stock
    return available < threshold

print(check_stock(50))   # True
print(message)           # NameError — message doesn't exist here
```

The key rule: **functions can read module-level variables, but variables they create stay inside them.**

### Concept: early returns

Return as soon as you have the answer. This keeps your code flat and readable:

```python
# hard to read — three levels of nesting
def route_order(order):
    if order["status"] == "pending":
        if order["quantity"] > 0:
            if order["warehouse"] in VALID_WAREHOUSES:
                return order["warehouse"]

# easier to read — one guard per line, no nesting
def route_order(order):
    if order["status"] != "pending":
        return None
    if order["quantity"] <= 0:
        return None
    if order["warehouse"] not in VALID_WAREHOUSES:
        return None
    return order["warehouse"]
```

Each guard checks one condition and exits early on failure. The final `return` only runs when everything passed. This pattern is called **guard clauses**.

### Concept: multiple return values

A function can return more than one value by separating them with a comma. Python packages them as a tuple, and you unpack them on the calling side:

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

    return dispatched, skipped, total   # three values, comma-separated


dispatched, skipped, value = summarise_batch(orders)   # unpack on one line
print(f"Dispatched: {dispatched}, Skipped: {skipped}, Value: ${value:,.2f}")
```

Unpack immediately at the call site — avoid indexing into the tuple later (`result[0]`, etc.).

### Step 1: Run the demo

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

### Your turn — exercises

Scroll to the `# YOUR TURN` section at the bottom of `src/03_functions.py`. You will find two function stubs — `classify_order` and `batch_statistics` — with rules in their docstrings.

The file already has three complete example functions above (`route_order`, `calculate_value`, `summarise_batch`). Read them carefully to understand the patterns, then implement the stubs.

```bash
python3 src/03_functions.py
```

The verification output at the bottom of the file shows the expected result.

---

## Challenge 4 — None and truthiness

**Goal:** Understand Python's concept of "nothing" and how to write clean conditional checks.

### Concept: None — the absence of a value

`None` is Python's way of saying "there is no value here". It is not zero. It is not an empty string. It is the **explicit absence** of a value.

```python
draft_response = None      # no draft yet

if draft_response is None:
    print("no draft — generate one")
else:
    print(f"draft ready: {draft_response}")
```

**Always** use `is None` or `is not None` to check for None — not `== None`. The `is` operator checks identity (is this the exact `None` object?), not equality.

### Concept: truthiness — what counts as True or False

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

### Concept: the trap — `if x` vs `if x is not None`

This is the most common mistake when working with numeric values:

```python
quantity = 0

if quantity:                    # False — 0 is falsy, so this block is skipped
    print("has quantity")

if quantity is not None:        # True — 0 is not None, so this block runs
    print("quantity was set")   # prints this
```

`if quantity` treats `0` as "no value". `if quantity is not None` correctly treats `0` as a valid value that happens to be zero.

**Use `if x is not None`** when `0` or `""` are valid values you want to keep.
**Use `if x`** when any falsy value means "nothing useful is here".

### Step 1: Run the demo

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

### Your turn — exercises

Scroll to the `# YOUR TURN` section at the bottom of `src/04_none_truthiness.py`. Complete two exercises:

1. **Implement `validate_shipment()`** — same pattern as `validate_order()` above, applied to a different domain. The rules and hints are in the docstring.
2. **Fix `buggy_validate()`** — three bugs related to None checks and truthiness. Identify each one and correct it.

```bash
python3 src/04_none_truthiness.py
```

---

## Challenge 5 — Mini order processor

**Goal:** Implement a complete order processing script using everything from this phase.

This is the capstone. There is no demo to run first — **you write everything**. The script processes a full batch of orders and prints a report.

### What you will build

`src/05_order_processor.py` contains five function stubs with docstrings, hints, and the data already set up. The main script at the bottom calls your functions. Your output must match the expected output below.

### The five functions

Work through them top to bottom — each one depends on the one before it:

| Function | What it does |
|---|---|
| `validate_order(order)` | Returns `(True, None)` or `(False, reason)` |
| `calculate_value(order, prices)` | Returns `unit_price × quantity` |
| `process_order(order, prices)` | Validates, calculates, returns a result dict |
| `process_batch(orders, prices)` | Loops over orders, returns list of result dicts |
| `print_summary(results)` | Aggregates and prints the final report |

### Step 1: Implement the functions

Open `src/05_order_processor.py`. Read each docstring in full before writing any code for that function. The docstrings tell you the exact rules, the return shape, and where the tricky parts are.

```bash
python3 src/05_order_processor.py
```

Run after each function. The output will be incomplete (or crash) until all five are done, but running early helps you catch mistakes.

### Step 2: Verify your output

When all five functions are implemented, your output should be:

```
=== Meridian Order Processor ===
Processing batch of 8 orders...

ORD-001  enterprise   north   TENT-3P-GRN      qty=2  $179.98    → dispatched
ORD-002  pro          south   PACK-45L-BLK     qty=1  $149.99    → dispatched
ORD-003  free         west    SLEEP-REG-BLU    qty=0  —          → rejected (zero quantity)
ORD-004  enterprise   north   JACKET-M-RED     qty=4  $599.96    → dispatched
ORD-005  pro          —       BOOT-42-BRN      qty=2  —          → rejected (missing warehouse)
ORD-006  free         west    TENT-3P-GRN      qty=1  $89.99     → dispatched
ORD-007  enterprise   south   PACK-45L-BLK     qty=3  —          → rejected (cancelled)
ORD-008  pro          north   SLEEP-REG-BLU    qty=6  $359.94    → dispatched

=== End of Batch Summary ===
Total orders    : 8
Dispatched      : 5
Rejected        : 3
Batch value     : $1,379.86
By warehouse    : north=$779.94  south=$149.99  west=$89.99
Fill rate       : 62.5%
```

### Step 3: Trace through the code

Once it works, trace one order through all five function calls manually. Follow `ORD-005` (the one with `warehouse=None`):

1. `process_batch(orders, PRICES)` — picks up ORD-005 in the loop
2. `process_order(order, PRICES)` — calls validate_order
3. `validate_order(order)` — which rule catches it? What does it return?
4. Back in `process_order` — what does the result dict look like?
5. `print_summary(results)` — does ORD-005 appear in dispatched or rejected?

Every function does one thing. Each one is testable on its own. This is the pattern you will use in every phase from here on.

---

## What you built

| Before | After |
|---|---|
| Manual triage of every order | Every order classified in one loop |
| "Is this order valid?" answered by a human | `validate_order()` answers it in microseconds |
| Warehouse routing done from memory | `validate_order()` applies the rules consistently |
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
- Use **early returns** (guard clauses) to flatten nested logic
- Functions can return multiple values — unpack them immediately
- Use `is None` / `is not None` for None checks, never `== None`
- Empty list, `0`, `""`, and `None` are all **falsy** — know when that matters

---

## Files in this phase

```
phase-1-core-python/
├── README.md
└── src/
    ├── 01_control_flow.py      — demo: if/elif/else, logical operators
    ├── 01_control_flow_test.py — exercises: implement four functions, asserts verify your work
    ├── 02_loops.py             — demo + exercises: for, while, break, continue, enumerate, zip
    ├── 03_functions.py         — demo + exercises: scope, early returns, multiple return values
    ├── 04_none_truthiness.py   — demo + exercises: None, is/is not, truthiness
    └── 05_order_processor.py   — capstone exercise: implement the full mini processor
```

---

→ **Next: [Phase 2 — Data Structures](../phase-2-data-structures/README.md)**
