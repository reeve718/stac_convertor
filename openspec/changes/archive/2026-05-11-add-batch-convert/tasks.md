## 1. CLI Updates

- [ ] 1.1 Add `--input-dir` option to CLI in `src/cli.py`
- [ ] 1.2 Add glob pattern detection and handling for `INPUT_FILE` argument
- [ ] 1.3 Implement mutual exclusivity check between `INPUT_FILE` and `--input-dir`
- [ ] 1.4 Implement batch loop in `src/cli.py` that calls `convert_file()` per file
- [ ] 1.5 Add per-file error handling with continue-on-error semantics
- [ ] 1.6 Add summary output (succeeded/failed count) at end of batch
- [ ] 1.7 Update `README.md` with new `--input-dir` and glob pattern documentation

## 2. Testing

- [ ] 2.1 Add unit tests for glob pattern detection in CLI
- [ ] 2.2 Add unit tests for mutual exclusivity check
- [ ] 2.3 Add integration test for `--input-dir` with multiple files
- [ ] 2.4 Add integration test for error handling (one file fails, others continue)
