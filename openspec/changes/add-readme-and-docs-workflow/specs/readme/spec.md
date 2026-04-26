## ADDED Requirements

### Requirement: README SHALL exist at repo root

The repository root SHALL contain a `README.md` file rendered on the GitHub repository homepage.

#### Scenario: README is present
- **WHEN** a user visits the GitHub repository
- **THEN** the repository homepage displays the contents of `README.md`

#### Scenario: README is missing
- **WHEN** `README.md` does not exist at the repo root
- **THEN** the build is considered incomplete

---

### Requirement: README SHALL include installation instructions

The `README.md` SHALL document how to install the tool, including:
- Minimum Python version (from `pyproject.toml`)
- Install from pip
- Install in editable mode for development

#### Scenario: Installation via pip
- **WHEN** a user reads the Installation section of README
- **THEN** they can copy a `pip install` command that installs the tool

#### Scenario: Development installation
- **WHEN** a developer reads the Installation section of README
- **THEN** they can clone the repo and run `pip install -e .` to install in editable mode

---

### Requirement: README SHALL include a quick start example

The `README.md` SHALL include a minimal working example converting `data/CTRY_PARK.json` to STAC output.

#### Scenario: Quick start with sample data
- **WHEN** a user copies and runs the quick start command
- **THEN** the tool produces STAC output in `stac/CTRY_PARK/`

---

### Requirement: README SHALL document all CLI arguments

The `README.md` SHALL list every CLI argument and option accepted by the Typer CLI in `src/cli.py`.

#### Scenario: CLI reference matches implementation
- **WHEN** a user runs `geojson2stac --help`
- **THEN** the output matches the CLI reference section in README

#### Scenario: New CLI argument added
- **WHEN** a developer adds a new CLI argument to `src/cli.py`
- **THEN** the README CLI reference section is updated to document it

---

### Requirement: README SHALL include development setup

The `README.md` SHALL document how to run tests and set up a development environment.

#### Scenario: Running tests
- **WHEN** a developer reads the Development section
- **THEN** they can run `pytest` to execute the test suite

---

### Requirement: README SHALL include license information

The `README.md` SHALL specify the project license.

#### Scenario: License visible
- **WHEN** a user reads the README
- **THEN** they can find the license name or a link to the license file
