from __future__ import annotations

import argparse
import contextlib
import io
import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote

import nbformat
import numpy as np
import pymupdf
from nbclient import NotebookClient

DECKS = {
    "introduction": 6,
    "python101": 28,
    "numpy101": 16,
    "linear_regression": 10,
}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"```(python|bash|text)\n(.*?)```", re.DOTALL)


def fail(message: str) -> None:
    raise AssertionError(message)


def validate_structure(root: Path) -> None:
    total = 0
    for name, expected in DECKS.items():
        path = root / "docs" / f"{name}.md"
        parts = path.read_text(encoding="utf-8").split("\n---\n")
        slides = parts[1:]
        if len(slides) != expected:
            fail(f"{path}: expected {expected} slides, found {len(slides)}")
        for number, slide in enumerate(slides, 1):
            visible = re.sub(r"<!--.*?-->", "", slide, flags=re.DOTALL).strip()
            if not visible or not re.search(r"^#{1,2} ", visible, flags=re.MULTILINE):
                fail(f"{path}: slide {number} is empty or has no heading")
        total += len(slides)
    if total != 60:
        fail(f"expected 60 total slides, found {total}")

    for relative in [
        "README.md",
        *[f"docs/{name}.md" for name in DECKS],
        "docs/instructor_guide.md",
    ]:
        path = root / relative
        text = path.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().split()[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if target and not (path.parent / target).resolve().exists():
                fail(f"{path}: missing local link or asset {raw_target!r}")

    core = "\n".join((root / "docs" / f"{name}.md").read_text() for name in DECKS)
    if "TP1_Ridge" in core:
        fail("accidental TP1_Ridge material entered a core deck")

    python_deck = (root / "docs" / "python101.md").read_text(encoding="utf-8")
    python_exercise = python_deck.split("## Exercise · pure-Python MSE", 1)[1].split(
        "## Python checklist for today", 1
    )[0]
    guide = (root / "docs" / "instructor_guide.md").read_text(encoding="utf-8")
    if "mse_py" not in python_exercise:
        fail("Python deck exercise must use the notebook function name mse_py")
    # Scan the whole python101 document (including error-reading / traceback
    # examples) so no learner-facing string calls a bare `mse(...)` function.
    if re.search(r"\bmse\(", python_deck):
        fail("python101 deck must not call a bare mse( function; use mse_py")
    if "assert mse_py(" not in guide or "assert mse(" in guide:
        fail("instructor guide MSE checks must use mse_py")

    numpy_deck = (root / "docs" / "numpy101.md").read_text(encoding="utf-8")
    if "centered_rows" in numpy_deck or "centered_rows" in guide:
        fail("row-centering deck and guide must use the notebook name centered")

    regression = (root / "docs" / "linear_regression.md").read_text(encoding="utf-8")
    assessment = regression.split("## Mini-assessment · 10 minutes", 1)[1].split(
        "---", 1
    )[0]
    questions = re.findall(r"^\d+\. ", assessment, re.MULTILINE)
    required_assessment_terms = (
        "def predict",
        "column_stack",
        "(50, 1)",
        "default_rng(42)",
        "mean baseline",
        "unseen data",
        "lstsq",
        "invariant",
    )
    missing_terms = [
        term for term in required_assessment_terms if term not in assessment
    ]
    if len(questions) != 6 or missing_terms:
        fail(
            "final assessment must contain six outcome-aligned prompts; "
            f"found {len(questions)} and missing {missing_terms}"
        )

    readme = (root / "README.md").read_text(encoding="utf-8")
    readme_minutes = [
        int(value)
        for value in re.findall(
            r"^\| \d\d:\d\d–\d\d:\d\d \|.*?\| (\d+) \|$", readme, re.MULTILINE
        )
    ]
    guide_minutes = [
        int(value)
        for value in re.findall(
            r"^\| \d\d:\d\d–\d\d:\d\d \| (\d+) \|", guide, re.MULTILINE
        )
    ]
    for label, values in (
        ("README", readme_minutes),
        ("instructor guide", guide_minutes),
    ):
        if sum(values) != 180 or sum(values[:-1]) != 175 or values[-1] != 5:
            fail(f"{label}: expected 175 prepared + 5 contingency, got {values}")
    print(f"structure: {total} non-empty slides; local links/assets and timing pass")


def execute_python_deck(root: Path) -> None:
    text = (root / "docs" / "python101.md").read_text()
    # Teaching-path execution stops at the first appendix marker: appendix and
    # bonus examples are reference material and must not alter the timed-block
    # namespace (their plain-list dot-product code would otherwise overwrite
    # the shared x/y arrays asserted below).
    teaching_text = text.split("<!-- _class: appendix -->", 1)[0]
    blocks = FENCE_RE.findall(teaching_text)
    namespace: dict[str, Any] = {}
    fragments = 0
    for index, (language, source) in enumerate(blocks, 1):
        if language != "python":
            continue
        compiled = compile(source, f"python101 block {index}", "exec")
        partial = (
            "..." in source
            or "assert mse_py(" in source
            or ("y_true" in source and "def mse_py" not in source)
            or ("x_values" in source and "def " not in source)
        )
        if partial:
            fragments += 1
            continue
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compiled, namespace)  # noqa: S102  # Trusted repository example.
    x, y, mse_py = namespace["x"], namespace["y"], namespace["mse_py"]
    assert x.shape == y.shape == (50,)
    assert mse_py([1.0, 2.0], [1.0, 2.0]) == 0.0
    assert mse_py([1.0, 3.0], [2.0, 1.0]) == 2.5
    print(
        f"python deck: {sum(lang == 'python' for lang, _ in blocks)} fences parse; {fragments} fragments classified"
    )


def execute_numpy_deck(root: Path) -> None:
    blocks = FENCE_RE.findall((root / "docs" / "numpy101.md").read_text())
    namespace: dict[str, Any] = {}
    fragments = 0
    for index, (language, source) in enumerate(blocks, 1):
        if language != "python":
            continue
        compiled = compile(source, f"numpy101 block {index}", "exec")
        partial = (
            "..." in source
            or source.lstrip().startswith("points[0]")
            or source.lstrip().startswith("assert row_means")
            or source.lstrip().startswith("assert predictions")
        )
        if partial:
            fragments += 1
            continue
        if "squared_errors = (y - predictions)" in source:
            namespace["predictions"] = namespace["y"].copy()
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compiled, namespace)  # noqa: S102  # Trusted repository example.
        if "rng = np.random.default_rng(42)" in source:
            namespace["_shared_shapes"] = (namespace["x"].shape, namespace["y"].shape)
    assert namespace["_shared_shapes"] == ((50,), (50,))
    assert namespace["row_means"].shape == (3, 1)
    assert namespace["centered"].shape == (3, 2)
    assert np.allclose(namespace["centered"].mean(axis=1), 0.0)
    print(
        f"NumPy deck: {sum(lang == 'python' for lang, _ in blocks)} fences parse; "
        f"{fragments} fragments classified"
    )


def expect_value_error(call: Any) -> None:
    try:
        call()
    except ValueError:
        return
    fail("expected ValueError")


def execute_regression_deck(root: Path) -> None:
    blocks = FENCE_RE.findall((root / "docs" / "linear_regression.md").read_text())
    namespace: dict[str, Any] = {}
    fragments = 0
    for index, (language, source) in enumerate(blocks, 1):
        if language != "python":
            continue
        compiled = compile(source, f"linear_regression block {index}", "exec")
        if source.lstrip().startswith("assert predictions_np.shape"):
            fragments += 1
            continue
        if "def fit_linear_py" in source:
            namespace["mean_py"] = lambda values: sum(values) / len(values)
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compiled, namespace)  # noqa: S102  # Trusted repository example.
    slope = namespace["slope_np"]
    intercept = namespace["intercept_np"]
    mse = namespace["mse_value_np"]
    assert np.allclose([slope, intercept], [2.5242, 0.5373], rtol=1e-4, atol=1e-4)
    assert np.isclose(mse, 2.2939, rtol=1e-4, atol=1e-4)
    assert namespace["design"].shape == (50, 2)
    assert np.allclose(
        [slope, intercept],
        [namespace["slope_ls"], namespace["intercept_ls"]],
        rtol=1e-12,
        atol=1e-12,
    )
    fit_py = namespace["fit_linear_py"]
    expect_value_error(lambda: fit_py([], []))
    expect_value_error(lambda: fit_py([0.0, 1.0, 2.0], [0.0, 1.0]))
    fit_np = namespace["fit_linear_numpy"]
    for bad_x, bad_y in [
        (np.array([]), np.array([])),
        (np.ones(2), np.ones(3)),
        (np.ones((2, 1)), np.ones(2)),
        (np.ones(2), np.arange(2.0)),
    ]:
        expect_value_error(lambda bad_x=bad_x, bad_y=bad_y: fit_np(bad_x, bad_y))
    print(
        f"regression deck: {sum(lang == 'python' for lang, _ in blocks)} fences parse; {fragments} fragment classified"
    )


def validate_notebooks(root: Path) -> None:
    notebook_dir = root / "notebooks"
    loaded: dict[str, Any] = {}
    for name in ("session01_starter.ipynb", "session01_solution.ipynb"):
        notebook = nbformat.read(notebook_dir / name, as_version=4)
        outputs = sum(len(cell.get("outputs", [])) for cell in notebook.cells)
        counters = sum(
            cell.get("execution_count") is not None
            for cell in notebook.cells
            if cell.cell_type == "code"
        )
        if outputs or counters:
            fail(
                f"{name}: source must be output-free, got {outputs} outputs/{counters} counters"
            )
        loaded[name] = notebook

    starter = loaded["session01_starter.ipynb"]
    solution = loaded["session01_solution.ipynb"]
    for name, notebook in (("starter", starter), ("solution", solution)):
        notebook_text = "\n".join(cell.source for cell in notebook.cells)
        required_centering = (
            "# centered = ..." if name == "starter" else "centered = points - row_means"
        )
        if "centered_rows" in notebook_text or required_centering not in notebook_text:
            fail(f"{name} notebook row-centering contract must use centered")
    section_one: list[str] = []
    inside_section_one = False
    for cell in starter.cells:
        source = cell.source
        if cell.cell_type == "markdown" and source.startswith("## 1."):
            inside_section_one = True
        elif cell.cell_type == "markdown" and source.startswith("## 2."):
            inside_section_one = False
        if inside_section_one:
            section_one.append(source)
    section_one_text = "\n".join(section_one)
    definitions = re.findall(r"^def (\w+)\(", section_one_text, re.MULTILINE)
    required_mse_contract = (
        "**Time:** 15 minutes",
        "def mse_py",
        "assert mse_py([1.0, 2.0], [1.0, 2.0]) == 0.0",
        "assert mse_py([1.0, 3.0], [2.0, 1.0]) == 2.5",
        "Hint at minute 5 of the block",
        "empty and unequal inputs raise `ValueError`",
    )
    missing_contract = [
        term for term in required_mse_contract if term not in section_one_text
    ]
    if definitions != ["mse_py"] or missing_contract:
        fail(
            "starter Python exercise must be the bounded MSE-only micro-exercise; "
            f"definitions={definitions}, missing={missing_contract}"
        )

    solution.cells.append(
        nbformat.v4.new_code_cell(
            """import numpy as np

def expect_value_error_local(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError('expected ValueError')

expect_value_error_local(lambda: mean_py([]))
expect_value_error_local(lambda: covariance_py([1.0], []))
expect_value_error_local(lambda: fit_linear_py([1.0, 1.0], [2.0, 3.0]))
expect_value_error_local(lambda: mse_py([1.0], []))
expect_value_error_local(lambda: fit_linear_numpy(np.array([]), np.array([])))
expect_value_error_local(lambda: fit_linear_numpy(np.ones((2, 1)), np.ones(2)))
expect_value_error_local(lambda: fit_linear_numpy(np.ones(2), np.arange(2.0)))
expect_value_error_local(lambda: mse_numpy(np.array([]), np.array([])))
expect_value_error_local(lambda: mse_numpy(np.ones(2), np.ones(3)))
assert np.allclose([slope_py, intercept_py], [slope_np, intercept_np])
assert np.allclose([slope_np, intercept_np], [slope_lstsq, intercept_lstsq])
"""
        )
    )
    NotebookClient(solution, timeout=120, kernel_name="python3").execute()
    NotebookClient(
        loaded["session01_starter.ipynb"], timeout=120, kernel_name="python3"
    ).execute()
    print("notebooks: starter and solution execute; source outputs/counters are zero")


def validate_rendered(root: Path, build_dir: Path) -> None:
    expected_files = [build_dir / "index.html"]
    for name in DECKS:
        expected_files.extend(
            [build_dir / "docs" / f"{name}.html", build_dir / "docs" / f"{name}.pdf"]
        )
    expected_files.extend(
        [
            build_dir / "docs" / "assets" / "regression_workflow.png",
            build_dir / "notebooks" / "session01_starter.ipynb",
            build_dir / "notebooks" / "session01_solution.ipynb",
        ]
    )
    missing = [
        str(path)
        for path in expected_files
        if not path.is_file() or path.stat().st_size == 0
    ]
    if missing:
        fail(f"missing or empty rendered files: {missing}")

    for name, expected_pages in DECKS.items():
        pdf_path = build_dir / "docs" / f"{name}.pdf"
        document = pymupdf.open(pdf_path)
        if len(document) != expected_pages:
            fail(f"{pdf_path}: expected {expected_pages} pages, found {len(document)}")
        for page_number, page in enumerate(document, 1):
            if len(page.get_text().strip()) < 20:
                fail(f"{pdf_path}: page {page_number} is unexpectedly empty")
            width, height = page.rect.width, page.rect.height
            for block in page.get_text("blocks"):
                x0, y0, x1, y1 = block[:4]
                if x0 < -0.5 or y0 < -0.5 or x1 > width + 0.5 or y1 > height + 0.5:
                    fail(
                        f"{pdf_path}: page {page_number} has out-of-bounds text {block[:5]}"
                    )
    print(
        f"rendered output: HTML/PDF/assets/notebooks present; {sum(DECKS.values())} PDF pages pass geometry"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate course sources and rendered artifacts."
    )
    parser.add_argument("--build-dir", default="build")
    parser.add_argument("--skip-rendered", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    validate_structure(root)
    execute_python_deck(root)
    execute_numpy_deck(root)
    execute_regression_deck(root)
    validate_notebooks(root)
    if not args.skip_rendered:
        validate_rendered(root, (root / args.build_dir).resolve())
    print("all validation gates passed")


if __name__ == "__main__":
    main()
