"""Main conversion logic - orchestrate all modules."""
from pathlib import Path
from typing import Any
from geojson_parser import stream_geojson
from stac_item_generator import feature_to_item, write_items_featurecollection
from stac_bulk_writer import write_items_bulk
from stac_collection_generator import start_collection, update_collection, finalize_collection, write_collection


def convert_file(
    input_path: Path,
    output_dir: Path,
    output_format: str = "stac"
) -> None:
    base_name = input_path.stem
    collection_output_dir = output_dir / base_name
    collection_output_dir.mkdir(parents=True, exist_ok=True)

    collection_state = start_collection(base_name)
    seen_ids = {}
    items = []

    for idx, (feature, crs) in enumerate(stream_geojson(input_path)):
        item = feature_to_item(feature, crs, seen_ids, idx)
        items.append(item)
        collection_state = update_collection(collection_state, item)

    collection = finalize_collection(collection_state, base_name)
    collection_id = collection["id"]
    items_path = collection_output_dir / "items.json"

    # Write items based on format
    if output_format == "bulk":
        write_items_bulk(
            {"type": "FeatureCollection", "features": items},
            items_path,
            collection_id
        )
    else:
        write_items_featurecollection(items, str(items_path))

    # Write collection.json
    collection_path = collection_output_dir / "collection.json"
    write_collection(collection, str(collection_path))