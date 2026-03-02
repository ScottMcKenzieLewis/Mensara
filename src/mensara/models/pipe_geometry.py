from pydantic import BaseModel, Field, model_validator


class PipeGeometry(BaseModel):
    od_in: float = Field(gt=0, description="Outer diameter (in)")
    id_in: float | None = Field(default=None, gt=0, description="Inner diameter (in)")
    thickness_in: float | None = Field(default=None, gt=0, description="Wall thickness (in)")

    @model_validator(mode="after")
    def validate_geometry(self) -> "PipeGeometry":
        if self.id_in is None and self.thickness_in is None:
            raise ValueError("Provide either id_in OR thickness_in.")
        if self.id_in is not None and self.thickness_in is not None:
            raise ValueError("Provide only one of id_in OR thickness_in (not both).")

        if self.thickness_in is not None:
            # derive id from od & thickness
            derived_id = self.od_in - (2 * self.thickness_in)
            if derived_id <= 0:
                raise ValueError("Invalid geometry: thickness too large for given OD.")
            object.__setattr__(self, "id_in", derived_id)

        # final sanity
        if self.id_in is not None and self.id_in >= self.od_in:
            raise ValueError("ID must be less than OD.")

        return self
    