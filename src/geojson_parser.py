"""Parse and validate GeoJSON FeatureCollections."""
import ijson
import json
import sys
from pathlib import Path
from typing import Any


SUPPORTED_GEOMETRY_TYPES = {
    "Point",
    "LineString",
    "Polygon",
    "MultiPoint",
    "MultiLineString",
    "MultiPolygon",
}


def parse_geojson(path: Path) -> dict[str, Any]:
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    validate_featurecollection(data)
    return data


def validate_featurecollection(obj: dict[str, Any]) -> None:
    if obj.get("type") != "FeatureCollection":
        print("Error: Root object must be a FeatureCollection", file=sys.stderr)
        sys.exit(1)


def extract_features(fc: dict[str, Any]) -> list[dict[str, Any]]:
    features = fc.get("features", [])
    if not features:
        print("Error: No features found in FeatureCollection", file=sys.stderr)
        sys.exit(1)
    return features


def detect_crs(fc: dict[str, Any]) -> str:
    crs = fc.get("crs")
    if crs and crs.get("type") == "name":
        name = crs.get("properties", {}).get("name", "")
        if name.startswith("EPSG:"):
            return name
    print("Warning: No CRS found, defaulting to WGS84 (EPSG:4326)")
    return "EPSG:4326"


def validate_geometry_type(geom_type: str) -> None:
    if geom_type not in SUPPORTED_GEOMETRY_TYPES:
        print(f"Error: Unsupported geometry type: {geom_type}", file=sys.stderr)
        sys.exit(1)


def stream_features(path: Path) -> Any:
    """Stream features from a GeoJSON file using ijson."""
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "rb") as f:
        # ijson yields events; we parse the 'features.item' path to get features
        parser = ijson.items(f, "features.item")
        for feature in parser:
            yield feature


def stream_geojson(path: Path) -> Any:
    """Stream features and CRS from a GeoJSON file.

    Yields:
        Tuple of (feature, crs) where crs is the EPSG string or "EPSG:4326" default.
    """
    crs = "EPSG:4326"
    with open(path, "rb") as f:
        # First pass: extract crs from the root object
        for prefix, event, value in ijson.parse(f):
            if prefix == "crs.properties.name" and event == "string":
                if value.startswith("EPSG:"):
                    crs = value
                    break
    # Reset file and stream features
    with open(path, "rb") as f:
        parser = ijson.items(f, "features.item")
        for feature in parser:
            yield feature, crs