## 1. Project Setup

- [ ] 1.1 Initialize Python project with pyproject.toml
- [ ] 1.2 Add dependencies: typer, pystac, pyproj, shapely
- [ ] 1.3 Create src/ directory structure
- [ ] 1.4 Add __init__.py files

## 2. CLI Entry Point

- [ ] 2.1 Create src/cli.py with `geojson2stac` command using Typer
- [ ] 2.2 Add argument: input GeoJSON file path
- [ ] 2.3 Add option: output directory (default: stac/)
- [ ] 2.4 Add verbose/quiet output flag
- [ ] 2.5 Add --help documentation

## 3. GeoJSON Parser Module

- [ ] 3.1 Create src/geojson_parser.py
- [ ] 3.2 Implement `parse_geojson(path)` function
- [ ] 3.3 Implement `validate_featurecollection(obj)` function
- [ ] 3.4 Implement `extract_features(fc)` function
- [ ] 3.5 Implement `detect_crs(fc)` function with EPSG:2326 detection
- [ ] 3.6 Implement geometry validation for all types

## 4. CRS Transformer Module

- [ ] 4.1 Create src/crs_transformer.py
- [ ] 4.2 Implement `transform_coordinates(coords, from_crs, to_crs)` for single point
- [ ] 4.3 Implement `transform_point(x, y)` for EPSG:2326 → WGS84
- [ ] 4.4 Implement `transform_geometry(geometry)` for all GeoJSON types
- [ ] 4.5 Implement `calculate_bbox(coordinates)` for bounding box

## 5. STAC Item Generator

- [ ] 5.1 Create src/stac_item_generator.py
- [ ] 5.2 Implement `generate_item_id(feature)` with NAME_EN fallback to OBJECTID
- [ ] 5.3 Implement `handle_duplicate_ids(items)` to append suffixes
- [ ] 5.4 Implement `feature_to_item(feature, crs)` function
- [ ] 5.5 Add geometry_type property to item properties
- [ ] 5.6 Implement `write_item(item, output_path)` function

## 6. STAC Collection Generator

- [ ] 6.1 Create src/stac_collection_generator.py
- [ ] 6.2 Implement `generate_collection(id, items, bbox, extent)` function
- [ ] 6.3 Implement `calculate_extent_bbox(items)` function
- [ ] 6.4 Implement `create_collection_links(items_link, self_link)` function
- [ ] 6.5 Implement `write_collection(collection, output_path)` function

## 7. Main Conversion Logic

- [ ] 7.1 Create src/convertor.py
- [ ] 7.2 Implement `convert_file(input_path, output_dir)` function
- [ ] 7.3 Create output directory structure (stac/<basename>/items/)
- [ ] 7.4 Wire up all modules in correct order
- [ ] 7.5 Handle errors and report progress

## 8. Testing

- [ ] 8.1 Run CLI with sample data: `python -m src.cli data/CTRY_PARK.json`
- [ ] 8.2 Verify stac/CTRY_PARK/collection.json is created
- [ ] 8.3 Verify stac/CTRY_PARK/items/ contains 25 JSON files
- [ ] 8.4 Verify collection.json has valid STAC structure
- [ ] 8.5 Verify item coordinates are in WGS84 (EPSG:4326)
- [ ] 8.6 Verify item IDs are kebab-case from NAME_EN