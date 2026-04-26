## ADDED Requirements

### Requirement: Parse GeoJSON FeatureCollection
The system SHALL read a GeoJSON file from the given path and parse it as a GeoJSON FeatureCollection object per RFC 7946.

#### Scenario: Valid FeatureCollection input
- **WHEN** the CLI is invoked with a path to a valid GeoJSON FeatureCollection file
- **THEN** the system SHALL return the parsed FeatureCollection with all features accessible

#### Scenario: Missing file
- **WHEN** the CLI is invoked with a path to a non-existent file
- **THEN** the system SHALL exit with an error message indicating the file was not found

#### Scenario: Invalid JSON
- **WHEN** the CLI is invoked with a path to a file containing invalid JSON
- **THEN** the system SHALL exit with an error message indicating JSON parsing failed

#### Scenario: Valid GeoJSON but not a FeatureCollection
- **WHEN** the CLI is invoked with a path to a valid GeoJSON file that is not a FeatureCollection
- **THEN** the system SHALL exit with an error message indicating the root object must be a FeatureCollection

### Requirement: Extract Features
The system SHALL extract all Feature objects from the parsed FeatureCollection.

#### Scenario: Multiple features
- **WHEN** the FeatureCollection contains 25 features
- **THEN** the system SHALL extract exactly 25 Feature objects

#### Scenario: Empty FeatureCollection
- **WHEN** the FeatureCollection contains zero features
- **THEN** the system SHALL exit with an error message indicating no features were found

### Requirement: Detect GeoJSON CRS
The system SHALL detect the coordinate reference system from the GeoJSON's `crs` field if present.

#### Scenario: EPSG:2326 CRS
- **WHEN** the FeatureCollection has `crs.properties.name = "EPSG:2326"`
- **THEN** the system SHALL store that CRS identifier for use by the CRS transformer

#### Scenario: No CRS specified
- **WHEN** the FeatureCollection has no `crs` field
- **THEN** the system SHALL assume WGS84 (EPSG:4326) as the default CRS and log a warning

### Requirement: Validate Geometry Types
The system SHALL support all GeoJSON geometry types: Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon.

#### Scenario: Point geometry
- **WHEN** a Feature has geometry type "Point"
- **THEN** the system SHALL pass the coordinates array to the CRS transformer

#### Scenario: Polygon geometry
- **WHEN** a Feature has geometry type "Polygon"
- **THEN** the system SHALL pass the coordinates array (list of rings) to the CRS transformer

#### Scenario: Unknown geometry type
- **WHEN** a Feature has an unsupported geometry type
- **THEN** the system SHALL exit with an error indicating the geometry type is not supported