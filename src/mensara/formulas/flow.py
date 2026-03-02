
import math
from mensara.models.pipe_flow import PipeFlow
from mensara.config import load_config

def flow_gpm(
    flow: PipeFlow,
) -> float:
    """
    Compute volumetric flow rate in gallons per minute.
    """

    cfg = load_config()

    area_ft2 = math.pi * (flow.diameter_ft / 2.0) ** 2

    flow_ft3_s = area_ft2 * flow.velocity_ft_s

    return (
        flow_ft3_s
        * cfg.flow.gallons_per_ft3
        * cfg.flow.seconds_per_minute
    )