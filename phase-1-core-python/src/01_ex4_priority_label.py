"""Exercise 4 — Priority label with a ternary expression.

Implement `priority_label` using a ternary expression (one line).

Rules:
  "enterprise" → "priority"
  anything else → "standard"

Pattern reminder:
  value_if_true  if  condition  else  value_if_false

Do not use an if/elif/else block — the whole function body is one `return` line.

Run:
    python3 src/01_ex4_priority_label.py
"""


def priority_label(tier):
    pass   # replace with your code — one line only


# ─── assertions ───────────────────────────────────────────────────────────────
assert priority_label("enterprise") == "priority",  f"got: {priority_label('enterprise')}"
assert priority_label("pro")        == "standard",  f"got: {priority_label('pro')}"
assert priority_label("free")       == "standard",  f"got: {priority_label('free')}"
assert priority_label("unknown")    == "standard",  f"got: {priority_label('unknown')}"

print("Exercise 4 passed.")
