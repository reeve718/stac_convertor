import pytest
from src.stac_item_generator import (
    generate_item_id,
    handle_duplicate_ids,
    feature_to_item,
)


class TestGenerateItemID:
    def test_id_from_name_en(self):
        feature = {"properties": {"NAME_EN": "Clear Water Bay Country Park"}}
        item_id = generate_item_id(feature, "EPSG:2326")
        assert item_id == "clear-water-bay-country-park"

    def test_id_fallback_to_objectid(self):
        feature = {"properties": {"OBJECTID": 42}}
        item_id = generate_item_id(feature, "EPSG:2326")
        assert item_id == "item-42"

    def test_id_name_en_snake_to_kebab(self):
        feature = {"properties": {"NAME_EN": "Sai_Kung_East Country_Park"}}
        item_id = generate_item_id(feature, "EPSG:2326")
        assert item_id == "sai-kung-east-country-park"


class TestHandleDuplicateIDs:
    def test_no_duplicates(self):
        items = [
            {"id": "a", "geometry": {}},
            {"id": "b", "geometry": {}},
        ]
        result = handle_duplicate_ids(items)
        ids = [item["id"] for item in result]
        assert ids == ["a", "b"]

    def test_duplicate_appends_suffix(self):
        items = [
            {"id": "park", "geometry": {}},
            {"id": "park", "geometry": {}},
        ]
        result = handle_duplicate_ids(items)
        ids = [item["id"] for item in result]
        assert ids == ["park", "park-1"]


class TestFeatureToItem:
    def test_point_feature_to_item(self):
        feature = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [848550, 817395]},
            "properties": {"OBJECTID": 1, "NAME_EN": "Clear Water Bay Country Park", "NAME_TC": "清水灣郊野公園"},
        }
        item = feature_to_item(feature, "EPSG:2326", "ctry-park")
        assert item["id"] == "clear-water-bay-country-park"
        assert item["type"] == "Feature"
        assert item["properties"]["geometry_type"] == "Point"
        assert item["properties"]["OBJECTID"] == 1
        assert item["properties"]["NAME_EN"] == "Clear Water Bay Country Park"
        # Geometry should be transformed to WGS84
        assert 114.2 < item["geometry"]["coordinates"][0] < 114.4
        assert 22.2 < item["geometry"]["coordinates"][1] < 22.4
