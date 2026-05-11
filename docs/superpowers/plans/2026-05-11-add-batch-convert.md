# Batch Convert Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add batch conversion support to `geojson2stac` CLI via `--input-dir` option and glob patterns, enabling conversion of multiple files in a single invocation.

**Architecture:** The CLI is refactored to detect whether the input is a glob pattern or a directory, then iterates over matching files. Each file is converted via the existing `convert_file()` function. Errors are collected per-file and reported at the end.

**Tech Stack:** Python 3.10+, `typer`, `pathlib`, `glob` (stdlib)

---

## File Map

```
src/cli.py          # Main entry point - add --input-dir, glob detection, batch loop, error handling
src/convertor.py    # No changes needed (already file-agnostic)
README.md           # Update CLI reference with new options
tests/test_cli.py   # New tests for batch behavior (create if not exists)
```

---

## Task 1: Glob Pattern Detection Helper

**Files:**
- Create: `src/cli.py` (modify/add helper function)

- [ ] **Step 1: Write the failing test**

In `tests/test_cli.py` (create if not exists):

```python
from pathlib import Path
from cli import expand_input_pattern

def test_expand_input_pattern_glob():
    """Glob patterns with * should expand to matching files."""
    files = expand_input_pattern(Path("data/*.json"), Path("stac"))
    assert isinstance(files, list)
    assert all(f.suffix == ".json" for f in files)

def test_expand_input_pattern_single_file():
    """Non-glob path should return list with single file."""
    files = expand_input_pattern(Path("data/CTRY_PARK.json"), Path("stac"))
    assert files == [Path("data/CTRY_PARK.json")]

def test_expand_input_pattern_no_matches():
    """Glob with no matches should return empty list."""
    files = expand_input_pattern(Path("data/nonexistent*.json"), Path("stac"))
    assert files == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_cli.py::test_expand_input_pattern_glob -v`
Expected: FAIL with "NameError: name 'expand_input_pattern' not defined"

- [ ] **Step 3: Write minimal implementation**

Add to `src/cli.py`:

```python
from pathlib import Path
import glob as glob_module

def expand_input_pattern(input_path: Path, output_dir: Path) -> list[Path]:
    """
    Expand input path to list of matching file paths.

    If input_path contains '*', treat as glob pattern and expand.
    Otherwise, return single-element list.

    Args:
        input_path: File path or glob pattern
        output_dir: Output directory (unused, for API consistency)

    Returns:
        List of matching file paths
    """
    input_str = str(input_path)
    if '*' in input_str:
        matches = glob_module.glob(input_str, recursive=False)
        return [Path(m) for m in matches if Path(m).is_file()]
    return [input_path] if input_path.is_file() else []
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_cli.py::test_expand_input_pattern_glob tests/test_cli.py::test_expand_input_pattern_single_file tests/test_cli.py::test_expand_input_pattern_no_matches -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_cli.py src/cli.py
git commit -m "feat: add glob pattern detection helper"
```

---

## Task 2: Directory Input Expansion

**Files:**
- Modify: `src/cli.py` (add directory scanning function)

- [ ] **Step 1: Write the failing test**

In `tests/test_cli.py`:

```python
def test_expand_input_dir():
    """--input-dir should return all .json files in directory."""
    files = expand_input_dir(Path("data"), Path("stac"))
    assert isinstance(files, list)
    assert all(f.suffix == ".json" for f in files)
    assert all(f.is_relative_to(Path("data")) for f in files)

def test_expand_input_dir_empty():
    """Empty directory should return empty list."""
    files = expand_input_dir(Path("data/empty_dir"), Path("stac"))
    assert files == []

def test_expand_input_dir_non_json_skipped():
    """Non-.json files should be silently skipped."""
    files = expand_input_dir(Path("data"), Path("stac"))
    assert all(f.suffix == ".json" for f in files)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_cli.py::test_expand_input_dir -v`
Expected: FAIL with "NameError: name 'expand_input_dir' not defined"

- [ ] **Step 3: Write minimal implementation**

Add to `src/cli.py`:

```python
def expand_input_dir(input_dir: Path, output_dir: Path) -> list[Path]:
    """
    Get all .json files in a directory for batch conversion.

    Args:
        input_dir: Directory containing GeoJSON files
        output_dir: Output directory (unused, for API consistency)

    Returns:
        List of .json file paths in the directory
    """
    if not input_dir.is_dir():
        return []
    return sorted([f for f in input_dir.iterdir() if f.suffix == ".json" and f.is_file()])
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_cli.py::test_expand_input_dir tests/test_cli.py::test_expand_input_dir_empty tests/test_cli.py::test_expand_input_dir_non_json_skipped -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/cli.py tests/test_cli.py
git commit -m "feat: add directory scanning for batch convert"
```

---

## Task 3: CLI Mutual Exclusivity and Batch Main Function

**Files:**
- Modify: `src/cli.py` (restructure main function)

- [ ] **Step 1: Write the failing test**

In `tests/test_cli.py`:

```python
from typer.testing import CliRunner
from cli import app

runner = CliRunner()

def test_mutual_exclusivity_error():
    """Providing both input_file and --input-dir should error."""
    result = runner.invoke(app, ["data/CTRY_PARK.json", "--input-dir", "data/"])
    assert result.exit_code != 0
    assert "mutually exclusive" in result.output.lower() or "cannot use both" in result.output.lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_cli.py::test_mutual_exclusivity_error -v`
Expected: FAIL with "NameError: name 'app' not importable" or exit_code == 0 (test fails)

- [ ] **Step 3: Write minimal implementation**

Replace `src/cli.py` content with:

```python
"""CLI entry point for geojson2stac."""
import sys
import typer
from pathlib import Path
from typing import Annotated
from convertor import convert_file


app = typer.Typer(help="Convert GeoJSON FeatureCollections to STAC Collections and Items")


@app.command()
def main(
    input_file: Annotated[Path, typer.Argument(
        ..., exists=True, readable=True,
        help="Path to GeoJSON file or glob pattern (e.g., data/*.json)"
    )] = None,
    output_dir: Path = typer.Option(
        Path("stac"), "--output", "-o", help="Output directory (default: stac/)"
    ),
    input_dir: Annotated[Path, typer.Option(
        "--input-dir", help="Directory containing GeoJSON files to convert"
    )] = None,
    output_format: str = typer.Option("stac", "--output-format", help="Output format: stac or bulk"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
) -> None:
    """Convert GeoJSON files to STAC format."""
    # Handle mutual exclusivity
    if input_file is not None and input_dir is not None:
        print("Error: Cannot use both INPUT_FILE and --input-dir. They are mutually exclusive.", file=sys.stderr)
        raise typer.Exit(1)

    # Collect files to process
    if input_dir is not None:
        files = expand_input_dir(input_dir, output_dir)
        if not files:
            print(f"Warning: No .json files found in {input_dir}", file=sys.stderr)
            return
        mode = "directory"
    elif input_file is not None:
        input_str = str(input_file)
        if '*' in input_str:
            files = expand_input_pattern(input_file, output_dir)
            mode = "glob"
        else:
            files = [input_file]
            mode = "single"
    else:
        print("Error: Must provide INPUT_FILE or --input-dir", file=sys.stderr)
        raise typer.Exit(1)

    # Process files
    succeeded = 0
    failed = 0
    errors = []

    for file_path in files:
        try:
            if verbose:
                print(f"Converting: {file_path}")
            convert_file(file_path, output_dir, output_format=output_format)
            succeeded += 1
        except Exception as e:
            failed += 1
            errors.append((file_path, str(e)))
            if verbose:
                print(f"Error converting {file_path}: {e}", file=sys.stderr)

    # Summary output
    if mode in ("directory", "glob"):
        if failed > 0:
            print(f"\nBatch complete: {succeeded} succeeded, {failed} failed", file=sys.stderr)
            for path, err in errors:
                print(f"  - {path}: {err}", file=sys.stderr)
            raise typer.Exit(1)
        else:
            print(f"\nBatch complete: {succeeded} succeeded")


def expand_input_pattern(input_path: Path, output_dir: Path) -> list[Path]:
    """Expand glob pattern to list of matching file paths."""
    import glob as glob_module
    input_str = str(input_path)
    if '*' in input_str:
        matches = glob_module.glob(input_str, recursive=False)
        return [Path(m) for m in matches if Path(m).is_file()]
    return [input_path] if input_path.is_file() else []


def expand_input_dir(input_dir: Path, output_dir: Path) -> list[Path]:
    """Get all .json files in a directory for batch conversion."""
    if not input_dir.is_dir():
        return []
    return sorted([f for f in input_dir.iterdir() if f.suffix == ".json" and f.is_file()])


if __name__ == "__main__":
    app()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_cli.py::test_mutual_exclusivity_error -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/cli.py tests/test_cli.py
git commit -m "feat: restructure CLI with batch convert support"
```

---

## Task 4: Update README Documentation

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Read current README**

Run: `head -70 README.md` to see the CLI reference section

- [ ] **Step 2: Write the failing test**

In `tests/test_readme.py`:

```python
def test_readme_documents_input_dir_option():
    content = read_readme()
    assert "--input-dir" in content

def test_readme_documents_glob_pattern():
    content = read_readme()
    assert "*.json" in content or "glob" in content.lower()
```

- [ ] **Step 3: Run test to verify it fails**

Run: `pytest tests/test_readme.py::test_readme_documents_input_dir_option tests/test_readme.py::test_readme_documents_glob_pattern -v`
Expected: FAIL

- [ ] **Step 4: Update README with new CLI options**

Edit README.md CLI reference section to add:

```
## CLI Reference

```bash
geojson2stac INPUT_FILE [-o OUTPUT_DIR] [--output-format FORMAT] [-v]
geojson2stac --input-dir INPUT_DIR [-o OUTPUT_DIR] [--output-format FORMAT] [-v]
```

| Argument / Option | Description | Default |
| --- | --- | --- |
| `INPUT_FILE` | Path to GeoJSON file or glob pattern (e.g., `data/*.json`) | — |
| `--input-dir` | Directory containing GeoJSON files to convert | — |
| `-o`, `--output` | Output directory | `stac/` |
| `--output-format` | Output format: `stac` (default) or `bulk` | `stac` |
| `-v`, `--verbose` | Enable verbose output | `false` |

**Examples:**

```bash
# Convert all files in a directory
geojson2stac --input-dir data/

# Convert files matching glob pattern
geojson2stac "data/*.json"

# Custom output directory
geojson2stac data/CTRY_PARK.json -o ./output
```
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/test_readme.py::test_readme_documents_input_dir_option tests/test_readme.py::test_readme_documents_glob_pattern -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add README.md
git commit -m "docs: add batch convert options to README"
```

---

## Task 5: Integration Tests for Batch Behavior

**Files:**
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write the integration tests**

In `tests/test_cli.py`:

```python
import tempfile
import shutil
from pathlib import Path
from typer.testing import CliRunner
from cli import app

runner = CliRunner()

def test_batch_convert_directory(tmp_path):
    """--input-dir should convert all .json files in directory."""
    # Create test input files
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    stac_dir = tmp_path / "stac"

    # Copy actual sample data for testing
    sample = Path("data/CTRY_PARK.json")
    if sample.exists():
        (data_dir / "file1.json").write_bytes(sample.read_bytes())
        (data_dir / "file2.json").write_bytes(sample.read_bytes())

        result = runner.invoke(app, ["--input-dir", str(data_dir), "-o", str(stac_dir)])

        assert result.exit_code == 0
        assert (stac_dir / "file1").exists()
        assert (stac_dir / "file2").exists()
        assert (stac_dir / "file1" / "collection.json").exists()
        assert (stac_dir / "file2" / "collection.json").exists()

def test_batch_error_handling_continues(tmp_path):
    """If one file fails, processing continues and reports at end."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    stac_dir = tmp_path / "stac"

    # Create a corrupt file and a valid one
    (data_dir / "valid.json").write_text('{"type":"FeatureCollection","features":[]}')
    (data_dir / "invalid.json").write_text('not json')

    result = runner.invoke(app, ["--input-dir", str(data_dir), "-o", str(stac_dir)])

    # Should complete with non-zero exit and report failure
    assert result.exit_code != 0
    assert "1 succeeded, 1 failed" in result.output or "failed" in result.output.lower()
```

- [ ] **Step 2: Run tests to verify they fail (expected behavior for now)**

Run: `pytest tests/test_cli.py::test_batch_convert_directory tests/test_cli.py::test_batch_error_handling_continues -v`
Expected: May pass or fail depending on test data setup

- [ ] **Step 3: Commit if passing**

If tests pass, commit. If not, investigate and fix the test or implementation.

---

## Spec Coverage Check

| Spec Requirement | Task |
|---|---|
| Batch directory conversion (`--input-dir`) | Task 2, Task 3 |
| Glob pattern support | Task 1, Task 3 |
| Mutual exclusivity | Task 3 |
| Per-file error handling continue-on-error | Task 3 |
| Summary output (succeeded/failed) | Task 3 |
| README update | Task 4 |

**Plan complete and saved to `docs/superpowers/plans/2026-05-11-add-batch-convert.md`.**

**Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
