# Phase 3 — Files & Exceptions

> **Concepts introduced:** `open()`, file modes, `with` statement, `csv.DictReader/DictWriter`, `json.load/dump`, `try/except/else/finally`, raising exceptions, custom exception classes, `pathlib.Path` | **Difficulty:** Beginner–Intermediate | **Cost:** Free

---

## The problem

The inventory manager from Phase 2 runs on hardcoded data. That was fine for learning — but Meridian's real orders arrive as CSV exports from their order management system, and their warehouse stock levels are stored in a JSON config that the ops team edits.

Every time you change the data, you should not have to change the code. The code reads from files. The files hold the data. This phase teaches you how to read and write both.

It also teaches you what to do when things go wrong. Files can be missing. CSV rows can be malformed. JSON can be invalid. A program that crashes on the first bad row is not production code. A program that catches errors, logs them, and keeps processing is.

---

## How Python works with files

```
Your script                 The file system
───────────────────         ──────────────────────────────
with open("orders.csv")     open a channel to the file
    reader = csv.DictReader     wrap it with a CSV parser
    for row in reader:          read one row at a time
        process(row)            each row is a dict of field→value
                            file closed automatically when with block exits
```

The `with` statement guarantees the file is closed even if an exception is raised inside the block. Always use `with open(...)` — never call `open()` without it.

---

## Challenge 1 — Text files

**Goal:** Read and write plain text files. Understand file modes and the `with` statement.

### File modes

| Mode | Meaning |
|---|---|
| `"r"` | Read (default). File must exist. |
| `"w"` | Write. Creates file if missing. **Overwrites** if it exists. |
| `"a"` | Append. Creates file if missing. Adds to the end if it exists. |
| `"x"` | Exclusive create. Fails if file already exists. |

### Reading

```python
with open("data/orders.csv", "r") as f:
    contents = f.read()       # entire file as one string

with open("data/orders.csv", "r") as f:
    for line in f:            # iterate line by line — memory-efficient for large files
        print(line.rstrip())  # rstrip() removes the trailing newline
```

### Writing

```python
with open("output/report.txt", "w") as f:
    f.write("=== Daily Report ===\n")
    f.write(f"Orders processed: 12\n")

# append to an existing file (or create it)
with open("output/report.txt", "a") as f:
    f.write("Appended line\n")
```

### `pathlib.Path` — the modern way to handle paths

```python
from pathlib import Path

data_dir = Path("data")
orders_file = data_dir / "orders.csv"       # / operator builds paths

print(orders_file.exists())                 # True / False
print(orders_file.suffix)                   # ".csv"
print(orders_file.stem)                     # "orders"

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)             # create dir if it doesn't exist
```

### Step 1: Run `src/01_text_files.py`

```bash
python3 src/01_text_files.py
```

Expected output:
```
=== Reading orders.csv (raw) ===
Line 1 : order_id,sku,quantity,warehouse,customer_tier,status
Line 2 : ORD-001,TENT-3P-GRN,2,north,enterprise,pending
Line 3 : ORD-002,PACK-45L-BLK,1,south,pro,pending
... (12 data lines)

Total lines (including header): 13

Report written to output/report.txt
```

---

## Challenge 2 — CSV files

**Goal:** Parse orders from `data/orders.csv` using `csv.DictReader` and write results with `csv.DictWriter`.

### Why `DictReader` instead of `reader`

```python
import csv

# csv.reader — rows as lists, you address fields by index
with open("data/orders.csv") as f:
    reader = csv.reader(f)
    next(reader)                  # skip the header row manually
    for row in reader:
        order_id = row[0]         # fragile — breaks if column order changes
        sku      = row[1]

# csv.DictReader — rows as dicts, you address fields by name
with open("data/orders.csv") as f:
    reader = csv.DictReader(f)    # header row consumed automatically
    for row in reader:
        order_id = row["order_id"]   # robust — column order doesn't matter
        sku      = row["sku"]
```

Always use `DictReader`. Column order in CSV files changes. Field names don't (or shouldn't).

### Writing CSV with `DictWriter`

```python
import csv

results = [
    {"order_id": "ORD-001", "status": "dispatched", "value": 179.98},
    {"order_id": "ORD-002", "status": "dispatched", "value": 149.99},
]

with open("output/results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["order_id", "status", "value"])
    writer.writeheader()
    writer.writerows(results)
```

Note: always pass `newline=""` when opening a file for CSV writing — it prevents double newlines on Windows.

### Step 1: Run `src/02_csv_files.py`

```bash
python3 src/02_csv_files.py
```

Expected output:
```
=== Orders loaded from CSV ===
Loaded 12 orders

order_id  sku                  qty  warehouse  tier        status
ORD-001   TENT-3P-GRN          2    north      enterprise  pending
ORD-002   PACK-45L-BLK         1    south      pro         pending
ORD-003   SLEEP-REG-BLU        5    west       free        pending
...

Products loaded: 5

Results written to output/results.csv (12 rows)
```

---

## Challenge 3 — JSON files

**Goal:** Load inventory from `data/inventory.json` and save updated stock back to disk.

### Reading JSON

```python
import json

with open("data/inventory.json") as f:
    inventory = json.load(f)      # parses the file into a Python dict/list

print(inventory["TENT-3P-GRN"]["stock"])   # 312
```

### Writing JSON

```python
with open("data/inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)   # indent=2 makes it human-readable
```

### `json.loads` / `json.dumps` — for strings, not files

```python
# when you have a JSON string (e.g. from an API response):
raw = '{"sku": "TENT-3P-GRN", "stock": 312}'
data = json.loads(raw)          # string → Python object

# when you need a JSON string (e.g. to send to an API):
payload = json.dumps(data, indent=2)   # Python object → string
```

### What JSON can and cannot store

| Python type | JSON equivalent |
|---|---|
| `dict` | object `{}` |
| `list` | array `[]` |
| `str` | string `""` |
| `int` / `float` | number |
| `True` / `False` | `true` / `false` |
| `None` | `null` |
| `tuple` | array `[]` (loses tuple type on reload) |
| `datetime` | ✗ — must convert to string first |
| custom class | ✗ — must serialise manually |

### Step 1: Run `src/03_json_files.py`

```bash
python3 src/03_json_files.py
```

Expected output:
```
=== Inventory loaded from JSON ===
TENT-3P-GRN      stock=312  threshold=50   OK
PACK-45L-BLK     stock= 88  threshold=30   OK
SLEEP-REG-BLU    stock= 14  threshold=20   REORDER
JACKET-M-RED     stock=  0  threshold=25   OUT OF STOCK
BOOT-42-BRN      stock=203  threshold=40   OK

Dispatching 10 units of TENT-3P-GRN...
Stock updated: 312 → 302

Updated inventory saved to output/inventory_updated.json
```

---

## Challenge 4 — Exceptions

**Goal:** Handle errors gracefully so one bad row doesn't crash the whole pipeline.

### The try/except pattern

```python
try:
    result = int("abc")          # raises ValueError
except ValueError as e:
    print(f"conversion failed: {e}")
```

Python stops executing the `try` block the moment an exception is raised and jumps to the matching `except`.

### Catching specific exceptions

Always catch the most specific exception you can:

```python
try:
    with open("missing.csv") as f:
        data = json.load(f)
except FileNotFoundError:
    print("file not found")
except json.JSONDecodeError as e:
    print(f"invalid JSON: {e}")
except Exception as e:
    print(f"unexpected error: {e}")   # catch-all — last resort only
```

Never write a bare `except:` (no exception type). It catches `KeyboardInterrupt` and `SystemExit`, which makes your program impossible to stop.

### `else` and `finally`

```python
try:
    value = int(row["quantity"])
except ValueError:
    value = 0
    print("bad quantity — defaulting to 0")
else:
    print("quantity parsed ok")     # runs only if no exception was raised
finally:
    print("this always runs")       # cleanup — runs whether or not there was an error
```

### Raising exceptions

```python
def load_inventory(path):
    if not Path(path).exists():
        raise FileNotFoundError(f"inventory file not found: {path}")
    with open(path) as f:
        return json.load(f)
```

Raise when the caller needs to know something went wrong and cannot proceed. Don't raise for normal control flow.

### Step 1: Run `src/04_exceptions.py`

```bash
python3 src/04_exceptions.py
```

Expected output:
```
=== Processing orders with error handling ===
ORD-001   TENT-3P-GRN      qty=2    → ok
ORD-002   PACK-45L-BLK     qty=1    → ok
ORD-003   SLEEP-REG-BLU    qty=5    → ok
ORD-004   JACKET-M-RED     qty=4    → ok
ORD-005   BOOT-42-BRN      qty=2    → ok
ORD-006   TENT-3P-GRN      qty=1    → ok
ORD-007   PACK-45L-BLK     qty=3    → skipped (cancelled)
ORD-008   SLEEP-REG-BLU    qty=6    → ok
ORD-009   JACKET-M-RED     qty=0    → error: zero quantity (ValueError)
ORD-010   BOOT-42-BRN      qty=8    → ok
ORD-011   TENT-3P-GRN      qty=12   → ok
ORD-012   UNKNOWN-SKU      qty=2    → error: unknown SKU (KeyError)

Processed : 10
Skipped   : 1
Errors    : 2
```

---

## Challenge 5 — Custom exceptions

**Goal:** Define your own exception hierarchy so callers can handle different error cases precisely.

### Why custom exceptions?

```python
# with built-in exceptions — caller can't distinguish error types
raise ValueError("unknown SKU")
raise ValueError("zero quantity")
raise ValueError("insufficient stock")

# with custom exceptions — caller can handle each case differently
raise UnknownSKUError("CRAMPONS-S")
raise ZeroQuantityError("ORD-009")
raise InsufficientStockError(sku="TENT-3P-GRN", requested=50, available=12)
```

### Defining a hierarchy

```python
class MeridianError(Exception):
    """Base class for all Meridian application errors."""

class OrderError(MeridianError):
    """Raised when an order cannot be processed."""

class UnknownSKUError(OrderError):
    def __init__(self, sku):
        self.sku = sku
        super().__init__(f"unknown SKU: {sku}")

class InsufficientStockError(OrderError):
    def __init__(self, sku, requested, available):
        self.sku       = sku
        self.requested = requested
        self.available = available
        super().__init__(
            f"{sku}: requested {requested}, only {available} available"
        )
```

Catching a parent class catches all its children:

```python
try:
    dispatch(order)
except OrderError as e:
    log_error(e)           # catches UnknownSKUError, InsufficientStockError, etc.
```

### Step 1: Run `src/05_custom_exceptions.py`

```bash
python3 src/05_custom_exceptions.py
```

Expected output:
```
=== Dispatch with custom exceptions ===
ORD-001  TENT-3P-GRN      qty=2   → dispatched ($179.98)
ORD-004  JACKET-M-RED     qty=4   → OrderError: JACKET-M-RED: out of stock
ORD-009  JACKET-M-RED     qty=0   → OrderError: ORD-009: zero quantity
ORD-011  TENT-3P-GRN      qty=50  → OrderError: TENT-3P-GRN: requested 50, only 308 available
ORD-012  UNKNOWN-SKU      qty=2   → OrderError: unknown SKU: UNKNOWN-SKU

Catching by specific type:
  InsufficientStockError on ORD-011: sku=TENT-3P-GRN requested=50 available=308
```

---

## Challenge 6 — File pipeline (capstone)

**Goal:** A complete pipeline that reads from files, processes data, handles every error, and writes results — just like production code does.

### What it does

1. Loads inventory from `data/inventory.json`
2. Loads products from `data/products.csv`
3. Reads orders from `data/orders.csv` one row at a time
4. Validates and dispatches each order, catching all errors
5. Writes dispatched orders to `output/dispatched.csv`
6. Writes rejected orders and reasons to `output/rejected.csv`
7. Saves the updated inventory back to `output/inventory_updated.json`
8. Appends a run summary to `output/run_log.txt`

No order crashes the pipeline. Every error is caught, recorded, and the next order is processed.

### Step 1: Run it

```bash
python3 src/06_pipeline.py
```

Expected output:
```
=== Meridian File Pipeline ===
Loaded 5 SKUs from data/inventory.json
Loaded 5 products from data/products.csv
Processing data/orders.csv...

ORD-001   TENT-3P-GRN      qty=2    $179.98   → dispatched
ORD-002   PACK-45L-BLK     qty=1    $149.99   → dispatched
ORD-003   SLEEP-REG-BLU    qty=5    $299.95   → dispatched
ORD-004   JACKET-M-RED     qty=4    —         → rejected: out of stock
ORD-005   BOOT-42-BRN      qty=2    $239.98   → dispatched
ORD-006   TENT-3P-GRN      qty=1    $89.99    → dispatched
ORD-007   PACK-45L-BLK     qty=3    —         → rejected: cancelled
ORD-008   SLEEP-REG-BLU    qty=6    $359.94   → dispatched
ORD-009   JACKET-M-RED     qty=0    —         → rejected: zero quantity
ORD-010   BOOT-42-BRN      qty=8    $959.92   → dispatched
ORD-011   TENT-3P-GRN      qty=12   $1079.88  → dispatched
ORD-012   UNKNOWN-SKU      qty=2    —         → rejected: unknown SKU

=== Run Complete ===
Dispatched : 8   →  output/dispatched.csv
Rejected   : 4   →  output/rejected.csv
Batch value: $3,359.63
Updated inventory → output/inventory_updated.json
Run log appended  → output/run_log.txt
```

### Step 2: Inspect the output files

```bash
cat output/dispatched.csv
cat output/rejected.csv
cat output/run_log.txt
```

---

## What you built

| Before | After |
|---|---|
| Data hardcoded in Python variables | Loaded from CSV and JSON files at runtime |
| Any bad row crashes the whole script | Every error caught, logged, pipeline continues |
| No record of what happened | Results written to output files, log appended on each run |
| Output printed to terminal only | Structured CSV output ready for the next system to consume |

In Phase 5 (OOP) the pipeline functions become methods on a `Pipeline` class. In Phase 7 (Testing) you will write tests that feed known-bad files to the pipeline and assert the errors are handled correctly.

---

## Key things to remember

- Always use `with open(...)` — it guarantees the file is closed
- Use `"r"` to read, `"w"` to overwrite, `"a"` to append
- `csv.DictReader` gives you rows as dicts — always prefer it over `csv.reader`
- Pass `newline=""` when opening files for CSV writing
- `json.load()` reads from a file; `json.loads()` parses a string
- Catch **specific** exceptions — never bare `except:`
- `else` runs when no exception occurred; `finally` always runs
- Custom exceptions make error handling at the call site precise and readable
- Use `pathlib.Path` for all file path operations — never string concatenation

---

## Files in this phase

```
phase-3-files-exceptions/
├── README.md
├── data/
│   ├── orders.csv           — 12 sample orders (some intentionally bad)
│   ├── inventory.json       — stock levels and reorder thresholds per SKU
│   └── products.csv         — SKU catalogue with names and prices
└── src/
    ├── 01_text_files.py     — open(), read/write modes, pathlib.Path
    ├── 02_csv_files.py      — DictReader, DictWriter
    ├── 03_json_files.py     — json.load/dump, loads/dumps
    ├── 04_exceptions.py     — try/except/else/finally, specific exceptions
    ├── 05_custom_exceptions.py — exception hierarchy, raise
    └── 06_pipeline.py       — capstone: full file-based processing pipeline
```

---

→ **Next: [Phase 4 — Functions In Depth](../phase-4-functions/README.md)**
