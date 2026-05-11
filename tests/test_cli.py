from pathlib import Path
from cli import expand_input_pattern


def test_expand_input_pattern_glob():
    """Glob patterns with * should expand to matching files."""
    files = expand_input_pattern(Path("test-data/*.json"), Path("stac"))
    assert isinstance(files, list)
    assert all(f.suffix == ".json" for f in files)


def test_expand_input_pattern_single_file():
    """Non-glob path should return list with single file."""
    files = expand_input_pattern(Path("test-data/CTRY_PARK.json"), Path("stac"))
    assert files == [Path("test-data/CTRY_PARK.json")]


def test_expand_input_pattern_no_matches():
    """Glob with no matches should return empty list."""
    files = expand_input_pattern(Path("test-data/nonexistent*.json"), Path("stac"))
    assert files == []