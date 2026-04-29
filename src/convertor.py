"""Main conversion logic - orchestrate all modules."""
from pathlib import Path
from typing import Any
from geojson_parser import stream_geojson
from stac_item_generator import feature_to_item, write_items_featurecollection
from stac_collection_generator import start_collection, update_collection, finalize_collection, write_collection


def convert_file(input_path: Path, output_dir: Path) -> None:
    base_name = input_path.stem
    collection_output_dir = output_dir / base_name
    collection_output_dir.mkdir(parents=True, exist_ok=True)

    collection_state = start_collection(base_name)
    seen_ids = {}
    items = []

    for feature, crs in stream_geojson(input_path):
        item = feature_to_item(feature, crs, seen_ids)
        items.append(item)
        collection_state = update_collection(collection_state, item)

    # Write items.json (FeatureCollection)
    items_path = collection_output_dir / "items.json"
    write_items_featurecollection(items, str(items_path))

    # Write collection.json
    collection = finalize_collection(collection_state, base_name)
    collection_path = collection_output_dir / "collection.json"
    write_collection(collection, str(collection_path))