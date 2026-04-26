## ADDED Requirements

### Requirement: Repository SHALL use `src/stac_convertor/` as the Python package

All source modules SHALL live under `src/stac_convertor/` as a proper Python package.

#### Scenario: Package structure is correct
- **WHEN** a user inspects the repo root
- **THEN** `src/stac_convertor/` exists and contains all modules (`cli.py`, `convertor.py`, etc.)

#### Scenario: Package is importable after install
- **WHEN** a developer runs `pip install -e .`
- **THEN** `import src.stac_convertor` works from any directory

---

### Requirement: CLI entry point SHALL work after install

The `geojson2stac` command SHALL be available after `pip install -e .` or `pip install .`.

#### Scenario: CLI available after editable install
- **WHEN** a developer runs `pip install -e .`
- **THEN** `geojson2stac --help` prints the CLI help output

#### Scenario: CLI works with sample data
- **WHEN** a user runs `geojson2stac data/CTRY_PARK.json`
- **THEN** `stac/CTRY_PARK/` is created with `collection.json` and item files

---

### Requirement: Tests SHALL pass after restructure

All tests SHALL pass after the folder restructure, with updated import paths.

#### Scenario: All tests pass
- **WHEN** a developer runs `pytest`
- **THEN** all tests pass with 0 failures

#### Scenario: Test imports use correct package path
- **WHEN** a test file imports a module
- **THEN** it uses `from src.stac_convertor import ...` (not `from src import ...`)

---

### Requirement: Repository SHALL have only one branch

The GitHub repo SHALL have only the `main` branch after restructuring.

#### Scenario: Only main branch exists
- **WHEN** a user views the GitHub repo branches
- **THEN** only `main` is listed

#### Scenario: Worktree directory removed
- **WHEN** a user inspects the repo root
- **THEN** `.worktrees/` directory does not exist
