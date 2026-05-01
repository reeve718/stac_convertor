## 1. Fix key-id matching in transform_to_bulk_format

- [ ] 1.1 Change `items[str(idx)]` to `items[str(props.get("OBJECTID", idx))]` in `src/stac_bulk_writer.py`

## 2. Update tests

- [ ] 2.1 Verify existing tests pass with new key behavior