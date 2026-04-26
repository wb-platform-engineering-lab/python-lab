# Phase 4 — Functions In Depth

> **Concepts introduced:** `*args`, `**kwargs`, keyword-only parameters, closures, factory functions, decorators, `functools.wraps`, decorator factories, `functools.partial`, `functools.lru_cache`, lambdas, `map`, `filter` | **Difficulty:** Intermediate | **Cost:** Free

---

## The problem

The Phase 3 pipeline works — but every concern is tangled together. The dispatch function validates, updates stock, calculates value, and would need to log, retry on failure, and track timing if this were production code. Add all that inline and the function becomes unreadable.

The solution is the same pattern used in every web framework, every test library, and every production Python codebase: **decorators and closures**. Write each concern once as a wrapper. Stack the wrappers. The core logic stays clean.

This phase teaches you how those wrappers work from the inside.

---

## Challenge 1 — `*args` and `**kwargs`

**Goal:** Write functions that accept a variable number of arguments.

### The problem with fixed signatures

```python
def total_value(price, qty):
    return price * qty

# What if you want to sum values from 3 orders? Or 10? Or 1?
# You'd need a different function for each count.
```

### `*args` — variable positional arguments

```python
def total_value(*amounts):
    """Accept any number of amounts and return their sum."""
    return sum(amounts)

total_value(179.98)                         # 179.98
total_value(179.98, 149.99, 299.95)        # 629.92
total_value(*[179.98, 149.99, 299.95])     # unpack a list with *
```

Inside the function, `amounts` is a **tuple** of all positional arguments passed in.

### `**kwargs` — variable keyword arguments

```python
def create_order(**fields):
    """Accept any keyword arguments and return them as a dict."""
    return fields

order = create_order(order_id="ORD-001", sku="TENT-3P-GRN", quantity=2)
# order == {"order_id": "ORD-001", "sku": "TENT-3P-GRN", "quantity": 2}
```

Inside the function, `kwargs` is a **dict** of all keyword arguments passed in.

### Combining them

```python
def log(message, *tags, level="INFO", **context):
    tag_str  = " ".join(f"[{t}]" for t in tags)
    ctx_str  = " ".join(f"{k}={v}" for k, v in context.items())
    print(f"[{level}] {tag_str} {message} {ctx_str}")

log("order dispatched", "orders", "north", order_id="ORD-001", sku="TENT-3P-GRN")
# [INFO] [orders] [north] order dispatched order_id=ORD-001 sku=TENT-3P-GRN
```

### Keyword-only parameters

Any parameter after `*` or `*args` must be passed by name — it cannot be positional:

```python
def dispatch(sku, quantity, *, dry_run=False, warehouse="north"):
    # dry_run and warehouse MUST be passed as keyword arguments
    ...

dispatch("TENT-3P-GRN", 2, dry_run=True)   # ok
dispatch("TENT-3P-GRN", 2, True)           # TypeError — dry_run is keyword-only
```

### Step 1: Run `src/01_args_kwargs.py`

```bash
python3 src/01_args_kwargs.py
```

Expected output:
```
=== *args ===
batch_value(179.98)                    → $179.98
batch_value(179.98, 149.99, 299.95)   → $629.92
batch_value(*values)                   → $2,999.69

=== **kwargs ===
create_order(...)  → {'order_id': 'ORD-001', 'sku': 'TENT-3P-GRN', 'quantity': 2, 'warehouse': 'north'}

=== keyword-only ===
dispatch TENT-3P-GRN qty=2 warehouse=north dry_run=False
dispatch TENT-3P-GRN qty=2 warehouse=south dry_run=True  [DRY RUN — no stock change]

=== log ===
[INFO]    [orders] [north] dispatched order_id=ORD-001 value=179.98
[WARNING] [stock]          low stock sku=SLEEP-REG-BLU remaining=4
```

---

## Challenge 2 — Closures

**Goal:** Write functions that remember values from their enclosing scope.

### What is a closure?

A closure is an inner function that **captures** variables from the enclosing function, even after the enclosing function has returned.

```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor    # 'factor' is captured from make_multiplier's scope
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(50))   # 100
print(triple(50))   # 150
```

`double` and `triple` are closures. Each one remembers its own `factor`.

### Factory functions

A factory function returns a configured function:

```python
def make_validator(valid_warehouses, max_quantity):
    """Return a validation function pre-configured with business rules."""
    def validate(order):
        if order["warehouse"] not in valid_warehouses:
            return False, f"unknown warehouse: {order['warehouse']}"
        if order["quantity"] > max_quantity:
            return False, f"quantity {order['quantity']} exceeds limit {max_quantity}"
        return True, None
    return validate

# Create two validators with different rules
standard_validator    = make_validator({"north", "south", "west"}, max_quantity=50)
enterprise_validator  = make_validator({"north", "south", "west"}, max_quantity=500)
```

### Counter and accumulator closures

```python
def make_counter(name):
    count = 0
    def increment(amount=1):
        nonlocal count       # needed to reassign a variable from enclosing scope
        count += amount
        return count
    def reset():
        nonlocal count
        count = 0
    increment.reset = reset  # attach reset as an attribute of increment
    increment.name  = name
    return increment

dispatched = make_counter("dispatched")
dispatched()    # 1
dispatched()    # 2
dispatched(3)   # 5
```

### Step 1: Run `src/02_closures.py`

```bash
python3 src/02_closures.py
```

Expected output:
```
=== Multiplier factory ===
double(50)  = 100
triple(50)  = 150

=== Validator factory ===
ORD-001  standard    north   qty=2   → valid
ORD-002  standard    north   qty=75  → invalid: quantity 75 exceeds limit 50
ORD-003  enterprise  north   qty=75  → valid
ORD-004  standard    unknown qty=1   → invalid: unknown warehouse: unknown

=== Counters ===
dispatched: 6   rejected: 3
After reset — dispatched: 1
```

---

## Challenge 3 — Decorators

**Goal:** Wrap functions to add timing, logging, and retry logic without modifying their internals.

### What is a decorator?

A decorator is a function that takes a function, wraps it in another function, and returns the wrapper:

```python
def shout(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return str(result).upper()
    return wrapper

@shout
def greet(name):
    return f"hello, {name}"

greet("meridian")   # "HELLO, MERIDIAN"
```

`@shout` is syntactic sugar for `greet = shout(greet)`.

### Always use `functools.wraps`

Without `@wraps`, the wrapper replaces the original function's name and docstring:

```python
import functools

def shout(func):
    @functools.wraps(func)    # copies __name__, __doc__ etc. from func to wrapper
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return str(result).upper()
    return wrapper
```

### A timing decorator

```python
import time, functools

def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed*1000:.1f}ms")
        return result
    return wrapper

@timed
def process_batch(orders):
    ...
```

### Decorator factories (decorators with arguments)

When you need to pass configuration to a decorator, add an outer function:

```python
def retry(max_attempts=3, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    print(f"attempt {attempt} failed: {e} — retrying")
        return wrapper
    return decorator

@retry(max_attempts=3, exceptions=(TimeoutError,))
def call_warehouse_api(order_id):
    ...
```

### Stacking decorators

```python
@timed
@retry(max_attempts=2)
def dispatch(order):
    ...
# equivalent to: dispatch = timed(retry(max_attempts=2)(dispatch))
# outer decorator runs first (timed wraps retry which wraps dispatch)
```

### Step 1: Run `src/03_decorators.py`

```bash
python3 src/03_decorators.py
```

Expected output:
```
=== @timed ===
process_batch took ~Xms
Processed 5 orders

=== @logged ===
→ dispatch_order(ORD-001, TENT-3P-GRN)
← dispatch_order returned in Xms
→ dispatch_order(ORD-002, PACK-45L-BLK)
← dispatch_order returned in Xms

=== @retry ===
attempt 1 failed: warehouse unavailable — retrying
attempt 2 failed: warehouse unavailable — retrying
attempt 3 succeeded

=== stacked: @timed + @retry ===
attempt 1 failed: connection error — retrying
success on attempt 2
call_api took ~Xms
```

---

## Challenge 4 — `functools`

**Goal:** Use `partial`, `lru_cache`, and `reduce` to write leaner, faster code.

### `functools.partial` — pre-fill arguments

`partial` creates a new function with some arguments already filled in:

```python
from functools import partial

def dispatch(sku, quantity, warehouse, dry_run=False):
    ...

# Create a pre-configured function for north warehouse dispatches
dispatch_north = partial(dispatch, warehouse="north")
dispatch_north("TENT-3P-GRN", 2)   # warehouse is already "north"

# Create a dry-run version for testing
dry_dispatch = partial(dispatch, dry_run=True)
```

### `functools.lru_cache` — memoisation

Cache the return value of a function keyed on its arguments. Subsequent calls with the same arguments return instantly from cache:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_product(sku):
    """Expensive lookup — cached after first call."""
    print(f"  loading {sku} from database...")
    return PRODUCTS[sku]

get_product("TENT-3P-GRN")   # prints "loading..."
get_product("TENT-3P-GRN")   # returns instantly from cache
get_product("TENT-3P-GRN")   # returns instantly from cache

print(get_product.cache_info())
# CacheInfo(hits=2, misses=1, maxsize=128, currsize=1)
```

Only works on functions with **hashable arguments** — no lists or dicts as parameters.

### `functools.reduce`

Reduce a sequence to a single value by applying a function cumulatively:

```python
from functools import reduce

values = [179.98, 149.99, 299.95, 239.98]
total  = reduce(lambda acc, x: acc + x, values, 0)
# equivalent to sum() — but reduce handles any accumulation logic
```

### Step 1: Run `src/04_functools.py`

```bash
python3 src/04_functools.py
```

Expected output:
```
=== partial ===
dispatch_north("TENT-3P-GRN", 2)  → dispatched to north
dispatch_south("PACK-45L-BLK", 1) → dispatched to south
dry_dispatch("BOOT-42-BRN", 5)    → [DRY RUN] would dispatch to north

=== lru_cache ===
  loading TENT-3P-GRN from catalogue...
  loading PACK-45L-BLK from catalogue...
TENT-3P-GRN  → $89.99   (from cache on repeat calls)
PACK-45L-BLK → $149.99  (from cache on repeat calls)
CacheInfo(hits=4, misses=2, maxsize=128, currsize=2)

=== reduce ===
Batch total : $869.90
Max value   : $299.95
```

---

## Challenge 5 — Lambdas and higher-order functions

**Goal:** Use `lambda`, `sorted`, `map`, and `filter` to transform collections concisely.

### Lambda — an anonymous function

```python
square = lambda x: x ** 2
square(5)   # 25

# equivalent to:
def square(x):
    return x ** 2
```

A lambda is a single-expression function with no name. Use it when:
- You need a short function as an argument to another function
- Defining a full `def` would be more noise than signal

If the logic is more than one expression, or you need to reuse it, use `def`.

### `sorted` with a key function

```python
orders = [
    {"order_id": "ORD-003", "quantity": 12, "value": 1079.88},
    {"order_id": "ORD-001", "quantity": 2,  "value": 179.98},
    {"order_id": "ORD-002", "quantity": 1,  "value": 149.99},
]

by_value    = sorted(orders, key=lambda o: o["value"], reverse=True)
by_qty      = sorted(orders, key=lambda o: o["quantity"])
by_id       = sorted(orders, key=lambda o: o["order_id"])
```

### `map` — transform every item

```python
quantities = [2, 5, 1, 12, 8]
doubled    = list(map(lambda q: q * 2, quantities))

# usually clearer as a comprehension:
doubled    = [q * 2 for q in quantities]
```

### `filter` — keep items matching a condition

```python
orders  = [...]
pending = list(filter(lambda o: o["status"] == "pending", orders))

# usually clearer as a comprehension:
pending = [o for o in orders if o["status"] == "pending"]
```

`map` and `filter` return lazy iterators. Wrap in `list()` to materialise. Comprehensions are generally preferred for readability — use `map`/`filter` when working with other higher-order functions or when the function already exists.

### Step 1: Run `src/05_lambdas.py`

```bash
python3 src/05_lambdas.py
```

Expected output:
```
=== sorted with lambda ===
By value (desc):
  ORD-011  $1079.88  qty=12
  ORD-004  $599.96   qty=4
  ORD-010  $959.92   qty=8
  ...

By warehouse then value:
  ORD-001  north  $179.98
  ORD-004  north  $599.96
  ...

=== map ===
SKUs upper-cased : ['TENT-3P-GRN', 'PACK-45L-BLK', 'SLEEP-REG-BLU', ...]
Discounted prices: {'TENT-3P-GRN': 80.99, 'PACK-45L-BLK': 134.99, ...}

=== filter ===
Enterprise pending orders : 3
High-value orders (>$500) : 3
```

---

## Challenge 6 — Decorated pipeline (capstone)

**Goal:** Wrap the Phase 3 pipeline's dispatch function with timing, logging, and retry decorators — keeping the core logic untouched.

### What it does

The `dispatch` function from Phase 3 is unchanged. Three decorators are added around it:

- `@timed` — records how long each dispatch takes
- `@logged` — prints entry/exit with arguments and result
- `@retry(max_attempts=2)` — retries on transient `IOError`

A `make_dispatcher` factory pre-binds the inventory and prices to the dispatch function using a closure, so the caller only passes the order.

### Step 1: Run `src/06_decorated_pipeline.py`

```bash
python3 src/06_decorated_pipeline.py
```

Expected output:
```
=== Decorated Pipeline ===

→ dispatch(ORD-001, TENT-3P-GRN, qty=2)
← dispatch OK  $179.98  [0.0ms]
→ dispatch(ORD-002, PACK-45L-BLK, qty=1)
← dispatch OK  $149.99  [0.0ms]
→ dispatch(ORD-003, SLEEP-REG-BLU, qty=5)
← dispatch OK  $299.95  [0.0ms]
→ dispatch(ORD-004, JACKET-M-RED, qty=4)
← dispatch ERR out of stock  [0.0ms]
→ dispatch(ORD-005, BOOT-42-BRN, qty=2)
← dispatch OK  $239.98  [0.0ms]

=== Summary ===
Dispatched : 4
Rejected   : 1
Total value: $869.90
```

---

## What you built

| Before | After |
|---|---|
| Functions with fixed signatures | `*args`/`**kwargs` for flexible, composable interfaces |
| Config baked into function bodies | Closures and factories for pre-configured behaviour |
| Cross-cutting concerns (logging, timing) mixed into business logic | Decorators isolate each concern cleanly |
| Repeated expensive lookups on every call | `lru_cache` memoises them transparently |

The decorator and closure patterns in this phase are the foundation of every Python framework you will use: Flask's `@app.route`, pytest's `@pytest.fixture`, `@property` in classes. Once you see the pattern, you see it everywhere.

---

## Key things to remember

- `*args` → tuple of extra positional args; `**kwargs` → dict of extra keyword args
- Parameters after `*` are **keyword-only** — callers must name them
- A **closure** captures variables from its enclosing scope — useful for factories and pre-configuration
- Use `nonlocal` to reassign (not just read) an enclosing variable
- Always decorate wrappers with `@functools.wraps(func)` to preserve metadata
- Decorator factories have three levels: outer fn (config) → decorator (func) → wrapper (call)
- `partial` pre-fills arguments; `lru_cache` memoises return values
- Use `lambda` for short one-expression key functions; use `def` for anything else
- `map`/`filter` return iterators — comprehensions are usually clearer

---

## Files in this phase

```
phase-4-functions/
├── README.md
└── src/
    ├── 01_args_kwargs.py        — *args, **kwargs, keyword-only params
    ├── 02_closures.py           — inner functions, captured scope, factory functions
    ├── 03_decorators.py         — @decorator, @functools.wraps, decorator factories
    ├── 04_functools.py          — partial, lru_cache, reduce
    ├── 05_lambdas.py            — lambda, sorted, map, filter
    └── 06_decorated_pipeline.py — capstone: decorators + closures on the dispatch pipeline
```

---

→ **Next: [Phase 5 — Object-Oriented Python](../phase-5-oop/README.md)**
