## Context

The `geojson2stac` CLI currently converts one GeoJSON file per invocation. Users with many files must run the command repeatedly or write shell loops. This friction is unnecessary since the underlying `convert_file()` function in `convertor.py` is already file-agnostic—it takes a `Path` and produces output to a matching subdirectory structure.

## Goals / Non-Goals

**Goals:**
- Enable converting multiple GeoJSON files with a single CLI invocation
- Support both directory-based batch (`--input-dir`) and glob patterns
- Preserve existing single-file behavior when `INPUT_FILE` is provided
- Report errors per-file without aborting the entire batch

**Non-Goals:**
- Recursive directory traversal (non-recursive is sufficient for typical data folders)
- Parallel processing (sequential is simpler and avoids I/O contention)
- Modifying STAC item generation, CRS transformation, or bulk writer logic

## Decisions

**1. Two modes: `--input-dir` and glob pattern**

| Mode | Example | Behavior |
|------|---------|----------|
| Single file | `geojson2stac data/CTRY_PARK.json` | Existing behavior |
| Glob pattern | `geojson2stac "data/*.json"` | Convert all matching files |
| Directory | `geojson2stac --input-dir data/` | Convert all `.json` files in directory |

Rationale: Glob is natural for shell users; `--input-dir` is clearer for documentation and discoverability. Both achieve the same result.

**2. Output structure per input file**

Each input file gets its own output subdirectory under `output_dir`:
```
output_dir/
├── file1/
│   ├── collection.json
│   └── items.json
├── file2/
│   ├── collection.json
│   └── items.json
└── ...
```

Rationale: This already matches the existing behavior for single files and keeps each dataset isolated.

**3. Error handling: continue-on-error**

When processing multiple files:
- If file N fails, log the error and continue to file N+1
- At the end, summarize: "N succeeded, M failed"
- Exit code = non-zero if any failed

Rationale: Partial success is useful—users shouldn't have to re-run everything if one file is corrupt.

**4. No parallelization**

Process files sequentially in a simple loop.

Rationale: Simpler code, no additional dependencies, and I/O-bound workloads don't benefit much from threading in this context.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| User confusion when both `INPUT_FILE` and `--input-dir` are provided | Raise an error if both are present; mutually exclusive |
| Empty directory passed to `--input-dir` | Print warning, exit gracefully |
| Non-.json files in directory | Skip non-`.json` files silently |
| Very large directories (hundreds of files) | No change needed; existing streaming approach handles memory well |

## Open Questions

None at this time. The design is straightforward given the existing architecture.
