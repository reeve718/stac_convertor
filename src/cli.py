"""CLI entry point for geojson2stac."""
import sys
import glob as glob_module
import typer
from pathlib import Path
from typing import Annotated
from convertor import convert_file


app = typer.Typer(help="Convert GeoJSON FeatureCollections to STAC Collections and Items")


def expand_input_pattern(input_path: Path, output_dir: Path) -> list[Path]:
    """
    Expand input path to list of matching file paths.

    If input_path contains '*', treat as glob pattern and expand.
    Otherwise, return single-element list.

    Args:
        input_path: File path or glob pattern
        output_dir: Output directory (unused, for API consistency)

    Returns:
        List of matching file paths
    """
    input_str = str(input_path)
    if '*' in input_str:
        matches = glob_module.glob(input_str, recursive=False)
        return [Path(m) for m in matches if Path(m).is_file()]
    return [input_path] if input_path.is_file() else []


def expand_input_dir(input_dir: Path, output_dir: Path) -> list[Path]:
    """
    Get all .json files in a directory for batch conversion.

    Args:
        input_dir: Directory containing GeoJSON files
        output_dir: Output directory (unused, for API consistency)

    Returns:
        List of .json file paths in the directory
    """
    if not input_dir.is_dir():
        return []
    return sorted([f for f in input_dir.iterdir() if f.suffix == ".json" and f.is_file()])


@app.command()
def main(
    input_file: Path = typer.Argument(..., exists=True, readable=True, help="Path to GeoJSON file"),
    output_dir: Path = typer.Option(
        Path("stac"), "--output", "-o", help="Output directory (default: stac/)"
    ),
    output_format: Annotated[str, typer.Option("--output-format", help="Output format: stac or bulk")] = "stac",
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
) -> None:
    if verbose:
        print(f"Converting: {input_file}")
        print(f"Output directory: {output_dir}")

    try:
        convert_file(input_file, output_dir, output_format=output_format)
        print(f"Successfully converted {input_file} -> {output_dir / input_file.stem}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
