## 1. Fix pyproject.toml script entry

- [ ] 1.1 Change `geojson2stac = "src.cli:app"` to `geojson2stac = "cli:app"` in pyproject.toml

## 2. Verify the fix

- [ ] 2.1 Reinstall package in development mode (`pip install -e .`)
- [ ] 2.2 Run `geojson2stac --help` to confirm CLI works
