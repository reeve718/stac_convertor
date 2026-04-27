## Context

The `geojson2stac` CLI command is defined in `pyproject.toml` with:
```toml
[project.scripts]
geojson2stac = "src.cli:app"
```

The setuptools configuration uses `where = ["src"]` which means packages in the `src/` directory are installed with the `src/` prefix stripped. Therefore `src/cli.py` becomes `cli` when installed, not `src.cli`.

## Goals / Non-Goals

**Goals:**
- Fix the CLI entry point to use the correct module path
- Ensure `geojson2stac` command works after pip install

**Non-Goals:**
- No changes to CLI functionality or arguments
- No changes to package structure

## Decisions

Change `pyproject.toml` line 22 from:
```toml
geojson2stac = "src.cli:app"
```
to:
```toml
geojson2stac = "cli:app"
```

## Risks / Trade-offs

None - this is a single-line fix with no side effects.
