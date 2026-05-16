"""Transform GeoJSON coordinates between CRS."""
from pyproj import Transformer
from typing import Any


def transform_point(x: float, y: float, from_crs: str) -> tuple[float, float]:
    """Transform a single point from source CRS to WGS84."""
    transformer = Transformer.from_crs(from_crs, "EPSG:4326", always_xy=True)
    lon, lat = transformer.transform(x, y)
    return float(lon), float(lat)


def transform_geometry(geometry: dict[str, Any], transformer: Transformer) -> dict[str, Any]:
    """Transform all coordinates in a GeoJSON geometry to WGS84."""
    geom_type = geometry["type"]
    coords = geometry["coordinates"]

    if geom_type == "Point":
        lon, lat = transformer.transform(coords[0], coords[1])
        return {"type": "Point", "coordinates": [float(lon), float(lat)]}

    elif geom_type == "LineString":
        return {
            "type": "LineString",
            "coordinates": [
                [float(lon), float(lat)] for lon, lat in (transformer.transform(x, y) for x, y in coords)
            ],
        }

    elif geom_type == "Polygon":
        return {
            "type": "Polygon",
            "coordinates": [
                [
                    [float(lon), float(lat)] for lon, lat in (transformer.transform(x, y) for x, y in ring)
                ]
                for ring in coords
            ],
        }

    elif geom_type == "MultiPoint":
        return {
            "type": "MultiPoint",
            "coordinates": [
                [float(lon), float(lat)] for lon, lat in (transformer.transform(x, y) for x, y in coords)
            ],
        }

    elif geom_type == "MultiLineString":
        return {
            "type": "MultiLineString",
            "coordinates": [
                [
                    [float(lon), float(lat)] for lon, lat in (transformer.transform(x, y) for x, y in line)
                ]
                for line in coords
            ],
        }

    elif geom_type == "MultiPolygon":
        return {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [
                        [float(lon), float(lat)] for lon, lat in (transformer.transform(x, y) for x, y in ring)
                    ]
                    for ring in poly
                ]
                for poly in coords
            ],
        }

    else:
        raise ValueError(f"Unknown geometry type: {geom_type}")


def calculate_bbox(coordinates: Any) -> list[float]:
    """Calculate bounding box [min_x, min_y, max_x, max_y] from coordinates."""
    all_coords = _flatten_coords(coordinates)
    if not all_coords:
        return [0.0, 0.0, 0.0, 0.0]
    lons = [c[0] for c in all_coords]
    lats = [c[1] for c in all_coords]
    return [min(lons), min(lats), max(lons), max(lats)]


def _flatten_coords(coords: Any) -> list[tuple[float, float]]:
    """Recursively flatten coordinate arrays to a list of (x, y) tuples."""
    result = []
    if coords and isinstance(coords[0], list):
        for item in coords:
            result.extend(_flatten_coords(item))
    elif coords and isinstance(coords[0], (int, float)):
        result.append((float(coords[0]), float(coords[1])))
    return result
