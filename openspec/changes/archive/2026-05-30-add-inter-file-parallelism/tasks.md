## 1. CLI Updates

- [ ] 1.1 Add `--workers` option to CLI in `src/cli.py`
- [ ] 1.2 Update README.md with `--workers` documentation

## 2. Parallel Processing Implementation

- [ ] 2.1 Refactor batch loop to use `ThreadPoolExecutor`
- [ ] 2.2 Implement thread-safe error collection
- [ ] 2.3 Verify parallel processing works with `--recursive`

## 3. Testing

- [ ] 3.1 Add unit tests for parallel batch processing
- [ ] 3.2 Add integration test for `--workers` flag
- [ ] 3.3 Run full test suite to verify no regressions
