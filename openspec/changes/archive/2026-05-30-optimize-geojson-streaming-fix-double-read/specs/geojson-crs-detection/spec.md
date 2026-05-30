## ADDED Requirements

### Requirement: Bounded prefix CRS detection
The CRS detection SHALL read only the first 4KB of the GeoJSON file to extract the coordinate reference system.

#### Scenario: CRS found within prefix
- **WHEN** a GeoJSON file has `crs` at the root level within the first 4KB
- **THEN** CRS is extracted from `crs.properties.name`
- **AND** the value is returned (e.g., `"EPSG:2326"`)

#### Scenario: CRS beyond prefix boundary
- **WHEN** a GeoJSON file has `crs` at a position beyond 4KB
- **THEN** CRS detection falls back to WGS84 (EPSG:4326)

#### Scenario: Partial JSON at prefix boundary
- **WHEN** the 4KB prefix ends mid-token (e.g., partial `"name": "EP`)
- **THEN** `json.JSONDecodeError` is caught
- **AND** CRS detection falls back to WGS84 (EPSG:4326)

#### Scenario: No CRS in file
- **WHEN** a GeoJSON file has no `crs` property
- **THEN** CRS detection falls back to WGS84 (EPSG:4326)
- **AND** a warning is logged (if verbose logging enabled)

### Requirement: Single-pass file reading
The `stream_geojson()` function SHALL perform CRS detection and feature streaming with no more than one full file read.

#### Scenario: CRS and features streamed sequentially
- **WHEN** `stream_geojson()` is called on a valid GeoJSON file
- **THEN** CRS is detected from a bounded prefix (one file handle opened)
- **AND** features are streamed from the same file (same file handle reused)
- **AND** no second full file read occurs

### Requirement: CRS format validation
The detected CRS SHALL be validated to ensure it is a valid EPSG coordinate reference system.

#### Scenario: Valid EPSG CRS
- **WHEN** `crs.properties.name` starts with `"EPSG:"`
- **THEN** the full CRS string is returned (e.g., `"EPSG:4326"`)

#### Scenario: Non-EPSG CRS
- **WHEN** `crs.properties.name` does not start with `"EPSG:"`
- **THEN** CRS detection falls back to WGS84 (EPSG:4326)

#### Scenario: CRS type is not "name"
- **WHEN** `crs.type` is not `"name"` (e.g., `"EPSG"` or absent)
- **THEN** CRS detection falls back to WGS84 (EPSG:4326)
