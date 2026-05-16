# Reuse PyProj Transformer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create one `pyproj.Transformer` per file instead of one per coordinate, reducing large-file conversion time from minutes to seconds.

**Architecture:** The `Transformer` is created once in `stream_geojson()` and passed through the call chain to `transform_geometry()`. The `transform_point` function is eliminated by inlining its logic directly into `transform_geometry` to avoid function-call overhead.

**Tech Stack:** Python, `pyproj`, `ijson` (for streaming)

---

## File Map

```
src/geojson_parser.py    # stream_geojson() now yields (feature, crs, transformer)
src/convertor.py         # Unpack transformer, pass to feature_to_item()
src/stac_item_generator.py  # feature_to_item() accepts transformer, passes to transform_geometry()
src/crs_transformer.py   # transform_geometry() accepts transformer instead of CRS string
tests/test_crs_transformer.py  # Update tests for new signatures
```

---

## Task 1: Update `stream_geojson()` to create and yield Transformer

**Files:**
- Modify: `src/geojson_parser.py:75-93`
- Test: `tests/test_geojson_parser.py`

- [ ] **Step 1: Write the failing test**

In `tests/test_geojson_parser.py`:

```python
from pathlib import Path
from pyproj import Transformer
from geojson_parser import stream_geojson

def test_stream_geojson_yields_three_values():
    """stream_geojson should yield (feature, crs, transformer) tuples."""
    path = Path("test-data/CTRY_PARK.json")
    for feature, crs, transformer in stream_geojson(path):
        assert isinstance(feature, dict)
        assert isinstance(crs, str)
        assert isinstance(transformer, Transformer)
        break  # Only check first item

def test_transformer_is_reused():
    """The same transformer instance should be used for all features."""
    path = Path("test-data/CTRY_PARK.json")
    transformers = []
    for feature, crs, transformer in stream_geojson(path):
        transformers.append(transformer)
    # All transformers should be the same instance
    assert len(set(id(t) for t in transformers)) == 1, "Transformer should be reused"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_geojson_parser.py::test_stream_geojson_yields_three_values -v`
Expected: FAIL — "not enough values to unpack"

- [ ] **Step 3: Update `stream_geojson()` implementation**

Modify `src/geojson_parser.py:75-93`:

```python
def stream_geojson(path: Path) -> Any:
    """Stream features, CRS, and Transformer from a GeoJSON file.

    Yields:
        Tuple of (feature, crs, transformer) where crs is the EPSG string
        and transformer is a reusable pyproj.Transformer instance.
    """
    crs = "EPSG:4326"
    transformer = None

    with open(path, "rb") as f:
        # First pass: extract crs from the root object and create Transformer
        for prefix, event, value in ijson.parse(f):
            if prefix == "crs.properties.name" and event == "string":
                if value.startswith("EPSG:"):
                    crs = value
                    break

    # Create Transformer once with the detected CRS
    transformer = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)

    # Reset file and stream features
    with open(path, "rb") as f:
        parser = ijson.items(f, "features.item")
        for feature in parser:
            yield feature, crs, transformer
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_geojson_parser.py::test_stream_geojson_yields_three_values tests/test_geojson_parser.py::test_transformer_is_reused -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_geojson_parser.py src/geojson_parser.py
git commit -m "feat: stream_geojson yields transformer for reuse"
```

---

## Task 2: Update `convert_file()` to unpack and pass Transformer

**Files:**
- Modify: `src/convertor.py:23-26`
- Test: `tests/test_convertor.py` (existing tests should still pass)

- [ ] **Step 1: Write the failing test (if needed)**

The existing tests in `test_convertor.py` should catch a broken integration. No new test needed — verify existing tests fail first.

Run: `pytest tests/test_convertor.py -v`
Expected: FAIL — "not enough values to unpack"

- [ ] **Step 2: Update `convert_file()` implementation**

Modify `src/convertor.py:19-27`:

```python
    collection_state = start_collection(base_name)
    seen_ids = {}
    items = []

    for idx, (feature, crs, transformer) in enumerate(stream_geojson(input_path)):
        item = feature_to_item(feature, transformer, seen_ids, idx)
        items.append(item)
        collection_state = update_collection(collection_state, item)
```

- [ ] **Step 3: Run tests to verify they pass**

Run: `pytest tests/test_convertor.py -v`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add src/convertor.py
git commit -m "feat: convert_file unpacks and passes transformer"
```

---

## Task 3: Update `feature_to_item()` to accept and pass Transformer

**Files:**
- Modify: `src/stac_item_generator.py:42-98`
- Test: Existing tests in `test_stac_item_generator.py`

- [ ] **Step 1: Write the failing test**

Run: `pytest tests/test_stac_item_generator.py -v`
Expected: FAIL — "transform_geometry() missing required argument: 'transformer'"

- [ ] **Step 2: Update `feature_to_item()` signature and call**

Modify `src/stac_item_generator.py:42-68`:

```python
def feature_to_item(
    feature: dict[str, Any],
    transformer: Transformer,
    seen_ids: dict[str, int] | None = None,
    index: int | None = None,
) -> dict[str, Any]:
    if seen_ids is None:
        seen_ids = {}

    props = feature.get("properties", {})
    item_id = generate_item_id(feature, index)

    # Handle duplicate IDs inline
    if item_id in seen_ids:
        seen_ids[item_id] += 1
        item_id = f"{item_id}-{seen_ids[item_id]}"
        seen_ids[item_id] = 0
    else:
        seen_ids[item_id] = 0

    geom = feature.get("geometry")
    if not geom:
        geom = {"type": "Point", "coordinates": []}
    geom_type = geom.get("type", "Unknown")
    transformed_geom = transform_geometry(geom, transformer)  # Pass transformer, not CRS
    bbox = calculate_bbox(transformed_geom["coordinates"])
```

- [ ] **Step 3: Run tests to verify they pass**

Run: `pytest tests/test_stac_item_generator.py -v`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add src/stac_item_generator.py
git commit -m "feat: feature_to_item accepts transformer instead of crs string"
```

---

## Task 4: Update `transform_geometry()` to accept Transformer and inline transform logic

**Files:**
- Modify: `src/crs_transformer.py:13-79`
- Test: `tests/test_crs_transformer.py`

- [ ] **Step 1: Write the failing test**

Run: `pytest tests/test_crs_transformer.py -v`
Expected: FAIL — "Transformer.from_crs() missing required argument: 'transform_crs'"

- [ ] **Step 2: Update `transform_geometry()` with inlined transform logic**

Replace `src/crs_transformer.py:13-79` with:

```python
def transform_geometry(geometry: dict[str, Any], transformer: Transformer) -> dict[str, Any]:
    """Transform all coordinates in a GeoJSON geometry to WGS84 using the provided Transformer."""
    geom_type = geometry["type"]
    coords = geometry["coordinates"]

    if geom_type == "Point":
        lon, lat = transformer.transform(coords[0], coords[1])
        return {"type": "Point", "coordinates": [float(lon), float(lat)]}

    elif geom_type == "LineString":
        return {
            "type": "LineString",
            "coordinates": [
                [float(lon), float(lat)] for lon, lat in transformer.transform.coords(coords)
            ],
        }

    elif geom_type == "Polygon":
        return {
            "type": "Polygon",
            "coordinates": [
                [
                    [float(lon), float(lat)] for lon, lat in transformer.transform.coords(ring)
                ]
                for ring in coords
            ],
        }

    elif geom_type == "MultiPoint":
        return {
            "type": "MultiPoint",
            "coordinates": [
                [float(lon), float(lat)] for lon, lat in transformer.transform.coords(coords)
            ],
        }

    elif geom_type == "MultiLineString":
        return {
            "type": "MultiLineString",
            "coordinates": [
                [
                    [float(lon), float(lat)] for lon, lat in transformer.transform.coords(line)
                ]
                for line in coords
            ],
        }

    elif geom_type == "MultiPolygon":
        return {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [
                        [float(lon), float(lat)] for lon, lat in transformer.transform.coords(ring)
                    ]
                    for ring in poly
                ]
                for poly in coords
            ],
        }

    else:
        raise ValueError(f"Unknown geometry type: {geom_type}")
```

- [ ] **Step 3: Run tests to verify they pass**

Run: `pytest tests/test_crs_transformer.py -v`
Expected: PASS

Note: The tests in `test_crs_transformer.py` call `transform_geometry(geom, "EPSG:2326")` with a string, not a Transformer. You need to update the tests too. See Task 5.

- [ ] **Step 4: Commit**

```bash
git add src/crs_transformer.py
git commit -m "feat: transform_geometry accepts Transformer and inlines transform logic"
```

---

## Task 5: Update `test_crs_transformer.py` for new signature

**Files:**
- Modify: `tests/test_crs_transformer.py`

- [ ] **Step 1: Update test file to use Transformer instead of CRS string**

Replace `tests/test_crs_transformer.py` content:

```python
import pytest
from pyproj import Transformer
from crs_transformer import (
    transform_geometry,
    calculate_bbox,
)


class TestTransformGeometry:
    @pytest.fixture
    def transformer_2326(self):
        return Transformer.from_crs("EPSG:2326", "EPSG:4326", always_xy=True)

    def test_transform_point_geometry(self, transformer_2326):
        geom = {"type": "Point", "coordinates": [848550, 817395]}
        result = transform_geometry(geom, transformer_2326)
        assert result["type"] == "Point"
        assert len(result["coordinates"]) == 2
        assert 114.2 < result["coordinates"][0] < 114.4

    def test_transform_linestring_geometry(self, transformer_2326):
        geom = {
            "type": "LineString",
            "coordinates": [[848550, 817395], [848560, 817400]],
        }
        result = transform_geometry(geom, transformer_2326)
        assert result["type"] == "LineString"
        assert len(result["coordinates"]) == 2
        assert 114.2 < result["coordinates"][0][0] < 114.4

    def test_transform_polygon_geometry(self, transformer_2326):
        geom = {
            "type": "Polygon",
            "coordinates": [[[848550, 817395], [848560, 817400], [848550, 817395]]],
        }
        result = transform_geometry(geom, transformer_2326)
        assert result["type"] == "Polygon"
        assert len(result["coordinates"]) == 1
        assert len(result["coordinates"][0]) == 3

    def test_transform_multipoint_geometry(self, transformer_2326):
        geom = {
            "type": "MultiPoint",
            "coordinates": [[848550, 817395], [848560, 817400]],
        }
        result = transform_geometry(geom, transformer_2326)
        assert result["type"] == "MultiPoint"
        assert len(result["coordinates"]) == 2


class TestCalculateBBox:
    def test_bbox_point(self):
        coords = [114.26, 22.31]
        bbox = calculate_bbox(coords)
        assert bbox == [114.26, 22.31, 114.26, 22.31]

    def test_bbox_polygon(self):
        coords = [
            [[114.2, 22.3], [114.3, 22.3], [114.3, 22.4], [114.2, 22.4], [114.2, 22.3]],
            [[114.25, 22.35], [114.26, 22.35], [114.26, 22.36], [114.25, 22.36], [114.25, 22.35]],
        ]
        bbox = calculate_bbox(coords)
        assert bbox[0] == pytest.approx(114.2, abs=0.01)
        assert bbox[1] == pytest.approx(22.3, abs=0.01)
        assert bbox[2] == pytest.approx(114.3, abs=0.01)
        assert bbox[3] == pytest.approx(114.4, abs=0.01)
```

- [ ] **Step 2: Run tests to verify they pass**

Run: `pytest tests/test_crs_transformer.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/test_crs_transformer.py
git commit -m "test: update crs_transformer tests for new Transformer-based signature"
```

---

## Task 6: Full integration test and performance verification

**Files:**
- None (verification only)

- [ ] **Step 1: Run full test suite**

Run: `pytest -v`
Expected: ALL TESTS PASS

- [ ] **Step 2: Time a large file conversion (optional verification)**

If a large sample file exists:
```bash
time geojson2stac data/FinalisedHabitatMap_shapefile_Woody_shrubland_converted.geojson -o stac_perf/
```

Before: Expect ~50ms × number_of_features overhead
After: Expect ~0.1-1s total

- [ ] **Step 3: Verify output is identical**

Compare output before and after by converting same file twice:
```bash
# Convert with old (if you kept a backup) vs new
# Diff the stac directories
diff -r stac_old/ stac_new/
```

---

## Spec Coverage Check

| Spec Requirement | Task |
|---|---|
| Single Transformer per file | Task 1 |
| Transformer reused for all features | Task 1 |
| Coordinate accuracy unchanged | Tasks 4, 5 |
| MultiPolygon transformation | Tasks 4, 5 |
| All existing tests pass | Tasks 2, 3, 6 |

**Plan complete and saved to `docs/superpowers/plans/2026-05-16-reuse-pyproj-transformer.md`.**

**Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**