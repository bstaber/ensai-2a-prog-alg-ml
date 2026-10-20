from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

MARP_VERSION = "4.2.3"
DECK = "session01"


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Render the pinned Marp deck.")
    parser.add_argument("output", nargs="?", default="build")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    output_dir = (root / args.output).resolve()
    if output_dir == root or output_dir in root.parents:
        parser.error("output must not be the repository root or one of its ancestors")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    (output_dir / "docs").mkdir(parents=True)

    for extension in ("html", "pdf"):
        render_deck(root, output_dir, DECK, extension)

    shutil.copytree(root / "docs" / "assets", output_dir / "docs" / "assets")
    shutil.copytree(root / "notebooks", output_dir / "notebooks")
    shutil.copy2(root / "site" / "index.html", output_dir / "index.html")
    print(f"Rendered {DECK} with Marp CLI {MARP_VERSION} into {output_dir}")


if __name__ == "__main__":
    main()
