## 1. Create new package structure

- [ ] 1.1 Create `src/stac_convertor/` directory with `__init__.py`
- [ ] 1.2 Move all `.py` files from `src/` into `src/stac_convertor/`
- [ ] 1.3 Verify directory structure: `src/stac_convertor/` contains 7 modules

## 2. Update pyproject.toml

- [ ] 2.1 Add `[tool.setuptools.packages.find]` pointing to `src/`
- [ ] 2.2 Verify `pip install -e .` succeeds

## 3. Update test imports

- [ ] 3.1 Update all `from src import X` → `from src.stac_convertor import X` in test files
- [ ] 3.2 Run `pytest` — all tests pass

## 4. Verify CLI works

- [ ] 4.1 Run `geojson2stac --help` — CLI help prints
- [ ] 4.2 Run `geojson2stac data/CTRY_PARK.json` — output created in `stac/`

## 5. Clean up git structure

- [ ] 5.1 Remove `.worktrees/` directory from repo
- [ ] 5.2 Update `.gitignore` to: `__pycache__/`, `*.pyc`, `.pytest_cache/`, `stac/`, `.worktrees/`
- [ ] 5.3 Commit all restructure changes

## 6. Delete remote branches and push

- [ ] 6.1 Delete `master` branch on GitHub
- [ ] 6.2 Delete `feature/geojson-to-stac` branch on GitHub
- [ ] 6.3 Push `main` — verify only `main` branch exists on GitHub
