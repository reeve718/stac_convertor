## Why

STAC (SpatioTemporal Asset Catalog) provides a standardized way to describe geospatial assets, enabling interoperability between different GIS systems and services. Converting GeoJSON FeatureCollections to STAC format unlocks integration with tools like STAC Browser, STAC API, and cloud-native geospatial platforms.

## What Changes

- New `geojson2stac` CLI command built with Typer
- Convert GeoJSON FeatureCollection → STAC Collection (single file)
- Convert each GeoJSON Feature → STAC Item (one file per feature)
- Output structure: `stac/<geojson_filename>/collection.json` + `items/<id>.json` per feature
- Support for Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon geometries
- CRS transformation: EPSG:2326 (Hong Kong 1980 Grid) → WGS84 (EPSG:4326)
- ID generation from feature properties (OBJECTID as fallback)

## Capabilities

### New Capabilities

- `geojson-to-stac`: CLI tool that reads GeoJSON files from a specified input path, transforms each Feature into a STAC Item, and writes a STAC Collection with links to all Items
  - `geojson-parser`: Parse GeoJSON FeatureCollection, validate structure, extract features
  - `stac-collection-generator`: Generate STAC Collection JSON with proper STAC fields and links
  - `stac-item-generator`: Generate STAC Item JSON from GeoJSON Feature with geometry, properties, and required STAC fields
  - `crs-transformer`: Transform coordinates from EPSG:2326 to WGS84 (EPSG:4326)

### Modified Capabilities

(None)

## Impact

- New files: `src/cli.py`, `src/convertor.py`, `stac/` output directory
- Dependencies: `typer`, `pystac` (or manual STAC construction), `pyproj` for CRS transformation
- Input: `data/*.json` (GeoJSON FeatureCollection)
- Output: `stac/<name>/collection.json`, `stac/<name>/items/*.json`