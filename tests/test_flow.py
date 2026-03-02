import math

from mensara.formulas.flow import flow_gpm
from mensara.models.pipe_flow import PipeFlow


def test_flow_zero_velocity_is_zero():
    q = flow_gpm(PipeFlow(id_in=6.0, velocity_ft_s=0.0))
    assert math.isclose(q, 0.0)


def test_flow_positive_reasonable_range():
    # sanity: 6" ID at 5 ft/s should be hundreds of gpm
    q = flow_gpm(PipeFlow(id_in=6.0, velocity_ft_s=5.0))
    assert 300.0 < q < 600.0


def test_flow_scales_linearly_with_velocity():
    base = PipeFlow(id_in=6.0, velocity_ft_s=3.0)
    double = PipeFlow(id_in=6.0, velocity_ft_s=6.0)

    q1 = flow_gpm(base)
    q2 = flow_gpm(double)

    assert math.isclose(q2, 2.0 * q1, rel_tol=1e-12)
