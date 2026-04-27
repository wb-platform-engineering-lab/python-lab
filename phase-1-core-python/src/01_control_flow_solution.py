"""Solutions — Control flow exercises (01_ex1 through 01_ex4).

Do not open this file until you have attempted all four exercises yourself.
The value of the exercises comes from writing the code, not reading it.
"""

VALID_WAREHOUSES = {"north", "south", "west"}


# ── Exercise 1 ────────────────────────────────────────────────────────────────

def get_queue(tier):
    if tier == "enterprise":
        return "priority queue"
    elif tier == "pro":
        return "standard queue"
    else:
        return "self-service"


# ── Exercise 2 ────────────────────────────────────────────────────────────────

def classify_quantity(quantity):
    if quantity <= 0:
        return "invalid"
    elif 1 <= quantity <= 5:
        return "small"
    elif 6 <= quantity <= 12:
        return "standard"
    else:
        return "bulk"


# ── Exercise 3 ────────────────────────────────────────────────────────────────

def is_routable(status, warehouse, quantity):
    return status == "pending" and warehouse in VALID_WAREHOUSES and quantity > 0


# ── Exercise 4 ────────────────────────────────────────────────────────────────

def priority_label(tier):
    return "priority" if tier == "enterprise" else "standard"


# ─── verify all solutions ─────────────────────────────────────────────────────

assert get_queue("enterprise") == "priority queue"
assert get_queue("pro")        == "standard queue"
assert get_queue("free")       == "self-service"
assert get_queue("unknown")    == "self-service"

assert classify_quantity(0)   == "invalid"
assert classify_quantity(-1)  == "invalid"
assert classify_quantity(1)   == "small"
assert classify_quantity(5)   == "small"
assert classify_quantity(6)   == "standard"
assert classify_quantity(12)  == "standard"
assert classify_quantity(13)  == "bulk"
assert classify_quantity(100) == "bulk"

assert is_routable("pending",   "north",   3)  is True
assert is_routable("cancelled", "north",   3)  is False
assert is_routable("pending",   "unknown", 3)  is False
assert is_routable("pending",   "west",    0)  is False
assert is_routable("pending",   "south",   1)  is True
assert is_routable("shipped",   "north",   5)  is False

assert priority_label("enterprise") == "priority"
assert priority_label("pro")        == "standard"
assert priority_label("free")       == "standard"
assert priority_label("unknown")    == "standard"

print("All solutions verified.")
