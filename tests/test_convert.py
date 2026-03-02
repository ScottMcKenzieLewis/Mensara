import math

from mensara.unit import to_us, from_us


def test_convert_round_trip_mm_in():
    x = 150.0
    inches = to_us(x, "mm")
    mm = from_us(inches, "mm")
    assert math.isclose(mm, x, rel_tol=1e-12)


def test_convert_round_trip_bar_psi():
    x = 3.0
    psi = to_us(x, "bar")
    ba = from_us(psi, "bar")
    assert math.isclose(ba, x, rel_tol=1e-12)
