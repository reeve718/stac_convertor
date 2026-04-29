# Fix README Markdown Lint - Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix all markdownlint violations in README.md to eliminate VSCode warnings.

**Architecture:** Simple markdown edits to fix 6 lint issues. Single file modification, no architectural impact.

**Tech Stack:** markdownlint (for verification)

---

### Task 1: Fix README.md Markdown Style Issues

**Files:**
- Modify: `README.md`

**Current state (with line numbers):**
```
1  [![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
2  [![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
3  [![CI](https://img.shields.io/badge/CI-none-red.svg)](#)
4
5  # stac-convertor
6
7  Convert GeoJSON FeatureCollections to STAC Collections and Items.
...
27  Output is written to `stac/CTRY_PARK/`:
28  ```
29  stac/CTRY_PARK/
30  ├── collection.json        ← STAC Collection
31  └── items.json            ← STAC Items (GeoJSON FeatureCollection)
32  ```
...
35  ## CLI Reference
36  ```
37  geojson2stac INPUT_FILE [-o OUTPUT_DIR] [-v]
38  ```
...
40  | Argument / Option | Description | Default |
41  |---|---|---|
...
63  Supported input CRS includes:
64  - EPSG:2326 (Hong Kong 1980 Grid System)
65  - Any CRS supported by `pyproj`
```

**Required changes:**
1. Move `# stac-convertor` to line 1, badges move below
2. Remove empty link `(#)` from CI badge line
3. Add blank lines around code block at line 28
4. Add `bash` language to code block at line 28
5. Add blank lines around code block at line 36
6. Add `bash` language to code block at line 36
7. Fix table pipes at line 41: `|---|---|---|` → `| --- | --- | --- |`
8. Add blank line before list at line 63

- [ ] **Step 1: Verify current lint errors**

```bash
markdownlint README.md
```
Expected: Shows all 6 violation types

- [ ] **Step 2: Edit README.md - Fix ordering**

Move badges after H1 heading:
```markdown
# stac-convertor

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![CI](https://img.shields.io/badge/CI-none-red.svg)](#)
```

- [ ] **Step 3: Edit README.md - Fix empty link**

Change line 3 from `(#)` to just remove the link portion, keeping the badge:
```markdown
[![CI](https://img.shields.io/badge/CI-none-red.svg)
```

- [ ] **Step 4: Edit README.md - Fix first code block**

Add blank lines and `bash` language:
```markdown

```bash
stac/CTRY_PARK/
├── collection.json        ← STAC Collection
└── items.json            ← STAC Items (GeoJSON FeatureCollection)
```

```

- [ ] **Step 5: Edit README.md - Fix CLI Reference code block**

Add `bash` language:
```markdown
```bash
geojson2stac INPUT_FILE [-o OUTPUT_DIR] [-v]
```
```

- [ ] **Step 6: Edit README.md - Fix table pipes**

Change to:
```markdown
| --- | --- | --- |
```

- [ ] **Step 7: Edit README.md - Add blank line before list**

Add blank line before "Supported input CRS includes:" at line 63

- [ ] **Step 8: Run markdownlint to verify all issues fixed**

```bash
markdownlint README.md
```
Expected: No output (0 errors)

- [ ] **Step 9: Commit**

```bash
git add README.md
git commit -m "fix: resolve markdownlint violations in README"
```
