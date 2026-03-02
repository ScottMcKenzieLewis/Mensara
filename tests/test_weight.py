import math

import pytest

from mensara.formulas.weight import pipe_weight_ft
from mensara.models.pipe_geometry import PipeGeometry


def test_pipe_weight_positive():
    geom = PipeGeometry(od_in=6.9, thickness_in=0.3, id_in=None)
    w = pipe_weight_ft(geom, length_ft=20.0, density_lb_in3=0.255)
    assert w > 0


def test_pipe_weight_scales_linearly_with_length():
    geom = PipeGeometry(od_in=6.9, thickness_in=0.3, id_in=None)

    w1 = pipe_weight_ft(geom, length_ft=10.0, density_lb_in3=0.255)
    w2 = pipe_weight_ft(geom, length_ft=20.0, density_lb_in3=0.255)

    # linear scaling: doubling length doubles weight
    assert math.isclose(w2, 2.0 * w1, rel_tol=1e-10)


def test_pipe_weight_rejects_nonpositive_length():
    geom = PipeGeometry(od_in=6.9, thickness_in=0.3, id_in=None)
    with pytest.raises(ValueError):
        pipe_weight_ft(geom, length_ft=0.0, density_lb_in3=0.255)
