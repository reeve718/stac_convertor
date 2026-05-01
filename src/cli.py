"""CLI entry point for geojson2stac."""
import sys
import typer
from pathlib import Path
from typing import Annotated
from convertor import convert_file


app = typer.Typer(help="Convert GeoJSON FeatureCollections to STAC Collections and Items")


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
