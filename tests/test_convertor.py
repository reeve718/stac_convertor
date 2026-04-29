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

    def test_convert_creates_items_json(self, tmp_path):
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
        items_path = output_dir / "parks" / "items.json"
        assert items_path.exists()
        items_data = json.loads(items_path.read_text())
        assert items_data["type"] == "FeatureCollection"
        assert len(items_data["features"]) == 2

    def test_convert_file_produces_items_json(self, tmp_path):
        import json
        input_path = tmp_path / "input.json"
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        geojson = {
            "type": "FeatureCollection",
            "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
            "features": [
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [114.3, 22.4]}, "properties": {"OBJECTID": 1, "NAME_EN": "Park A"}},
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [114.5, 22.6]}, "properties": {"OBJECTID": 2, "NAME_EN": "Park B"}},
            ]
        }
        input_path.write_text(json.dumps(geojson))

        convert_file(input_path, output_dir)

        items_path = output_dir / "input" / "items.json"
        collection_path = output_dir / "input" / "collection.json"

        assert items_path.exists(), "items.json should exist"
        assert collection_path.exists(), "collection.json should exist"

        with open(items_path) as f:
            items_data = json.load(f)
        assert items_data["type"] == "FeatureCollection"
        assert len(items_data["features"]) == 2

        with open(collection_path) as f:
            collection_data = json.load(f)
        assert collection_data["type"] == "Collection"
