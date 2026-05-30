# Add Inter-File Parallelism Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `--workers` CLI flag to enable parallel batch conversion of multiple GeoJSON files using ThreadPoolExecutor.

**Architecture:** Refactor the sequential `for file_path in files:` loop into a ThreadPoolExecutor-based parallel loop. Each file conversion is independent — no shared state. Use `concurrent.futures.as_completed()` for thread-safe error collection and progress reporting.

**Tech Stack:** Python 3.10+, `typer`, `concurrent.futures` (stdlib), `pathlib`

---

## File Map

```
src/cli.py           # Add --workers flag, refactor batch loop to use ThreadPoolExecutor
README.md            # Document --workers flag
tests/test_cli.py    # Add tests for parallel batch processing
```

---

## Task 1: Add `--workers` CLI flag

**Files:**
- Modify: `src/cli.py:25-26` (main function signature)

- [ ] **Step 1: Add the --workers option**

In `src/cli.py`, add after line 25 (`recursive: bool = typer.Option(...)`):

```python
workers: int = typer.Option(
    1,
    "--workers",
    "-w",
    help="Number of parallel workers for batch conversion (default: 1, sequential)"
),
```

- [ ] **Step 2: Verify tests still pass**

Run: `pytest tests/test_cli.py -v`
Expected: PASS (no behavior change yet)

- [ ] **Step 3: Commit**

```bash
git add src/cli.py
git commit -m "feat: add --workers CLI option"
```

---

## Task 2: Refactor batch loop to use ThreadPoolExecutor

**Files:**
- Modify: `src/cli.py:58-90` (batch processing section)

- [ ] **Step 1: Write the failing test**

In `tests/test_cli.py`, add:

```python
def test_batch_convert_with_workers_sequential(tmp_path):
    """--workers 1 should behave identically to sequential processing."""
    from typer.testing import CliRunner
    from cli import app

    runner = CliRunner()

    data_dir = tmp_path / "data"
    data_dir.mkdir()
    stac_dir = tmp_path / "stac"

    sample = Path("test-data/CTRY_PARK.json")
    if sample.exists():
        (data_dir / "file1.json").write_bytes(sample.read_bytes())
        (data_dir / "file2.json").write_bytes(sample.read_bytes())

        # Run with --workers 1
        result = runner.invoke(app, [
            "--input-dir", str(data_dir),
            "-o", str(stac_dir),
            "--workers", "1"
        ])

        assert result.exit_code == 0
        assert (stac_dir / "file1").exists()
        assert (stac_dir / "file2").exists()


def test_batch_convert_with_workers_parallel(tmp_path):
    """--workers 2 should process files in parallel."""
    from typer.testing import CliRunner
    from cli import app

    runner = CliRunner()

    data_dir = tmp_path / "data"
    data_dir.mkdir()
    stac_dir = tmp_path / "stac"

    sample = Path("test-data/CTRY_PARK.json")
    if sample.exists():
        (data_dir / "file1.json").write_bytes(sample.read_bytes())
        (data_dir / "file2.json").write_bytes(sample.read_bytes())

        result = runner.invoke(app, [
            "--input-dir", str(data_dir),
            "-o", str(stac_dir),
            "--workers", "2"
        ])

        assert result.exit_code == 0
        assert (stac_dir / "file1").exists()
        assert (stac_dir / "file2").exists()
        assert (stac_dir / "file1" / "collection.json").exists()
        assert (stac_dir / "file2" / "collection.json").exists()


def test_batch_convert_error_handling_parallel(tmp_path):
    """Errors in parallel workers should be collected and reported."""
    from typer.testing import CliRunner
    from cli import app

    runner = CliRunner()

    data_dir = tmp_path / "data"
    data_dir.mkdir()
    stac_dir = tmp_path / "stac"

    # One valid file, one corrupt
    sample = Path("test-data/CTRY_PARK.json")
    if sample.exists():
        (data_dir / "valid.json").write_bytes(sample.read_bytes())
        (data_dir / "invalid.json").write_text("not json")

        result = runner.invoke(app, [
            "--input-dir", str(data_dir),
            "-o", str(stac_dir),
            "--workers", "2"
        ])

        # Should fail with error summary
        assert result.exit_code != 0
        assert "1 succeeded, 1 failed" in result.output
```

- [ ] **Step 2: Run tests — expect failures**

Run: `pytest tests/test_cli.py::test_batch_convert_with_workers_sequential tests/test_cli.py::test_batch_convert_with_workers_parallel tests/test_cli.py::test_batch_convert_error_handling_parallel -v`
Expected: FAIL — workers not implemented yet

- [ ] **Step 3: Refactor batch loop**

Replace `src/cli.py:58-90` with:

```python
# Process files
from concurrent.futures import ThreadPoolExecutor, as_completed

def convert_one(file_path: Path, input_dir: Path | None, output_dir: Path,
               output_format: str, recursive: bool, verbose: bool) -> tuple[Path, bool, str | None]:
    """Convert a single file. Returns (path, success, error_message)."""
    try:
        if verbose:
            print(f"Converting: {file_path}")

        if input_dir is not None and recursive:
            relative_subpath = file_path.parent.relative_to(input_dir)
            convert_file(file_path, output_dir, output_format=output_format, output_subdir=relative_subpath)
        else:
            convert_file(file_path, output_dir, output_format=output_format)
        return (file_path, True, None)
    except Exception as e:
        return (file_path, False, str(e))

succeeded = 0
failed = 0
errors = []

if workers == 1:
    # Sequential processing (original behavior)
    for file_path in files:
        path, ok, err = convert_one(file_path, input_dir, output_dir, output_format, recursive, verbose)
        if ok:
            succeeded += 1
        else:
            failed += 1
            errors.append((path, err))
else:
    # Parallel processing
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(convert_one, fp, input_dir, output_dir, output_format, recursive, verbose): fp
            for fp in files
        }
        for future in as_completed(futures):
            path, ok, err = future.result()
            if ok:
                succeeded += 1
            else:
                failed += 1
                errors.append((path, err))

# Summary output
if mode in ("directory", "glob"):
    if failed > 0:
        print(f"\nBatch complete: {succeeded} succeeded, {failed} failed", file=sys.stderr)
        for path, err in errors:
            print(f"  - {path}: {err}", file=sys.stderr)
        raise typer.Exit(1)
    else:
        print(f"\nBatch complete: {succeeded} succeeded")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_cli.py::test_batch_convert_with_workers_sequential tests/test_cli.py::test_batch_convert_with_workers_parallel tests/test_cli.py::test_batch_convert_error_handling_parallel -v`
Expected: PASS

- [ ] **Step 5: Run all tests**

Run: `pytest tests/test_cli.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/cli.py
git commit -m "feat: parallel batch processing with ThreadPoolExecutor"
```

---

## Task 3: Update README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add --workers to CLI reference**

Add to the options table:
```
| `--workers`, `-w` | Number of parallel workers for batch conversion (default: 1) | `1` |
```

Add example:
```bash
# Parallel batch conversion (4 workers)
geojson2stac --input-dir data/ --recursive --workers 4
```

- [ ] **Step 2: Run README tests**

Run: `pytest tests/test_readme.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add --workers flag to README"
```

---

## Spec Coverage Check

| Spec Requirement | Task |
|---|---|
| Workers CLI option | Task 1 |
| Workers defaults to 1 | Task 1, Task 2 |
| Parallel batch processing | Task 2 |
| Thread-safe error handling | Task 2 |
| Backward compatibility | Task 2 |
| README updated | Task 3 |

**Plan complete and saved to `docs/superpowers/plans/2026-05-30-add-inter-file-parallelism.md`.**

**Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
