# Fix README Test Assertion - Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the failing test by changing the assertion from checking for the word "editable" to checking for the `-e` flag that indicates an editable pip install.

**Architecture:** Simple one-line test fix. The test file `tests/test_readme.py` line 20 currently asserts `assert "editable" in content.lower()` but should assert `assert "-e" in content` since `-e` is the actual pip syntax for editable installs.

**Tech Stack:** pytest, Python

---

### Task 1: Fix Test Assertion

**Files:**
- Modify: `tests/test_readme.py:20`

- [ ] **Step 1: Write the failing test**

```bash
pytest tests/test_readme.py::test_readme_has_installation_section -v
```
Expected: FAIL - assertion fails because "editable" check vs "-e" flag

- [ ] **Step 2: Update the assertion**

Change line 20 from:
```python
assert "editable" in content.lower()
```
to:
```python
assert "-e" in content
```

- [ ] **Step 3: Run test to verify it passes**

```bash
pytest tests/test_readme.py::test_readme_has_installation_section -v
```
Expected: PASS

- [ ] **Step 4: Run all README tests to ensure no regression**

```bash
pytest tests/test_readme.py -v
```
Expected: All tests PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_readme.py
git commit -m "fix: update test assertion from 'editable' to '-e' flag"
```
