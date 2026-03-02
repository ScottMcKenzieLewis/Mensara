from __future__ import annotations

import typer

from mensara.config import UnitSystem, load_config
from mensara.formulas.flow import flow_gpm
from mensara.formulas.pressure import pressure_estimate_psi
from mensara.formulas.weight import pipe_weight_ft
from mensara.models.pipe_flow import PipeFlow
from mensara.models.pipe_geometry import PipeGeometry
from mensara.models.pipe_pressure import PipePressure

app = typer.Typer(add_completion=False, no_args_is_help=True)

# ----------------------------
# Units + formatting helpers
# ----------------------------

MM_PER_IN = 25.4
M_PER_FT = 0.3048
BAR_PER_PSI = 0.0689476
M3HR_PER_GPM = 0.2271247
UNITS_HELP = "Display units: us or metric."


def _print_header(title: str) -> None:
    print()
    print(f"Mensara | {title}")
    print("-" * (len("Mensara | ") + len(title)))
    print()


def _fmt_source(is_override: bool) -> str:
    return "override" if is_override else "config/default"


def _validate_units(units: str) -> str:
    u = (units or "").strip().lower()
    if u not in {UnitSystem.US.value, UnitSystem.METRIC.value}:
        raise typer.BadParameter("Invalid --units. Use 'us' or 'metric'.")
    return u


def _fmt_value(value_us: float, quantity: str, precision: int, units: str) -> str:
    """
    Format a value stored in US internal units into the desired unit system.

    quantity:
      - "length_in"   (in -> mm)
      - "length_ft"   (ft -> m)
      - "velocity"    (ft/s -> m/s)
      - "pressure"    (psi -> bar)
      - "flow"        (gpm -> m^3/hr)
    """
    units = _validate_units(units)

    if units == UnitSystem.US.value:
        suffix = {
            "length_in": "in",
            "length_ft": "ft",
            "velocity": "ft/s",
            "pressure": "psi",
            "flow": "gpm",
        }[quantity]
        return f"{value_us:.{precision}f} {suffix}"

    converted, suffix = {
        "length_in": (value_us * MM_PER_IN, "mm"),
        "length_ft": (value_us * M_PER_FT, "m"),
        "velocity": (value_us * M_PER_FT, "m/s"),
        "pressure": (value_us * BAR_PER_PSI, "bar"),
        "flow": (value_us * M3HR_PER_GPM, "m³/hr"),
    }[quantity]

    return f"{converted:.{precision}f} {suffix}"


def _to_us(value: float, unit: str) -> float:
    """
    Convert a scalar from the given unit into Mensara's internal US units.

    Supported:
      - in, mm  -> inches
      - ft, m   -> feet
      - ft/s, m/s -> ft/s
      - psi, bar -> psi
      - gpm, m3/hr -> gpm
    """
    u = unit.strip().lower()

    if u in {"in", "inch", "inches"}:
        return value
    if u == "mm":
        return value / MM_PER_IN

    if u in {"ft", "foot", "feet"}:
        return value
    if u == "m":
        return value / M_PER_FT

    if u in {"ft/s", "ftps"}:
        return value
    if u in {"m/s", "mps"}:
        return value / M_PER_FT

    if u == "psi":
        return value
    if u == "bar":
        return value / BAR_PER_PSI

    if u == "gpm":
        return value
    if u in {"m3/hr", "m^3/hr", "m3h"}:
        return value / M3HR_PER_GPM

    raise typer.BadParameter(
        "Unsupported unit. Try: in, mm, ft, m, ft/s, m/s, psi, bar, gpm, m3/hr"
    )


def _from_us(value_us: float, unit: str) -> float:
    """Convert a scalar from internal US units into the requested unit."""
    u = unit.strip().lower()

    if u in {"in", "inch", "inches"}:
        return value_us
    if u == "mm":
        return value_us * MM_PER_IN

    if u in {"ft", "foot", "feet"}:
        return value_us
    if u == "m":
        return value_us * M_PER_FT

    if u in {"ft/s", "ftps"}:
        return value_us
    if u in {"m/s", "mps"}:
        return value_us * M_PER_FT

    if u == "psi":
        return value_us
    if u == "bar":
        return value_us * BAR_PER_PSI

    if u == "gpm":
        return value_us
    if u in {"m3/hr", "m^3/hr", "m3h"}:
        return value_us * M3HR_PER_GPM

    raise typer.BadParameter(
        "Unsupported unit. Try: in, mm, ft, m, ft/s, m/s, psi, bar, gpm, m3/hr"
    )


def _resolve_material_density(cfg, material: str | None, density_override: float | None) -> tuple[str, float, str]:
    """
    Resolve material/density for weight calculation.

    Precedence:
      1) density_override
      2) material (if provided)
      3) cfg.materials.default_material

    Returns: (material_key, density, density_source_label)
    """
    if density_override is not None:
        # material key is still useful for display; choose provided material else default
        material_key = material or cfg.materials.default_material
        return material_key, density_override, "override"

    material_key = material or cfg.materials.default_material

    try:
        density = cfg.materials.material_specs[material_key].density_lb_in3
    except KeyError as e:
        available = ", ".join(sorted(cfg.materials.material_specs.keys()))
        raise typer.BadParameter(f"Unknown material '{material_key}'. Available: {available}") from e

    # If user provided --material, call it override; otherwise config/default
    source = "override" if material is not None else "config/default"
    return material_key, density, source


# ----------------------------
# Commands
# ----------------------------

@app.command()
def convert(
    value: float = typer.Argument(..., help="Value to convert."),
    from_unit: str = typer.Argument(
        ..., help="Unit to convert FROM (e.g., mm, in, m, ft, m/s, ft/s, psi, bar, gpm, m3/hr)."
    ),
    to_unit: str = typer.Argument(
        ..., help="Unit to convert TO (e.g., in, mm, ft, m, ft/s, m/s, psi, bar, gpm, m3/hr)."
    ),
    precision: int = typer.Option(4, "--precision", help="Decimal places to display."),
) -> None:
    """Convert between supported US and metric units."""
    value_us = _to_us(value, from_unit)
    out = _from_us(value_us, to_unit)

    _print_header("Convert")
    print(f"Input  : {value:.{precision}f} {from_unit}")
    print(f"Output : {out:.{precision}f} {to_unit}")
    print()


@app.command()
def weight(
    od_in: float = typer.Option(..., "--od-in", help="Outer diameter (in)"),
    id_in: float | None = typer.Option(None, "--id-in", help="Inner diameter (in). Provide OR --thickness-in."),
    thickness_in: float | None = typer.Option(None, "--thickness-in", help="Wall thickness (in). Provide OR --id-in."),
    length_ft: float = typer.Option(..., "--length-ft", help="Length (ft)"),
    material: str | None = typer.Option(
        None,
        "--material",
        help="Material key from config (e.g., cast_iron). Ignored if --density-lb-in3 is provided.",
    ),
    density_lb_in3: float | None = typer.Option(
        None,
        "--density-lb-in3",
        help="Override density (lb/in^3). Otherwise material/config/default.",
    ),
    units: str = typer.Option(UnitSystem.US.value, "--units", help=UNITS_HELP),
    precision: int = typer.Option(2, "--precision", help="Decimal places to display."),
) -> None:
    """Compute pipe weight (lb) from geometry and length."""
    cfg = load_config()
    units = _validate_units(units)

    geom = PipeGeometry(od_in=od_in, id_in=id_in, thickness_in=thickness_in)

    material_key, effective_density, density_source = _resolve_material_density(cfg, material, density_lb_in3)
    weight_lb = pipe_weight_ft(geom, length_ft=length_ft, density_lb_in3=effective_density)

    _print_header("Pipe Weight")

    print(f"OD       : {_fmt_value(geom.od_in, 'length_in', precision, units)}")
    print(f"ID       : {_fmt_value(geom.id_in, 'length_in', precision, units)}")
    print(f"Length   : {_fmt_value(length_ft, 'length_ft', precision, units)}")
    print(f"Material : {material_key} ({_fmt_source(material is not None)})")
    print(f"Density  : {effective_density:.3f} lb/in^3 ({density_source})")
    print()
    print(f"Weight   : {weight_lb:.{precision}f} lb")
    print()


@app.command()
def flow(
    id_in: float = typer.Option(..., "--id-in", "--diameter-in", help="Inner diameter (in)"),
    velocity_ft_s: float | None = typer.Option(
        None, "--velocity-ft-s", help="Fluid velocity (ft/s). Defaults from config if omitted."
    ),
    units: str = typer.Option(UnitSystem.US.value, "--units", help=UNITS_HELP),
    precision: int = typer.Option(2, "--precision", help="Decimal places to display."),
) -> None:
    """Compute flow rate (gallons per minute)."""
    cfg = load_config()
    units = _validate_units(units)

    effective_velocity = velocity_ft_s if velocity_ft_s is not None else cfg.flow.default_velocity_ft_s
    flow_model = PipeFlow(id_in=id_in, velocity_ft_s=effective_velocity)

    q = flow_gpm(flow_model)

    _print_header("Flow Rate")

    print(f"ID       : {_fmt_value(flow_model.id_in, 'length_in', precision, units)}")
    print(
        f"Velocity : {_fmt_value(flow_model.velocity_ft_s, 'velocity', precision, units)} "
        f"({_fmt_source(velocity_ft_s is not None)})"
    )
    print()
    print(f"Flow     : {_fmt_value(q, 'flow', precision, units)}")
    print()


@app.command()
def pressure(
    diameter_in: float = typer.Option(..., "--diameter-in", help="Inner diameter (in)"),
    thickness_in: float = typer.Option(..., "--thickness-in", help="Wall thickness (in)"),
    allowable_stress_psi: float | None = typer.Option(
        None, "--allowable-stress-psi", help="Override allowable stress (psi). Otherwise config/default."
    ),
    fs: float | None = typer.Option(None, "--fs", help="Factor of safety (overrides config default)"),
    units: str = typer.Option(UnitSystem.US.value, "--units", help=UNITS_HELP),
    precision: int = typer.Option(2, "--precision", help="Decimal places to display."),
) -> None:
    """Estimate internal pressure capacity (psi) using a thin-wall approximation."""
    cfg = load_config()
    units = _validate_units(units)

    effective_fs = fs if fs is not None else cfg.pressure.default_factor_of_safety
    effective_allowable = allowable_stress_psi if allowable_stress_psi is not None else cfg.pressure.allowable_stress_psi

    spec = PipePressure(diameter_in=diameter_in, thickness_in=thickness_in, factor_of_safety=effective_fs)
    p = pressure_estimate_psi(spec, allowable_stress_psi=effective_allowable)

    _print_header("Pressure Estimate")

    print(f"Diameter  : {_fmt_value(diameter_in, 'length_in', precision, units)}")
    print(f"Thickness : {_fmt_value(thickness_in, 'length_in', precision, units)}")
    print(f"FS        : {effective_fs:.{precision}f} ({_fmt_source(fs is not None)})")
    print(f"Allowable : {effective_allowable:.{precision}f} psi ({_fmt_source(allowable_stress_psi is not None)})")
    print()
    print(f"Pressure  : {_fmt_value(p, 'pressure', precision, units)}")
    print()
    print("Note: Thin-wall approximation. Not a code rating.")
    print()
    