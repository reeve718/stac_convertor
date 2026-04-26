## ADDED Requirements

### Requirement: Generate STAC Collection JSON
The system SHALL generate a valid STAC Collection JSON object per the STAC spec.

#### Scenario: Valid collection output
- **WHEN** conversion begins with 25 features
- **THEN** the system SHALL create a Collection with `type: "Collection"` and all required STAC fields

#### Scenario: Collection ID from filename
- **WHEN** input file is `CTRY_PARK.json`
- **THEN** the Collection `id` SHALL be `ctry-park` (kebab-case of filename without extension)

### Requirement: STAC Collection Required Fields
The system SHALL include all required STAC Collection fields: id, type, stac_version, stac_extensions, geometry, bounding_box,, time_start, time_end, license,, properties, keywords, providers, summaries, and links.

#### Scenario: All required fields present
- **WHEN** the Collection is generated
- **THEN** it SHALL include: id, type, stac_version, stac_extensions, geometry, bounding_box, start_datetime, end_datetime, license, title, description, keywords, providers, extent, and links

#### Scenario: Item links in collection
- **WHEN** the Collection is generated
- **THEN** it SHALL include a `links` array containing:
  - A `self` link pointing to the collection JSON file
  - An `items` link with `rel: "items"` pointing to the items directory or search endpoint

### Requirement: Bounding Box Calculation
The system SHALL calculate the bounding box from the transformed Item geometries.

#### Scenario: Point features bounding box
- **WHEN** all features are points
- **THEN** the bounding box SHALL be [min_lon, min_lat, max_lon, max_lat]

#### Scenario: Mixed geometry bounding box
- **WHEN** features include polygons
- **THEN** the bounding box SHALL encompass all vertex coordinates

### Requirement: Write Collection to File
The system SHALL write the Collection JSON to `stac/<basename>/collection.json`.

#### Scenario: Create output directory
- **WHEN** the output directory does not exist
- **THEN** the system SHALL create `stac/<basename>/` directory structure

#### Scenario: Write collection JSON
- **WHEN** the Collection object is complete
- **THEN** the system SHALL write it as formatted JSON to `stac/<basename>/collection.json`