# Algorithms and Programming in Python

Lecture material for second-year students at [ENSAI](https://ensai.fr/) in Rennes, France.

**Course website: <https://bstaber.github.io/ensai-2a-prog-alg-ml/>**, with the session list, slides, PDFs, and notebooks.

## Setup before class

The repository uses Python 3.12 and [uv](https://docs.astral.sh/uv/) with a committed lock file. From the repository root, install the exact teaching environment:

```bash
uv sync --locked
```

Run the smoke test:

```bash
uv run python -c "import numpy as np; import matplotlib; print('NumPy', np.__version__); print('Matplotlib', matplotlib.__version__)"
```

Then start JupyterLab:

```bash
uv run jupyter lab
```

Open [`notebooks/session01_starter.ipynb`](notebooks/session01_starter.ipynb) for the in-class exercises. [`notebooks/session01_solution.ipynb`](notebooks/session01_solution.ipynb) contains the complete executable reference workflow.

## For instructors

- [Session 1 instructor guide](docs/instructor_guide.md): run sheet, exercise cues, and contingency cuts.
- Slides are authored in [Marp](https://marp.app/) Markdown in [`docs/session01.md`](docs/session01.md); the website is [`site/index.html`](site/index.html).

Render the slides and run every source, notebook, asset, slide-count, and PDF-geometry check:

```bash
uv run python scripts/render_slides.py build
uv run python scripts/validate.py --build-dir build
```

Pushing to `main` validates the course and deploys `build/` to the website.

## License

See [`LICENSE`](LICENSE).
