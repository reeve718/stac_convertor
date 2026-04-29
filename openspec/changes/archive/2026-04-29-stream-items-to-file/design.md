## Context

The `stac_convertor` project converts GeoJSON FeatureCollections to STAC Collections and Items. Currently it uses `json.load()` to load the entire input file into memory, then writes each feature as a separate item file. This approach fails for large files (hundreds of MB to 3GB) containing hundreds of thousands of features.

The conversion pipeline consists of:
```
geojson_parser.py → parse_geojson(), extract_features(), detect_crs()
stac_item_generator.py → feature_to_item(), handle_duplicate_ids(), write_item()
stac_collection_generator.py → generate_collection(), write_collection()
convertor.py → orchestrates the above
```

## Goals / Non-Goals

**Goals:**
- Handle GeoJSON files from hundreds of MB to 3GB without memory issues
- Stream-parse input using `ijson` — process one feature at a time
- Write all items to a single `items.json` (FeatureCollection format)
- Generate collection metadata incrementally during streaming
- Detect and handle duplicate IDs inline (no second pass)

**Non-Goals:**
- Resume on failure — if processing fails, restart from beginning
- Keep backward compatibility with `items/*.json` output structure
- Support non-GeoJSON FeatureCollection input formats

## Decisions

### 1. Use `ijson` for streaming JSON parsing

**Decision:** Add `ijson` library as a dependency for streaming parser.

**Why:** `ijson` provides a Python iterator-based JSON parser that yields events, allowing us to process features without loading the full file. It's the standard library for this use case in Python.

**Alternatives considered:**
- `orjson`: Faster but still loads full file into memory
- `json.load()` with generators: Doesn't work — `json.load()` requires the full structure
- Manual chunked reading: Fragile, error-prone JSON parsing

### 2. Single `items.json` instead of per-feature files

**Decision:** Write all STAC items to one `items.json` as a GeoJSON FeatureCollection.

**Why:** Eliminates filesystem overhead for large datasets (500k+ files is problematic). FeatureCollection is the natural GeoJSON container for multiple features. STAC API supports this format natively.

**Format:**
```json
{
  "type": "FeatureCollection",
  "features": [item1, item2, ...]
}
```

### 3. Inline duplicate ID tracking with incremental rename

**Decision:** Track seen IDs in a dictionary during streaming. When a duplicate is encountered, rename by appending `-{counter}` suffix.

**Why:** Avoids a separate pass over all items. Memory overhead is O(unique_ids) which is bounded by total item count — acceptable for any realistic dataset.

**Example:** `name-en`, `name-en`, `name-en` → `name-en`, `name-en-1`, `name-en-2`

### 4. Incremental collection metadata

**Decision:** Collection (bounding box, item count, temporal extent) is updated after each item is processed. Final collection.json is written after streaming completes.

**Why:** All metadata can be computed incrementally — no need to read back items.json.

**Implementation:** Maintain running bbox (min/max of all item bboxes), item count. On completion, generate collection with final values.

### 5. Output directory structure

**Decision:** Output stays at `stac/<basename>/items.json` and `stac/<basename>/collection.json`.

**Why:** Minimal change to existing structure. Just replacing `items/` directory contents with single file.

```
Before:
stac/CTRY_PARK/
├── collection.json
└── items/
    ├── item1.json
    ├── item2.json
    └── ...

After:
stac/CTRY_PARK/
├── collection.json
└── items.json   ← single FeatureCollection
```

## Risks / Trade-offs

- **ijson dependency**: Adds external dependency. Mitigated by it being a pure Python, well-maintained library.
- **No resume**: If process dies at 99%, entire file must be reprocessed. Accepted tradeoff for simplicity.
- **items.json size**: For 500k items, items.json could be 500MB+. Some filesystems struggle with very large single files. Mitigation: this is the nature of the problem; consumers need streaming read if they can't load it.

## Open Questions

- Should `items.json` be pretty-printed (indent=2) or compact? Pretty-print aids debugging but increases file size significantly for large datasets.