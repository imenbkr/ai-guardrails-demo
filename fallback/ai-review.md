# Example AI review (fallback)

> Saved example of the kind of review Claude Code gives for `src/shop/pricing.py`.
> Use it if the live call fails (no network, no account, rate limit).
> Re-run it once before the session and replace this file with your real output.

**Prompt:** Review `src/shop/pricing.py` against `SPEC.md`. Only list problems that
the linter and the existing tests would NOT catch.

**Findings**

1. **`price_cart` changes the caller's data (AC5).** `item["price"] = ...` overwrites
   the price inside the list that was passed in. After calling `price_cart`, the cart
   shows discounted prices, and calling it twice discounts twice. The existing
   `test_cart_total` passes because it only checks the total.
   *Suggestion:* compute the total without writing back, and add a test that the
   items are unchanged after the call.
2. **`applied` leaks state between calls.** The list keeps growing across every call
   and is never returned or used. It looks like leftover code.
3. **Discount + loyalty can exceed 100%.** With a 100% discount and a loyal customer,
   `total_percent` is 105. Once `apply_discount` validates its input, this will raise
   for a valid case. Cap the combined percent at 100.
4. **The bare `except` hides the real problem.** Besides being a lint error, it turns
   bad input into a silent full-price sale, which contradicts AC6.

**Summary:** the tests check *results*, not *side effects*. Finding 1 is the most
important: it would pass CI today.
