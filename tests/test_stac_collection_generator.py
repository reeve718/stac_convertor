import pytest
from src.stac_collection_generator import generate_collection, write_collection
from datetime import datetime, timezone


class TestGenerateCollection:
    def test_collection_id_from_filename(self):
        items = []
        collection = generate_collection("CTRY_PARK", items)
        assert collection["id"] == "ctry-park"

    def test_collection_has_required_fields(self):
        items = []
        collection = generate_collection("test-data", items)
        required = ["id", "type", "stac_version", "geometry", "bbox", "properties",
                    "links", "keywords", "providers", "extent"]
        for field in required:
            assert field in collection, f"Missing field: {field}"
        assert collection["type"] == "Collection"
        assert collection["stac_version"] == "1.0.0"

    def test_collection_bbox_from_items(self):
        items = [
            {"bbox": [114.0, 22.0, 114.1, 22.1]},
            {"bbox": [114.2, 22.2, 114.3, 22.3]},
        ]
        collection = generate_collection("multi-item", items)
        assert collection["bbox"] == [114.0, 22.0, 114.3, 22.3]

    def test_collection_links(self):
        collection = generate_collection("test", [])
        link_rels = [link["rel"] for link in collection["links"]]
        assert "self" in link_rels
        assert "items" in link_rels