---
theme: rose-pine
_class: lead
marp: true
paginate: true
size: 16:9
header: ENSAI - 2A - Programmation algorithmique en Python - 2025/2026
# footer: 2025 - 2026
markdown.marp.enableHtml: true
---

## Python 101 🐍

```python
print("Hello, world!")
```

Run with:

```bash
$ python hello_world.py
```

---

### What is Python? 🐍

- **Created in 1991** by *Guido van Rossum*  
- Open source, community-driven: [python.org](https://www.python.org)  
- **General-purpose**: web, data science, ML, automation, scripting...  
- **Easy to learn**, readable syntax
- Main implementation: **CPython** (default, in C)  
- Other implementations: PyPy (JIT), Jython (Java), MicroPython, RustPython, ...
- **Popularity**: great community and big ecosystems

---

### Python timeline

- **1991**: First release by Guido van Rossum  
- **2000**: Python 2.0 (list comprehensions, ...)  
- **2008**: Python 3.0 (major redesign)  
- **2020**: Python 2 officially retired  
- **2023–2025**: Python 3.11–3.13 (faster, typing, match/case, async)

Python keeps evolving, with strong focus on speed and clarity

---

### Python: interpreted language

- **Compiled languages** (C, C++, Rust…)
  - Code is **translated to machine code** before running
  - Fast execution, but need to recompile after changes

- **Interpreted languages** (Python, JavaScript, R, ...)
  - Code is **executed line by line** by an interpreter (CPython)
  - Easier to test and debug, no compilation step
  - Usually slower than compiled code

---

### Python: interpreted language

Python = interpreted (CPython), but…
- Many libraries (NumPy, PyTorch) use **compiled C/C++/Fortran** under the hood
- You get the **ease of Python** + **speed of compiled code**
- You can even make python bindings for your own C/C++ codes (`pybind11`, `nanobind`, ...)

---

### Setting up Python

**Ways to develop and run python code**
- Scripts: `python file.py`
- IDEs: **VSCode**, PyCharm
- Notebooks: Jupyter (`notebook.ipynb`), marimo (`notebook.py`)

**Nowadays, the classical combo is**:
* VSCode with Python extensions
* Jupyter or marimo for notebooks and fast prototyping

---

### Setting up Python

**Managing environments**
- pyenv (switch Python versions)
- `venv` (built-in, simple)
- pip (install packages)
- advanced tools: poetry, uv
- scientific computing: conda, mamba, pixi

---

### Setting up Python

You don't know which python you have right now?

In a command line:
```bash
which python
```

And:
```bash
python --version
```

---

### The basics

- Variables and types
- Strings
- Collections: list, tuple, dict, set
- Control flow (if/else, match)
- For/while loops
- Functions and classes
- Modules
- Type hints and docstrings
- Bonus: `uv`

---

### Variables & basic types

We have the four classic types:
```python
x = 42        # int
pi = 3.14     # float
name = "Alice"  # str
is_valid = True # bool
```

In your code, you can check the type of any object:
```python
print(type(x), type(pi))
```

---

### Strings

You can combine strings together in many ways.
```python
greeting = "Hello"
name = "Alice"
msg = f"{greeting}, {name}!"
```

There are many existing methods for strings:
```python
text = "  Python Basics  "
text.strip()
text.lower()
"-".join(["A", "B"])
```

---

### Collections: lists

Lists are the most basic collections / containers.

```python
fruits = ["apple", "banana", "cherry"]
fruits.append("kiwi")
print(fruits[0])
```

You can also build a list *in comprehension*.
```python
squares = [x**2 for x in range(5)]
```

---

### Collections: lists

**Features**:
- **Mutable**: you can add, remove, or change elements.
- **Ordered**: elements keep their order of insertion.
- **Indexable & sliceable**: access by index (fruits[0]) or slices (fruits[1:3]).
- Can hold mixed types ([1, "two", 3.0]).

---

### Collections: tuples

A tuple looks quite similar.
```python
point = (2, 3)
x, y = point
```

**Features**:
- **Immutable**: once created, cannot be changed.
- **Ordered**: like lists, preserve insertion order.
- Support unpacking (x, y = point).

---

### Collections: dicts

A dictionnary is a collection keys and values:
```python
person = {"name": "Alice", "age": 30}
print(person["name"])
```

You can also safely access the dictionnary or update it:
```python
person.get("age", "unknown")
person.update({"age": 31})
```

---

### Collections: sets

Unorder collection:
```python
x = set([1, 2, 2, 3])
print(x)  # {1, 2, 3}
```

You can add items and perform *set operations*:
```python
unique.add(4)
unique.union({5, 6})
```

---

### Collections: sets

**Features**:
- Unordered: no guaranteed order when iterating.
- Unique elements only (duplicates removed automatically).
- Support set operations (union, intersection, difference).
- Mutable (you can add/remove), but there’s also an immutable version called frozenset.

---

### Collections: recap

| Type   | Properties | Best Use |
|--------|------------|----------|
| **List** | Ordered, mutable, indexable | Sequences of items |
| **Tuple** | Ordered, immutable | Fixed-size records |
| **Dict** | Key → Value mapping, fast O(1) lookup | Structured data (JSON-like) |
| **Set** | Unordered, unique, O(1) membership | Membership tests, set operations |


---

### Control flow: conditionals

Classic if/else statements like in any other language:
```python
if age > 18:
    print("Adult")
elif age == 18:
    print("Just turned adult")
else:
    print("Minor")
```

---

### Control flow: loops

Classical loop over a list:
```python
for fruit in fruits:
    print(fruit)
```

Get the index and the value at the same time:
```python
for i, fruit in enumerate(fruits):
    print(i, fruit)
```

---
### Control flow: loops

Loop over multiple iterables:
```python
for fruit, vegetable in zip(fruits, vegetables):
    print(fruit, vegetable)

for i, (fruit, vegetable) in enumerate(zip(fruits, vegetables)):
    print(fruit, vegetable)

```

Classic while loop:
```python
while i < 3:
    i += 1
```

---

### Functions

Simple function with a single input with default value:
```python
def greet(name="world"):
    return f"Hello, {name}!"
```

Function with multiple inputs:
```python
def foofoo(x, y, z=1.0):
    return z*(x + y)
```

---

### Classes

Simple class:
```python
class Person:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print(f"Hey, I'm {self.name}")
```

Usage:
```python
p = Person("Emmanuel")
p.say_hello()
```
---

### Importing modules

Python has several standard modules. The `math` module:
```python
import math
print(math.sqrt(16))
print(math.pi)
```

The `os` module:
```python
import os
print(os.getcwd())
print(os.listdir())
```

---

### Importing modules

Shorter alias:
```python
import numpy as np
```

Import specific objects from a module:
```python
from math import sqrt
x = 4.0
y = sqrt(x)
```

---

### A few good practices: type hints and docstrings

Totally optional but really useful in practice.
```python
def mean(x: list[float]) -> float:
    """Compute the mean value of the list.

    Args:
        x: list of floats
    
    Returns:
        The empirical mean of x
    """
    return sum(x)/len(x)
```

---

### Bonus: setup a project with `uv`

Install [uv](https://docs.astral.sh/uv/getting-started/installation/). Create a new project:
```bash
uv init --lib my_project
```

This automatically creates a project with a standard layout:
```bash
my_project/
├── README.md
├── pyproject.toml
└── src
    └── my_project
        ├── __init__.py
        └── py.typed
```
---

### Bonus: setup a project with `uv`

Pick a python version:
```bash
uv python install 3.12
```

Add libraries:
```bash
uv add numpy
```

This automatically updates `pyproject.toml`.

---

### Bonus: setup a project with `uv`

You can add a module with functions in `src/my_project`, e.g.:
```python
# src/my_project/my_module.py
def add(x, y):
    return x + y
```

Then in any other script, you can import your functions:
```python
# my_project/main.py
from my_project.my_module import add
x = add(2.0, 3.0)
```

---

### Bonus: setup a project with `uv`

Run your scripts with:
```bash
uv run python main.py
```

That's it! 

For more information about [uv](https://docs.astral.sh/uv/getting-started/installation/), check out their website.

---

### Resources

- [Python homepage](https://www.python.org)  
- [Python docs](https://docs.python.org/3/)  
- [Python tutorial](https://docs.python.org/3/tutorial/index.html)  
- [Python standard library](https://docs.python.org/3/library/index.html)  

💡 You don't need to read these like books:  
- Scroll and skim what looks useful  
- Use them as a reference when stuck  
