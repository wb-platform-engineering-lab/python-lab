"""Challenge 1 — Text files.

Reading and writing plain text files using open(), with, and pathlib.Path.
"""
from pathlib import Path

DATA_DIR   = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

orders_file = DATA_DIR / "orders.csv"

# --- read entire file at once ---
print("=== Reading orders.csv (raw) ===")
with open(orders_file, "r") as f:
    contents = f.read()

lines = contents.splitlines()
for i, line in enumerate(lines[:4], start=1):
    print(f"Line {i} : {line}")
print(f"...")
print(f"\nTotal lines (including header): {len(lines)}")

# --- read line by line (memory-efficient for large files) ---
line_count = 0
with open(orders_file, "r") as f:
    for line in f:
        line_count += 1

assert line_count == len(lines)

# --- write a report ---
report_path = OUTPUT_DIR / "report.txt"

with open(report_path, "w") as f:
    f.write("=== Meridian Daily Report ===\n")
    f.write(f"Source file : {orders_file.name}\n")
    f.write(f"Total rows  : {line_count - 1} orders + 1 header\n")

# --- append to the report ---
with open(report_path, "a") as f:
    f.write("Status      : processed\n")

print(f"\nReport written to {report_path}")

# --- pathlib operations ---
print()
print("--- pathlib ---")
print(f"orders_file.exists() : {orders_file.exists()}")
print(f"orders_file.suffix   : {orders_file.suffix}")
print(f"orders_file.stem     : {orders_file.stem}")
print(f"orders_file.parent   : {orders_file.parent.name}")
