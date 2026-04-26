"""Challenge 3 — Inheritance.

InventoryItem base class with Product and BundleProduct subclasses.
Demonstrates super(), method overriding, and isinstance().
"""


class InventoryItem:
    """Base class for anything that can be stocked and reordered."""

    def __init__(self, sku, stock, reorder_threshold):
        self.sku               = sku
        self.stock             = stock
        self.reorder_threshold = reorder_threshold

    def needs_reorder(self):
        return self.stock <= self.reorder_threshold

    def value_of(self, quantity):
        """Return the value of dispatching `quantity` units. Subclasses override this."""
        raise NotImplementedError(f"{type(self).__name__} must implement value_of()")

    def __str__(self):
        flag = "REORDER" if self.needs_reorder() else "OK"
        return (f"{self.sku:<20} stock={self.stock:>3}  "
                f"reorder={self.reorder_threshold:>3}   [{flag}]")


class Product(InventoryItem):
    """A single individually-priced product."""

    def __init__(self, sku, stock, reorder_threshold, name, unit_price):
        super().__init__(sku, stock, reorder_threshold)   # initialise base fields
        self.name       = name
        self.unit_price = unit_price

    def value_of(self, quantity):
        """Price is per individual unit."""
        return self.unit_price * quantity

    def __str__(self):
        base = super().__str__()
        return f"{base}  value(10)=${self.value_of(10):.2f}"


class BundleProduct(Product):
    """A product sold as a fixed bundle (e.g. 3-item kit)."""

    def __init__(self, sku, stock, reorder_threshold, name, unit_price, bundle_size):
        super().__init__(sku, stock, reorder_threshold, name, unit_price)
        self.bundle_size = bundle_size

    def value_of(self, quantity):
        """Override: price is per complete bundle, not per unit."""
        complete_bundles = quantity // self.bundle_size
        return self.unit_price * complete_bundles

    def __str__(self):
        base = super().__str__()
        return f"{base}  (bundle of {self.bundle_size})"


# --- create the catalogue ---
items = [
    Product("TENT-3P-GRN",   312, 50,  "3-Person Tent",    89.99),
    Product("PACK-45L-BLK",   88, 30,  "45L Backpack",    149.99),
    Product("SLEEP-REG-BLU",  14, 20,  "Sleeping Bag",     59.99),
    BundleProduct("BUNDLE-TENT-PACK", 25, 10, "Tent+Pack Kit", 239.97, bundle_size=3),
]

print("=== Product hierarchy ===")
for item in items:
    print(item)

# --- isinstance checks ---
print()
print("=== isinstance checks ===")
tent   = items[0]
bundle = items[3]

print(f"TENT-3P-GRN   is Product       : {isinstance(tent, Product)}")
print(f"TENT-3P-GRN   is InventoryItem : {isinstance(tent, InventoryItem)}")
print(f"BUNDLE-TENT-PACK is BundleProduct  : {isinstance(bundle, BundleProduct)}")
print(f"BUNDLE-TENT-PACK is Product        : {isinstance(bundle, Product)}")
print(f"BUNDLE-TENT-PACK is InventoryItem  : {isinstance(bundle, InventoryItem)}")

# --- polymorphism: same call, different behaviour ---
print()
print("=== Polymorphism: value_of(10) ===")
for item in items:
    print(f"  {item.sku:<22} → ${item.value_of(10):.2f}")
