## ADDED Requirements

### Requirement: Bulk Insert Output Format
The system SHALL support generating STAC items in bulk insert format for API import.

#### Scenario: Generate bulk format with string keys
- **WHEN** user specifies `--output-format bulk`
- **THEN** items are written as an object with string keys ("0", "1", ...)
- **THEN** top-level field `method: "insert"` is added

#### Scenario: ID from OBJECTID
- **WHEN** item has `properties.OBJECTID`
- **THEN** item `id` SHALL be the string representation of OBJECTID (e.g., "1", "2")
- **AND** ID SHALL be unique and non-repeating

#### Scenario: Collection field on each item
- **WHEN** generating bulk format
- **THEN** each item SHALL include `collection` field with value from collection.json `id`
- **AND** all items in the same collection SHALL have the same collection value

#### Scenario: Default datetime
- **WHEN** item does not have `properties.datetime`
- **THEN** system SHALL use `"1900-01-01T00:00:00"` as the datetime value

#### Scenario: stac_version field
- **WHEN** generating bulk format
- **THEN** each item SHALL include `stac_version: "1.0.0"` at item level

#### Scenario: Strip links and assets
- **WHEN** generating bulk format
- **THEN** items SHALL NOT include `links` array
- **AND** items SHALL NOT include `assets` object

#### Scenario: Default output format is STAC
- **WHEN** user does not specify `--output-format`
- **THEN** system SHALL default to `stac` format (existing behavior)