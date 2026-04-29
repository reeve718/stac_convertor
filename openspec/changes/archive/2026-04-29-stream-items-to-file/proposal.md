## Why

Input GeoJSON files for STAC conversion can range from hundreds of MB to 3GB, containing hundreds of thousands of features. The current implementation loads the entire file into memory and writes each feature as a separate item file, making it unsuitable for large-scale data processing. This change introduces streaming-based conversion that handles arbitrarily large files efficiently.

## What Changes

- Use `ijson` library for streaming JSON parsing instead of `json.load()`
- Stream features one-by-one from the GeoJSON input without loading the entire file into memory
- Write all STAC items to a single `items.json` file (GeoJSON FeatureCollection format) instead of one file per feature
- Generate collection metadata incrementally during the streaming process
- **BREAKING**: Output directory structure changes from `stac/<name>/items/*.json` to `stac/<name>/items.json`
- Consumers reading `items/*.json` must be updated to read `items.json` instead

## Capabilities

### New Capabilities

- `streaming-geojson`: Stream-parse large GeoJSON files using `ijson`, yielding features one-by-one without full file in memory
- `single-items-file`: Write all STAC items to a single `items.json` file in FeatureCollection format

### Modified Capabilities

- (none)

## Impact

- **New dependency**: `ijson` for streaming JSON parsing
- **Modified**: `geojson_parser.py` — add streaming parse function
- **Modified**: `convertor.py` — use streaming approach, remove per-item file writing
- **Modified**: `stac_item_generator.py` — inline duplicate ID tracking, buffer items for batch write
- **Modified**: `stac_collection_generator.py` — collection metadata generated incrementally during streaming
- **Breaking output change**: Directory structure shifts from `items/*.json` (individual files) to `items.json` (single FeatureCollection file)
