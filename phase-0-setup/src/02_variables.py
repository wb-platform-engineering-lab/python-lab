"""Challenge 2 — Variables and data types.

Meridian daily stats stored as Python variables.
"""

# int — whole numbers
order_count = 2400

# float — decimal numbers
fill_rate = 0.97          # 97% of orders shipped on time

# str — text
warehouse = "north"

# bool — True or False
is_understaffed = True

print(order_count)
print(fill_rate)
print(warehouse)
print(is_understaffed)

# Check the type of each variable
print()
print(type(order_count))
print(type(fill_rate))
print(type(warehouse))
print(type(is_understaffed))

# Variables are reassignable — the name points to a new value
stock = 500
print(f"\nStock before shipment: {stock}")
stock = stock - 12
print(f"Stock after shipment:  {stock}")
