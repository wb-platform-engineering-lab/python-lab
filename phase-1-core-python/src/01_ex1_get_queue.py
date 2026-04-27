"""Exercise 1 — Tier routing with if/elif/else.

Implement `get_queue` so it returns the correct queue name for a customer tier.

Rules:
  "enterprise"  → "priority queue"
  "pro"         → "standard queue"
  anything else → "self-service"

Use if/elif/else. No ternary expression for this one — be explicit.

Run:
    python3 src/01_ex1_get_queue.py
"""


def get_queue(tier):
    pass   # replace with your code


# ─── assertions ───────────────────────────────────────────────────────────────
assert get_queue("enterprise") == "priority queue",  f"got: {get_queue('enterprise')}"
assert get_queue("pro")        == "standard queue",  f"got: {get_queue('pro')}"
assert get_queue("free")       == "self-service",    f"got: {get_queue('free')}"
assert get_queue("unknown")    == "self-service",    f"got: {get_queue('unknown')}"

print("Exercise 1 passed.")
