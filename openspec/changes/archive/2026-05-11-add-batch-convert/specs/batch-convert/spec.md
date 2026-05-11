## ADDED Requirements

### Requirement: Batch directory conversion
The CLI SHALL support an `--input-dir` option that processes all `.json` files in the specified directory, converting each independently and writing output to separate subdirectories under the output directory.

#### Scenario: Convert all files in directory
- **WHEN** user runs `geojson2stac --input-dir data/`
- **THEN** CLI iterates over all `*.json` files in `data/`
- **AND** for each file, creates a subdirectory under the output directory named after the input filename
- **AND** writes `collection.json` and `items.json` into that subdirectory

#### Scenario: Empty directory
- **WHEN** user runs `geojson2stac --input-dir empty_dir/` where no `.json` files exist
- **THEN** CLI prints a warning and exits cleanly with code 0

#### Scenario: Directory with mixed file types
- **WHEN** user runs `geojson2stac --input-dir data/` where `data/` contains `.json` and `.geojson` files
- **THEN** CLI processes only `.json` files
- **AND** silently skips files without `.json` extension

### Requirement: Glob pattern support
The CLI SHALL treat the `INPUT_FILE` argument as a glob pattern when it contains `*`, converting all files matching the pattern.

#### Scenario: Glob pattern matches multiple files
- **WHEN** user runs `geojson2stac "data/*.json"`
- **THEN** CLI expands the glob and converts each matching file
- **AND** output structure matches the per-file subdirectory pattern

### Requirement: Mutual exclusivity
The CLI SHALL raise an error if both `INPUT_FILE` and `--input-dir` are provided.

#### Scenario: Both options present
- **WHEN** user runs `geojson2stac data/CTRY_PARK.json --input-dir data/`
- **THEN** CLI exits with an error message explaining mutual exclusivity

### Requirement: Per-file error handling
When processing multiple files, the CLI SHALL continue processing remaining files if a file fails, and SHALL report all failures at the end.

#### Scenario: One file fails during batch
- **WHEN** user runs `geojson2stac --input-dir data/` and file N is corrupt
- **THEN** CLI logs the error for file N
- **AND** continues processing remaining files
- **AND** at the end, reports "N succeeded, M failed"
- **AND** exits with non-zero code if any failed

#### Scenario: All files succeed
- **WHEN** user runs `geojson2stac --input-dir data/` and all files convert successfully
- **THEN** CLI reports success
- **AND** exits with code 0
