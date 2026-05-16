# stac-convertor

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![CI](https://img.shields.io/badge/CI-none-red.svg)]

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

```bash
stac/CTRY_PARK/
├── collection.json        ← STAC Collection
└── items.json            ← STAC Items (GeoJSON FeatureCollection)
```

## CLI Reference

```bash
geojson2stac INPUT_FILE [-o OUTPUT_DIR] [--output-format FORMAT] [-v]
geojson2stac --input-dir INPUT_DIR [-o OUTPUT_DIR] [--output-format FORMAT] [-v]
```

| Argument / Option | Description | Default |
| --- | --- | --- |
| `INPUT_FILE` | Path to GeoJSON file or glob pattern (e.g. `data/*.json`) | — |
| `--input-dir` | Directory containing GeoJSON files (`.json` or `.geojson`) | — |
| `--recursive` | Recursively scan subdirectories when used with `--input-dir` | `false` |
| `-o`, `--output` | Output directory | `stac/` |
| `--output-format` | Output format: `stac` (default) or `bulk` | `stac` |
| `-v`, `--verbose` | Enable verbose output | `false` |

**Examples:**

```bash
# Recursive directory conversion (preserves folder structure)
geojson2stac --input-dir data/ --recursive

# Output structure mirrors input:
# data/sub/file.json → stac/sub/file/

# Convert all files in a directory
geojson2stac --input-dir data/

# Convert files matching glob pattern
geojson2stac "data/*.json"

# Custom output directory
geojson2stac data/CTRY_PARK.json -o ./output

# Bulk format for API import
geojson2stac data/CTRY_PARK.json --output-format bulk

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
