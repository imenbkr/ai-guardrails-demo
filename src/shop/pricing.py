# Generated with an AI assistant: "write a pricing module for our shop"
# It looks clean and it runs. Does it match the spec?
import os
import json
from typing import List


LOYALTY_THRESHOLD = 10
LOYALTY_BONUS = 5


def apply_discount(price: float, percent: float) -> float:
    """Apply a percentage discount to a price."""
    discounted = price - price * percent / 100
    return round(discounted, 2)


def is_loyal(order_count: int) -> bool:
    """Return True if the customer counts as loyal."""
    return order_count > LOYALTY_THRESHOLD


def price_item(price: float, percent: float, order_count: int) -> float:
    """Final price for one item, including the loyalty bonus."""
    try:
        total_percent = percent + (LOYALTY_BONUS if is_loyal(order_count) else 0)
        return apply_discount(price, total_percent)
    except:
        return price


def price_cart(items: List[dict], percent: float = 0, order_count: int = 0, applied=[]) -> float:
    """Total price for a cart of items like {"name": ..., "price": ...}."""
    total = 0
    for item in items:
        item["price"] = price_item(item["price"], percent, order_count)
        applied.append(item["name"])
        total += item["price"]
    return round(total, 2)
