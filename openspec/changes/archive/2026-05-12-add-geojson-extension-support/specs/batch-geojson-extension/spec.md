## ADDED Requirements

### Requirement: Batch directory conversion supports .geojson extension
The CLI SHALL process both `.json` and `.geojson` files when using `--input-dir` batch mode.

#### Scenario: Directory with .geojson files
- **WHEN** user runs `geojson2stac --input-dir data/` where `data/` contains `.json` and `.geojson` files
- **THEN** CLI processes all files with `.json` extension
- **AND** CLI processes all files with `.geojson` extension

#### Scenario: Directory with only .geojson files
- **WHEN** user runs `geojson2stac --input-dir data/` where `data/` contains only `.geojson` files
- **THEN** CLI processes all `.geojson` files
- **AND** no warning is printed

#### Scenario: Empty directory
- **WHEN** user runs `geojson2stac --input-dir empty_dir/` where no `.json` or `.geojson` files exist
- **THEN** CLI prints a warning and exits cleanly with code 0