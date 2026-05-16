## Context

The current implementation of `transform_point()` in `crs_transformer.py` creates a new `pyproj.Transformer` instance for every coordinate transformation:

```python
def transform_point(x: float, y: float, from_crs: str) -> tuple[float, float]:
    transformer = Transformer.from_crs(from_crs, "EPSG:4326", always_xy=True)
    lon, lat = transformer.transform(x, y)
    return float(lon), float(lat)
```

This is called from `transform_geometry()`, which is called from `feature_to_item()` for every feature. Creating a `Transformer` is expensive (~50ms), making large file conversion prohibitively slow.

## Goals / Non-Goals

**Goals:**
- Reduce conversion time for large GeoJSON files by reusing a single `Transformer` instance per file
- Maintain identical output (coordinates, bbox, geometry type)
- No changes to CLI, public function signatures (except where necessary for the optimization)

**Non-Goals:**
- Parallel processing (out of scope)
- Caching transformer across multiple files (single-file reuse is sufficient)
- Supporting multiple output CRS (WGS84 only for now)

## Decisions

**1. Create `Transformer` once in `stream_geojson`**

The `stream_geojson` function is the entry point that reads the file and yields `(feature, crs)` tuples. We modify it to also yield the `Transformer`, so each iteration yields `(feature, crs, transformer)`.

Rationale: `stream_geojson` is where the CRS is first read from the file. Creating the `Transformer` here keeps the change localized to the parsing layer. Alternatives like creating it in `convert_file()` or passing it as a parameter are equivalent, but `stream_geojson` is the cleanest origin point since it's already reading the file.

**2. Pass `Transformer` through the call chain**

```
stream_geojson → convert_file → feature_to_item → transform_geometry → transform_point
```

The `Transformer` is passed as an additional parameter through these functions. The signatures change but the semantics remain the same.

**3. Inline `transform_point` into `transform_geometry`**

For performance, `transform_point` logic is inlined directly into `transform_geometry` to avoid function call overhead on every coordinate. This is a micro-optimization but meaningful when transforming thousands of coordinates.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Transformer is not thread-safe | N/A — sequential processing only |
| CRS change mid-file | CRS is read once at start; all features use same CRS |
| Memory use | Transformer is small (~few KB); holding one per file is negligible |

## Open Questions

None — the implementation is straightforward.