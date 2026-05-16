## Context

The current `expand_input_dir()` function in `src/cli.py` uses `Path.iterdir()` which only lists immediate children of a directory:

```python
return sorted([f for f in input_dir.iterdir() if f.suffix in (".json", ".geojson") and f.is_file()])
```

Users with nested folder structures like `data/subfolder/nested/file.json` must either flatten their data or run multiple commands. We need to support recursive scanning while preserving folder hierarchy in output.

## Goals / Non-Goals

**Goals:**
- Add `--recursive` flag that enables recursive directory scanning
- Output structure mirrors input structure: `data/subfolder/file.json` → `stac/subfolder/file/`
- Non-recursive mode (without `--recursive`) remains unchanged

**Non-Goals:**
- Parallel processing (sequential only)
- Recursive glob patterns via `**` in glob mode (keep scope focused)
- Modifying `convert_file()` — it remains unchanged

## Decisions

**1. Handle relative path computation in the CLI batch loop, not in `convert_file()`**

The CLI batch loop computes output paths. When `--recursive` is used, it computes the relative path from `input_dir` to the found file and uses that to build the correct output subdirectory.

Rationale: Keeps `convert_file()` simple and unchanged. The complexity of relative path computation stays at the CLI layer where it belongs.

**2. Use `Path.rglob()` for recursive scanning**

```python
# Non-recursive (current):
input_dir.iterdir()

# Recursive (new):
input_dir.rglob("*.json")  # or rglob("*.geojson")
```

Rationale: Python's built-in `Path.rglob()` handles recursion correctly across all platforms. No need for `os.walk()` or external libraries.

**3. Output directory mirrors input hierarchy**

When scanning `data/` with `--recursive`:
- `data/file.json` → `stac/file/`
- `data/sub/file.json` → `stac/sub/file/`
- `data/sub/deep/file.json` → `stac/sub/deep/file/`

The relative path from `input_dir` to the file becomes the output subdirectory under `output_dir`.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Deeply nested files create very long output paths | Acceptable — users choose their input structure |
| Same filename in different subdirectories | Each gets its own output subdirectory (no conflict) |
| Performance with very deep directories | `rglob` is lazy; streaming approach handles this well |

## Open Questions

None — design is straightforward.