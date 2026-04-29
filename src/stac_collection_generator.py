"""Generate STAC Collection from converted items."""
from datetime import datetime, timezone
from typing import Any


def start_collection(collection_id: str) -> dict[str, Any]:
    """Initialize collection state for incremental building."""
    return {
        "id": collection_id,
        "min_lon": None,
        "min_lat": None,
        "max_lon": None,
        "max_lat": None,
        "count": 0,
    }


def update_collection(state: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    """Update collection state with a new item's bbox."""
    bbox = item.get("bbox", [])
    if len(bbox) >= 4:
        if state["min_lon"] is None:
            state["min_lon"] = bbox[0]
            state["min_lat"] = bbox[1]
            state["max_lon"] = bbox[2]
            state["max_lat"] = bbox[3]
        else:
            state["min_lon"] = min(state["min_lon"], bbox[0])
            state["min_lat"] = min(state["min_lat"], bbox[1])
            state["max_lon"] = max(state["max_lon"], bbox[2])
            state["max_lat"] = max(state["max_lat"], bbox[3])
    state["count"] += 1
    return state


def finalize_collection(state: dict[str, Any], collection_id: str) -> dict[str, Any]:
    """Generate final collection dict from accumulated state."""
    collection_id_kebab = collection_id.replace("_", "-").lower()

    if state["min_lon"] is not None:
        bbox = [state["min_lon"], state["min_lat"], state["max_lon"], state["max_lat"]]
    else:
        bbox = [0.0, 0.0, 0.0, 0.0]

    now = datetime.now(timezone.utc).isoformat()

    return {
        "type": "Collection",
        "stac_version": "1.0.0",
        "id": collection_id_kebab,
        "title": collection_id_kebab.replace("-", " ").replace("_", " ").title(),
        "description": f"STAC Collection generated from GeoJSON file: {collection_id}",
        "keywords": [],
        "providers": [],
        "extent": {
            "spatial": {"bbox": [bbox]},
            "temporal": {"interval": [[now, now]]},
        },
        "license": "proprietary",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [bbox[0], bbox[1]],
                [bbox[2], bbox[1]],
                [bbox[2], bbox[3]],
                [bbox[0], bbox[3]],
                [bbox[0], bbox[1]],
            ]],
        } if bbox != [0.0, 0.0, 0.0, 0.0] else None,
        "bbox": bbox,
        "properties": {
            "created": now,
            "modified": now,
            "item_count": state["count"],
        },
        "links": [
            {"rel": "self", "href": "collection.json", "type": "application/json"},
            {"rel": "items", "href": "items.json", "type": "application/geo+json"},
            {"rel": "parent", "href": "../", "type": "application/json"},
        ],
    }


def generate_collection(collection_id: str, items: list[dict[str, Any]]) -> dict[str, Any]:
    collection_id_kebab = collection_id.replace("_", "-").lower()

    # Calculate bounding box from items
    all_bboxes = [item.get("bbox", []) for item in items if item.get("bbox")]
    if all_bboxes:
        min_lon = min(b[0] for b in all_bboxes)
        min_lat = min(b[1] for b in all_bboxes)
        max_lon = max(b[2] for b in all_bboxes)
        max_lat = max(b[3] for b in all_bboxes)
        bbox = [min_lon, min_lat, max_lon, max_lat]
    else:
        bbox = [0.0, 0.0, 0.0, 0.0]

    now = datetime.now(timezone.utc).isoformat()

    collection = {
        "type": "Collection",
        "stac_version": "1.0.0",
        "id": collection_id_kebab,
        "title": collection_id_kebab.replace("-", " ").replace("_", " ").title(),
        "description": f"STAC Collection generated from GeoJSON file: {collection_id}",
        "keywords": [],
        "providers": [],
        "extent": {
            "spatial": {"bbox": [bbox]},
            "temporal": {
                "interval": [
                    [now, now],
                ],
            },
        },
        "license": "proprietary",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [bbox[0], bbox[1]],
                [bbox[2], bbox[1]],
                [bbox[2], bbox[3]],
                [bbox[0], bbox[3]],
                [bbox[0], bbox[1]],
            ]],
        } if bbox != [0.0, 0.0, 0.0, 0.0] else None,
        "bbox": bbox,
        "properties": {
            "created": now,
            "modified": now,
        },
        "links": [
            {
                "rel": "self",
                "href": "collection.json",
                "type": "application/json",
            },
            {
                "rel": "items",
                "href": "items.json",
                "type": "application/geo+json",
            },
            {
                "rel": "parent",
                "href": "../",
                "type": "application/json",
            },
        ],
    }

    return collection


def write_collection(collection: dict[str, Any], output_path: str) -> None:
    import json
    from pathlib import Path
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)