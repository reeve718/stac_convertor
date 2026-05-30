## Why

The `stream_geojson()` function in `geojson_parser.py` reads each GeoJSON file twice: once to detect the CRS (coordinate reference system) from the root object, and once again to stream features. For 1000 large GeoJSON files, this doubles I/O time. A user processing 1000 files reports ~1 hour total — the double-read is a significant contributor to this overhead.

## What Changes

- Add `detect_crs_quick()` function that reads only the first 4KB of a file to extract CRS
- Modify `stream_geojson()` to use single-pass reading: detect CRS from bounded prefix, then stream features
- Remove the second full file read that currently exists
- Fall back to WGS84 (EPSG:4326) if CRS cannot be detected from the prefix

## Capabilities

### New Capabilities
- `geojson-crs-detection`: Single-pass CRS detection from a bounded file prefix (4KB), with fallback to WGS84

### Modified Capabilities
- (none)

## Impact

- **Affected file**: `src/geojson_parser.py`
- **Behavior change**: CRS detection now reads only a prefix instead of the full file
- **Fallback**: Files with CRS in an unexpected position (rare) will default to WGS84 instead of being read incorrectly
- **Performance gain**: ~50% reduction in file I/O for batch conversion of large GeoJSON files
