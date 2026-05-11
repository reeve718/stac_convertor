"""Transform STAC items to bulk insert format for API import."""
import json
from pathlib import Path
from typing import Any


DEFAULT_DATETIME = "1900-01-01T00:00:00"


def transform_to_bulk_format(stac_featurecollection: dict[str, Any], collection_id: str) -> dict[str, Any]:
    """
    Transform STAC FeatureCollection to bulk insert format.

    Args:
        stac_featurecollection: Dict with "type": "FeatureCollection" and "features": [...]
        collection_id: The collection ID to add to each item (e.g., "ctry-park")

    Returns:
        Dict with {"items": {"0": item0, "1": item1, ...}, "method": "insert"}
    """
    items: dict[str, Any] = {}
    for idx, feature in enumerate(stac_featurecollection.get("features", [])):
        props = feature.get("properties", {})

        # Get datetime, use default if missing
        datetime_val = props.get("datetime")
        if not datetime_val:
            datetime_val = DEFAULT_DATETIME

        # Determine key/id: OBJECTID if present, otherwise sequential index
        objectid = props.get("OBJECTID")
        key = str(objectid) if objectid is not None else str(idx)

        # Build bulk item - strip links/assets, add collection and stac_version
        bulk_item = {
            "id": key,
            "type": "Feature",
            "geometry": feature.get("geometry"),
            "bbox": feature.get("bbox"),
            "properties": {
                "OBJECTID": props.get("OBJECTID"),
                "NAME_EN": props.get("NAME_EN"),
                "NAME_TC": props.get("NAME_TC"),
                "datetime": datetime_val,
            },
            "collection": collection_id,
            "stac_version": "1.0.0",
        }

        items[key] = bulk_item

    return {
        "items": items,
        "method": "insert",
    }


def write_items_bulk(stac_featurecollection: dict[str, Any], output_path: str, collection_id: str) -> None:
    """
    Transform STAC items to bulk format and write to file.

    Args:
        stac_featurecollection: STAC FeatureCollection dict
        output_path: Path to write bulk JSON file
        collection_id: Collection ID for items
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    bulk_data = transform_to_bulk_format(stac_featurecollection, collection_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(bulk_data, f, indent=2, ensure_ascii=False)