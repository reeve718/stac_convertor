from pathlib import Path
from typer.testing import CliRunner
from cli import expand_input_pattern, expand_input_dir, app

runner = CliRunner()


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


def test_mutual_exclusivity_error():
    """Providing both input_file and --input-dir should error."""
    result = runner.invoke(app, ["data/CTRY_PARK.json", "--input-dir", "data/"])
    assert result.exit_code != 0
    assert "mutually exclusive" in result.output.lower() or "cannot use both" in result.output.lower()


def test_batch_convert_directory(tmp_path):
    """--input-dir should convert all .json files in directory."""
    # Create test input files
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    stac_dir = tmp_path / "stac"

    # Copy actual sample data for testing
    sample = Path("test-data/CTRY_PARK.json")
    if sample.exists():
        (data_dir / "file1.json").write_bytes(sample.read_bytes())
        (data_dir / "file2.json").write_bytes(sample.read_bytes())

        result = runner.invoke(app, ["--input-dir", str(data_dir), "-o", str(stac_dir)])

        assert result.exit_code == 0
        assert (stac_dir / "file1").exists()
        assert (stac_dir / "file2").exists()
        assert (stac_dir / "file1" / "collection.json").exists()
        assert (stac_dir / "file2" / "collection.json").exists()


def test_batch_error_handling_continues(tmp_path):
    """If one file fails, processing continues and reports at end."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    stac_dir = tmp_path / "stac"

    # Create a corrupt file and a valid one
    (data_dir / "valid.json").write_text('{"type":"FeatureCollection","features":[]}')
    (data_dir / "invalid.json").write_text('not json')

    result = runner.invoke(app, ["--input-dir", str(data_dir), "-o", str(stac_dir)])

    # Should complete with non-zero exit and report failure
    assert result.exit_code != 0
    assert "1 succeeded, 1 failed" in result.output, f"Expected batch summary, got: {result.output}"


def test_expand_input_dir_accepts_geojson_extension(tmp_path):
    """When directory contains .geojson files, they should be included in batch conversion."""
    # Arrange
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "file1.json").write_text('{"type": "FeatureCollection", "features": []}')
    (data_dir / "file2.geojson").write_text('{"type": "FeatureCollection", "features": []}')

    # Act
    from cli import expand_input_dir
    result = expand_input_dir(data_dir, tmp_path / "out")

    # Assert
    assert len(result) == 2
    assert any(f.suffix == ".json" for f in result)
    assert any(f.suffix == ".geojson" for f in result)


def test_expand_input_dir_recursive(tmp_path):
    """expand_input_dir with recursive=True should find nested files."""
    input_dir = tmp_path / "data"
    input_dir.mkdir()
    (input_dir / "root.json").write_text('{"type":"FeatureCollection","features":[]}')

    sub_dir = input_dir / "sub"
    sub_dir.mkdir()
    (sub_dir / "nested.json").write_text('{"type":"FeatureCollection","features":[]}')

    deep_dir = sub_dir / "deep"
    deep_dir.mkdir()
    (deep_dir / "deep_nested.json").write_text('{"type":"FeatureCollection","features":[]}')

    files = expand_input_dir(input_dir, Path("stac"), recursive=True)
    file_names = {f.name for f in files}

    assert "root.json" in file_names
    assert "nested.json" in file_names
    assert "deep_nested.json" in file_names


def test_expand_input_dir_non_recursive(tmp_path):
    """expand_input_dir with recursive=False should NOT find nested files."""
    input_dir = tmp_path / "data"
    input_dir.mkdir()
    (input_dir / "root.json").write_text('{"type":"FeatureCollection","features":[]}')

    sub_dir = input_dir / "sub"
    sub_dir.mkdir()
    (sub_dir / "nested.json").write_text('{"type":"FeatureCollection","features":[]}')

    files = expand_input_dir(input_dir, Path("stac"), recursive=False)
    file_names = {f.name for f in files}

    assert "root.json" in file_names
    assert "nested.json" not in file_names  # Should NOT be found


def test_relative_path_computation(tmp_path):
    """Output subdirectory should mirror input folder structure."""
    input_dir = tmp_path / "data"
    input_dir.mkdir()

    sub_dir = input_dir / "sub"
    sub_dir.mkdir()

    file_path = sub_dir / "file.json"
    file_path.write_text('{"type":"FeatureCollection","features":[]}')

    relative_to_input = file_path.parent.relative_to(input_dir)
    assert str(relative_to_input) == "sub"