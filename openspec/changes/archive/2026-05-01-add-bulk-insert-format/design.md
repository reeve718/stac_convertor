## Context

The converter outputs STAC items in GeoJSON FeatureCollection format. The API for bulk import requires a different structure:
- Items wrapped in `items` object with string keys ("0", "1", ...)
- Top-level `method: "insert"` field
- Each item has `collection` and `stac_version` at item level
- No `links` or `assets` arrays

The conversion should be applied after STAC items are generated but before writing to disk.

## Goals / Non-Goals

**Goals:**
- Add CLI option `--output-format` with values `stac` (default) or `bulk`
- Create transformation function that converts STAC FeatureCollection to bulk insert format
- Bulk format uses `properties.OBJECTID` as item ID (string)
- Default datetime to `"1900-01-01T00:00:00"` if not present
- Set `collection` to match collection.json id
- Set `stac_version: "1.0.0"` on each item

**Non-Goals:**
- No change to existing STAC format output (backward compatible, default is `stac`)
- No modification to collection.json generation
- No validation of API acceptance (API requirements assumed stable)

## Decisions

### CLI Option: `--output-format`

**Decision:** Add `--output-format` CLI argument with choices `stac` and `bulk`.

**Rationale:** Allows user to select output format without changing existing workflow. Default `stac` maintains backward compatibility.

```
geojson2stac input_file [--output-format stac|bulk] [-o output_dir]
```

### ID Selection from OBJECTID

**Decision:** Use `properties.OBJECTID` as the item `id`, converted to string.

**Rationale:** OBJECTID is unique per feature and guaranteed to exist in the source GeoJSON. API requires unique, non-repeating IDs.

**Alternative:** Derive from NAME_EN (kebab-case) — more descriptive but requires sanitization and may collide.

### Default Datetime

**Decision:** If `properties.datetime` is missing or null, use `"1900-01-01T00:00:00"`.

**Rationale:** The bulk sample shows this value as default. API accepts any datetime format, but `"1900-01-01T00:00:00"` is the established convention.

### Module Structure

**Decision:** Create `src/stac_bulk_writer.py` with function `write_items_bulk()`.

**Rationale:** Separation of concerns — transformation logic is separate from CLI and existing STAC writing logic.

```
src/
  stac_item_generator.py   # existing
  stac_bulk_writer.py      # new: bulk format transformation
```

## Risks / Trade-offs

- **API format stability** — If API requirements change, transformation may break. → Mitigation: Document the expected API format in tests with the sample file.
- **Memory usage** — Loading all items into memory for transformation. → Acceptable for typical GeoJSON sizes. Stream processing could be added later if needed.

## Open Questions

None at this time. All requirements are defined based on the bulk insert sample analysis.