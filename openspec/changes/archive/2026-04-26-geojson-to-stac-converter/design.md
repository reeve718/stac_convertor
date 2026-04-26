## Context

STAC is a specification for standardized geospatial asset metadata. GeoJSON is a common format for vector data. This tool bridges the two by converting GeoJSON FeatureCollections into STAC Collections + Items.

The sample data (`CTRY_PARK.json`) contains 25 Hong Kong Country Park points in EPSG:2326 coordinate system. The output must be valid STAC that works with STAC tooling.

## Goals / Non-Goals

**Goals:**
- CLI command `geojson2stac <input>` that processes a GeoJSON file and outputs STAC
- Generate one STAC Collection per input GeoJSON file
- Generate one STAC Item per GeoJSON Feature
- Transform EPSG:2326 coordinates to WGS84 (EPSG:4326)
- Use pystac library for STAC construction
- Support all GeoJSON geometry types

**Non-Goals:**
- Batch processing multiple files (single file at a time)
- Recursive directory scanning
- Writing back to GeoJSON
- STAC API server implementation
- Custom asset definitions (items will have no additional assets)

## Decisions

**1. Use pystac library for STAC construction**
- Why: Handles STAC spec compliance (required fields, link relations, extension support) automatically
- Alternative: Manual JSON construction — error-prone, requires deep STAC spec knowledge

**2. Use pyproj for CRS transformation**
- Why: Well-maintained, handles EPSG:2326 → EPSG:4326 correctly
- Alternative: Manual transformation — complex, error-prone

**3. Item ID from NAME_EN or OBJECTID**
- Why: `NAME_EN` is human-readable and meaningful; OBJECTID as fallback ensures uniqueness
- Format: `kebab-case(NAME_EN)` or `item-{OBJECTID}`

**4. Output structure: `stac/<base>/collection.json` and `stac/<base>/items/<id>.json`**
- Why: Mirrors STAC Browser / STAC API convention
- `<base>` = input filename without extension

**5. GeoJSON CRS (crs.properties.name) auto-detected**
- Why: The sample data uses EPSG:2326; future data may use different CRS
- Fallback to WGS84 if no CRS specified

**6. Collection `keywords` and `providers` left empty / optional**
- Why: Not meaningful for converted data without external metadata

## Risks / Trade-offs

[No CRS in GeoJSON] → Default to WGS84, warn user
[Non-point geometry bounding box] → Calculate from coordinates
[Duplicate Item IDs] → Append counter suffix (-1, -2)
[Large FeatureCollections] → Process sequentially, no threading needed for sample data

## Open Questions

- Should the CLI support specifying a base URL for item self-links? (Not in v1, use relative paths)
- Should geometry type be stored as Item property? (Yes, in `geometry_type` key)