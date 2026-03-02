from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, ValidationError

DEFAULT_CONFIG_PATH = "mensara.yaml"

class UnitSystem(str, Enum):
    US = "us"
    METRIC = "metric"

class PressureConfig(BaseModel):
    allowable_stress_psi: float = Field(20000.0, gt=0)
    default_factor_of_safety: float = Field(2.0, gt=0)

class FlowConfig(BaseModel):
    # constants used in formulas
    gallons_per_ft3: float = Field(7.48051948, gt=0)
    seconds_per_minute: float = Field(60.0, gt=0)
    default_velocity_ft_s: float = Field(5.0, ge=0)

class MaterialSpec(BaseModel):
    density_lb_in3: float = Field(..., gt=0)


class MaterialsConfig(BaseModel):
    default_material: str = Field("cast_iron")
    material_specs: dict[str, MaterialSpec] = Field(
        default_factory=lambda: {
            "cast_iron": MaterialSpec(density_lb_in3=0.26),
        }
    )

class MensaraConfig(BaseModel):
    materials: MaterialsConfig = Field(default_factory=MaterialsConfig)
    pressure: PressureConfig = Field(default_factory=PressureConfig)
    flow: FlowConfig = Field(default_factory=FlowConfig)


@lru_cache(maxsize=8)
def load_config(path: str | Path = DEFAULT_CONFIG_PATH) -> MensaraConfig:
    """
    Load configuration from YAML, applying defaults for missing values.

    Default location: ./mensara.yaml
    """
    config_path = Path(path) if path else Path(DEFAULT_CONFIG_PATH)

    if not config_path.exists():
        return MensaraConfig()

    raw = _read_yaml(config_path)

    try:
        return MensaraConfig.model_validate(raw)
    except ValidationError as e:
        raise ValueError(f"Invalid config in {config_path}:\n{e}") from e


def reload_config(path: str | Path = DEFAULT_CONFIG_PATH) -> MensaraConfig:
    load_config.cache_clear()
    return load_config(path)


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}