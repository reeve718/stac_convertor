## 1. Implementation

- [ ] 1.1 Add `detect_crs_quick()` function to `src/geojson_parser.py`
- [ ] 1.2 Modify `stream_geojson()` to use single-pass reading (bounded prefix for CRS, then stream features)

## 2. Testing

- [ ] 2.1 Add unit tests for `detect_crs_quick()` covering all spec scenarios
- [ ] 2.2 Run full test suite to verify no regressions
