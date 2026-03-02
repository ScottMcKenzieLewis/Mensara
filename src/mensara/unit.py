import typer

MM_PER_IN = 25.4
M_PER_FT = 0.3048
BAR_PER_PSI = 0.0689476
M3HR_PER_GPM = 0.2271247

def in_to_mm(x: float) -> float:
    return x * MM_PER_IN


def ft_to_m(x: float) -> float:
    return x * M_PER_FT


def ftps_to_mps(x: float) -> float:
    return x * M_PER_FT


def psi_to_bar(x: float) -> float:
    return x * BAR_PER_PSI


def gpm_to_m3hr(x: float) -> float:
    return x * M3HR_PER_GPM

def to_us(value: float, unit: str) -> float:
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


def from_us(value_us: float, unit: str) -> float:
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


