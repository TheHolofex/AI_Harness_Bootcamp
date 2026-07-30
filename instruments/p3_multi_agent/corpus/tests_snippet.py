"""Thin tests that look green while missing the teaching defects."""

from service_snippet import apply_discount, authorize_transfer, normalize_amount


def test_normalize_plain():
    assert normalize_amount("12.50") == 12.5


def test_discount_ten_percent():
    assert apply_discount(100.0, 10) == 90.0


def test_admin_can_move_small():
    assert authorize_transfer("admin", 100.0) is True
