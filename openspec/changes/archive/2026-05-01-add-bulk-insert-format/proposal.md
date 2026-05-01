## Why

The converter currently outputs STAC items in GeoJSON FeatureCollection format, but the API requires a different format for bulk import operations. We need to add the ability to transform STAC items into the bulk insert format that the API accepts.

## What Changes

- Add new output format: bulk insert format (items as object with string keys + method)
- CLI option to select output format (`--output-format` with values `stac` or `bulk`)
- New function to transform STAC items to bulk insert format
- Bulk format applies to items.json output only (collection.json remains unchanged)

## Capabilities

### New Capabilities
- `bulk-insert-format`: Transform STAC items to API bulk insert format with `items` object and `method: "insert"`

### Modified Capabilities
None — this is an additive feature that doesn't change existing STAC output behavior.

## Impact

- **Affected code**: CLI (`src/cli.py`) — add `--output-format` option
- **New module**: `src/stac_bulk_writer.py` — transform STAC items to bulk format
- **Output files**: `stac/{collection}/items.json` — can now be generated in bulk format
- **No breaking changes**: Existing STAC format output continues to work by default