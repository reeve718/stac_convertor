## Context

The batch conversion loop in `src/cli.py` processes files sequentially:

```python
for file_path in files:
    convert_file(file_path, output_dir, ...)
```

Each `convert_file()` call is independent — no shared state, no ordering requirements. Files write to isolated output directories (determined by input path relative to `--input-dir`). This independence makes parallelism straightforward.

## Goals / Non-Goals

**Goals:**
- Add `--workers` CLI option to control thread count
- Parallelize batch processing when `--workers > 1`
- Thread-safe error collection and reporting
- Default to sequential (workers=1) for backward compatibility

**Non-Goals:**
- Intra-file parallelism (parallelizing within a single file)
- Process pool (multiprocessing) — threads sufficient for I/O-bound work
- Changing output format or structure

## Decisions

**1. ThreadPoolExecutor over ProcessPoolExecutor**

Threads are sufficient because:
- Work is I/O-bound (file reading, JSON parsing, writing)
- Python's GIL is released during I/O operations
- No shared mutable state between file conversions
- Lower overhead than multiprocessing

**Alternatives considered:**
- `multiprocessing.Pool` — higher overhead, unnecessary for I/O-bound work
- `asyncio` — adds complexity; ThreadPoolExecutor is simpler for this use case

**2. Thread-safe error collection**

Results collected via `concurrent.futures.as_completed()`:

```python
with ThreadPoolExecutor(max_workers=workers) as executor:
    future_to_path = {executor.submit(convert_one, fp): fp for fp in files}
    for future in as_completed(future_to_path):
        path = future_to_path[future]
        try:
            future.result()
            succeeded += 1
        except Exception as e:
            failed += 1
            errors.append((path, str(e)))
```

**3. Workers default to 1 (sequential)**

Backward compatible — existing scripts without `--workers` behave identically.

**4. CLI option: `--workers`**

```python
workers: int = typer.Option(1, "--workers", help="Number of parallel workers for batch conversion")
```

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| Over-saturating disk I/O with too many workers | User controls worker count; can experiment |
| Thread-safety issues in `convert_file()` | No shared mutable state; each call is independent |
| Error messages interleaved with verbose output | Verbose prints happen per-thread; summary at end |
| Same output filename in non-recursive mode | Files are independent; outputs can overwrite (rare case) |

## Open Questions

None — the approach is straightforward.
