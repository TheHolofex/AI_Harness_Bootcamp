"""Small payment helper, used as a review target.

Synthetic code for a review exercise. Not production, and not a complete
service. Read it the way you would read a colleague's pull request.
"""

from __future__ import annotations


def normalize_amount(raw: str) -> float:
    """Parse a currency-ish string into a float dollars value.

    Accepts "12.50" or "$12.50". Does not handle thousands separators.
    """
    cleaned = raw.strip().replace("$", "")
    if cleaned == "":
        return 0.0
    return float(cleaned)


def apply_discount(amount: float, percent: int) -> float:
    """Apply a whole-number percent discount to an amount."""
    return amount * (1.0 - (percent / 100.0))


def authorize_transfer(user_role: str, amount: float) -> bool:
    """Return True if the role is allowed to move this amount."""
    if user_role == "admin":
        return amount <= 10_000.0
    if user_role == "clerk":
        return amount <= 500.0
    return False
