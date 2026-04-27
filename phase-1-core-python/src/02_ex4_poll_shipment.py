"""Exercise 4 — while loop.

Implement `poll_shipment` so it simulates polling for a shipment confirmation.

Rules:
  - Start with arrived=False and checks=0 (already declared for you below)
  - Loop while not arrived AND checks < max_checks
  - Each iteration: increment checks
  - When checks reaches success_on_check: set arrived=True and break
  - Return (arrived, checks)

The caller decides both the limit and the check number that triggers success.
This lets the assertions test different scenarios without changing your code.

Run:
    python3 src/02_ex4_poll_shipment.py
"""


def poll_shipment(max_checks, success_on_check):
    """Simulate polling. Return (arrived, checks_used)."""
    arrived = False
    checks  = 0
    # write your code here — keep the variables above, add the while loop


# ─── assertions ───────────────────────────────────────────────────────────────

# success on check 3 of 4
arrived, checks = poll_shipment(max_checks=4, success_on_check=3)
assert arrived is True, f"expected arrived=True, got {arrived}"
assert checks  == 3,    f"expected 3 checks, got {checks}"

# success_on_check beyond max — should exhaust the loop without arriving
arrived, checks = poll_shipment(max_checks=3, success_on_check=10)
assert arrived is False, f"expected arrived=False, got {arrived}"
assert checks  == 3,     f"expected 3 checks, got {checks}"

# success on the very first check
arrived, checks = poll_shipment(max_checks=5, success_on_check=1)
assert arrived is True, f"expected arrived=True, got {arrived}"
assert checks  == 1,    f"expected 1 check, got {checks}"

print("Exercise 4 passed.")
