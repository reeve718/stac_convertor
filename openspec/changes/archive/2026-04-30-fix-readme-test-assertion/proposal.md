## Why

The `test_readme_has_installation_section` test in `tests/test_readme.py` incorrectly asserts that the word "editable" appears in the README content. However, the README correctly documents editable installs using the standard `-e` flag: `pip install -e ".[dev]"`. The test fails because it searches for the substring "editable" rather than the `-e` flag that actually indicates an editable install.

## What Changes

- Change the assertion in `test_readme_has_installation_section` from checking for the string "editable" to checking for the `-e` flag that indicates an editable pip install

## Capabilities

### New Capabilities
None — this is a bug fix that doesn't introduce new capabilities.

### Modified Capabilities
None — no spec-level behavior changes.

## Impact

- **Affected code**: `tests/test_readme.py` (line 20)
- **Behavior**: The test will correctly validate editable install documentation using the `-e` flag
