import pytest
from src.stac_bulk_writer import transform_to_bulk_format

def test_transform_featurecollection_to_bulk_format():
    """STAC FeatureCollection transforms to bulk insert format."""
    stac_input = {
        "type": "FeatureCollection",
        "features": [
            {
                "id": "clear-water-bay-country-park",
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [114.29, 22.29]},
                "bbox": [114.29, 22.29, 114.29, 22.29],
                "properties": {
                    "datetime": "2026-04-29T16:32:59+00:00",
                    "OBJECTID": 1,
                    "NAME_EN": "Clear Water Bay Country Park",
                    "NAME_TC": "清水灣郊野公園",
                    "geometry_type": "Point"
                },
                "stac_version": "1.0.0",
                "links": [],
                "assets": {}
            }
        ]
    }
    collection_id = "ctry-park"
    result = transform_to_bulk_format(stac_input, collection_id)

    assert result == {
        "items": {
            "1": {
                "id": "1",
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [114.29, 22.29]},
                "bbox": [114.29, 22.29, 114.29, 22.29],
                "properties": {
                    "OBJECTID": 1,
                    "NAME_EN": "Clear Water Bay Country Park",
                    "NAME_TC": "清水灣郊野公園",
                    "datetime": "2026-04-29T16:32:59+00:00"
                },
                "collection": "ctry-park",
                "stac_version": "1.0.0"
            }
        },
        "method": "insert"
    }

def test_transform_uses_objectid_as_id():
    """OBJECTID from properties becomes item id as string."""
    stac_input = {
        "type": "FeatureCollection",
        "features": [
            {
                "id": "some-kebab-id",
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [114.29, 22.29]},
                "bbox": [114.29, 22.29, 114.29, 22.29],
                "properties": {
                    "OBJECTID": 42,
                    "NAME_EN": "Test"
                },
                "stac_version": "1.0.0",
                "links": [],
                "assets": {}
            }
        ]
    }
    result = transform_to_bulk_format(stac_input, "test-collection")
    assert result["items"]["42"]["id"] == "42"

def test_transform_strips_links_and_assets():
    """Bulk format does not include links or assets."""
    stac_input = {
        "type": "FeatureCollection",
        "features": [
            {
                "id": "item-1",
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [0, 0]},
                "bbox": [0, 0, 0, 0],
                "properties": {"OBJECTID": 1},
                "stac_version": "1.0.0",
                "links": [{"rel": "self", "href": "items.json"}],
                "assets": {"thumbnail": {"href": "thumb.png"}}
            }
        ]
    }
    result = transform_to_bulk_format(stac_input, "collection")
    assert "links" not in result["items"]["1"]
    assert "assets" not in result["items"]["1"]

def test_transform_default_datetime():
    """Missing datetime uses default '1900-01-01T00:00:00'."""
    stac_input = {
        "type": "FeatureCollection",
        "features": [
            {
                "id": "item-1",
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [0, 0]},
                "bbox": [0, 0, 0, 0],
                "properties": {"OBJECTID": 1},
                "stac_version": "1.0.0",
                "links": [],
                "assets": {}
            }
        ]
    }
    result = transform_to_bulk_format(stac_input, "collection")
    assert result["items"]["1"]["properties"]["datetime"] == "1900-01-01T00:00:00"

def test_transform_adds_collection_field():
    """Each item gets collection field from parameter."""
    stac_input = {
        "type": "FeatureCollection",
        "features": [
            {
                "id": "item-1",
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [0, 0]},
                "bbox": [0, 0, 0, 0],
                "properties": {"OBJECTID": 1},
                "stac_version": "1.0.0",
                "links": [],
                "assets": {}
            }
        ]
    }
    result = transform_to_bulk_format(stac_input, "my-collection")
    assert result["items"]["1"]["collection"] == "my-collection"

def test_transform_multiple_items():
    """Multiple features become multiple string-keyed items."""
    stac_input = {
        "type": "FeatureCollection",
        "features": [
            {
                "id": "item-1",
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [0, 0]},
                "bbox": [0, 0, 0, 0],
                "properties": {"OBJECTID": 1},
                "stac_version": "1.0.0",
                "links": [],
                "assets": {}
            },
            {
                "id": "item-2",
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [1, 1]},
                "bbox": [1, 1, 1, 1],
                "properties": {"OBJECTID": 2},
                "stac_version": "1.0.0",
                "links": [],
                "assets": {}
            }
        ]
    }
    result = transform_to_bulk_format(stac_input, "collection")
    assert "1" in result["items"]
    assert "2" in result["items"]
    assert result["items"]["1"]["id"] == "1"
    assert result["items"]["2"]["id"] == "2"
    assert result["method"] == "insert"