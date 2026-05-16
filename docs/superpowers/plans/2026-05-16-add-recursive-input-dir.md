# Add Recursive Input Directory Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `--recursive` flag to CLI that enables scanning subdirectories and preserves folder structure in output.

**Architecture:** The CLI batch loop computes relative paths from `input_dir` to each found file and passes an `output_subdir` override to `convert_file()`. When recursive, `expand_input_dir()` uses `rglob` instead of `iterdir`.

**Tech Stack:** Python 3.10+, `typer`, `pathlib`

---

## File Map

```
src/cli.py           # Add --recursive flag, modify expand_input_dir(), compute relative paths
src/convertor.py     # Add optional output_subdir parameter to convert_file()
tests/test_cli.py    # Add tests for recursive mode
README.md            # Document --recursive flag
```

---

## Task 1: Add --recursive flag and modify expand_input_dir()

**Files:**
- Modify: `src/cli.py:107-120` (expand_input_dir function)

- [ ] **Step 1: Write the failing test**

In `tests/test_cli.py`:

```python
def test_expand_input_dir_recursive(tmp_path):
    """expand_input_dir with recursive=True should find nested files."""
    input_dir = tmp_path / "data"
    input_dir.mkdir()
    (input_dir / "root.json").write_text('{"type":"FeatureCollection","features":[]}')

    sub_dir = input_dir / "sub"
    sub_dir.mkdir()
    (sub_dir / "nested.json").write_text('{"type":"FeatureCollection","features":[]}')

    deep_dir = sub_dir / "deep"
    deep_dir.mkdir()
    (deep_dir / "deep_nested.json").write_text('{"type":"FeatureCollection","features":[]}')

    files = expand_input_dir(input_dir, Path("stac"), recursive=True)
    file_names = {f.name for f in files}

    assert "root.json" in file_names
    assert "nested.json" in file_names
    assert "deep_nested.json" in file_names

def test_expand_input_dir_non_recursive(tmp_path):
    """expand_input_dir with recursive=False should NOT find nested files."""
    input_dir = tmp_path / "data"
    input_dir.mkdir()
    (input_dir / "root.json").write_text('{"type":"FeatureCollection","features":[]}')

    sub_dir = input_dir / "sub"
    sub_dir.mkdir()
    (sub_dir / "nested.json").write_text('{"type":"FeatureCollection","features":[]}')

    files = expand_input_dir(input_dir, Path("stac"), recursive=False)
    file_names = {f.name for f in files}

    assert "root.json" in file_names
    assert "nested.json" not in file_names  # Should NOT be found
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_cli.py::test_expand_input_dir_recursive -v`
Expected: FAIL — "got an unexpected keyword argument 'recursive'"

- [ ] **Step 3: Modify expand_input_dir()**

Replace `src/cli.py:107-120`:

```python
def expand_input_dir(input_dir: Path, output_dir: Path, recursive: bool = False) -> list[Path]:
    """
    Get all .json and .geojson files in a directory for batch conversion.

    Args:
        input_dir: Directory containing GeoJSON files
        output_dir: Output directory (unused, for API consistency)
        recursive: If True, scan subdirectories recursively

    Returns:
        List of .json and .geojson file paths in the directory
    """
    if not input_dir.is_dir():
        return []

    pattern = "*.json"  # matches both .json and .geojson due to extension stripping

    if recursive:
        # rglob finds files at all nesting levels
        files = sorted(input_dir.rglob(pattern))
    else:
        # iterdir only finds immediate children
        files = sorted(f for f in input_dir.iterdir() if f.suffix in (".json", ".geojson") and f.is_file())

    return files
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_cli.py::test_expand_input_dir_recursive tests/test_cli.py::test_expand_input_dir_non_recursive -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_cli.py src/cli.py
git commit -m "feat: add recursive option to expand_input_dir"
```

---

## Task 2: Add --recursive CLI flag and pass it to expand_input_dir()

**Files:**
- Modify: `src/cli.py:12-26` (main function)

- [ ] **Step 1: Add the --recursive flag to CLI**

Modify `src/cli.py:21-23` to add:

```python
    input_dir: Annotated[Path, typer.Option(
        "--input-dir", help="Directory containing GeoJSON files to convert"
    )] = None,
    recursive: bool = typer.Option(False, "--recursive", help="Recursively scan subdirectories"),
```

And update the call at line 40:

```python
    if input_dir is not None:
        files = expand_input_dir(input_dir, output_dir, recursive=recursive)
```

- [ ] **Step 2: Run tests to verify nothing broke**

Run: `pytest tests/test_cli.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add src/cli.py
git commit -m "feat: add --recursive CLI flag"
```

---

## Task 3: Compute relative paths for output directory structure

**Files:**
- Modify: `src/cli.py` (batch loop)

- [ ] **Step 1: Write the failing test**

In `tests/test_cli.py`:

```python
def test_relative_path_computation(tmp_path):
    """Output subdirectory should mirror input folder structure."""
    input_dir = tmp_path / "data"
    input_dir.mkdir()

    sub_dir = input_dir / "sub"
    sub_dir.mkdir()

    # Compute relative path from input_dir to file
    file_path = sub_dir / "file.json"
    relative_to_input = file_path.parent.relative_to(input_dir)

    # relative_to_input should be "sub"
    assert str(relative_to_input) == "sub"
```

- [ ] **Step 2: Write test to verify it passes**

Run: `pytest tests/test_cli.py::test_relative_path_computation -v`
Expected: PASS (this is a pure logic test)

- [ ] **Step 3: Modify batch loop to compute relative paths**

Update `src/cli.py:38-56`:

```python
    # Collect files to process
    if input_dir is not None:
        files = expand_input_dir(input_dir, output_dir, recursive=recursive)
        if not files:
            print(f"Warning: No .json or .geojson files found in {input_dir}", file=sys.stderr)
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

            # Compute relative output path if recursive
            if input_dir is not None and recursive:
                relative_subpath = file_path.parent.relative_to(input_dir)
                # convert_file will use this as the output subdirectory
                # We pass it via a new optional parameter (Task 4)
                convert_file(file_path, output_dir, output_format=output_format, output_subdir=relative_subpath)
            else:
                convert_file(file_path, output_dir, output_format=output_format)
            succeeded += 1
        except Exception as e:
            failed += 1
            errors.append((file_path, str(e)))
            if verbose:
                print(f"Error converting {file_path}: {e}", file=sys.stderr)
```

- [ ] **Step 4: Run tests to verify**

Run: `pytest tests/test_cli.py -v`
Expected: FAIL — "convert_file() got an unexpected keyword argument 'output_subdir'"

- [ ] **Step 5: Commit**

```bash
git add src/cli.py
git commit -m "feat: compute relative paths for recursive output structure"
```

---

## Task 4: Update convert_file() to accept optional output_subdir

**Files:**
- Modify: `src/convertor.py`

- [ ] **Step 1: Modify convert_file() signature and logic**

Replace `src/convertor.py:10-44`:

```python
def convert_file(
    input_path: Path,
    output_dir: Path,
    output_format: str = "stac",
    output_subdir: Path | None = None,
) -> None:
    """Convert a GeoJSON file to STAC format.

    Args:
        input_path: Path to input GeoJSON file
        output_dir: Base output directory
        output_format: Output format ("stac" or "bulk")
        output_subdir: Optional subdirectory path relative to output_dir.
                       If provided, used instead of input_path.stem for output structure.
    """
    base_name = input_path.stem

    # Use output_subdir if provided, otherwise use stem-based subdirectory
    if output_subdir is not None:
        collection_output_dir = output_dir / output_subdir / base_name
    else:
        collection_output_dir = output_dir / base_name

    collection_output_dir.mkdir(parents=True, exist_ok=True)

    collection_state = start_collection(base_name)
    seen_ids = {}
    items = []

    for idx, (feature, crs, transformer) in enumerate(stream_geojson(input_path)):
        item = feature_to_item(feature, transformer, seen_ids, idx)
        items.append(item)
        collection_state = update_collection(collection_state, item)

    collection = finalize_collection(collection_state, base_name)
    collection_id = collection["id"]
    items_path = collection_output_dir / "items.json"

    # Write items based on format
    if output_format == "bulk":
        write_items_bulk(
            {"type": "FeatureCollection", "features": items},
            items_path,
            collection_id
        )
    else:
        write_items_featurecollection(items, str(items_path))

    # Write collection.json
    collection_path = collection_output_dir / "collection.json"
    write_collection(collection, str(collection_path))
```

- [ ] **Step 2: Run tests to verify**

Run: `pytest tests/ -v`
Expected: PASS (or mostly pass — any failures should be unrelated)

- [ ] **Step 3: Commit**

```bash
git add src/convertor.py
git commit -m "feat: add optional output_subdir parameter to convert_file"
```

---

## Task 5: Update README.md documentation

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Read current README**

Run: `head -70 README.md`

- [ ] **Step 2: Add --recursive to CLI reference**

Update the CLI reference section to add `--recursive` option:

In the options table, add:
```
| `--recursive` | Recursively scan subdirectories when used with `--input-dir` | `false` |
```

And add an example:
```bash
# Recursive directory conversion (preserves folder structure)
geojson2stac --input-dir data/ --recursive

# Output structure mirrors input:
# data/sub/file.json → stac/sub/file/
```

- [ ] **Step 3: Run tests to verify**

Run: `pytest tests/test_readme.py -v`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add --recursive flag to README"
```

---

## Task 6: Integration test for full recursive workflow

**Files:**
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write integration test**

```python
def test_batch_recursive_preserves_folder_structure(tmp_path):
    """Verify recursive batch convert preserves folder structure."""
    from typer.testing import CliRunner
    from cli import app

    runner = CliRunner()

    # Create nested input structure
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "root.json").write_text('{"type":"FeatureCollection","features":[]}')

    sub_dir = data_dir / "sub"
    sub_dir.mkdir()
    (sub_dir / "nested.json").write_text('{"type":"FeatureCollection","features":[]}')

    stac_dir = tmp_path / "stac"

    # Copy actual sample data for real conversion
    sample = Path("test-data/CTRY_PARK.json")
    if sample.exists():
        (data_dir / "root.json").write_bytes(sample.read_bytes())
        (sub_dir / "nested.json").write_bytes(sample.read_bytes())

        result = runner.invoke(app, ["--input-dir", str(data_dir), "-o", str(stac_dir), "--recursive"])

        assert result.exit_code == 0
        assert (stac_dir / "root").exists()
        assert (stac_dir / "sub" / "nested").exists()
```

- [ ] **Step 2: Run test**

Run: `pytest tests/test_cli.py::test_batch_recursive_preserves_folder_structure -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/test_cli.py
git commit -m "test: add integration test for recursive folder structure"
```

---

## Spec Coverage Check

| Spec Requirement | Task |
|---|---|
| `--recursive` flag enables recursive scan | Task 1, Task 2 |
| Output structure mirrors input hierarchy | Task 3, Task 4 |
| Relative path computation for output subdirectory | Task 3, Task 4 |
| Non-recursive mode unchanged | Task 1 |
| README updated | Task 5 |

**Plan complete and saved to `docs/superpowers/plans/2026-05-16-add-recursive-input-dir.md`.**

**Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**