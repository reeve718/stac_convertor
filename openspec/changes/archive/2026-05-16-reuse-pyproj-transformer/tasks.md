## 1. Core Implementation

- [ ] 1.1 Create `Transformer` once in `stream_geojson()` and yield it alongside features
- [ ] 1.2 Update `convert_file()` to unpack transformer and pass to `feature_to_item()`
- [ ] 1.3 Update `feature_to_item()` to accept transformer and pass to `transform_geometry()`
- [ ] 1.4 Update `transform_geometry()` to accept transformer and inline transform logic

## 2. Verification

- [ ] 2.1 Run existing tests to verify output unchanged
- [ ] 2.2 Time large file conversion before/after to confirm performance improvement