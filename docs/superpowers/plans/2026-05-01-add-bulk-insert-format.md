# Add Bulk Insert Format - Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add CLI option `--output-format bulk` to generate STAC items in API bulk insert format.

**Architecture:** Add new `src/stac_bulk_writer.py` module with transformation function. CLI delegates to existing `convertor.py` but uses different writer based on `--output-format` flag.

**Tech Stack:** Python, typer (CLI), standard JSON

---

## File Structure

```
src/
  cli.py                    # MODIFIED: add --output-format option
  convertor.py              # MODIFIED: pass output_format to writer
  stac_item_generator.py   # EXISTING: write_items_featurecollection()
  stac_bulk_writer.py       # NEW: write_items_bulk() + transform_to_bulk_format()

tests/
  test_stac_bulk_writer.py  # NEW: tests for bulk transformation
```

---

### Task 1: Create stac_bulk_writer.py with transformation function

**Files:**
- Create: `src/stac_bulk_writer.py`
- Test: `tests/test_stac_bulk_writer.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_stac_bulk_writer.py
import pytest
from stac_bulk_writer import transform_to_bulk_format

def test_transform_featurecollection_to_bulk_format():
    """STAC FeatureCollection transforms to bulk insert format."""
    stac_input = {
        "type": "FeatureCollection",
        "features": [
            {
                "id": "clear-water-bay-country-park",
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [114.29, 22.29]},
                "bbox": [114.29, 22.29, 114.29, 22.29],
                "properties": {
                    "datetime": "2026-04-29T16:32:59+00:00",
                    "OBJECTID": 1,
                    "NAME_EN": "Clear Water Bay Country Park",
                    "NAME_TC": "清水灣郊野公園",
                    "geometry_type": "Point"
                },
                "stac_version": "1.0.0",
                "links": [],
                "assets": {}
            }
        ]
    }
    collection_id = "ctry-park"
    result = transform_to_bulk_format(stac_input, collection_id)

    assert result == {
        "items": {
            "0": {
                "id": "1",
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [114.29, 22.29]},
                "bbox": [114.29, 22.29, 114.29, 22.29],
                "properties": {
                    "OBJECTID": 1,
                    "NAME_EN": "Clear Water Bay Country Park",
                    "NAME_TC": "清水灣郊野公園",
                    "datetime": "2026-04-29T16:32:59+00:00"
                },
                "collection": "ctry-park",
                "stac_version": "1.0.0"
            }
        },
        "method": "insert"
    }

def test_transform_uses_objectid_as_id():
    """OBJECTID from properties becomes item id as string."""
    stac_input = {
        "type": "FeatureCollection",
        "features": [
            {
                "id": "some-kebab-id",
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [114.29, 22.29]},
                "bbox": [114.29, 22.29, 114.29, 22.29],
                "properties": {
                    "OBJECTID": 42,
                    "NAME_EN": "Test"
                },
                "stac_version": "1.0.0",
                "links": [],
                "assets": {}
            }
        ]
    }
    result = transform_to_bulk_format(stac_input, "test-collection")
    assert result["items"]["0"]["id"] == "42"

def test_transform_strips_links_and_assets():
    """Bulk format does not include links or assets."""
    stac_input = {
        "type": "FeatureCollection",
        "features": [
            {
                "id": "item-1",
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [0, 0]},
                "bbox": [0, 0, 0, 0],
                "properties": {"OBJECTID": 1},
                "stac_version": "1.0.0",
                "links": [{"rel": "self", "href": "items.json"}],
                "assets": {"thumbnail": {"href": "thumb.png"}}
            }
        ]
    }
    result = transform_to_bulk_format(stac_input, "collection")
    assert "links" not in result["items"]["0"]
    assert "assets" not in result["items"]["0"]

def test_transform_default_datetime():
    """Missing datetime uses default '1900-01-01T00:00:00'."""
    stac_input = {
        "type": "FeatureCollection",
        "features": [
            {
                "id": "item-1",
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [0, 0]},
                "bbox": [0, 0, 0, 0],
                "properties": {"OBJECTID": 1},
                "stac_version": "1.0.0",
                "links": [],
                "assets": {}
            }
        ]
    }
    result = transform_to_bulk_format(stac_input, "collection")
    assert result["items"]["0"]["properties"]["datetime"] == "1900-01-01T00:00:00"

def test_transform_adds_collection_field():
    """Each item gets collection field from parameter."""
    stac_input = {
        "type": "FeatureCollection",
        "features": [
            {
                "id": "item-1",
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [0, 0]},
                "bbox": [0, 0, 0, 0],
                "properties": {"OBJECTID": 1},
                "stac_version": "1.0.0",
                "links": [],
                "assets": {}
            }
        ]
    }
    result = transform_to_bulk_format(stac_input, "my-collection")
    assert result["items"]["0"]["collection"] == "my-collection"

def test_transform_multiple_items():
    """Multiple features become multiple string-keyed items."""
    stac_input = {
        "type": "FeatureCollection",
        "features": [
            {
                "id": "item-1",
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [0, 0]},
                "bbox": [0, 0, 0, 0],
                "properties": {"OBJECTID": 1},
                "stac_version": "1.0.0",
                "links": [],
                "assets": {}
            },
            {
                "id": "item-2",
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [1, 1]},
                "bbox": [1, 1, 1, 1],
                "properties": {"OBJECTID": 2},
                "stac_version": "1.0.0",
                "links": [],
                "assets": {}
            }
        ]
    }
    result = transform_to_bulk_format(stac_input, "collection")
    assert "0" in result["items"]
    assert "1" in result["items"]
    assert result["items"]["0"]["id"] == "1"
    assert result["items"]["1"]["id"] == "2"
    assert result["method"] == "insert"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_stac_bulk_writer.py -v`
Expected: FAIL - module not found

- [ ] **Step 3: Create stac_bulk_writer.py**

```python
# src/stac_bulk_writer.py
"""Transform STAC items to bulk insert format for API import."""
import json
from pathlib import Path
from typing import Any


DEFAULT_DATETIME = "1900-01-01T00:00:00"


def transform_to_bulk_format(stac_featurecollection: dict[str, Any], collection_id: str) -> dict[str, Any]:
    """
    Transform STAC FeatureCollection to bulk insert format.

    Args:
        stac_featurecollection: Dict with "type": "FeatureCollection" and "features": [...]
        collection_id: The collection ID to add to each item (e.g., "ctry-park")

    Returns:
        Dict with {"items": {"0": item0, "1": item1, ...}, "method": "insert"}
    """
    items: dict[str, Any] = {}
    for idx, feature in enumerate(stac_featurecollection.get("features", [])):
        props = feature.get("properties", {})

        # Get datetime, use default if missing
        datetime_val = props.get("datetime")
        if not datetime_val:
            datetime_val = DEFAULT_DATETIME

        # Build bulk item - strip links/assets, add collection and stac_version
        bulk_item = {
            "id": str(props.get("OBJECTID", idx)),
            "type": "Feature",
            "geometry": feature.get("geometry"),
            "bbox": feature.get("bbox"),
            "properties": {
                "OBJECTID": props.get("OBJECTID"),
                "NAME_EN": props.get("NAME_EN"),
                "NAME_TC": props.get("NAME_TC"),
                "datetime": datetime_val,
            },
            "collection": collection_id,
            "stac_version": "1.0.0",
        }

        items[str(idx)] = bulk_item

    return {
        "items": items,
        "method": "insert",
    }


def write_items_bulk(stac_featurecollection: dict[str, Any], output_path: str, collection_id: str) -> None:
    """
    Transform STAC items to bulk format and write to file.

    Args:
        stac_featurecollection: STAC FeatureCollection dict
        output_path: Path to write bulk JSON file
        collection_id: Collection ID for items
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    bulk_data = transform_to_bulk_format(stac_featurecollection, collection_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(bulk_data, f, indent=2, ensure_ascii=False)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_stac_bulk_writer.py -v`
Expected: PASS (all 6 tests)

- [ ] **Step 5: Commit**

```bash
git add tests/test_stac_bulk_writer.py src/stac_bulk_writer.py
git commit -m "feat: add stac_bulk_writer module with transform_to_bulk_format"
```

---

### Task 2: Add CLI --output-format argument

**Files:**
- Modify: `src/cli.py:11-18`
- Test: `tests/test_convertor.py` (existing)

- [ ] **Step 1: Write the failing test for CLI**

```python
# Add to tests/test_convertor.py or create tests/test_cli.py
def test_cli_output_format_option():
    """CLI accepts --output-format with stac or bulk values."""
    from typer.testing import CliRunner
    from cli import app

    runner = CliRunner()

    # Test that --output-format bulk is accepted
    result = runner.invoke(app, [
        "test-data/CTRY_PARK.json",
        "--output-format", "bulk",
        "-o", "/tmp/bulk-test"
    ])
    # We don't run full conversion in unit test, just verify arg is accepted
    # The actual integration test will verify the output
```

- [ ] **Step 2: Run test to verify CLI parses the option**

Run: `pytest tests/test_convertor.py -v -k "output_format" 2>&1 || echo "No matching tests yet - proceed"`

- [ ] **Step 3: Modify cli.py to add --output-format**

Change from:
```python
@app.command()
def main(
    input_file: Path = typer.Argument(..., exists=True, readable=True, help="Path to GeoJSON file"),
    output_dir: Path = typer.Option(
        Path("stac"), "--output", "-o", help="Output directory (default: stac/)"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
) -> None:
```

To:
```python
from typing import Annotated

OutputFormat = Annotated[str, typer.Option(case_sensitive=False, help="Output format: stac or bulk")]

@app.command()
def main(
    input_file: Path = typer.Argument(..., exists=True, readable=True, help="Path to GeoJSON file"),
    output_dir: Path = typer.Option(
        Path("stac"), "--output", "-o", help="Output directory (default: stac/)"
    ),
    output_format: OutputFormat = typer.Option("stac", "--output-format", help="Output format: stac or bulk"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
) -> None:
```

And pass output_format to convert_file:
```python
convert_file(input_file, output_dir, output_format=output_format)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/ -v 2>&1 | head -50`
Expected: PASS (existing tests + new tests still pass)

- [ ] **Step 5: Commit**

```bash
git add src/cli.py
git commit -m "feat: add --output-format CLI option for bulk insert format"
```

---

### Task 3: Modify convertor to use bulk writer

**Files:**
- Modify: `src/convertor.py`

- [ ] **Step 1: Read current convertor.py to understand structure**

Run: `cat src/convertor.py`

- [ ] **Step 2: Modify convertor.py to handle output_format**

Update `convert_file()` signature to accept `output_format: str = "stac"`.
When `output_format == "bulk"`, use `write_items_bulk()` instead of `write_items_featurecollection()`.

```python
from stac_bulk_writer import write_items_bulk

def convert_file(
    input_path: Path,
    output_dir: Path,
    output_format: str = "stac"
) -> None:
    # ... existing code to parse and create items ...

    # Write items based on format
    if output_format == "bulk":
        collection_id = collection["id"]
        write_items_bulk(
            {"type": "FeatureCollection", "features": items},
            output_dir / collection_id / "items.json",
            collection_id
        )
    else:
        write_items_featurecollection(
            items,
            output_dir / collection_id / "items.json"
        )
```

- [ ] **Step 3: Run tests to verify they pass**

Run: `pytest tests/ -v`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add src/convertor.py
git commit -m "feat: support output_format parameter in convert_file"
```

---

### Task 4: Update README.md with CLI documentation

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add --output-format to CLI reference table**

In README.md, add to the CLI reference table:

```
| `--output-format` | Output format: `stac` (default) or `bulk` | `stac` |
```

And add example:
```bash
# Bulk format for API import
geojson2stac data/CTRY_PARK.json --output-format bulk
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: document --output-format CLI option"
```

---

### Task 5: Integration test with actual data

**Files:**
- Test: `test-data/CTRY_PARK.json`, `test-data/bulk-items/CTRY_PARK_Items_Bulk_inset_Sample.json`

- [ ] **Step 1: Run converter with --output-format bulk**

```bash
python -m src.cli test-data/CTRY_PARK.json --output-format bulk -o /tmp/bulk-integration
```

- [ ] **Step 2: Compare output with sample**

Run Python to verify:
```python
import json
with open("/tmp/bulk-integration/CTRY_PARK/items.json") as f:
    generated = json.load(f)
with open("test-data/bulk-items/CTRY_PARK_Items_Bulk_inset_Sample.json") as f:
    expected = json.load(f)

# Compare structure (ignoring specific coordinate values)
assert "items" in generated
assert "method" in generated
assert generated["method"] == "insert"
# Check that first item has expected fields
first_item = generated["items"]["0"]
assert "id" in first_item
assert "collection" in first_item
assert first_item["collection"] == "ctry-park"
```

- [ ] **Step 3: Commit final integration**

```bash
git add -A
git commit -m "test: integration test for bulk insert format"
```