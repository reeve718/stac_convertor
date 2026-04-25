import json
import pytest
from pathlib import Path
from src.convertor import convert_file


class TestConvertFile:
    def test_convert_creates_output_directory(self, tmp_path):
        geojson_path = tmp_path / "test.json"
        fc = {
            "type": "FeatureCollection",
            "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [114.26, 22.31]},
                    "properties": {"OBJECTID": 1, "NAME_EN": "Test Park"},
                },
            ],
        }
        geojson_path.write_text(json.dumps(fc))
        output_dir = tmp_path / "stac"
        convert_file(geojson_path, output_dir)
        assert (output_dir / "test").is_dir()

    def test_convert_creates_collection(self, tmp_path):
        geojson_path = tmp_path / "parks.json"
        fc = {
            "type": "FeatureCollection",
            "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [114.26, 22.31]},
                    "properties": {"OBJECTID": 1, "NAME_EN": "Test Park"},
                },
            ],
        }
        geojson_path.write_text(json.dumps(fc))
        output_dir = tmp_path / "stac"
        convert_file(geojson_path, output_dir)
        collection_path = output_dir / "parks" / "collection.json"
        assert collection_path.exists()
        collection = json.loads(collection_path.read_text())
        assert collection["id"] == "parks"

    def test_convert_creates_items(self, tmp_path):
        geojson_path = tmp_path / "parks.json"
        fc = {
            "type": "FeatureCollection",
            "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [114.26, 22.31]},
                    "properties": {"OBJECTID": 1, "NAME_EN": "Park One"},
                },
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [114.27, 22.32]},
                    "properties": {"OBJECTID": 2, "NAME_EN": "Park Two"},
                },
            ],
        }
        geojson_path.write_text(json.dumps(fc))
        output_dir = tmp_path / "stac"
        convert_file(geojson_path, output_dir)
        items_dir = output_dir / "parks" / "items"
        assert items_dir.is_dir()
        item_files = list(items_dir.glob("*.json"))
        assert len(item_files) == 2
