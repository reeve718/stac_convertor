## Context

The `stream_geojson()` function in `src/geojson_parser.py` currently reads each GeoJSON file twice:

1. **First pass**: `ijson.parse()` iterates the entire file to find `crs.properties.name` at the root level
2. **Second pass**: `ijson.items()` iterates the entire file again to stream features

For large files (hundreds of MB), this doubles I/O time. The CRS is a root-level property in GeoJSON FeatureCollections and is always near the start of the file — reading the entire file to find it is wasteful.

## Goals / Non-Goals

**Goals:**
- Eliminate the second full file read in `stream_geojson()`
- Maintain current behavior for CRS detection and feature streaming
- Handle edge cases gracefully with fallback to WGS84

**Non-Goals:**
- Adding parallel/concurrent processing (separate optimization)
- Supporting non-standard CRS locations (e.g., inside features)
- Changing the output format or STAC structure

## Decisions

**1. Bounded prefix read for CRS detection**

Read only the first 4KB of the file to extract CRS. The GeoJSON spec places `crs` at the root level alongside `type`, `name`, and `features` — it is always within the first few kilobytes of a valid file.

```python
def detect_crs_quick(path: Path) -> str:
    with open(path, "rb") as f:
        prefix = f.read(4096)
    try:
        obj = json.loads(prefix)
        if obj.get("crs", {}).get("type") == "name":
            name = obj["crs"]["properties"]["name"]
            if name.startswith("EPSG:"):
                return name
    except json.JSONDecodeError:
        pass  # Partial JSON at boundary - fall through
    return "EPSG:4326"
```

**Alternatives considered:**
- Read in chunks until `features` prefix detected — more complex, ijson isn't designed for this
- Single ijson pass yielding both CRS and features — requires significant API restructuring

**2. Single file handle, sequential streaming**

After detecting CRS from the prefix, re-open the file and stream features using the existing `ijson.items()` approach. This maintains the streaming architecture (memory-efficient for large files) while eliminating the redundant CRS scan.

**3. Graceful fallback**

If CRS cannot be detected from the prefix (malformed JSON at boundary, or CRS stored unusually), default to WGS84. This matches the existing fallback behavior when no CRS is found at all.

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| CRS property beyond 4KB | Unlikely per GeoJSON spec — CRS is root-level; fallback to WGS84 covers this |
| Partial JSON at 4KB boundary | `json.JSONDecodeError` caught, falls through to default CRS |
| Performance gain smaller than expected | I/O is halved for large files; CPU parsing remains similar |

## Open Questions

None — the approach is straightforward.
