## Why

The bulk insert format transformation currently uses sequential index (`0`, `1`, `2`, ...) as the item key, but uses `OBJECTID` as the item `id`. This causes key and id to mismatch when features have `OBJECTID` (e.g., key="0" but id="1"). The API requires key and id to match.

## What Changes

- Modify `stac_bulk_writer.py` to use `OBJECTID` as both key and id when properties contain `OBJECTID`
- When `OBJECTID` is missing, fallback to sequential index for both key and id
- Update tests to verify key-id consistency

## Capabilities

### New Capabilities
None — this is a bug fix that corrects existing behavior.

### Modified Capabilities
- `bulk-insert-format`: Fix key-id matching so key uses `OBJECTID` when available

## Impact

- **Affected code**: `src/stac_bulk_writer.py` (one line change in `transform_to_bulk_format`)
- **Behavior**: Key and id will now match for items with `OBJECTID`
- **No breaking changes**: Items without `OBJECTID` continue to work as before (using index)