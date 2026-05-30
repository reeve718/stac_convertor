## ADDED Requirements

### Requirement: Workers CLI option
The CLI SHALL accept a `--workers` option to control the number of parallel worker threads for batch conversion.

#### Scenario: Workers defaults to 1
- **WHEN** user runs batch conversion without `--workers`
- **THEN** files are processed sequentially (1 worker)

#### Scenario: Workers set to specific value
- **WHEN** user runs batch conversion with `--workers 4`
- **THEN** up to 4 files are processed in parallel

#### Scenario: Workers set to 1
- **WHEN** user explicitly sets `--workers 1`
- **THEN** files are processed sequentially (same as default)

### Requirement: Parallel batch processing
The CLI SHALL process multiple files in parallel when `--workers` is greater than 1.

#### Scenario: Multiple files processed concurrently
- **WHEN** user runs `geojson2stac --input-dir data/ --workers 4`
- **THEN** up to 4 files are converted concurrently
- **AND** each file's output is written to its designated output directory

#### Scenario: Files are processed independently
- **WHEN** files are processed in parallel
- **THEN** each file's conversion is independent of others
- **AND** no cross-file state is shared between workers

### Requirement: Thread-safe error handling
Errors during parallel processing SHALL be collected and reported without crashing other workers.

#### Scenario: One file fails during parallel processing
- **WHEN** worker processes a file that raises an exception
- **THEN** the exception is caught and recorded
- **AND** other workers continue processing their files
- **AND** final summary reports which files failed

#### Scenario: All files succeed
- **WHEN** all files are processed successfully in parallel
- **THEN** summary reports "Batch complete: N succeeded"

#### Scenario: Some files fail
- **WHEN** K files fail during parallel processing
- **THEN** summary reports "Batch complete: M succeeded, K failed"
- **AND** each failed file path and error message is listed

### Requirement: Backward compatibility
The parallel processing feature SHALL NOT change behavior when `--workers` is not specified or is set to 1.

#### Scenario: Sequential mode produces identical output
- **WHEN** user runs with `--workers 1` or without `--workers`
- **THEN** output is identical to previous sequential implementation
