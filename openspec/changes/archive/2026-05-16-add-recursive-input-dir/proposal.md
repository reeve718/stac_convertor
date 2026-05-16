## Why

The current `--input-dir` option only scans the first level of a directory, missing GeoJSON files in subdirectories. Users with nested data structures cannot convert their entire dataset with a single command. Adding `--recursive` flag enables recursive directory scanning while preserving the folder hierarchy in the output structure.

## What Changes

- Add `--recursive` flag to the CLI that enables recursive scanning of input directories
- When `--recursive` is used, `rglob` finds all `.json` and `.geojson` files at all nesting levels
- Output directory structure mirrors the input directory structure relative to the `--input-dir` root
- Example: `data/subfolder/nested/file.json` converts to `stac/subfolder/nested/file/collection.json`
- Non-recursive behavior (without `--recursive`) remains unchanged

## Capabilities

### New Capabilities

- `recursive-directory-scan`: CLI flag `--recursive` that, when combined with `--input-dir`, scans all subdirectories recursively using `Path.rglob()` and preserves the relative folder structure in the output

### Modified Capabilities

None — no existing capability requirements change

## Impact

- **CLI** (`src/cli.py`): Add `--recursive` boolean flag; modify `expand_input_dir()` to use `rglob` when recursive; compute relative paths for output subdirectory structure
- **Convertor** (`src/convertor.py`): No changes needed — receives full paths from CLI
- **README.md**: Document the new `--recursive` option in CLI reference