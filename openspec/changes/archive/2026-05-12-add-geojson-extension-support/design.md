## Context

The `expand_input_dir()` function in `src/cli.py` currently filters files by extension using `f.suffix == ".json"`. This excludes `.geojson` files from batch directory conversion, even though both formats contain valid GeoJSON data.

## Goals / Non-Goals

**Goals:**
- Support `.geojson` extension in `--input-dir` batch mode alongside `.json`

**Non-Goals:**
- No changes to single-file or glob pattern input modes (already work with `.geojson`)
- No validation of file content — files with `.geojson` extension are assumed to be valid GeoJSON

## Decisions

### Change `f.suffix == ".json"` to check for both extensions

**Option A:** Tuple membership check
```python
if f.suffix in (".json", ".geojson") and f.is_file()
```

**Option B:** OR condition
```python
if (f.suffix == ".json" or f.suffix == ".geojson") and f.is_file()
```

**Decision:** Option A — more concise and easily extensible for future extensions.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| User has non-GeoJSON `.geojson` files | File content is not validated; invalid files will fail at conversion time with clear error message |
| Mixing `.json` and `.geojson` in output | Both extensions produce identical STAC output; no conflict |

## Open Questions

None — the change is minimal and well-scoped.