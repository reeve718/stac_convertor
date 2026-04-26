"""Main conversion logic - orchestrate all modules."""
from pathlib import Path
from typing import Any
from src.geojson_parser import parse_geojson, extract_features, detect_crs
from src.stac_item_generator import feature_to_item, handle_duplicate_ids, write_item
from src.stac_collection_generator import generate_collection, write_collection


def convert_file(input_path: Path, output_dir: Path) -> None:
    fc = parse_geojson(input_path)
    features = extract_features(fc)
    crs = detect_crs(fc)
    base_name = input_path.stem

    collection_output_dir = output_dir / base_name
    items_output_dir = collection_output_dir / "items"
    items_output_dir.mkdir(parents=True, exist_ok=True)

    items = []
    for feature in features:
        item = feature_to_item(feature, crs)
        items.append(item)

    items = handle_duplicate_ids(items)

    for item in items:
        item_path = items_output_dir / f"{item['id']}.json"
        write_item(item, str(item_path))

    collection = generate_collection(base_name, items)
    collection_path = collection_output_dir / "collection.json"
    write_collection(collection, str(collection_path))
