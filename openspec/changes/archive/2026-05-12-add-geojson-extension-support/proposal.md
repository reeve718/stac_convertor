## Why

The CLI's `--input-dir` batch mode only processes `.json` files, ignoring files with the `.geojson` extension. Since `.geojson` is a standard extension for GeoJSON files, users expect batch conversion to pick up these files automatically.

## What Changes

- Modify `expand_input_dir()` in `cli.py` to include `.geojson` files alongside `.json` files
- Update documentation in `README.md` to reflect the new supported extensions

## Capabilities

### New Capabilities

- `batch-geojson-extension`: Support for `.geojson` file extension in batch directory conversion mode

### Modified Capabilities

- None

## Impact

- **Affected code**: `src/cli.py` — `expand_input_dir()` function
- **Documentation**: `README.md` — CLI reference table
- **No breaking changes**: Existing `.json` processing behavior remains unchanged