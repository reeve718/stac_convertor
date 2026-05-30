## Why

Batch conversion of many GeoJSON files (e.g., 1000 files) is currently sequential — each file is processed one at a time. Even with the recent 4KB prefix optimization for CRS detection, processing large batches can still take an hour or more. Adding a `--workers` flag enables parallel processing of independent files, significantly reducing batch conversion time on multi-core systems.

## What Changes

- Add `--workers` CLI option to control parallel thread count
- Implement `ThreadPoolExecutor`-based parallel batch processing in CLI
- Thread-safe error collection and reporting
- Preserve existing sequential behavior when `--workers` is not specified (default: 1)
- Maintain backward compatibility with all existing CLI options

## Capabilities

### New Capabilities
- `batch-parallel-processing`: Parallel conversion of multiple GeoJSON files using configurable worker threads

### Modified Capabilities
- (none)

## Impact

- **Affected file**: `src/cli.py`
- **New dependency**: `concurrent.futures.ThreadPoolExecutor` (stdlib)
- **CLI change**: Adds `--workers` flag to control parallelism
- **Performance**: Expected ~linear speedup with worker count (up to I/O saturation)
- **Output**: No change to output format or structure
