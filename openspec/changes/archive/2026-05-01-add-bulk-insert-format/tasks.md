## 1. Create stac_bulk_writer module

- [ ] 1.1 Create `src/stac_bulk_writer.py` with `write_items_bulk()` function
- [ ] 1.2 Add function to transform FeatureCollection to bulk format

## 2. Add CLI argument

- [ ] 2.1 Add `--output-format` argument to CLI in `src/cli.py`
- [ ] 2.2 Update README.md to document the new CLI option

## 3. Implement bulk transformation

- [ ] 3.1 Implement `transform_to_bulk_format()` function
- [ ] 3.2 Map OBJECTID to item id as string
- [ ] 3.3 Add default datetime `"1900-01-01T00:00:00"` if missing
- [ ] 3.4 Add `collection` field to each item
- [ ] 3.5 Add `stac_version: "1.0.0"` to each item
- [ ] 3.6 Strip `links` and `assets` from items

## 4. Testing

- [ ] 4.1 Add unit tests for `stac_bulk_writer.py`
- [ ] 4.2 Test bulk format output matches expected structure
- [ ] 4.3 Test with sample data `test-data/CTRY_PARK.json`