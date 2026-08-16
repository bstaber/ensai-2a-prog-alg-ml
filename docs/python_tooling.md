---
theme: rose-pine
_class: lead
marp: true
paginate: true
size: 16:9
header: ENSAI · Python tooling
markdown.marp.enableHtml: true
---

# Python tooling & environments

A companion reference on running, managing, and shipping Python. Separate from the 3-hour lesson and not timed.

- running code: scripts vs notebooks vs REPL
- which Python is installed, and where
- environments: why and how (`venv`, `uv`, `conda`, …)
- a quick `uv` workflow for this course

---

## CPython in one paragraph

The most common Python is **CPython**: an interpreter written in C that compiles your source to *bytecode* and runs it on a virtual machine.

- You usually never see bytecode; you just run the `.py` file.
- Other implementations exist: **PyPy** (JIT-compiles hot loops, often faster), **MicroPython** (small embedded devices), **RustPython** (written in Rust).
- "Python" almost always means CPython.

---

## Three ways to run code

| Way | Command / tool | Best for |
|---|---|---|
| **Script** | `python hello.py` | a whole program end to end |
| **Notebook** | Jupyter `.ipynb` | exploring, mixing text + code, fast feedback |
| **REPL** | `python` (interactive session) | tiny experiments, checking one expression |

For short questions use the REPL. For a finished pipeline use a script. For today's guided practice use the notebooks.

---

## Scripts vs notebooks

**A script** runs top to bottom; its state resets each run. Great for reproducibility and automation.

**A notebook** holds cells you run in any order, and its outputs persist. Great for exploration, but order-dependent state can bite you:

```text
cell order is not guaranteed to match "top to bottom"
```

Rule: **explore in a notebook, commit a script** for anything you re-run or hand to someone else.

---

## Which Python am I actually using?

Find the interpreter and its version:

```bash
which python        # path of the python on your PATH
python --version    # e.g. Python 3.12.11
```

Inside a virtual environment these point at the environment's interpreter instead of the system one. That is exactly the point.

---

## The environment problem

Different projects need different versions of the same packages.

- Project A: `numpy 1.26`
- Project B: `numpy 2.0`

Installing both "globally" is how you break your own machine. The fix is **isolated environments**: each project gets its own interpreter + dependency set.

A lock file (`uv.lock`, `poetry.lock`, `requirements.txt`) records the exact versions so anyone can rebuild the same environment.

---

## The environment toolbox at a glance

| Tool | Role |
|---|---|
| **`venv`** | built-in, minimal virtual environment (`python -m venv`) |
| **pip** | installs packages from PyPI into the current environment |
| **`uv`** | fast `venv` + `pip` + version/lockfile in one tool (used here) |
| **pyenv** | switch between multiple Python **versions** |
| **conda / mamba / pixi** | environments + compiled/scientific packages, beyond Python only |
| **Poetry / PDM** | full project manager: deps + build + lockfile |

You do not need all of these. Pick one workflow and stay consistent.

---

## `venv`, the built-in baseline

```bash
python -m venv .venv      # create an isolated environment in .venv
source .venv/bin/activate # activate it (Windows: .venv\Scripts\activate)
pip install numpy         # installs only inside this environment
```

Common pitfall: forgetting to activate, so `pip` installs to the *system* interpreter. `uv` avoids most of this by defaulting to the project environment.

---

## `uv`, one fast tool with a lockfile

`uv` manages the environment, resolves versions, and records a `uv.lock`.

```bash
uv sync                 # create env + install pinned deps from uv.lock
uv add numpy            # add a dep, update uv.lock
uv run python hello.py  # run in the project env regardless of activation
uv run jupyter lab      # start the teaching notebooks
```

Reproducible and fast; this is the workflow this repository uses.

---

## `uv init`, create a new project

```bash
uv init my_project
```

This creates a standard layout:

```text
my_project/
├── pyproject.toml      # metadata + direct dependencies
├── .python-version     # the Python version for this project
├── main.py             # a "Hello, world!" example entry point
├── README.md
└── .gitignore
```

It also initializes a git repo (`.git/`) and a `uv.lock` appears on the first `uv sync`.

Pick a Python version and add libraries:

```bash
uv python install 3.12
uv add numpy
```

`uv add` records the dependency in `pyproject.toml` and resolves `uv.lock`.

---

## Project files for reproducibility

Inside the project you will find:

```bash
pyproject.toml   # metadata + direct dependencies
uv.lock          # exact resolved versions (commit this)
.python-version  # the Python version (3.12 for this course)
```

Anyone can run `uv sync` from a clean clone and get the same environment. That is what "reproducible" means.

---

## Pinning: why `.python-version` and `uv.lock` matter

Without pinned versions, "it works on my machine" is a coin flip.

```bash
# wrong: whatever is installed
uv run python script.py

# right: the exact locked environment
uv sync --locked   # fail if uv.lock would change
uv run python script.py
```

Reproducibility = deterministic data, pinned languages, pinned tools, pinned versions.

---

## `which python`, `uv`, and PATH in one line of mental model

- `which python` tells you the first match on `PATH`.
- A virtualenv puts `.venv/bin` (or `Scripts`) ahead of the system interpreter.
- `uv run` uses the project interpreter without you activating anything.

So the golden habit for this course: **`uv sync` once, then always `uv run …`**. No manual activation needed.

---

## Resources

- [`uv` documentation](https://docs.astral.sh/uv/)
- [Python packaging guide](https://packaging.python.org/en/latest/)
- ["Hitchhiker's Guide to Python" – environments](https://docs.python-guide.org/dev/virtualenvs/)
- [Real Python: virtual environments primer](https://realpython.com/python-virtual-environments-a-primer/)

Skim when needed; do not read like a book.