import json
import pytest
from pathlib import Path
from src.geojson_parser import (
    parse_geojson,
    validate_featurecollection,
    extract_features,
    detect_crs,
    stream_features,
    stream_geojson,
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


def test_stream_features_yields_features(tmp_path):
    import ijson
    fc = {
        "type": "FeatureCollection",
        "crs": {"type": "name", "properties": {"name": "EPSG:2326"}},
        "features": [
            {"type": "Feature", "geometry": {"type": "Point", "coordinates": [1, 2]}, "properties": {"NAME_EN": "Park A"}},
            {"type": "Feature", "geometry": {"type": "Point", "coordinates": [3, 4]}, "properties": {"NAME_EN": "Park B"}},
        ]
    }
    path = tmp_path / "test.json"
    path.write_text(json.dumps(fc))
    features = list(stream_features(path))
    assert len(features) == 2


def test_stream_features_extracts_crs(tmp_path):
    from pyproj import Transformer

    fc = {
        "type": "FeatureCollection",
        "crs": {"type": "name", "properties": {"name": "EPSG:2326"}},
        "features": [
            {"type": "Feature", "geometry": {"type": "Point", "coordinates": [1, 2]}, "properties": {"NAME_EN": "Park"}},
        ]
    }
    path = tmp_path / "test.json"
    path.write_text(json.dumps(fc))
    result = list(stream_geojson(path))
    assert len(result) == 1
    feature, crs, transformer = result[0]
    assert crs == "EPSG:2326"


def test_stream_geojson_yields_three_values(tmp_path):
    """stream_geojson should yield (feature, crs, transformer) tuples."""
    from pyproj import Transformer

    fc = {
        "type": "FeatureCollection",
        "crs": {"type": "name", "properties": {"name": "EPSG:2326"}},
        "features": [
            {"type": "Feature", "geometry": {"type": "Point", "coordinates": [1, 2]}, "properties": {"NAME_EN": "Park A"}},
            {"type": "Feature", "geometry": {"type": "Point", "coordinates": [3, 4]}, "properties": {"NAME_EN": "Park B"}},
        ]
    }
    path = tmp_path / "test.json"
    path.write_text(json.dumps(fc))
    for feature, crs, transformer in stream_geojson(path):
        assert isinstance(feature, dict)
        assert isinstance(crs, str)
        assert isinstance(transformer, Transformer)
        break  # Only check first item


def test_transformer_is_reused(tmp_path):
    """The same transformer instance should be used for all features."""
    from pyproj import Transformer

    fc = {
        "type": "FeatureCollection",
        "crs": {"type": "name", "properties": {"name": "EPSG:2326"}},
        "features": [
            {"type": "Feature", "geometry": {"type": "Point", "coordinates": [1, 2]}, "properties": {"NAME_EN": "Park A"}},
            {"type": "Feature", "geometry": {"type": "Point", "coordinates": [3, 4]}, "properties": {"NAME_EN": "Park B"}},
            {"type": "Feature", "geometry": {"type": "Point", "coordinates": [5, 6]}, "properties": {"NAME_EN": "Park C"}},
        ]
    }
    path = tmp_path / "test.json"
    path.write_text(json.dumps(fc))
    transformers = []
    for feature, crs, transformer in stream_geojson(path):
        transformers.append(transformer)
    # All transformers should be the same instance
    assert len(set(id(t) for t in transformers)) == 1, "Transformer should be reused"