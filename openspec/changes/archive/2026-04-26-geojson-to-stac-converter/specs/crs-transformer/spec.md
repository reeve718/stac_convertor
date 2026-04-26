## ADDED Requirements

### Requirement: Transform EPSG:2326 to WGS84
The system SHALL transform coordinates from EPSG:2326 (Hong Kong 1980 Grid) to WGS84 (EPSG:4326).

#### Scenario: Point transformation
- **WHEN** input coordinates are `[848550, 817395]` in EPSG:2326
- **THEN** output SHALL be approximately `[114.26, 22.31]` in WGS84 (longitude, latitude)

#### Scenario: Polygon ring transformation
- **WHEN** input coordinates are a polygon ring with multiple vertices
- **THEN** each vertex SHALL be transformed individually to WGS84

### Requirement: Support All Geometry Coordinate Structures
The system SHALL handle coordinate arrays for all geometry types.

#### Scenario: Point coordinates
- **WHEN** geometry type is Point
- **THEN** transform `[x, y]` to `[lon, lat]`

#### Scenario: LineString coordinates
- **WHEN** geometry type is LineString
- **THEN** transform each `[x, y]` pair in the coordinates array

#### Scenario: Polygon coordinates
- **WHEN** geometry type is Polygon
- **THEN** transform each ring's coordinates array (each ring is a list of `[x, y]` pairs)

#### Scenario: Multi* geometries
- **WHEN** geometry type is MultiPoint, MultiLineString, or MultiPolygon
- **THEN** transform all coordinates within all sub-geometries

### Requirement: Calculate Bounding Box for Item
The system SHALL calculate the bounding box (bbox) for a STAC Item from transformed coordinates.

#### Scenario: Point bounding box
- **WHEN** geometry is a point at `[114.26, 22.31]`
- **THEN** bbox SHALL be `[114.26, 22.31, 114.26, 22.31]`

#### Scenario: Multi-vertex bounding box
- **WHEN** geometry has coordinates spanning multiple points
- **THEN** bbox SHALL be `[min_lon, min_lat, max_lon, max_lat]` encompassing all coordinates

### Requirement: Handle Coordinate Transformation Errors
The system SHALL handle and report coordinate transformation errors gracefully.

#### Scenario: Invalid EPSG code
- **WHEN** the GeoJSON specifies an unrecognized EPSG code
- **THEN** the system SHALL exit with an error indicating the CRS could not be identified

#### Scenario: Out-of-bounds coordinates
- **WHEN** coordinates are outside the valid range for the source CRS
- **THEN** the system SHALL log a warning and attempt transformation, or skip the feature with an error