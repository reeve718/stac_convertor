## 1. Flat src/ layout (chosen over src/stac_convertor/ package)

- [x] 1.1 Keep all source files in `src/` (flat layout — avoids CLI packaging issues)
- [x] 1.2 All 7 modules in `src/`: `__init__.py`, `cli.py`, `convertor.py`, `crs_transformer.py`, `geojson_parser.py`, `stac_collection_generator.py`, `stac_item_generator.py`
- [x] 1.3 Internal imports use `from src.X` pattern

## 2. Update pyproject.toml

- [x] 2.1 Add `[tool.setuptools.packages.find]` pointing to `src/` with `where = ["src"]`
- [x] 2.2 Verify `pip install -e .` succeeds

## 3. Update test imports

- [x] 3.1 All test imports use `from src.X` pattern
- [x] 3.2 Run `pytest` — all 38 tests pass

## 4. Verify CLI works

- [x] 4.1 Run `geojson2stac --help` — CLI help prints (via `.bat` launcher)
- [x] 4.2 Run `geojson2stac data/CTRY_PARK.json` — output created in `stac/CTRY_PARK/`

## 5. Clean up git structure

- [x] 5.1 Remove `.worktrees/` directory from repo (git submodule)
- [x] 5.2 Update `.gitignore` to include `.worktrees/`
- [x] 5.3 Commit all restructure changes

## 6. Delete remote branches and push

- [x] 6.1 Delete `main` branch on GitHub
- [x] 6.2 Delete `feature/geojson-to-stac` branch on GitHub (was not on remote)
- [x] 6.3 Push `master` — single branch on GitHub
