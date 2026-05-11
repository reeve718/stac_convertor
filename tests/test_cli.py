from pathlib import Path
from cli import expand_input_pattern, expand_input_dir


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


def test_expand_input_dir():
    """--input-dir should return all .json files in directory."""
    files = expand_input_dir(Path("test-data"), Path("stac"))
    assert isinstance(files, list)
    assert all(f.suffix == ".json" for f in files)
    assert all(f.is_relative_to(Path("test-data")) for f in files)


def test_expand_input_dir_empty():
    """Empty directory should return empty list."""
    files = expand_input_dir(Path("test-data/empty_dir"), Path("stac"))
    assert files == []


def test_expand_input_dir_non_json_skipped():
    """Non-.json files should be silently skipped."""
    files = expand_input_dir(Path("test-data"), Path("stac"))
    assert all(f.suffix == ".json" for f in files)