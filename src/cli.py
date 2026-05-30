"""CLI entry point for geojson2stac."""
import sys
import typer
from pathlib import Path
from typing import Annotated
from convertor import convert_file


app = typer.Typer(help="Convert GeoJSON FeatureCollections to STAC Collections and Items")


@app.command()
def main(
    input_file: Annotated[Path, typer.Argument(
        readable=True,
        help="Path to GeoJSON file or glob pattern (e.g., data/*.json)"
    )] = None,
    output_dir: Path = typer.Option(
        Path("stac"), "--output", "-o", help="Output directory (default: stac/)"
    ),
    input_dir: Annotated[Path, typer.Option(
        "--input-dir", help="Directory containing GeoJSON files to convert"
    )] = None,
    output_format: str = typer.Option("stac", "--output-format", help="Output format: stac or bulk"),
    recursive: bool = typer.Option(False, "--recursive", help="Recursively scan subdirectories when used with --input-dir"),
    workers: int = typer.Option(
        1,
        "--workers",
        "-w",
        help="Number of parallel workers for batch conversion (default: 1, sequential)"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
) -> None:
    """Convert GeoJSON files to STAC format."""
    # Handle mutual exclusivity
    if input_file is not None and input_dir is not None:
        print("Error: Cannot use both INPUT_FILE and --input-dir. They are mutually exclusive.", file=sys.stderr)
        raise typer.Exit(1)

    # Validate input_file exists if provided (and not a glob pattern)
    if input_file is not None and '*' not in str(input_file) and not input_file.exists():
        print(f"Error: INPUT_FILE '{input_file}' does not exist.", file=sys.stderr)
        raise typer.Exit(1)

    # Collect files to process
    if input_dir is not None:
        files = expand_input_dir(input_dir, output_dir, recursive=recursive)
        if not files:
            print(f"Warning: No .json or .geojson files found in {input_dir}", file=sys.stderr)
            return
        mode = "directory"
    elif input_file is not None:
        input_str = str(input_file)
        if '*' in input_str:
            files = expand_input_pattern(input_file, output_dir)
            mode = "glob"
        else:
            files = [input_file]
            mode = "single"
    else:
        print("Error: Must provide INPUT_FILE or --input-dir", file=sys.stderr)
        raise typer.Exit(1)

    # Validate workers
    if workers < 1:
        print("Error: --workers must be at least 1", file=sys.stderr)
        raise typer.Exit(1)

    # Process files
    from concurrent.futures import ThreadPoolExecutor, as_completed

    def convert_one(file_path: Path, input_dir: Path | None, output_dir: Path,
                   output_format: str, recursive: bool, verbose: bool) -> tuple[Path, bool, str | None]:
        """Convert a single file. Returns (path, success, error_message)."""
        try:
            if verbose:
                print(f"Converting: {file_path}")

            if input_dir is not None and recursive:
                relative_subpath = file_path.parent.relative_to(input_dir)
                convert_file(file_path, output_dir, output_format=output_format, output_subdir=relative_subpath)
            else:
                convert_file(file_path, output_dir, output_format=output_format)
            return (file_path, True, None)
        except Exception as e:
            return (file_path, False, str(e))

    succeeded = 0
    failed = 0
    errors = []

    if workers == 1:
        # Sequential processing (original behavior)
        for file_path in files:
            path, ok, err = convert_one(file_path, input_dir, output_dir, output_format, recursive, verbose)
            if ok:
                succeeded += 1
            else:
                failed += 1
                errors.append((path, err))
    else:
        # Parallel processing
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(convert_one, fp, input_dir, output_dir, output_format, recursive, verbose): fp
                for fp in files
            }
            for future in as_completed(futures):
                path, ok, err = future.result()
                if ok:
                    succeeded += 1
                else:
                    failed += 1
                    errors.append((path, err))

    # Summary output
    if mode in ("directory", "glob"):
        if failed > 0:
            print(f"\nBatch complete: {succeeded} succeeded, {failed} failed", file=sys.stderr)
            for path, err in errors:
                print(f"  - {path}: {err}", file=sys.stderr)
            raise typer.Exit(1)
        else:
            print(f"\nBatch complete: {succeeded} succeeded")


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
        import glob as glob_module
        matches = glob_module.glob(input_str, recursive=False)
        return [Path(m) for m in matches if Path(m).is_file()]
    return [input_path] if input_path.is_file() else []


def expand_input_dir(input_dir: Path, output_dir: Path, recursive: bool = False) -> list[Path]:
    """
    Get all .json and .geojson files in a directory for batch conversion.

    Args:
        input_dir: Directory containing GeoJSON files
        output_dir: Output directory (unused, for API consistency)
        recursive: If True, scan subdirectories recursively

    Returns:
        List of .json and .geojson file paths in the directory
    """
    if not input_dir.is_dir():
        return []

    if recursive:
        # rglob finds files at all nesting levels; two calls needed for different extensions
        json_files = sorted(input_dir.rglob("*.json"))
        geojson_files = sorted(input_dir.rglob("*.geojson"))
        files = sorted(set(json_files) | set(geojson_files))
    else:
        # iterdir only finds immediate children
        files = sorted(f for f in input_dir.iterdir() if f.suffix in (".json", ".geojson") and f.is_file())

    return files


if __name__ == "__main__":
    app()
