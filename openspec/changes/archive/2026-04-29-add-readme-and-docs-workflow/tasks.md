## 1. Create README.md

- [ ] 1.1 Add badge strip (license, Python version, build status link)
- [ ] 1.2 Write one-line project description
- [ ] 1.3 Document installation (pip install, editable dev install)
- [ ] 1.4 Add quick start with sample data (`data/CTRY_PARK.json`)
- [ ] 1.5 Document CLI reference (`--help` output: `input_file`, `--output/-o`, `--verbose/-v`)
- [ ] 1.6 Document how CRS transform works (EPSG:2326 → WGS84)
- [ ] 1.7 Add development setup section (clone, install deps, run pytest)
- [ ] 1.8 Add license section

## 2. Update CLAUDE.md

- [ ] 2.1 Add rule that CLI changes in `src/cli.py` require README update

## 3. Update OpenSpec config

- [ ] 3.1 Add per-artifact rule to `openspec/config.yaml`: CLI changes require README review in tasks
