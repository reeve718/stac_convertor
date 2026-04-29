## Context

The `test_readme_has_installation_section` test in `tests/test_readme.py` validates that the README documents editable pip installs. The current assertion checks for the word "editable" in README content, but pip's standard syntax for editable installs uses the `-e` flag, not the word "editable". The README correctly uses `pip install -e ".[dev]"`.

## Goals / Non-Goals

**Goals:**
- Fix the failing test by asserting on the correct string that indicates editable install

**Non-Goals:**
- No changes to README content (it's already correct)
- No changes to other tests

## Decisions

### Change assertion from "editable" to "-e"

**Decision:** Change `assert "editable" in content.lower()` to `assert "-e" in content` on line 20 of `tests/test_readme.py`.

**Rationale:** The `-e` flag is the actual pip syntax for editable installs. The test is validating that editable installs are documented, and the `-e` flag is the correct indicator of that. The word "editable" is ambiguous and doesn't match how editable installs are actually written in pip syntax.

**Alternatives considered:**
- `assert "--editable" in content` — not standard pip syntax; `--editable` is not a valid pip flag
- `assert "editable install" in content.lower()` — verbose and still doesn't match common documentation practice
- No test change, modify README instead — wrong direction; the README is correct as-is

## Risks / Trade-offs

No significant risks. This is a one-line test fix that corrects a false assertion.
