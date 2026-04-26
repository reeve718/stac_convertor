[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![CI](https://img.shields.io/badge/CI-none-red.svg)](#)

# stac-convertor

Convert GeoJSON FeatureCollections to STAC Collections and Items.

## Installation

**Requirements:** Python 3.10 or later.

```bash
git clone https://github.com/reeve718/stac_convertor.git
cd stac_convertor
pip install -e ".[dev]"
```

## Quick Start

Convert a GeoJSON file using the built-in sample data:

```bash
geojson2stac data/CTRY_PARK.json
```

Output is written to `stac/CTRY_PARK/`:
```
stac/CTRY_PARK/
├── collection.json        ← STAC Collection
└── items/
    ├── clear-water-bay-country-park.json
    ├── pok-fu-lam-country-park.json
    └── ... (one file per feature)
```

## CLI Reference

```
geojson2stac INPUT_FILE [-o OUTPUT_DIR] [-v]
```

| Argument / Option | Description | Default |
|---|---|---|
| `INPUT_FILE` | Path to GeoJSON file (required) | — |
| `-o`, `--output` | Output directory | `stac/` |
| `-v`, `--verbose` | Enable verbose output | `false` |

**Examples:**

```bash
# Basic usage
geojson2stac data/CTRY_PARK.json

# Custom output directory
geojson2stac data/CTRY_PARK.json -o ./output

# Verbose mode
geojson2stac data/CTRY_PARK.json -v
```

## How CRS Transform Works

The convertor transforms all geometry coordinates from their source CRS to WGS84 (EPSG:4326) automatically. No configuration needed — the CRS is read from the GeoJSON file's `crs` property.

Supported input CRS includes:
- EPSG:2326 (Hong Kong 1980 Grid System)
- Any CRS supported by `pyproj`

The output STAC Items always use WGS84 coordinates.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/reeve718/stac_convertor.git
cd stac_convertor

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

MIT License — see [LICENSE](LICENSE) file.
