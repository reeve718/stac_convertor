## Why

The current `geojson2stac` CLI accepts only a single input file per invocation. Users with many GeoJSON files must manually run the command repeatedly or wrap it in shell loops. Adding batch convert support lets users convert multiple files—or entire directories—with a single command, improving usability for bulk workflows.

## What Changes

- Add `--input-dir` option to the CLI that processes all `.json` files in a directory
- Add glob pattern support (e.g., `geojson2stac "data/*.json"`) as an alternative to `--input-dir`
- Each input file produces its own output subdirectory under the specified output directory
- The existing single-file behavior remains unchanged when `INPUT_FILE` is provided
- Progress output shows per-file status during batch processing
- Error handling: if one file fails, continue processing others and report failures at the end

## Capabilities

### New Capabilities

- `batch-convert`: CLI option `--input-dir` that iterates over all `.json` files in a directory and converts each independently, producing a separate STAC output subdirectory per input file. Also supports glob patterns as the input argument.

## Impact

- **CLI** (`src/cli.py`): New `--input-dir` option and glob pattern handling
- **Convertor** (`src/convertor.py`): No changes needed; `convert_file()` is already file-agnostic
- **No changes** to STAC item generation, CRS transformation, or bulk writer
