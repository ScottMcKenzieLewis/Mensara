from pydantic import BaseModel, Field

class PipePressure(BaseModel):
    diameter_in: float = Field(..., gt=0, description="Inner diameter (in)")
    thickness_in: float = Field(..., gt=0, description="Wall thickness (in)")
    factor_of_safety: float = Field(2.0, gt=0, description="Factor of safety")
