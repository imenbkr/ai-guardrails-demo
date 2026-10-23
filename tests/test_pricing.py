"""Tests written from SPEC.md acceptance criteria, not from the code."""

import pytest

from shop.pricing import apply_discount, price_cart, price_item


# AC1
def test_discount_is_applied_and_rounded():
    assert apply_discount(19.99, 10) == 17.99


# AC2
@pytest.mark.parametrize("bad_percent", [-5, 101, 150])
def test_invalid_percent_raises(bad_percent):
    with pytest.raises(ValueError):
        apply_discount(100, bad_percent)


# AC3
def test_price_never_negative():
    assert apply_discount(50, 100) == 0


# AC4: exactly 10 orders counts as loyal
def test_loyalty_bonus_at_ten_orders():
    assert price_item(100, 10, order_count=10) == 85.0


def test_no_loyalty_bonus_below_ten_orders():
    assert price_item(100, 10, order_count=9) == 90.0


# AC5
def test_cart_total():
    items = [{"name": "mug", "price": 10.0}, {"name": "shirt", "price": 20.0}]
    assert price_cart(items, percent=10) == 27.0
