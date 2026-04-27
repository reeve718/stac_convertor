## Why

The `geojson2stac` CLI command fails with `ModuleNotFoundError: No module named 'src'` when executed after installation. This prevents users from running the tool after installing the package via pip.

## What Changes

- Fix the `pyproject.toml` script entry to use correct module path
- Change `geojson2stac = "src.cli:app"` to `geojson2stac = "cli:app"` since setuptools with `where = ["src"]` strips the `src/` prefix when installing packages

## Capabilities

### New Capabilities
<!-- No new capabilities being introduced -->

### Modified Capabilities
<!-- No existing spec requirements changing -->

## Impact

- **File**: `pyproject.toml` - fix the `[project.scripts]` entry
- **Effect**: CLI command `geojson2stac` will work after pip install
