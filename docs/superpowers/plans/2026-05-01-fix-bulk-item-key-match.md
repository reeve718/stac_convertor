# Fix Bulk Item Key-Id Match - Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix key-id mismatch in bulk insert format - use OBJECTID as key when available.

**Architecture:** Single-line change in `transform_to_bulk_format()` to use `OBJECTID` as key instead of sequential index.

**Tech Stack:** Python

---

### Task 1: Fix key-id matching

**Files:**
- Modify: `src/stac_bulk_writer.py:46`

**Current code (line 46):**
```python
items[str(idx)] = bulk_item  # key always uses idx
```

**Fixed code:**
```python
objectid = props.get("OBJECTID")
items[str(objectid)] = bulk_item  # key uses OBJECTID if available, else idx
```

- [ ] **Step 1: Make the change**

Edit line 46 in `src/stac_bulk_writer.py` to use `objectid` as key:

```python
objectid = props.get("OBJECTID")
items[str(objectid)] = bulk_item
```

Note: The `objectid` variable is already declared in the function, so we can reuse it. But we need to ensure it's the same value used for `id`. Looking at the existing code:

```python
item_id = str(props.get("OBJECTID", idx))  # already uses OBJECTID for id
```

So `objectid = props.get("OBJECTID")` will give us the same value, and we should use `str(objectid)` if it exists, otherwise use `str(idx)`.

Actually, the cleaner approach is:
```python
objectid = props.get("OBJECTID")
items[str(objectid if objectid is not None else idx)] = bulk_item
```

- [ ] **Step 2: Run tests to verify they pass**

Run: `pytest tests/test_stac_bulk_writer.py -v`
Expected: PASS (existing tests should still pass with new key behavior)

- [ ] **Step 3: Commit**

```bash
git add src/stac_bulk_writer.py
git commit -m "fix: use OBJECTID as key in bulk format to match id"
```

---

### Task 2: Verify integration

**Files:**
- Test: `stac/CTRY_PARK/items.json` (generated output)

- [ ] **Step 1: Run converter with bulk format**

```bash
python -m src.cli test-data/CTRY_PARK.json --output-format bulk -o stac
```

- [ ] **Step 2: Verify key-id match in output**

Check that items.json has matching key and id:
```json
"1": { "id": "1", ... },  // key="1", id="1" ✓
"2": { "id": "2", ... },  // key="2", id="2" ✓
```

- [ ] **Step 3: Commit**

```bash
git add stac/CTRY_PARK/items.json
git commit -m "test: verify key-id match in bulk output"
```