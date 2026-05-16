## ADDED Requirements

### Requirement: Recursive directory scanning
The CLI SHALL support a `--recursive` flag that, when combined with `--input-dir`, scans all subdirectories recursively using `Path.rglob()` to find all `.json` and `.geojson` files.

#### Scenario: Recursive scan finds nested files
- **WHEN** user runs `geojson2stac --input-dir data/ --recursive`
- **THEN** CLI finds files at all nesting levels: `data/file.json`, `data/sub/file.json`, `data/sub/deep/file.json`

#### Scenario: Recursive mode is optional
- **WHEN** user runs `geojson2stac --input-dir data/` without `--recursive`
- **THEN** CLI finds only files at the first level of `data/`
- **AND** files in subdirectories are NOT processed

#### Scenario: Glob pattern files included in recursive scan
- **WHEN** user runs `geojson2stac --input-dir data/ --recursive`
- **THEN** files with `.geojson` extension are included alongside `.json` files

### Requirement: Output structure mirrors input hierarchy
When `--recursive` is used, the output directory structure SHALL mirror the input directory structure relative to the `--input-dir` root.

#### Scenario: Nested file output preserves folder structure
- **WHEN** user runs `geojson2stac --input-dir data/ --recursive`
- **AND** input file is `data/subfolder/nested/file.json`
- **THEN** output is written to `stac/subfolder/nested/file/collection.json` and `stac/subfolder/nested/file/items.json`

#### Scenario: Multiple files in same subdirectory
- **WHEN** user runs `geojson2stac --input-dir data/ --recursive`
- **AND** input directory contains `data/sub/file1.json` and `data/sub/file2.json`
- **THEN** outputs are `stac/sub/file1/` and `stac/sub/file2/` respectively
- **AND** no output folders are created for nesting levels without GeoJSON files

### Requirement: Relative path computation for output subdirectory
When `--recursive` is used, the CLI SHALL compute the relative path from `input_dir` to each found file and use that to construct the output subdirectory.

#### Scenario: Relative path excludes input directory prefix
- **WHEN** user runs `geojson2stac --input-dir data/ --recursive`
- **AND** a file at `data/sub/deep/file.json` is found
- **THEN** the output subdirectory is `output_dir/sub/deep/file/`
- **AND** the relative path `sub/deep/file` is computed by stripping `data/` from the file's parent path

#### Scenario: Files at root of input directory
- **WHEN** user runs `geojson2stac --input-dir data/ --recursive`
- **AND** a file at `data/root_file.json` is found
- **THEN** the output subdirectory is `output_dir/root_file/`
- **AND** no extra directory prefix is added