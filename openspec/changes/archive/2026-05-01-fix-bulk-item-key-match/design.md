## Context

In `transform_to_bulk_format()`, items are keyed by sequential index `str(idx)` but item `id` is `str(props.get("OBJECTID", idx))`. When `OBJECTID` exists, key and id mismatch (e.g., key="0" but id="1").

## Goals / Non-Goals

**Goals:**
- Key and id must match for each item
- Use `OBJECTID` as key when available
- Fallback to sequential index when no `OBJECTID`

**Non-Goals:**
- No change to other bulk format fields (collection, stac_version, etc.)
- No change to existing STAC format output

## Decisions

### Use OBJECTID as key when available

**Decision:** Change `items[str(idx)]` to `items[str(props.get("OBJECTID", idx))]`.

**Rationale:** Key should match id. If OBJECTID exists, use it for both. If not, use idx as fallback.

**Current code:**
```python
items[str(idx)] = bulk_item  # key always uses idx
```

**Fixed code:**
```python
objectid = props.get("OBJECTID")
items[str(objectid)] = bulk_item  # key uses OBJECTID if available, else idx
```

## Risks / Trade-offs

No significant risks. This is a one-line fix that makes behavior consistent.