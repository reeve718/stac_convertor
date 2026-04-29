## ADDED Requirements

### Requirement: Stream-parse large GeoJSON files
The system SHALL parse GeoJSON FeatureCollection files using a streaming approach that does not load the entire file into memory.

#### Scenario: Parse 3GB GeoJSON file
- **WHEN** a 3GB GeoJSON file with 500k features is provided as input
- **THEN** the system processes each feature individually without loading the entire file into memory
- **AND** peak memory usage remains bounded regardless of input file size

#### Scenario: Invalid JSON detected during streaming
- **WHEN** streaming parser encounters malformed JSON at position N
- **THEN** the system SHALL exit with an error message identifying the approximate position of the error
- **AND** no output file is written

### Requirement: Incremental feature processing
The system SHALL process features one-by-one from the input stream, converting each to a STAC item before the next feature is read from the input.

#### Scenario: Feature converted immediately
- **WHEN** a feature is read from the input stream
- **THEN** it is converted to a STAC item immediately
- **AND** the item is added to the output buffer before reading the next feature

## ADDED Requirements

### Requirement: Single items.json file output
The system SHALL write all STAC items to a single `items.json` file in GeoJSON FeatureCollection format.

#### Scenario: All features written to single file
- **WHEN** input GeoJSON contains N features
- **THEN** output `items.json` SHALL contain a FeatureCollection with exactly N features
- **AND** each feature is a valid STAC item

#### Scenario: Items file structure
- **WHEN** the conversion completes successfully
- **THEN** `items.json` SHALL be a valid GeoJSON FeatureCollection
- **AND** the file contains `type`, `features` fields
- **AND** `features` array contains all converted STAC items

### Requirement: Inline duplicate ID handling
The system SHALL detect and handle duplicate item IDs during the streaming process without requiring a second pass.

#### Scenario: Duplicate ID found mid-stream
- **WHEN** a feature with an already-seen ID is encountered during streaming
- **THEN** the system SHALL rename the item ID by appending an incrementing suffix (e.g., `name-en-1`, `name-en-2`)
- **AND** the renamed item is written to items.json

#### Scenario: No duplicates
- **WHEN** all features have unique IDs
- **THEN** all items are written with their original IDs unchanged
