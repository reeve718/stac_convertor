## ADDED Requirements

### Requirement: Generate STAC Item from GeoJSON Feature
The system SHALL generate a valid STAC Item JSON object per the STAC spec for each GeoJSON Feature.

#### Scenario: Valid item output
- **WHEN** a GeoJSON Feature is converted
- **THEN** the system SHALL create an Item with `type: "Feature"` and all required STAC Item fields

#### Scenario: Item ID from NAME_EN
- **WHEN** a Feature has property `NAME_EN = "Clear Water Bay Country Park"`
- **THEN** the Item `id` SHALL be `clear-water-bay-country-park`

#### Scenario: Item ID fallback to OBJECTID
- **WHEN** a Feature has no `NAME_EN` property but has `OBJECTID = 5`
- **THEN** the Item `id` SHALL be `item-5`

#### Scenario: Duplicate ID handling
- **WHEN** two Features have the same NAME_EN value
- **THEN** the second Item SHALL have an ID with `-1` suffix appended

### Requirement: STAC Item Required Fields
The system SHALL include all required STAC Item fields: id, type, geometry, bounding_box, properties, links, assets.

#### Scenario: Item geometry transformed
- **WHEN** a Feature has EPSG:2326 coordinates
- **THEN** the Item `geometry` SHALL contain the same coordinates transformed to WGS84

#### Scenario: Item properties
- **WHEN** a Feature has properties OBJECTID, NAME_EN, NAME_TC
- **THEN** the Item `properties` SHALL include:
  - `datetime`: ISO 8601 datetime (use current timestamp or null if not available)
  - `OBJECTID`: original value
  - `NAME_EN`: original value
  - `NAME_TC`: original value
  - `geometry_type`: the GeoJSON geometry type

### Requirement: Item Links
The system SHALL include required links for each STAC Item.

#### Scenario: Self link
- **WHEN** an Item is generated
- **THEN** it SHALL include a link with `rel: "self"` pointing to the item JSON file path

#### Scenario: Collection link
- **WHEN** an Item is generated
- **THEN** it SHALL include a link with `rel: "collection"` pointing to the collection JSON file

### Requirement: Write Item to File
The system SHALL write each Item JSON to `stac/<basename>/items/<id>.json`.

#### Scenario: Create items directory
- **WHEN** the items directory does not exist
- **THEN** the system SHALL create `stac/<basename>/items/` directory

#### Scenario: Formatted JSON output
- **WHEN** an Item is written to file
- **THEN** it SHALL be formatted JSON with 2-space indentation

### Requirement: Geometry Type Property
The system SHALL store the GeoJSON geometry type as a property in each Item.

#### Scenario: Point geometry
- **WHEN** a Feature has geometry type "Point"
- **THEN** the Item properties SHALL include `geometry_type: "Point"`

#### Scenario: Polygon geometry
- **WHEN** a Feature has geometry type "Polygon"
- **THEN** the Item properties SHALL include `geometry_type: "Polygon"`