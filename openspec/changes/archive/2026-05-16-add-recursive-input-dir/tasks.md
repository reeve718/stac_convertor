## 1. CLI Updates

- [ ] 1.1 Add `--recursive` option to CLI in `src/cli.py`
- [ ] 1.2 Modify `expand_input_dir()` to use `rglob` when recursive flag is set
- [ ] 1.3 Compute relative path from `input_dir` to found file for output subdirectory
- [ ] 1.4 Update README.md with `--recursive` documentation

## 2. Testing

- [ ] 2.1 Add unit test for `--recursive` flag with nested directory structure
- [ ] 2.2 Add integration test verifying output folder structure mirrors input
- [ ] 2.3 Add test for non-recursive mode (files at first level only)
- [ ] 2.4 Run full test suite to verify no regressions