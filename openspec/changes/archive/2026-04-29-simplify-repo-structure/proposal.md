## Why

The current repo has a confusing structure:
- Multiple branches (main, master, feature/*) with an unclear workflow
- Source code in `src/` instead of a proper Python package (`src/stac_convertor/`)
- Multiple git worktrees making local development fragmented
- `pyproject.toml` was broken until recently

This makes the repo hard to understand, install, or contribute to.

## What Changes

- **BREAKING** Move `src/*.py` → `src/stac_convertor/*.py` as a proper Python package
- **BREAKING** Update `pyproject.toml` entry points to `src.stac_convertor` module path
- **BREAKING** Delete `.worktrees/` directory — no more worktree isolation
- Delete `.gitignore` with old rules — replace with clean `.gitignore`
- Remove archived OpenSpec changes from `openspec/changes/archive/`
- Keep only `main` branch — delete `master` and `feature/geojson-to-stac` on GitHub
- Add `README.md`, `requirements.txt`, `LICENSE` to repo root
- Add `pyproject.toml` to repo root (already working)
- Update `CLAUDE.md` to remove worktree references

## Capabilities

### New Capabilities

- `repo-structure`: Clean, installable Python package structure

### Modified Capabilities

- (none — existing STAC conversion capabilities are unchanged)

## Impact

- All source files moved to `src/stac_convertor/`
- All test files remain in `tests/` (imports updated to use `src.stac_convertor`)
- `pyproject.toml` entry points updated
- Git history is preserved — only file locations change
- GitHub branches reduced to just `main`
