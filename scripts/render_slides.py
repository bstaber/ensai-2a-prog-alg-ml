from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

MARP_VERSION = "4.2.3"
DECKS = (
    "introduction",
    "python101",
    "numpy101",
    "linear_regression",
    "python_tooling",
)


def render_deck(root: Path, output_dir: Path, deck: str, extension: str) -> None:
    source = root / "docs" / f"{deck}.md"
    destination = output_dir / "docs" / f"{deck}.{extension}"
    command = [
        "npx",
        "--yes",
        f"@marp-team/marp-cli@{MARP_VERSION}",
        str(source),
        "--theme-set",
        str(root / "css" / "rose-pine.css"),
        "--allow-local-files",
        "--no-stdin",
        "--output",
        str(destination),
    ]
    result = subprocess.run(
        command,
        cwd=root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(result.stdout, end="")
    if result.returncode != 0:
        raise SystemExit(result.returncode)
    missing_file_warnings = (
        "Some of the local files are missing",
        "The local file is missing",
    )
    if any(warning in result.stdout for warning in missing_file_warnings):
        raise RuntimeError(f"Marp reported a missing local file in {source}")


def write_index(output_dir: Path) -> None:
    links = "\n".join(
        f'<li><a href="docs/{deck}.html">{deck.replace("_", " ").title()}</a> '
        f'(<a href="docs/{deck}.pdf">PDF</a>)</li>'
        for deck in DECKS
    )
    (output_dir / "index.html").write_text(
        f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Python and NumPy for machine learning</title>
<style>
body {{ max-width: 52rem; margin: 4rem auto; padding: 0 1.5rem;
       font: 1.15rem/1.6 system-ui, sans-serif; color: #e0def4; background: #191724; }}
a {{ color: #c4a7e7; }} li {{ margin: .7rem 0; }}
</style>
<h1>Python and NumPy for machine learning</h1>
<p>A three-hour bridge for mathematically trained students with prior programming experience.</p>
<ul>{links}</ul>
<p><a href="notebooks/session01_starter.ipynb">Starter notebook</a> ·
<a href="notebooks/session01_solution.ipynb">Solution notebook</a></p>
""",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Render the pinned Marp decks.")
    parser.add_argument("output", nargs="?", default="build")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    output_dir = (root / args.output).resolve()
    if output_dir == root or output_dir in root.parents:
        parser.error("output must not be the repository root or one of its ancestors")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    (output_dir / "docs").mkdir(parents=True)

    for deck in DECKS:
        for extension in ("html", "pdf"):
            render_deck(root, output_dir, deck, extension)

    shutil.copytree(root / "docs" / "assets", output_dir / "docs" / "assets")
    shutil.copytree(root / "notebooks", output_dir / "notebooks")
    write_index(output_dir)
    print(f"Rendered {len(DECKS)} decks with Marp CLI {MARP_VERSION} into {output_dir}")


if __name__ == "__main__":
    main()
