# README and Docs Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `README.md` to the repo root and enforce README updates via OpenSpec rules whenever the CLI changes.

**Architecture:** A single `README.md` at the repo root covers installation, quick start, CLI reference, development setup, and license. `CLAUDE.md` and `openspec/config.yaml` are updated to require README review on CLI changes.

**Tech Stack:** Python CLI tool (Typer), OpenSpec workflow, `pyproject.toml`.

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `README.md` | Create | User-facing documentation at repo root |
| `CLAUDE.md` | Modify | Add docs-enforcement rule for AI agents |
| `openspec/config.yaml` | Modify | Add per-artifact rule for tasks |
| `tests/test_readme.py` | Create | Validation: README sections and CLI consistency |

---

## Pre-flight: Verify Current State

Before starting, confirm the worktree is clean and on the right branch.

- [ ] **Step 1: Check worktree status**

Run: `git -C /c/Github/stac_convertor/.worktrees/geojson-to-stac status`
Expected: `nothing to commit, working tree clean`

Run: `git -C /c/Github/stac_convertor/.worktrees/geojson-to-stac branch`
Expected: `* main`

---

## Task 1: Write README.md

**Files:**
- Create: `.worktrees/geojson-to-stac/README.md`

The README should follow this exact section order:

```
1. Badge strip
2. One-line description
3. Installation
4. Quick start
5. CLI reference
6. How CRS transform works
7. Development setup
8. License
```

**Tech stack facts to use:**
- Package name: `stac-convertor`
- CLI entry point: `geojson2stac`
- Python requirement: `>=3.10`
- Key dependencies: `typer>=0.12.0`, `pyproj>=3.6.0`
- Dev deps: `pytest>=7.0.0`
- Sample data: `data/CTRY_PARK.json` (EPSG:2326 → WGS84)
- CRS: EPSG:2326 (Hong Kong) → EPSG:4326 (WGS84)
- License: not yet defined — use `MIT` (placeholder, can be changed later)

---

- [ ] **Step 1: Write README.md**

Create `.worktrees/geojson-to-stac/README.md` with this exact content:

```markdown
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

# stac-convertor

Convert GeoJSON FeatureCollections to STAC Collections and Items.

## Installation

**From pip:**

```bash
pip install stac-convertor
```

**Development (editable install):**

```bash
git clone https://github.com/reeve718/stac_convertor.git
cd stac_convertor
pip install -e ".[dev]"
```

Requires Python 3.10 or later.

## Quick Start

Convert a GeoJSON file using the built-in sample data:

```bash
geojson2stac data/CTRY_PARK.json
```

Output is written to `stac/CTRY_PARK/`:
```
stac/CTRY_PARK/
├── collection.json        ← STAC Collection
└── items/
    ├── clear-water-bay-country-park.json
    ├── pok-fu-lam-country-park.json
    └── ... (one file per feature)
```

## CLI Reference

```
geojson2stac INPUT_FILE [-o OUTPUT_DIR] [-v]
```

| Argument / Option | Description | Default |
|---|---|---|
| `INPUT_FILE` | Path to GeoJSON file (required) | — |
| `-o`, `--output` | Output directory | `stac/` |
| `-v`, `--verbose` | Enable verbose output | `false` |

**Examples:**

```bash
# Basic usage
geojson2stac data/CTRY_PARK.json

# Custom output directory
geojson2stac data/CTRY_PARK.json -o ./output

# Verbose mode
geojson2stac data/CTRY_PARK.json -v
```

## How CRS Transform Works

The convertor transforms all geometry coordinates from their source CRS to WGS84 (EPSG:4326) automatically. No configuration needed — the CRS is read from the GeoJSON file's `crs` property.

Supported input CRS includes:
- EPSG:2326 (Hong Kong 1980 Grid System)
- Any CRS supported by `pyproj`

The output STAC Items always use WGS84 coordinates.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/reeve718/stac_convertor.git
cd stac_convertor

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

MIT License — see [LICENSE](LICENSE) file.
```

- [ ] **Step 2: Verify README looks correct**

Run: `wc -l .worktrees/geojson-to-stac/README.md`
Expected: ~90 lines (within the ~100 line target from design)

- [ ] **Step 3: Commit**

```bash
git -C /c/Github/stac_convertor/.worktrees/geojson-to-stac add README.md
git -C /c/Github/stac_convertor/.worktrees/geojson-to-stac commit -m "docs: add README with installation, quick start, and CLI reference"
```

---

## Task 2: Update CLAUDE.md

**Files:**
- Modify: `.worktrees/geojson-to-stac/../claude.md` (in the main repo, accessible from worktree)

> Note: `claude.md` lives in the main repo (`stac_convertor/`), not the worktree. Edit it directly at `c:/Github/stac_convertor/claude.md`.

---

- [ ] **Step 1: Read current CLAUDE.md**

Read: `c:/Github/stac_convertor/claude.md`

- [ ] **Step 2: Append docs-enforcement rule to CLAUDE.md**

Add this section at the end of `claude.md`:

```markdown
## Documentation Enforcement

Any change that touches `src/cli.py` or adds/modifies CLI arguments MUST include an update to `README.md`. This is enforced via the OpenSpec per-artifact rule for tasks. The README is the source of truth for user-facing CLI documentation.
```

- [ ] **Step 3: Commit the CLAUDE.md change**

```bash
git -C /c/Github/stac_convertor add claude.md
git -C /c/Github/stac_convertor commit -m "docs: add CLI documentation enforcement rule to CLAUDE.md"
```

---

## Task 3: Update OpenSpec config

**Files:**
- Modify: `c:/Github/stac_convertor/openspec/config.yaml`

---

- [ ] **Step 1: Read current config**

Read: `c:/Github/stac_convertor/openspec/config.yaml`

- [ ] **Step 2: Add tasks per-artifact rule**

The current config has an empty `rules:` section with commented examples. Replace the `rules:` block with:

```yaml
# Per-artifact rules (optional)
# Add custom rules for specific artifacts.
  rules:
    tasks:
      - "For any change touching src/cli.py or adding CLI arguments, README.md MUST be updated in the tasks list"
```

- [ ] **Step 3: Commit the OpenSpec config change**

```bash
git -C /c/Github/stac_convertor add openspec/config.yaml
git -C /c/Github/stac_convertor commit -m "chore: add OpenSpec per-artifact rule requiring README update on CLI changes"
```

---

## Task 4: Validation Test (Optional — Recommended)

**Files:**
- Create: `.worktrees/geojson-to-stac/tests/test_readme.py`

This test validates that the README meets the spec requirements. Run it at the end to confirm the README is complete.

---

- [ ] **Step 1: Write the validation test**

Create `.worktrees/geojson-to-stac/tests/test_readme.py`:

```python
"""Validate README.md meets spec requirements."""
from pathlib import Path

ROOT = Path(__file__).parent.parent
README = ROOT / "README.md"


def test_readme_exists():
    assert README.exists(), "README.md must exist at repo root"


def test_readme_has_installation_section():
    content = README.read_text()
    assert "Installation" in content
    assert "pip install" in content
    assert "editable" in content.lower()


def test_readme_has_quick_start():
    content = README.read_text()
    assert "Quick Start" in content
    assert "CTRY_PARK" in content
    assert "geojson2stac" in content


def test_readme_documents_cli_arguments():
    content = README.read_text()
    assert "INPUT_FILE" in content or "input_file" in content.lower()
    assert "--output" in content or "-o" in content
    assert "--verbose" in content or "-v" in content


def test_readme_has_development_setup():
    content = README.read_text()
    assert "Development" in content
    assert "pytest" in content
    assert "clone" in content.lower()


def test_readme_has_license():
    content = README.read_text()
    assert "License" in content or "LICENSE" in content


def test_readme_has_crs_explanation():
    content = README.read_text()
    assert "CRS" in content or "crs" in content.lower()
    assert "WGS84" in content or "EPSG:4326" in content
```

- [ ] **Step 2: Run the validation tests**

Run: `git -C /c/Github/stac_convertor/.worktrees/geojson-to-stac pytest tests/test_readme.py -v`
Expected: 7 passes

- [ ] **Step 3: Commit the test**

```bash
git -C /c/Github/stac_convertor/.worktrees/geojson-to-stac add tests/test_readme.py
git -C /c/Github/stac_convertor/.worktrees/geojson-to-stac commit -m "test: add README validation test suite"
```

---

## Self-Review Checklist

- [ ] Spec coverage: Every requirement in `specs/readme/spec.md` and `specs/docs-enforcement/spec.md` has a corresponding task step. ✓
- [ ] No placeholders: All code blocks are complete (README content, CLAUDE.md rule, OpenSpec rule, test file). No TBD/TODO. ✓
- [ ] File paths: All paths are absolute from the worktree root. CLAUDE.md and openspec/config.yaml correctly point to the main repo. ✓
- [ ] Commit messages: Each task has its own commit with a conventional commit prefix (`docs:`, `chore:`, `test:`). ✓

---

## Summary

| Task | Files touched | Commit |
|------|--------------|--------|
| 1. README.md | `.worktrees/geojson-to-stac/README.md` | `docs: add README...` |
| 2. CLAUDE.md | `claude.md` | `docs: add CLI documentation enforcement...` |
| 3. OpenSpec config | `openspec/config.yaml` | `chore: add OpenSpec per-artifact rule...` |
| 4. Validation test | `tests/test_readme.py` | `test: add README validation...` |
