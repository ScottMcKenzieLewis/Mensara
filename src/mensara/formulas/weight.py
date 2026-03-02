import math
from mensara.models.pipe_geometry import PipeGeometry
from mensara.config import load_config


def pipe_weight_ft(
    geom: PipeGeometry,
    length_ft: float,
    density_lb_in3: float | None = None,
) -> float:
    if length_ft <= 0:
        raise ValueError("length_ft must be > 0")

    cfg = load_config()
    density = density_lb_in3 if density_lb_in3 is not None else cfg.materials.cast_iron_density_lb_in3

    length_in = length_ft * 12.0

    outer_volume = math.pi * (geom.od_in / 2.0) ** 2 * length_in
    inner_volume = math.pi * (geom.id_in / 2.0) ** 2 * length_in

    metal_volume = outer_volume - inner_volume
    return metal_volume * density
