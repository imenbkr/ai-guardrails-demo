"""The test the AI reviewer told us we were missing (AC5)."""

from shop.pricing import price_cart


def test_cart_items_are_not_changed():
    items = [{"name": "mug", "price": 10.0}]
    price_cart(items, percent=50)
    assert items == [{"name": "mug", "price": 10.0}]
