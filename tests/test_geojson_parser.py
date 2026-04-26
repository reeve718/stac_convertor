import json
import pytest
from pathlib import Path
from src.geojson_parser import (
    parse_geojson,
    validate_featurecollection,
    extract_features,
    detect_crs,
)


class TestParseGeoJSON:
    def test_parse_valid_featurecollection(self, tmp_path):
        fc = {"type": "FeatureCollection", "features": []}
        path = tmp_path / "test.json"
        path.write_text(json.dumps(fc))
        result = parse_geojson(path)
        assert result["type"] == "FeatureCollection"

    def test_parse_missing_file(self):
        with pytest.raises(SystemExit):
            parse_geojson(Path("/nonexistent/file.json"))

    def test_parse_invalid_json(self, tmp_path):
        path = tmp_path / "invalid.json"
        path.write_text("not valid json {")
        with pytest.raises(SystemExit):
            parse_geojson(path)

    def test_parse_not_featurecollection(self, tmp_path):
        path = tmp_path / "notfc.json"
        path.write_text(json.dumps({"type": "Feature", "geometry": None, "properties": {}}))
        with pytest.raises(SystemExit):
            parse_geojson(path)


class TestExtractFeatures:
    def test_extract_multiple_features(self):
        fc = {
            "type": "FeatureCollection",
            "features": [
                {"type": "Feature", "geometry": None, "properties": {"id": 1}},
                {"type": "Feature", "geometry": None, "properties": {"id": 2}},
            ],
        }
        features = extract_features(fc)
        assert len(features) == 2

    def test_extract_empty_features(self):
        fc = {"type": "FeatureCollection", "features": []}
        with pytest.raises(SystemExit):
            extract_features(fc)


class TestDetectCRS:
    def test_detect_epsg_2326(self):
        fc = {
            "type": "FeatureCollection",
            "crs": {"type": "name", "properties": {"name": "EPSG:2326"}},
            "features": [],
        }
        assert detect_crs(fc) == "EPSG:2326"

    def test_detect_wgs84_fallback(self, capsys):
        fc = {"type": "FeatureCollection", "features": []}
        crs = detect_crs(fc)
        assert crs == "EPSG:4326"
        captured = capsys.readouterr()
        assert "WGS84" in captured.out

    def test_detect_epsg_4326_explicit(self):
        fc = {
            "type": "FeatureCollection",
            "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
            "features": [],
        }
        assert detect_crs(fc) == "EPSG:4326"