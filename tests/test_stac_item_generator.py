import pytest
from src.stac_item_generator import (
    generate_item_id,
    handle_duplicate_ids,
    feature_to_item,
    write_items_featurecollection,
)


class TestGenerateItemID:
    def test_id_from_name_en(self):
        feature = {"properties": {"NAME_EN": "Clear Water Bay Country Park"}}
        item_id = generate_item_id(feature)
        assert item_id == "clear-water-bay-country-park"

    def test_id_fallback_to_objectid(self):
        feature = {"properties": {"OBJECTID": 42}}
        item_id = generate_item_id(feature)
        assert item_id == "item-42"

    def test_id_name_en_snake_to_kebab(self):
        feature = {"properties": {"NAME_EN": "Sai_Kung_East Country_Park"}}
        item_id = generate_item_id(feature)
        assert item_id == "sai-kung-east-country-park"

    def test_id_fallback_to_index(self):
        feature = {"properties": {}}
        item_id = generate_item_id(feature, fallback_index=5)
        assert item_id == "item-5"

    def test_id_no_fallback_raises(self):
        feature = {"properties": {}}
        with pytest.raises(ValueError, match="NAME_EN or OBJECTID"):
            generate_item_id(feature)


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
    def test_inline_duplicate_tracking(self):
        seen_ids = {}
        feature1 = {"properties": {"NAME_EN": "Park A"}, "geometry": {"type": "Point", "coordinates": [114.0, 22.0]}}
        feature2 = {"properties": {"NAME_EN": "Park A"}, "geometry": {"type": "Point", "coordinates": [114.1, 22.1]}}  # duplicate

        item1 = feature_to_item(feature1, "EPSG:4326", seen_ids)
        item2 = feature_to_item(feature2, "EPSG:4326", seen_ids)

        assert item1["id"] == "park-a"
        assert item2["id"] == "park-a-1"
        assert seen_ids == {"park-a": 1, "park-a-1": 0}

    def test_point_feature_to_item(self):
        feature = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [848550, 817395]},
            "properties": {"OBJECTID": 1, "NAME_EN": "Clear Water Bay Country Park", "NAME_TC": "清水灣郊野公園"},
        }
        item = feature_to_item(feature, "EPSG:2326")
        assert item["id"] == "clear-water-bay-country-park"
        assert item["type"] == "Feature"
        assert item["properties"]["geometry_type"] == "Point"
        assert item["properties"]["OBJECTID"] == 1
        assert item["properties"]["NAME_EN"] == "Clear Water Bay Country Park"
        # Geometry should be transformed to WGS84
        assert 114.2 < item["geometry"]["coordinates"][0] < 114.4
        assert 22.2 < item["geometry"]["coordinates"][1] < 22.4


def test_write_items_featurecollection(tmp_path):
    import json
    items = [
        {"id": "park-a", "type": "Feature", "geometry": {}, "bbox": [], "properties": {}},
        {"id": "park-b", "type": "Feature", "geometry": {}, "bbox": [], "properties": {}},
    ]
    output_path = tmp_path / "items.json"
    write_items_featurecollection(items, str(output_path))

    with open(output_path) as f:
        result = json.load(f)
    assert result["type"] == "FeatureCollection"
    assert len(result["features"]) == 2
