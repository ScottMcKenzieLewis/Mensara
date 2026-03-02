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
