# Algorithms and Programming in Python

Lecture material for second-year students at [ENSAI](https://ensai.fr/) in Rennes, France.

## Session 1 — Python and NumPy for machine learning

This three-hour session is a fast Python and NumPy bridge for mathematically trained students who have already programmed in at least one language. It is not intended as a first introduction to programming.

### Prerequisites

Before class, students should be able to:

- explain variables, conditions, loops, and functions in any programming language;
- work with elementary vectors, matrices, means, and variances;
- run a command in a terminal;
- start the supplied Python environment and notebook.

The setup check is a prerequisite, not part of the live three-hour schedule.

### Learning outcomes

By the end of the session, students should be able to:

1. write small Python functions using lists, loops, and comprehensions;
2. create NumPy arrays and reason about their shape, dtype, and axes;
3. replace a loop calculation with vectorized NumPy code;
4. generate reproducible synthetic data with an explicit random-number generator;
5. fit, predict, and evaluate a univariate linear-regression model;
6. verify numerical results with invariants and `numpy.linalg.lstsq`.

### Three-hour agenda

| Time | Activity | Minutes |
|---|---|---:|
| 00:00–00:10 | Outcomes, prerequisites, setup confirmation, diagnostic | 10 |
| 00:10–00:35 | Essential Python syntax | 25 |
| 00:35–00:50 | Guided Python micro-exercise | 15 |
| 00:50–01:15 | NumPy arrays, shapes, dtypes, indexing, reductions | 25 |
| 01:15–01:30 | Shape and broadcasting exercise | 15 |
| 01:30–01:40 | Break | 10 |
| 01:40–02:00 | Regression problem and pure-Python baseline | 20 |
| 02:00–02:30 | NumPy regression pair exercise | 30 |
| 02:30–02:40 | Debrief, `lstsq`, numerical practice, and next-step preview | 10 |
| 02:40–02:50 | Mini-assessment | 10 |
| 02:50–02:55 | Summary and bridge to the next lecture | 5 |
| 02:55–03:00 | Contingency | 5 |

**Total: 180 minutes.** Prepared content finishes by 02:55; the last five minutes are protected contingency. Exercise time is part of the schedule, not an optional extra.

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

The smoke test must succeed before class. Environment installation and troubleshooting are not included in the live three-hour agenda.

## Validate the complete course

Render the four decks with the repository-pinned Marp CLI and then run every source, notebook, asset, slide-count, and PDF-geometry check:

```bash
uv run python scripts/render_slides.py build
uv run python scripts/validate.py --build-dir build
```

The validator executes clean copies of both notebooks. Source notebooks must remain free of outputs and execution counters.

## Instructor materials

- [Exact run sheet, exercise cues, checks for understanding, and contingency cuts](docs/instructor_guide.md)

## Slides

- [Introduction](https://bstaber.github.io/ensai-2a-prog-alg-ml/docs/introduction)
- [Python 101](https://bstaber.github.io/ensai-2a-prog-alg-ml/docs/python101)
- [NumPy 101](https://bstaber.github.io/ensai-2a-prog-alg-ml/docs/numpy101)
- [Linear regression](https://bstaber.github.io/ensai-2a-prog-alg-ml/docs/linear_regression)
- [Python tooling & environments](https://bstaber.github.io/ensai-2a-prog-alg-ml/docs/python_tooling) *(optional companion, not part of the timed lesson)*

The slides are authored in [Marp](https://marp.app/) Markdown. Complete executable examples belong in the student and solution notebooks rather than being generated directly from the presentation files.

## Session boundaries

The live session focuses on the Python and NumPy concepts required to complete one fit–predict–evaluate workflow. Strings, tuples, dictionaries, sets, and a brief class example are taught as a fast refresher for prior programmers; Python history, environment-manager comparisons, and the depth of classes, multidimensional normal equations, Ridge regression, and k-means are reference or later-session topics.

## License

See [`LICENSE`](LICENSE).
