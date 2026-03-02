import math
import pytest

from mensara.formulas.pressure import pressure_estimate_psi
from mensara.models.pipe_pressure import PipePressure


def test_pressure_positive():
    spec = PipePressure(diameter_in=6.0, thickness_in=0.35, factor_of_safety=2.0)
    p = pressure_estimate_psi(spec, allowable_stress_psi=20000.0)
    assert p > 0.0


def test_pressure_inverse_with_factor_of_safety():
    spec1 = PipePressure(diameter_in=6.0, thickness_in=0.35, factor_of_safety=1.0)
    spec2 = PipePressure(diameter_in=6.0, thickness_in=0.35, factor_of_safety=2.0)

    p1 = pressure_estimate_psi(spec1, allowable_stress_psi=20000.0)
    p2 = pressure_estimate_psi(spec2, allowable_stress_psi=20000.0)

    assert math.isclose(p1, 2.0 * p2, rel_tol=1e-12)


def test_pressure_scales_linearly_with_allowable_stress():
    spec = PipePressure(diameter_in=6.0, thickness_in=0.35, factor_of_safety=2.0)

    p1 = pressure_estimate_psi(spec, allowable_stress_psi=10000.0)
    p2 = pressure_estimate_psi(spec, allowable_stress_psi=20000.0)

    assert math.isclose(p2, 2.0 * p1, rel_tol=1e-12)

def test_pressure_rejects_nonpositive_allowable():
    spec = PipePressure(diameter_in=6.0, thickness_in=0.35, factor_of_safety=2.0)
    with pytest.raises(ValueError):
        pressure_estimate_psi(spec, allowable_stress_psi=0.0)
    