## Context

The repo currently has:
- Source in `src/` (flat — not a package)
- Tests in `tests/` with broken imports (`from src import ...`)
- A git worktree at `.worktrees/geojson-to-stac/` with actual code
- Main repo on `master` with scaffold files (README, CLAUDE.md, etc.)
- Multiple branches: `main`, `master`, `feature/geojson-to-stac`

This is confusing and the package doesn't install cleanly.

## Goals / Non-Goals

**Goals:**
- One branch: `main`
- Proper Python package: `src/stac_convertor/`
- Clean install: `pip install -e .` works
- CLI: `geojson2stac` works after install
- All tests pass after restructure

**Non-Goals:**
- Restructuring OpenSpec workflow files — they stay as-is
- Changing any source code logic — only file locations change
- Rewriting git history — preserve all commits

## Decisions

### 1. Package structure: `src/stac_convertor/`

```
stac_convertor/
├── src/
│   └── stac_convertor/
│       ├── __init__.py
│       ├── cli.py
│       ├── convertor.py
│       ├── crs_transformer.py
│       ├── geojson_parser.py
│       ├── stac_collection_generator.py
│       └── stac_item_generator.py
├── tests/
│   ├── __init__.py
│   ├── test_*.py   (imports: from src.stac_convertor import ...)
├── data/
│   └── CTRY_PARK.json
├── docs/
├── openspec/
├── README.md
├── requirements.txt
├── pyproject.toml
├── LICENSE
└── CLAUDE.md
```

**Why:** Standard Python packaging layout. `src/` prevents accidental imports of the package without installing it.

### 2. `pyproject.toml` — use `[project]` + `[tool.setuptools.packages.find]`

```toml
[tool.setuptools.packages.find]
where = ["src"]
```

All packages found under `src/`. Tests stay at repo root (not under `src/`).

### 3. Single branch: `main`

Delete `master` and `feature/geojson-to-stac` from GitHub after restructuring. All commits live on `main`.

### 4. No worktrees

Remove `.worktrees/` directory entirely. Work in the main repo clone.

### 5. Test imports updated

Before: `from src import convertor`
After: `from src.stac_convertor import convertor`

## Risks / Trade-offs

- **Tests break after import rename** → Tests will fail until imports are updated — covered in implementation tasks
- **GitHub branches need deletion** → `master` and `feature/geojson-to-stac` must be deleted via GitHub web UI or `git push --delete`
- **Worktree branch history lost** → Commits are in shared `.git`, history is preserved

## Migration Plan

1. Create new folder structure at `main` branch root
2. Move source files to `src/stac_convertor/`
3. Update all test imports
4. Fix `pyproject.toml` package discovery
5. Remove `.worktrees/` directory
6. Push `main` — delete `master` and `feature/geojson-to-stac` on GitHub
7. Verify `pip install -e . && geojson2stac --help` works
8. Verify `pytest` passes

Rollback: `git reset --hard` to pre-change commit.
