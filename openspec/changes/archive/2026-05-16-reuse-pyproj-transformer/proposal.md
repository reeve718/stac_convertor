## Why

The `geojson2stac` tool is slow when converting large GeoJSON files because `pyproj.Transformer` is instantiated for every single coordinate transformation. Creating a `Transformer` is expensive (~50ms per instance), so files with thousands of features suffer significant overhead. This is a pure implementation improvement with no external behavior changes.

## What Changes

- Create a single `Transformer` instance per file (in `stream_geojson`), reusing it for all coordinate transformations
- Pass the `Transformer` through the call chain: `stream_geojson` → `feature_to_item` → `transform_geometry` → `transform_point`
- Remove redundant `Transformer` creation in `transform_point` and `transform_geometry`
- No changes to output format, CLI, or public APIs — the `transform_geometry` signature stays compatible

## Capabilities

### New Capabilities
None — this is an internal performance optimization

### Modified Capabilities
None — no spec-level behavior changes

## Impact

- **crs_transformer.py**: Remove `Transformer.from_crs()` calls from `transform_point` and `transform_geometry`; accept transformer as parameter
- **stac_item_generator.py**: Accept transformer in `feature_to_item` and pass to `transform_geometry`
- **geojson_parser.py**: Create `Transformer` once in `stream_geojson`, yield it alongside features
- **convertor.py**: Unpack transformer from `stream_geojson` and pass to `feature_to_item`
- No CLI changes, no README changes needed