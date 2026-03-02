from mensara.config import load_config
from mensara.models.pipe_pressure import PipePressure

def pressure_estimate_psi(
    spec: PipePressure,
    allowable_stress_psi: float | None = None,
) -> float:
    sigma = allowable_stress_psi if allowable_stress_psi is not None else cfg.pressure.allowable_stress_psi

    if sigma <= 0:
        raise ValueError("allowable_stress_psi must be > 0")

    cfg = load_config()

    fs = spec.factor_of_safety if spec.factor_of_safety is not None else cfg.pressure.default_factor_of_safety

    # Thin-wall hoop stress estimate (v1)
    return (2.0 * spec.thickness_in * sigma) / (spec.diameter_in * fs)
