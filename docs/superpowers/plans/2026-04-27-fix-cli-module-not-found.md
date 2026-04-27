# Fix CLI Module Not Found Bug - Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix `ModuleNotFoundError: No module named 'src'` when running `geojson2stac` command after installation.

**Architecture:** Single-line fix in `pyproject.toml`. The issue is that `where = ["src"]` in setuptools config strips the `src/` prefix when installing packages, so the module path should be `cli:app` not `src.cli:app`.

**Tech Stack:** Python, setuptools, pyproject.toml

---

## Task 1: Fix pyproject.toml Script Entry

**Files:**
- Modify: `pyproject.toml:22`

- [ ] **Step 1: Edit pyproject.toml to fix CLI script entry**

Change line 22 from:
```toml
geojson2stac = "src.cli:app"
```
to:
```toml
geojson2stac = "cli:app"
```

- [ ] **Step 2: Reinstall package in development mode**

```bash
pip install -e .
```

- [ ] **Step 3: Verify CLI works**

```bash
geojson2stac --help
```
Expected: Help text displayed without errors

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml
git commit -m "fix: correct pyproject.toml scripts entry to use cli:app instead of src.cli:app"
```
