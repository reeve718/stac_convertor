## ADDED Requirements

### Requirement: Reused Transformer per file
The system SHALL create a single `pyproj.Transformer` instance per input file and reuse it for all coordinate transformations within that file.

#### Scenario: Large file conversion performance
- **WHEN** user converts a GeoJSON file with 10,000 features
- **THEN** the system creates exactly one `Transformer` instance
- **AND** reuses that instance for all coordinate transformations
- **AND** conversion completes in under 5 seconds (vs. potentially minutes before)

#### Scenario: Multiple files
- **WHEN** user batch-converts multiple files with `geojson2stac --input-dir data/`
- **THEN** each file gets its own `Transformer` instance
- **AND** files are processed sequentially

### Requirement: Coordinate transformation accuracy
The system SHALL produce identical coordinate output whether Transformer is reused or created per transformation.

#### Scenario: Coordinate values unchanged
- **WHEN** a feature with Point geometry at EPSG:2326 is converted
- **THEN** the output coordinates SHALL match the reference value for EPSG:2326 → EPSG:4326 transformation
- **AND** the bbox SHALL be calculated correctly from transformed coordinates

#### Scenario: MultiPolygon transformation
- **WHEN** a feature with MultiPolygon geometry is converted
- **THEN** all rings and all polygons SHALL be transformed using the same Transformer instance
- **AND** no coordinates are skipped or duplicated