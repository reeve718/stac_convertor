"""Generate STAC Items from GeoJSON Features."""
import re
from datetime import datetime, timezone
from typing import Any
from crs_transformer import transform_geometry, calculate_bbox


def generate_item_id(feature: dict[str, Any], fallback_index: int | None = None) -> str:
    props = feature.get("properties", {})
    name = props.get("NAME_EN")
    if name:
        kebab = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()
        kebab = re.sub(r"-+", "-", kebab)
        return kebab
    objectid = props.get("OBJECTID")
    if objectid is not None:
        return f"item-{objectid}"
    if fallback_index is not None:
        return f"item-{fallback_index}"
    raise ValueError("Feature must have NAME_EN or OBJECTID property")


def handle_duplicate_ids(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: dict[str, int] = {}
    result = []
    for item in items:
        item_id = item["id"]
        if item_id in seen:
            seen[item_id] += 1
            item = dict(item)
            item["id"] = f"{item_id}-{seen[item_id]}"
            # Update self-link href to match renamed id
            for link in item.get("links", []):
                if link.get("rel") == "self":
                    link["href"] = f"items/{item['id']}.json"
        else:
            seen[item_id] = 0
        result.append(item)
    return result


def feature_to_item(
    feature: dict[str, Any],
    crs: str,
    seen_ids: dict[str, int] | None = None,
    index: int | None = None,
) -> dict[str, Any]:
    if seen_ids is None:
        seen_ids = {}

    props = feature.get("properties", {})
    item_id = generate_item_id(feature, index)

    # Handle duplicate IDs inline
    if item_id in seen_ids:
        seen_ids[item_id] += 1
        item_id = f"{item_id}-{seen_ids[item_id]}"
        seen_ids[item_id] = 0
    else:
        seen_ids[item_id] = 0

    geom = feature.get("geometry")
    if not geom:
        geom = {"type": "Point", "coordinates": []}
    geom_type = geom.get("type", "Unknown")
    transformed_geom = transform_geometry(geom, crs)
    bbox = calculate_bbox(transformed_geom["coordinates"])

    item_props = {
        "datetime": datetime.now(timezone.utc).isoformat(),
        "OBJECTID": props.get("OBJECTID"),
        "NAME_EN": props.get("NAME_EN"),
        "NAME_TC": props.get("NAME_TC"),
        "geometry_type": geom_type,
    }

    item = {
        "type": "Feature",
        "stac_version": "1.0.0",
        "id": item_id,
        "geometry": transformed_geom,
        "bbox": bbox,
        "properties": item_props,
        "links": [
            {
                "rel": "self",
                "href": f"items.json",
                "type": "application/geo+json",
            },
            {
                "rel": "collection",
                "href": "collection.json",
                "type": "application/json",
            },
        ],
        "assets": {},
    }

    return item


def write_item(item: dict[str, Any], output_path: str) -> None:
    import json
    from pathlib import Path
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(item, f, indent=2, ensure_ascii=False)


def write_items_featurecollection(items: list[dict[str, Any]], output_path: str) -> None:
    """Write all items to a single GeoJSON FeatureCollection file."""
    import json
    from pathlib import Path
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    collection = {
        "type": "FeatureCollection",
        "features": items,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)
