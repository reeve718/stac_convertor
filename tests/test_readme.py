"""Validate README.md meets spec requirements."""
from pathlib import Path

ROOT = Path(__file__).parent.parent
README = ROOT / "README.md"


def read_readme():
    return README.read_text(encoding="utf-8")


def test_readme_exists():
    assert README.exists(), "README.md must exist at repo root"


def test_readme_has_installation_section():
    content = read_readme()
    assert "Installation" in content
    assert "pip install" in content
    assert "editable" in content.lower()


def test_readme_has_quick_start():
    content = read_readme()
    assert "Quick Start" in content
    assert "CTRY_PARK" in content
    assert "geojson2stac" in content


def test_readme_documents_cli_arguments():
    content = read_readme()
    assert "INPUT_FILE" in content or "input_file" in content.lower()
    assert "--output" in content or "-o" in content
    assert "--verbose" in content or "-v" in content


def test_readme_has_development_setup():
    content = read_readme()
    assert "Development" in content
    assert "pytest" in content
    assert "clone" in content.lower()


def test_readme_has_license():
    content = read_readme()
    assert "License" in content or "LICENSE" in content


def test_readme_has_crs_explanation():
    content = read_readme()
    assert "CRS" in content or "crs" in content.lower()
    assert "WGS84" in content or "EPSG:4326" in content
