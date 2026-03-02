# mensara

Mensara is a lightweight engineering CLI for quick pipe calculations:

- Pipe weight
- Volumetric flow rate
- Thin-wall pressure estimate
- Unit conversion between US and metric units

It is built with Python and Typer, with values loaded from a local YAML config file.

## Requirements

- Python 3.14+
- Poetry (recommended for local development)

## Installation

### Using Poetry (recommended)

```bash
poetry install
```

Run commands with:

```bash
poetry run python -m mensara --help
```

## CLI Overview

Mensara provides these commands:

- `weight` — compute pipe weight from geometry, length, and material/density
- `flow` — compute flow in `gpm` from diameter and velocity
- `pressure` — estimate pressure in `psi` using a thin-wall approximation
- `convert` — convert a value between supported units

General help:

```bash
poetry run python -m mensara --help
```

Command help:

```bash
poetry run python -m mensara weight --help
poetry run python -m mensara flow --help
poetry run python -m mensara pressure --help
poetry run python -m mensara convert --help
```

## Examples

### Weight

Using wall thickness:

```bash
poetry run python -m mensara weight --od-in 6.9 --thickness-in 0.3 --length-ft 20 --material cast_iron
```

Using inner diameter and explicit density override:

```bash
poetry run python -m mensara weight --od-in 6.9 --id-in 6.3 --length-ft 20 --density-lb-in3 0.255
```

### Flow

Use explicit velocity:

```bash
poetry run python -m mensara flow --id-in 4.0 --velocity-ft-s 6.5
```

Use configured default velocity:

```bash
poetry run python -m mensara flow --id-in 4.0
```

### Pressure

Use configured allowable stress and factor of safety:

```bash
poetry run python -m mensara pressure --diameter-in 6.0 --thickness-in 0.28
```

Override allowable stress and FS:

```bash
poetry run python -m mensara pressure --diameter-in 6.0 --thickness-in 0.28 --allowable-stress-psi 18000 --fs 2.5
```

### Convert

```bash
poetry run python -m mensara convert 100 mm in
poetry run python -m mensara convert 3.5 m ft
poetry run python -m mensara convert 2.5 bar psi
poetry run python -m mensara convert 50 gpm m3/hr
```

## Units

`convert` supports:

- Length: `in`, `mm`, `ft`, `m`
- Velocity: `ft/s`, `m/s`
- Pressure: `psi`, `bar`
- Flow: `gpm`, `m3/hr` (also `m^3/hr`, `m3h` aliases)

Display units for `weight`, `flow`, and `pressure` commands can be set with:

- `--units us`
- `--units metric`

## Configuration

Mensara loads config from `mensara.yaml` in the project root.

Default example:

```yaml
materials:
	default_material: cast_iron
	material_specs:
		cast_iron:
			density_lb_in3: 0.255

pressure:
	allowable_stress_psi: 20000
	default_factor_of_safety: 2.0

flow:
	gallons_per_ft3: 7.48051948
	seconds_per_minute: 60.0
	default_velocity_ft_s: 5.0
```

### Value precedence

- CLI overrides config values when both are provided.
- If an override is not provided, Mensara falls back to config/default values.

## Model constraints

- `weight` requires exactly one of `--id-in` or `--thickness-in`.
- `od_in`, `id_in`, `thickness_in`, and `length_ft` must be positive.
- Derived/explicit `id_in` must be less than `od_in`.
- `pressure` and `flow` inputs must be positive (velocity can be zero).

## Engineering note

`pressure` uses a thin-wall hoop-stress estimate and is not a code rating.
Use this tool for preliminary checks only.

## Development

Install dev dependencies and run tests:

```bash
poetry install
poetry run pytest
```

## License

This project is licensed under the MIT License.

SPDX-License-Identifier: MIT

MIT License

Copyright (c) 2026 Scott McKenzie Lewis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.