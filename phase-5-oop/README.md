# Phase 5 — Object-Oriented Python

> **Concepts introduced:** `class`, `__init__`, instance/class/static methods, inheritance, `super()`, `@property`, dunder methods (`__str__`, `__repr__`, `__len__`, `__eq__`, `__lt__`, `__contains__`, `__iter__`), `@dataclass`, `field`, `__post_init__` | **Difficulty:** Intermediate | **Cost:** Free

---

## The problem

The Meridian pipeline is now a collection of functions that pass dicts around. Dicts are flexible but they have no rules: any key can hold any value, nothing is validated at the point of creation, and the code has no way to express that an `order` and a `product` are fundamentally different things.

Object-oriented programming gives you named types with behaviour attached. An `Order` knows how to validate itself. An `Inventory` knows how to dispatch stock. A `Product` knows its own value calculations. The code becomes self-documenting, and errors surface at the point where bad data is created — not three function calls later.

---

## Challenge 1 — Classes and instances

**Goal:** Define a class, create instances, and attach behaviour as methods.

### The anatomy of a class

```python
class Order:
    # __init__ runs every time you create an instance
    def __init__(self, order_id, sku, quantity, warehouse, status="pending"):
        self.order_id  = order_id    # instance variable — unique to each instance
        self.sku       = sku
        self.quantity  = quantity
        self.warehouse = warehouse
        self.status    = status

    def is_pending(self):
        """Instance method — receives the instance as first argument (self)."""
        return self.status == "pending"

    def total_value(self, unit_price):
        return self.quantity * unit_price
```

Creating instances:

```python
order1 = Order("ORD-001", "TENT-3P-GRN", 2, "north")
order2 = Order("ORD-002", "PACK-45L-BLK", 1, "south")

print(order1.sku)            # "TENT-3P-GRN"
print(order1.is_pending())   # True
print(order1.total_value(89.99))   # 179.98
```

Each instance has its own copy of the instance variables. Methods are shared.

### Step 1: Run `src/01_classes.py`

```bash
python3 src/01_classes.py
```

Expected output:
```
=== Order instances ===
ORD-001  TENT-3P-GRN    qty=2   north   pending
ORD-002  PACK-45L-BLK   qty=1   south   pending
ORD-003  SLEEP-REG-BLU  qty=5   west    pending
ORD-004  JACKET-M-RED   qty=4   north   cancelled

Pending orders : 3
Total value    : $629.92

=== Mutation ===
Before: ORD-001 status=pending
After : ORD-001 status=shipped
```

---

## Challenge 2 — Class methods and static methods

**Goal:** Write alternative constructors with `@classmethod` and pure utility functions with `@staticmethod`.

### Three kinds of methods

| Decorator | First parameter | Has access to |
|---|---|---|
| *(none)* | `self` (instance) | instance variables and class variables |
| `@classmethod` | `cls` (the class itself) | class variables, can create instances |
| `@staticmethod` | *(none)* | neither — it's just a plain function in the class namespace |

### `@classmethod` as an alternative constructor

```python
class Order:
    def __init__(self, order_id, sku, quantity, warehouse, status="pending"):
        ...

    @classmethod
    def from_dict(cls, data):
        """Create an Order from a dict (e.g. a parsed CSV row)."""
        return cls(
            order_id  = data["order_id"],
            sku       = data["sku"],
            quantity  = int(data["quantity"]),
            warehouse = data["warehouse"],
            status    = data.get("status", "pending"),
        )

    @classmethod
    def from_csv_row(cls, row):
        """Create an Order from a csv.DictReader row."""
        return cls.from_dict(row)   # reuse from_dict
```

### `@staticmethod` for utility functions

```python
class Order:
    VALID_WAREHOUSES = {"north", "south", "west"}

    @staticmethod
    def is_valid_warehouse(name):
        """Check whether a warehouse name is valid."""
        return name in Order.VALID_WAREHOUSES
```

### Step 1: Run `src/02_class_static_methods.py`

```bash
python3 src/02_class_static_methods.py
```

Expected output:
```
=== from_dict constructor ===
ORD-001  TENT-3P-GRN    qty=2  north  pending

=== from_csv_rows ===
Loaded 4 orders from dicts

=== static method ===
is_valid_warehouse("north")   → True
is_valid_warehouse("unknown") → False

=== class variable ===
Total orders created: 4
```

---

## Challenge 3 — Inheritance

**Goal:** Share behaviour through a base class and specialise it in subclasses.

### Base class and subclasses

```python
class InventoryItem:
    """Base class for anything that can be stocked."""
    def __init__(self, sku, stock, reorder_threshold):
        self.sku               = sku
        self.stock             = stock
        self.reorder_threshold = reorder_threshold

    def needs_reorder(self):
        return self.stock <= self.reorder_threshold

    def __str__(self):
        return f"{self.sku} (stock={self.stock})"


class Product(InventoryItem):
    """A single stocked product."""
    def __init__(self, sku, stock, reorder_threshold, name, unit_price):
        super().__init__(sku, stock, reorder_threshold)   # call the base __init__
        self.name       = name
        self.unit_price = unit_price

    def value_of(self, quantity):
        return self.unit_price * quantity


class BundleProduct(Product):
    """A product sold as a fixed bundle of items."""
    def __init__(self, sku, stock, reorder_threshold, name, unit_price, bundle_size):
        super().__init__(sku, stock, reorder_threshold, name, unit_price)
        self.bundle_size = bundle_size

    def value_of(self, quantity):
        """Override: price is per bundle, not per unit."""
        bundles = quantity // self.bundle_size
        return self.unit_price * bundles
```

### `isinstance()` and `issubclass()`

```python
p = Product(...)
b = BundleProduct(...)

isinstance(p, Product)        # True
isinstance(p, InventoryItem)  # True — Product inherits from InventoryItem
isinstance(p, BundleProduct)  # False

issubclass(BundleProduct, Product)       # True
issubclass(BundleProduct, InventoryItem) # True
```

### Step 1: Run `src/03_inheritance.py`

```bash
python3 src/03_inheritance.py
```

Expected output:
```
=== Product hierarchy ===
TENT-3P-GRN        stock=312  reorder=50   needs_reorder=False  value(10)=$899.90
PACK-45L-BLK       stock= 88  reorder=30   needs_reorder=False  value(10)=$1499.90
SLEEP-REG-BLU      stock= 14  reorder=20   needs_reorder=True   value(10)=$599.90
BUNDLE-TENT-PACK   stock= 25  reorder=10   needs_reorder=False  value(10)=$239.97  (bundle of 3)

=== isinstance checks ===
TENT-3P-GRN   is Product       : True
TENT-3P-GRN   is InventoryItem : True
BUNDLE-TENT-PACK is BundleProduct  : True
BUNDLE-TENT-PACK is Product        : True
```

---

## Challenge 4 — Properties

**Goal:** Control attribute access with `@property` to enforce validation and computed values.

### The problem with direct attribute access

```python
item.stock = -10    # nothing stops this — invalid state
```

A `@property` turns attribute access into a method call, letting you add validation:

```python
class InventoryItem:
    def __init__(self, sku, stock):
        self._stock = stock     # store on a private name by convention

    @property
    def stock(self):
        """Getter — called when you read item.stock"""
        return self._stock

    @stock.setter
    def stock(self, value):
        """Setter — called when you write item.stock = value"""
        if value < 0:
            raise ValueError(f"stock cannot be negative (got {value})")
        self._stock = value
```

Now `item.stock = -10` raises `ValueError`. The caller still writes `item.stock` — no change to the calling code.

### Read-only computed properties

```python
@property
def needs_reorder(self):
    """Computed from stock and threshold — no setter."""
    return self._stock <= self.reorder_threshold

# item.needs_reorder = True  → AttributeError: can't set attribute
```

### Step 1: Run `src/04_properties.py`

```bash
python3 src/04_properties.py
```

Expected output:
```
=== Properties ===
stock=312  needs_reorder=False  status=OK

Dispatching 300 units...
stock=12   needs_reorder=True   status=REORDER

=== Validation ===
Setting stock to -5: ValueError: stock cannot be negative (got -5)
Setting stock to 50: stock=50

=== Read-only ===
AttributeError: can't set attribute 'needs_reorder'
```

---

## Challenge 5 — Dunder methods

**Goal:** Make your objects work naturally with Python's built-in operators and functions.

### Why dunder methods matter

```python
print(order)            # calls __str__
repr(order)             # calls __repr__
len(inventory)          # calls __len__
"TENT-3P-GRN" in inventory  # calls __contains__
for item in inventory:  # calls __iter__
order1 == order2        # calls __eq__
sorted(orders)          # calls __lt__ on each pair
```

### The key ones

```python
class Order:
    def __str__(self):
        """Human-readable: print(order)"""
        return f"Order({self.order_id}, {self.sku}, qty={self.quantity})"

    def __repr__(self):
        """Unambiguous: repr(order), shown in REPL and debuggers"""
        return (f"Order(order_id={self.order_id!r}, sku={self.sku!r}, "
                f"quantity={self.quantity!r}, warehouse={self.warehouse!r})")

    def __eq__(self, other):
        """order1 == order2"""
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_id == other.order_id

    def __lt__(self, other):
        """order1 < order2 — enables sorted(orders)"""
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_id < other.order_id

    def __hash__(self):
        """Needed to use Order in sets or as dict keys when __eq__ is defined."""
        return hash(self.order_id)
```

```python
class Inventory:
    def __len__(self):
        return len(self._items)

    def __contains__(self, sku):
        return sku in self._items

    def __iter__(self):
        return iter(self._items.values())
```

### Step 1: Run `src/05_dunders.py`

```bash
python3 src/05_dunders.py
```

Expected output:
```
=== __str__ and __repr__ ===
str  : Order(ORD-001, TENT-3P-GRN, qty=2) @ north [pending]
repr : Order(order_id='ORD-001', sku='TENT-3P-GRN', quantity=2, warehouse='north', status='pending')

=== __eq__ and __lt__ ===
ORD-001 == ORD-001 : True
ORD-001 == ORD-002 : False
sorted orders: ['ORD-001', 'ORD-002', 'ORD-003', 'ORD-004', 'ORD-005']

=== Inventory dunders ===
len(inventory)              : 5
'TENT-3P-GRN' in inventory  : True
'CRAMPONS-S' in inventory   : False
Iterating:
  TENT-3P-GRN    stock=312
  PACK-45L-BLK   stock= 88
  SLEEP-REG-BLU  stock= 14
  JACKET-M-RED   stock=  0
  BOOT-42-BRN    stock=203
```

---

## Challenge 6 — Dataclasses

**Goal:** Eliminate `__init__` boilerplate with `@dataclass` while keeping full type clarity.

### The problem with hand-written `__init__`

A class with 8 fields needs 8 lines of `self.x = x`. Dataclasses generate this automatically:

```python
from dataclasses import dataclass, field

@dataclass
class Order:
    order_id:  str
    sku:       str
    quantity:  int
    warehouse: str
    status:    str  = "pending"     # default value
    tags:      list = field(default_factory=list)   # mutable default — must use field()
```

Python generates `__init__`, `__repr__`, and `__eq__` automatically.

### `__post_init__` for validation

```python
@dataclass
class Order:
    order_id: str
    sku:      str
    quantity: int

    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError(f"quantity cannot be negative: {self.quantity}")
```

### `frozen=True` for immutable records

```python
@dataclass(frozen=True)
class ProductKey:
    sku:       str
    warehouse: str

key = ProductKey("TENT-3P-GRN", "north")
key.sku = "other"    # FrozenInstanceError — immutable
hash(key)            # hashable — can be used as a dict key
```

### `order=True` for automatic comparison

```python
@dataclass(order=True)
class StockLevel:
    stock: int
    sku:   str

levels = [StockLevel(88, "PACK"), StockLevel(14, "SLEEP"), StockLevel(312, "TENT")]
sorted(levels)   # sorted by stock first, then sku
```

### Step 1: Run `src/06_dataclasses.py`

```bash
python3 src/06_dataclasses.py
```

Expected output:
```
=== @dataclass ===
Order(order_id='ORD-001', sku='TENT-3P-GRN', quantity=2, warehouse='north', status='pending', tags=[])
Order(order_id='ORD-002', sku='PACK-45L-BLK', quantity=1, warehouse='south', status='pending', tags=['fragile'])

=== __post_init__ validation ===
Created: Order(order_id='ORD-003', sku='SLEEP-REG-BLU', quantity=5, ...)
ValueError: quantity cannot be negative: -1

=== frozen dataclass ===
key = ProductKey(sku='TENT-3P-GRN', warehouse='north')
Hashable — can be dict key: stock=100
FrozenInstanceError on mutation

=== order=True ===
Sorted by stock:
  StockLevel(stock=0, sku='JACKET-M-RED')
  StockLevel(stock=14, sku='SLEEP-REG-BLU')
  StockLevel(stock=88, sku='PACK-45L-BLK')
  StockLevel(stock=203, sku='BOOT-42-BRN')
  StockLevel(stock=312, sku='TENT-3P-GRN')
```

---

## Challenge 7 — OOP pipeline (capstone)

**Goal:** Rebuild the Meridian pipeline with a full object-oriented design.

### The design

```
Order          — @dataclass, validation in __post_init__, from_dict() classmethod
Product        — @dataclass, value_of() method
Inventory      — class, stock dict, @property, dispatch(), reorder report
OrderProcessor — class, processes a list of Orders against an Inventory
```

Each class has one responsibility. The `OrderProcessor` orchestrates them. No raw dicts anywhere in the pipeline.

### Step 1: Run `src/07_oop_pipeline.py`

```bash
python3 src/07_oop_pipeline.py
```

Expected output:
```
=== Meridian OOP Pipeline ===
Inventory: 5 SKUs, 617 total units

Processing 8 orders...

ORD-001  TENT-3P-GRN      qty=2   $179.98   dispatched
ORD-002  PACK-45L-BLK     qty=1   $149.99   dispatched
ORD-003  SLEEP-REG-BLU    qty=5   $299.95   dispatched
ORD-004  JACKET-M-RED     qty=4   —         rejected: out of stock
ORD-005  BOOT-42-BRN      qty=2   $239.98   dispatched
ORD-006  TENT-3P-GRN      qty=1   $89.99    dispatched
ORD-007  PACK-45L-BLK     qty=3   —         rejected: cancelled
ORD-008  SLEEP-REG-BLU    qty=6   $359.94   dispatched

=== Results ===
Dispatched : 6  ($1319.83)
Rejected   : 2
Fill rate  : 75.0%

=== Reorder Report ===
JACKET-M-RED     stock=0    threshold=25   ← REORDER
SLEEP-REG-BLU    stock=3    threshold=20   ← REORDER
```

---

## What you built

| Before | After |
|---|---|
| Dicts with no enforced structure | `Order` and `Product` dataclasses with validated fields |
| Functions that accept raw dicts | Methods attached to the objects they operate on |
| Repeated validation logic across functions | `__post_init__` validates once at creation time |
| No way to distinguish order types in code | `isinstance()` checks and method dispatch |
| `sorted(orders, key=lambda o: o["order_id"])` | `sorted(orders)` — `__lt__` handles it |

This is the foundation every framework builds on. Flask routes are methods on an `App`. SQLAlchemy models are classes with column descriptors as properties. `pytest` fixtures are objects with lifecycle methods. The patterns are the same.

---

## Key things to remember

- `__init__` sets instance variables — each instance gets its own copy
- `@classmethod` receives `cls` — use it for alternative constructors
- `@staticmethod` receives nothing — it's just a namespaced function
- Always call `super().__init__(...)` first in a subclass `__init__`
- `@property` + setter: keep the private value on `self._name`; expose via `self.name`
- `__str__` is for humans; `__repr__` is for developers (REPL, logs, debuggers)
- Implement `__eq__` + `__hash__` together — if you override `__eq__`, Python removes `__hash__`
- `@dataclass` generates `__init__`, `__repr__`, `__eq__` — use `field(default_factory=list)` for mutable defaults
- `frozen=True` makes the dataclass hashable and immutable — use for dict keys and set members

---

## Files in this phase

```
phase-5-oop/
├── README.md
└── src/
    ├── 01_classes.py           — class, __init__, instance methods
    ├── 02_class_static_methods.py — @classmethod, @staticmethod, class variables
    ├── 03_inheritance.py       — base class, super(), isinstance()
    ├── 04_properties.py        — @property, setter, read-only computed attrs
    ├── 05_dunders.py           — __str__, __repr__, __eq__, __lt__, __len__, __contains__, __iter__
    ├── 06_dataclasses.py       — @dataclass, field, __post_init__, frozen, order
    └── 07_oop_pipeline.py      — capstone: Order, Product, Inventory, OrderProcessor
```

---

→ **Next: [Phase 6 — The Standard Library](../phase-6-stdlib/README.md)**
