# Phase 0 — Setup & First Script

> **Concepts introduced:** Installing Python, the REPL, running `.py` files, `print()`, variables, data types, string formatting, user input, basic arithmetic | **Difficulty:** Absolute beginner | **Cost:** Free

---

## The problem

Meridian's ops team tracks daily order counts in a spreadsheet. Every morning someone opens it, counts rows, and types a number into a Slack message. It takes 15 minutes and the number is often wrong.

Your first task: write a Python script that reads order data and prints a summary — automatically, correctly, every time.

Before you can do that, you need Python running on your machine and the mental model to write that first script.

---

## How Python runs your code

```
You write this:          Python does this:
─────────────────────    ────────────────────────────────────────
print("hello")    →      finds the built-in print function
                  →      passes it the string "hello"
                  →      print writes "hello\n" to stdout
                  →      your terminal displays: hello
```

Python reads your file top to bottom, line by line. Each line is a statement. A statement is an instruction. Instructions run in order.

That's the whole model. Everything else is detail on top of it.

---

## Setup

### Step 1: Install Python

**macOS**

```bash
# Check if you already have it:
python3 --version

# If not, install via Homebrew (recommended):
brew install python@3.11

# Or download the installer from python.org
```

**Windows**

Download the installer from [python.org/downloads](https://python.org/downloads). During installation, **check the box that says "Add Python to PATH"**.

**Linux (Ubuntu/Debian)**

```bash
sudo apt update && sudo apt install python3.11 python3.11-venv
```

### Step 2: Verify

```bash
python3 --version
```

Expected output:
```
Python 3.11.x
```

If you see `Python 2.x`, you have the old version. Use `python3` instead of `python` for every command in this lab.

### Step 3: Run the verify script

```bash
cd phase-0-setup
python3 src/00_verify.py
```

Expected output:
```
✓ Python version: 3.11.x
✓ Standard library available
✓ Ready for Phase 0
```

---

## Challenge 1 — Hello, Meridian

**Goal:** Write and run your first Python script. Understand `print()`, strings, and how Python executes a file.

### Step 1: Read the starter script

Open `src/01_hello.py`:

```python
print("Hello, Meridian!")
print("Orders processed today: 0")
print("Ready to automate.")
```

### Step 2: Run it

```bash
python3 src/01_hello.py
```

Expected output:
```
Hello, Meridian!
Orders processed today: 0
Ready to automate.
```

### Step 3: Understand what just happened

- `print()` is a **function** — a named action Python knows how to perform
- `"Hello, Meridian!"` is a **string** — text wrapped in quotes
- Python ran your three lines top to bottom, in order

### Step 4: Try the REPL

The REPL (Read–Eval–Print Loop) lets you run Python one line at a time. Open it:

```bash
python3
```

Type each line and press Enter:

```python
>>> print("testing")
testing
>>> 2 + 2
4
>>> "Meridian" + " orders"
'Meridian orders'
>>> exit()
```

The REPL is your scratchpad. Use it any time you want to try something quickly without creating a file.

---

## Challenge 2 — Variables and data types

**Goal:** Store values in variables and understand Python's four primitive types.

### What is a variable?

A variable is a name that points to a value:

```python
order_count = 2400       # the name "order_count" now points to the number 2400
warehouse = "north"      # the name "warehouse" points to the string "north"
```

When you write `order_count` later in your code, Python replaces it with `2400`.

### Step 1: Read `src/02_variables.py`

```python
# Meridian daily stats
order_count = 2400
fill_rate = 0.97          # 97% of orders shipped on time
warehouse = "north"
is_understaffed = True

print(order_count)
print(fill_rate)
print(warehouse)
print(is_understaffed)
```

### Step 2: Run it

```bash
python3 src/02_variables.py
```

Expected output:
```
2400
0.97
north
True
```

### Step 3: Python's four primitive types

| Type | Example | What it stores |
|---|---|---|
| `int` | `2400` | Whole numbers |
| `float` | `0.97` | Decimal numbers |
| `str` | `"north"` | Text |
| `bool` | `True` / `False` | True or false |

Check the type of any value with `type()`:

```python
>>> type(2400)
<class 'int'>
>>> type(0.97)
<class 'float'>
>>> type("north")
<class 'str'>
>>> type(True)
<class 'bool'>
```

### Step 4: Variables are reassignable

```python
stock = 500
print(stock)   # 500

stock = stock - 12    # ship 12 units
print(stock)          # 488
```

The name `stock` now points to the new value. The old value is gone.

---

## Challenge 3 — String formatting

**Goal:** Build readable output strings that mix fixed text with variable values.

### The problem with string concatenation

You can join strings with `+`:

```python
count = 2400
print("Orders today: " + count)   # TypeError — can't add str and int
```

Python will not silently convert `count` to a string. You have to be explicit:

```python
print("Orders today: " + str(count))   # works, but clunky
```

### The better way: f-strings

An f-string starts with `f"` and lets you embed any expression inside `{}`:

```python
count = 2400
warehouse = "north"
fill_rate = 0.97

print(f"Orders today: {count}")
print(f"Warehouse: {warehouse}")
print(f"Fill rate: {fill_rate:.1%}")   # format as percentage with 1 decimal
```

Output:
```
Orders today: 2400
Warehouse: north
Fill rate: 97.0%
```

### Step 1: Run `src/03_strings.py`

```bash
python3 src/03_strings.py
```

Expected output:
```
=== Meridian Daily Report ===
Warehouse  : north
Orders     : 2400
Fill rate  : 97.0%
Status     : ON TRACK
```

### Step 2: Useful string operations

```python
name = "  Meridian Warehouse North  "

print(name.strip())        # "Meridian Warehouse North"   — remove whitespace
print(name.lower())        # "  meridian warehouse north  "
print(name.upper())        # "  MERIDIAN WAREHOUSE NORTH  "
print(name.strip().split())  # ["Meridian", "Warehouse", "North"]  — split into words
print(len("north"))        # 5 — number of characters
```

### Step 3: Multi-line strings

For the report header, use triple quotes:

```python
header = """
=== Meridian Daily Report ===
Generated automatically by Python
"""
print(header)
```

---

## Challenge 4 — Numbers and arithmetic

**Goal:** Perform calculations on order and inventory data.

### Python arithmetic operators

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` | add | `100 + 50` | `150` |
| `-` | subtract | `100 - 30` | `70` |
| `*` | multiply | `12 * 5` | `60` |
| `/` | divide (float result) | `7 / 2` | `3.5` |
| `//` | floor divide (int result) | `7 // 2` | `3` |
| `%` | modulo (remainder) | `7 % 2` | `1` |
| `**` | exponent | `2 ** 8` | `256` |

### Step 1: Run `src/04_numbers.py`

```python
# Inventory check for a single SKU
total_stock = 1200
reserved    = 340     # units in pending orders
available   = total_stock - reserved

reorder_threshold = 200
needs_reorder = available < reorder_threshold

unit_price   = 89.99
order_qty    = 15
order_value  = unit_price * order_qty

print(f"Available stock : {available} units")
print(f"Needs reorder   : {needs_reorder}")
print(f"Order value     : ${order_value:.2f}")
```

```bash
python3 src/04_numbers.py
```

Expected output:
```
Available stock : 860 units
Needs reorder   : False
Order value     : $1349.85
```

### Step 2: Integer vs float division

```python
>>> 7 / 2
3.5          # float division — always gives a decimal

>>> 7 // 2
3            # floor division — rounds down to integer

>>> 7 % 2
1            # remainder after floor division
```

In inventory logic, use `//` when you need whole units:

```python
pallets = 250 // 12    # 12 units per pallet → 20 full pallets
leftover = 250 % 12    # 10 units left over
```

### Step 3: Comparison operators

These return `True` or `False`:

```python
available = 860
threshold = 200

print(available > threshold)    # True
print(available == threshold)   # False
print(available != threshold)   # True
print(available >= 860)         # True
print(available <= 200)         # False
```

---

## Challenge 5 — Your first function

**Goal:** Extract repeated logic into a named function you can call anywhere.

### The problem

You are going to check inventory for 12,000 SKUs. Writing the same calculation 12,000 times is not an option. A function lets you write it once and call it with different inputs.

### What is a function?

```python
def greet(name):          # def = define a function. "greet" is the name. "name" is a parameter.
    message = f"Hello, {name}!"
    return message        # return sends a value back to the caller

result = greet("Meridian")
print(result)             # Hello, Meridian!
```

- `def` defines a function
- The indented block is the function body — it only runs when you call the function
- `return` hands a value back to whoever called the function
- Parameters are placeholders; arguments are the actual values you pass in

### Step 1: Read `src/05_functions.py`

```python
def check_stock(available, threshold):
    """Return True if stock is below the reorder threshold."""
    return available < threshold


def fill_rate(shipped, total):
    """Return fill rate as a float between 0 and 1."""
    if total == 0:
        return 0.0
    return shipped / total


def format_report_line(sku, available, threshold):
    """Return a formatted inventory status line."""
    status = "REORDER" if check_stock(available, threshold) else "OK"
    return f"{sku:<20} stock={available:>5}  threshold={threshold:>5}  [{status}]"


# Test it
print(format_report_line("TENT-3P-GRN",  48, 100))
print(format_report_line("PACK-45L-BLK", 312,  50))
print(format_report_line("SLEEP-REG-BLU",   3,  20))

rate = fill_rate(shipped=2350, total=2400)
print(f"\nFill rate: {rate:.1%}")
```

### Step 2: Run it

```bash
python3 src/05_functions.py
```

Expected output:
```
TENT-3P-GRN          stock=   48  threshold=  100  [REORDER]
PACK-45L-BLK         stock=  312  threshold=   50  [OK]
SLEEP-REG-BLU        stock=    3  threshold=   20  [REORDER]

Fill rate: 97.9%
```

### Step 3: Understand docstrings

The string immediately after `def` is a docstring. It documents what the function does:

```python
def fill_rate(shipped, total):
    """Return fill rate as a float between 0 and 1."""
    ...
```

Access it with `help()`:

```python
>>> help(fill_rate)
fill_rate(shipped, total)
    Return fill rate as a float between 0 and 1.
```

Write a docstring for every function. Your future self will thank you.

### Step 4: Default parameter values

Parameters can have defaults so the caller can omit them:

```python
def check_stock(available, threshold=100):
    return available < threshold

check_stock(48)        # uses threshold=100
check_stock(48, 50)    # overrides to threshold=50
```

---

## What you built

| Before | After |
|---|---|
| Manual count in a spreadsheet | Script calculates values instantly |
| Numbers pasted into Slack by hand | Formatted report printed automatically |
| Copy-paste logic for each SKU | One function called for all 12,000 SKUs |
| No record of how numbers were calculated | Code is the record |

The script at the end of Phase 0 prints a formatted inventory status report from hardcoded data. In Phase 1, that data will come from real input. In Phase 3, it will be read from CSV files. By Phase 11, it will be triggered automatically on every new order.

---

## Key things to remember

- Python runs your file **top to bottom**, one statement at a time
- Variables are **names pointing at values** — not boxes storing values
- Use **f-strings** (`f"value: {x}"`) for all string formatting
- Use `/` for float division, `//` for integer (floor) division
- Define functions with **`def`**, return values with **`return`**
- Write a **docstring** under every `def`

---

## Files in this phase

```
phase-0-setup/
├── README.md
└── src/
    ├── 00_verify.py        — check Python version + standard library
    ├── 01_hello.py         — Challenge 1: print and run a script
    ├── 02_variables.py     — Challenge 2: variables and types
    ├── 03_strings.py       — Challenge 3: string formatting
    ├── 04_numbers.py       — Challenge 4: arithmetic and comparisons
    └── 05_functions.py     — Challenge 5: defining and calling functions
```

---

→ **Next: [Phase 1 — Core Python](../phase-1-core-python/README.md)**
