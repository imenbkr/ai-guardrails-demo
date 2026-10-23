"""Pricing module, fixed to match SPEC.md."""

LOYALTY_THRESHOLD = 10
LOYALTY_BONUS = 5


def apply_discount(price: float, percent: float) -> float:
    """Apply a percentage discount to a price (AC1-AC3)."""
    if not 0 <= percent <= 100:
        raise ValueError(f"percent must be between 0 and 100, got {percent}")
    discounted = price - price * percent / 100
    return max(round(discounted, 2), 0.0)


def is_loyal(order_count: int) -> bool:
    """Loyal customers have 10 or more past orders (AC4)."""
    return order_count >= LOYALTY_THRESHOLD


def price_item(price: float, percent: float, order_count: int) -> float:
    """Final price for one item, including the loyalty bonus (AC4, AC6)."""
    total_percent = percent + (LOYALTY_BONUS if is_loyal(order_count) else 0)
    return apply_discount(price, min(total_percent, 100))


def price_cart(items: list[dict], percent: float = 0, order_count: int = 0) -> float:
    """Total price for a cart, without changing the items passed in (AC5)."""
    total = sum(price_item(item["price"], percent, order_count) for item in items)
    return round(total, 2)
