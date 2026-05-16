import pytest
from pyproj import Transformer
from src.crs_transformer import (
    transform_geometry,
    calculate_bbox,
)


class TestTransformGeometry:
    @pytest.fixture
    def transformer_2326(self):
        return Transformer.from_crs("EPSG:2326", "EPSG:4326", always_xy=True)

    def test_transform_point_geometry(self, transformer_2326):
        geom = {"type": "Point", "coordinates": [848550, 817395]}
        result = transform_geometry(geom, transformer_2326)
        assert result["type"] == "Point"
        assert len(result["coordinates"]) == 2
        assert 114.2 < result["coordinates"][0] < 114.4

    def test_transform_linestring_geometry(self, transformer_2326):
        geom = {
            "type": "LineString",
            "coordinates": [[848550, 817395], [848560, 817400]],
        }
        result = transform_geometry(geom, transformer_2326)
        assert result["type"] == "LineString"
        assert len(result["coordinates"]) == 2
        assert 114.2 < result["coordinates"][0][0] < 114.4

    def test_transform_polygon_geometry(self, transformer_2326):
        geom = {
            "type": "Polygon",
            "coordinates": [[[848550, 817395], [848560, 817400], [848550, 817395]]],
        }
        result = transform_geometry(geom, transformer_2326)
        assert result["type"] == "Polygon"
        assert len(result["coordinates"]) == 1
        assert len(result["coordinates"][0]) == 3

    def test_transform_multipoint_geometry(self, transformer_2326):
        geom = {
            "type": "MultiPoint",
            "coordinates": [[848550, 817395], [848560, 817400]],
        }
        result = transform_geometry(geom, transformer_2326)
        assert result["type"] == "MultiPoint"
        assert len(result["coordinates"]) == 2


class TestCalculateBBox:
    def test_bbox_point(self):
        coords = [114.26, 22.31]
        bbox = calculate_bbox(coords)
        assert bbox == [114.26, 22.31, 114.26, 22.31]

    def test_bbox_polygon(self):
        coords = [
            [[114.2, 22.3], [114.3, 22.3], [114.3, 22.4], [114.2, 22.4], [114.2, 22.3]],
            [[114.25, 22.35], [114.26, 22.35], [114.26, 22.36], [114.25, 22.36], [114.25, 22.35]],
        ]
        bbox = calculate_bbox(coords)
        assert bbox[0] == pytest.approx(114.2, abs=0.01)
        assert bbox[1] == pytest.approx(22.3, abs=0.01)
        assert bbox[2] == pytest.approx(114.3, abs=0.01)
        assert bbox[3] == pytest.approx(22.4, abs=0.01)
