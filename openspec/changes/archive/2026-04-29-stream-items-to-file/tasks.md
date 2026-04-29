## 1. Add ijson dependency

- [ ] 1.1 Add `ijson` to `pyproject.toml` under dependencies

## 2. Add streaming parse function to geojson_parser.py

- [ ] 2.1 Add `stream_features()` function that uses ijson to yield features one-by-one
- [ ] 2.2 Add `stream_geojson()` generator that yields (feature, crs) tuples

## 3. Modify stac_item_generator.py for streaming output

- [ ] 3.1 Inline duplicate ID tracking in `feature_to_item()` (add `seen_ids` parameter)
- [ ] 3.2 Add `write_items_streaming()` function that writes FeatureCollection to items.json incrementally

## 4. Modify stac_collection_generator.py for incremental collection

- [ ] 4.1 Add `start_collection()` to initialize collection state
- [ ] 4.2 Add `update_collection()` to update bbox and count per item
- [ ] 4.3 Add `finalize_collection()` to write collection.json with final metadata

## 5. Modify convertor.py

- [ ] 5.1 Replace `parse_geojson()` + `extract_features()` with streaming approach
- [ ] 5.2 Wire streaming to item generator with inline duplicate tracking
- [ ] 5.3 Wire incremental collection updates during streaming
- [ ] 5.4 Write items.json as FeatureCollection on completion
- [ ] 5.5 Write collection.json with final metadata

## 6. Update tests

- [ ] 6.1 Add tests for `stream_features()` with valid and invalid GeoJSON
- [ ] 6.2 Add tests for inline duplicate ID handling
- [ ] 6.3 Add tests for streaming items.json output (verify FeatureCollection format)
- [ ] 6.4 Add tests for incremental collection metadata
- [ ] 6.5 Run full test suite to verify no regressions