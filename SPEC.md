# Spec: Order pricing

A small pricing module for the web shop. This is the "source of truth" the
code and the tests are checked against.

## Acceptance criteria

1. `apply_discount(price, percent)` returns the price after a percentage discount,
   rounded to 2 decimals.
2. `percent` must be between 0 and 100 (inclusive). Anything else raises `ValueError`.
3. A price can never go below 0.
4. Loyal customers (**10 or more** past orders) get an extra 5% off, on top of any discount.
5. `price_cart(items, ...)` returns the total for a list of items and **must not
   change the list it is given**.
6. Invalid input must raise an error, never be silently ignored.
