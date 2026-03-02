import math

from pydantic import BaseModel, Field


class PipeFlow(BaseModel):
    """Flow conditions inside a pipe."""

    id_in: float = Field(..., gt=0, description="Inner diameter (in)")
    velocity_ft_s: float = Field(..., ge=0, description="Fluid velocity (ft/s)")

    @property
    def diameter_ft(self) -> float:
        """Inner diameter (ft)."""
        return self.id_in / 12.0