---
theme: rose-pine
_class: lead
marp: true
paginate: true
size: 16:9
header: ENSAI · Python essentials
markdown.marp.enableHtml: true
---

# Python essentials 🐍

The syntax needed for today's fit–predict–evaluate workflow.

**25 minutes teaching · 15 minutes guided practice** · appendices are reference only

---

## How Python runs

The 10-second version:

- You run a Python file directly. There is no separate compile step before you see results.
- Statements run in order, top to bottom.
- A function's body runs only when you call it.
- When something fails, read the **last** line of the error first.

Heads-up: libraries like NumPy move the heavy numerical work into fast compiled code. You will see the payoff soon; the details are in Appendix B.

---

## Run a script

`hello.py`:

```python
message = "Hello, world!"
print(message)
```

From the repository environment:

```bash
uv run python hello.py
```

Output:

```text
Hello, world!
```

`uv` handles the Python environment for you. See the optional *Python tooling & environments* deck for `uv init`, `uv sync`, and how environments work.

---

## Names, values, and types

The four classic types:

```python
x = 42           # int
pi = 3.14        # float
name = "Alice"   # str
is_valid = True  # bool

print(type(x), type(pi))
```

- A name refers to a value.
- Values have runtime types; incompatible operations can fail at runtime.
- Type hints (`x: int = 42`) document intent for editors; Python does not enforce them.

---

## Strings

Combine strings in several ways:

```python
greeting = "Hello"
name = "Alice"
msg = f"{greeting}, {name}!"   # f-string: embed values

print(msg)  # Hello, Alice!
```

Many methods exist:

```python
text = "  Python Basics  "
text.strip()          # "Python Basics"
text.lower()          # "  python basics  " (whitespace preserved)
"-".join(["A", "B"])  # "A-B"
```

---

## Lists: ordered values

```python
values = [2.0, 4.0, 8.0, 16.0]

values[0]       # 2.0
values[-1]      # 16.0
values[1:3]     # [4.0, 8.0]
len(values)     # 4
```

Indexes start at zero. A slice includes its start and excludes its stop.

```text
 index       0    1    2     3
 value     2.0  4.0  8.0  16.0
```

---

## Lists are mutable

```python
values = [2.0, 4.0]
values.append(8.0)
values[0] = 1.0

print(values)  # [1.0, 4.0, 8.0]
```

Assignment does not copy a list:

```python
alias = values
alias.append(16.0)
print(values)  # [1.0, 4.0, 8.0, 16.0]
```

Use `values.copy()` for an independent shallow copy.

---

## Tuples: immutable, ordered

```python
point = (2, 3)
x, y = point     # unpacking

print(x)  # 2
```

- **Immutable**: once created, cannot be changed.
- **Ordered**: like lists, preserve insertion order.
- Support unpacking: `x, y = point`.

Use a tuple when the size and meaning are fixed, like a point `(x, y)`.

---

## Dictionaries map keys to values

```python
person = {"name": "Alice", "age": 30}

print(person["name"])  # Alice
```

Safely read and update:

```python
person.get("age", "unknown")   # 30
person.update({"age": 31})

print(person["age"])  # 31
```

Use a dict when you need lookup by a label rather than by integer index.

---

## Sets hold unique values

```python
tags = set([1, 2, 2, 3])
print(tags)  # {1, 2, 3}
```

```python
tags.add(4)
tags.union({5, 6})
```

Unordered iteration; duplicates are automatically removed; supports union, intersection, and difference; mutable.

---

## Conditions

```python
mse = 2.3
baseline_mse = 51.5

if mse < baseline_mse:
    print("the model beats the baseline")
else:
    print("check the implementation")
```

Blocks are defined by indentation. Comparisons produce Booleans.

Useful operators: `==`, `!=`, `<`, `<=`, `>`, `>=`, `and`, `or`, `not`.

---

## Loops and `range`

```python
squared = []
for value in range(5):
    squared.append(value**2)

print(squared)  # [0, 1, 4, 9, 16]
```

`range(5)` produces integers from `0` up to but not including `5`.

Use a loop when each iteration performs a meaningful step. Later, NumPy will replace many numerical loops with array operations.

---

## Comprehensions express simple transforms

Loop form:

```python
predictions = []
for value in x_values:
    predictions.append(intercept + slope * value)
```

Comprehension:

```python
predictions = [
    intercept + slope * value
    for value in x_values
]
```

Use the comprehension for a simple transform; keep the loop when the body has several steps.

---

## Iterate over paired data with `zip`

```python
observed = [3.0, 5.0, 8.0]
predicted = [2.5, 5.5, 7.0]

errors = []
for target, prediction in zip(observed, predicted):
    errors.append(target - prediction)

print(errors)  # [0.5, -0.5, 1.0]
```

`zip` stops at the shortest input. Validate equal lengths when silently dropping data would be an error.

---

## Functions package a contract

```python
def mean(values: list[float]) -> float:
    """Return the arithmetic mean of a non-empty list."""
    if not values:
        raise ValueError("mean requires at least one value")
    return sum(values) / len(values)

result = mean([2.0, 4.0, 6.0])
print(result)  # 4.0
```

A useful numerical function states its inputs, output, and invalid cases.

---

## Classes group data with behavior

```python
class Person:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print(f"Hey, I'm {self.name}")

p = Person("Alice")
p.say_hello()  # Hey, I'm Alice
```

We will not need to write classes today, but you will meet them in libraries and later sessions.

---

## Imports make dependencies explicit

```python
import math

distance = math.sqrt(3.0**2 + 4.0**2)
print(distance)  # 5.0
```

Later today:

```python
import numpy as np
import matplotlib.pyplot as plt
```

Keep imports near the start of a script or notebook. Avoid wildcard imports: they hide where names come from.

---

## Read the final line of an error first

```text
Traceback (most recent call last):
  File "metrics.py", line 8, in <module>
    score = mse_py(targets, predictions)
  File "metrics.py", line 3, in mse_py
    raise ValueError("inputs must have the same non-zero length")
ValueError: inputs must have the same non-zero length
```

1. Read the exception type and message.
2. Find the first frame that belongs to your code.
3. Inspect the values at that line.
4. Fix the cause, not the symptom.

---

## Bridge to the shared dataset

The notebook generates one reproducible NumPy dataset, then exposes the same observations as lists:

```python
rng = np.random.default_rng(42)
x = rng.uniform(0.0, 10.0, size=50)
y = 1.0 + 2.5 * x + rng.normal(0.0, 2.0, size=x.shape)

x_list = x.tolist()
y_list = y.tolist()
```

The Python and NumPy implementations therefore solve exactly the same problem.

---

<!-- _class: exercise -->

## Exercise · pure-Python MSE

**Time:** 7 minutes coding · 15 minutes including launch and debrief · **Work:** pairs

Implement:

```python
def mse_py(y_true: list[float], y_pred: list[float]) -> float:
    """Return the mean squared error of equal-length non-empty lists."""
    ...
```

Checks:

```python
assert mse_py([1.0, 2.0], [1.0, 2.0]) == 0.0
assert mse_py([1.0, 3.0], [2.0, 1.0]) == 2.5
```

Reject empty or mismatched inputs with `ValueError`.

<!--
Presenter cue: spend 2 minutes launching, then 7 minutes on pair coding. Move to the hint after 3 minutes of coding. Require both assertions and at least one invalid-input check.
-->

---

<!-- _class: hint -->

## Exercise hint

After three minutes:

1. check the two lengths;
2. pair targets and predictions with `zip`;
3. square each difference;
4. divide the total by the number of targets.

```python
squared_errors = [
    (target - prediction) ** 2
    for target, prediction in zip(y_true, y_pred)
]
```

What should happen if either input is empty?

---

<!-- _class: solution -->

## One solution

```python
def mse_py(y_true: list[float], y_pred: list[float]) -> float:
    if not y_true or len(y_true) != len(y_pred):
        raise ValueError("inputs must have the same non-zero length")
    return sum(
        (target - prediction) ** 2
        for target, prediction in zip(y_true, y_pred)
    ) / len(y_true)
```

The checks are examples, not a complete test suite.

<!--
Debrief cue: ask why the length check must happen before zip. Use the remaining 2 minutes to connect list arithmetic to NumPy vectorization.
-->

---

<!-- _class: summary -->

## Python checklist for today

You have met:

- run a script and read an error bottom-up;
- the classic types, strings, lists, tuples, dicts, and sets;
- conditions, loops, comprehensions, and `zip`;
- functions with explicit contracts and a brief look at classes.

We keep only what today's fit–predict–evaluate workflow needs; the rest is reference material.

---

<!-- _class: appendix -->

## Appendix A · A short history of Python

Reference only, not part of the 180-minute lesson.

- **1991**: first public release by Guido van Rossum, for readable general-purpose programming.
- **2000**: Python 2.0 (list comprehensions, cleaner stdlib).
- **2008**: Python 3.0, a deliberate breaking redesign; Python 2 retired in 2020.
- **2023–2025**: Python 3.11 to 3.13, with faster startup, richer typing, and better concurrency.
- Main implementation is **CPython** (written in C); neighbors include PyPy (JIT) and MicroPython.

---

<!-- _class: appendix -->

## Appendix B · Bytecode, the GIL, and why NumPy is fast

- **Bytecode**: CPython compiles your source to bytecode, then a virtual machine runs it. You usually never see it; you just run the file.
- **GIL** (Global Interpreter Lock): only one thread executes Python bytecode at a time. That is fine here, where the heavy work is inside small Python functions or NumPy kernels; it matters only if you someday try to parallelize CPU-bound *pure-Python* loops with threads.
- **Why NumPy is fast**: the hot loop is moved into compiled, vectorized C (and Fortran) code, so per-element Python overhead disappears.
- **Going further**: Numba JIT-compiles numeric loops; `pybind11` exposes C code to Python.

Rule of thumb: keep hot loops in compiled kernels (NumPy, Numba, or a binding), not in pure Python. See *Python tooling & environments* for the CPython overview.

---

<!-- _class: appendix -->

## Appendix C · Interpreted vs compiled and the C++ dot product

Reference only.

**Compiled languages** (C, C++, Rust, …) are translated to machine code **before** running. They are fast at runtime, but you recompile after each change.

**Interpreted languages** (Python, JavaScript, R, …) are run directly by an interpreter or virtual machine. They are easier to test and debug, there is no manual compile step, but raw loops are usually slower.

Python's dot product:

```python
x = [1, 2, 3]
y = [4, 5, 6]

dot = sum(x_i * y_i for x_i, y_i in zip(x, y))
print(dot)  # 32
```

```bash
python my_script.py
```

The same dot in C++ needs a separate compile step first:

```bash
g++ dot.cpp -o dot && ./dot
```

Python trades a little raw speed for much shorter, easier-to-read code. That is exactly why we delegate the hot loops to libraries like NumPy.

---

<!-- _class: appendix -->

## Bonus · setting up `uv`

Environment setup (`uv init`, `uv sync`, `uv run`, lockfiles, and the full toolbox) is covered in the optional **Python tooling & environments** deck. The short version for this course: `uv sync`, then always `uv run …`.

---

<!-- _class: appendix -->

## Resources

Use when stuck, not as a cover-to-cover read:

- [Python home](https://www.python.org)
- [Python documentation](https://docs.python.org/3/)
- [Python tutorial](https://docs.python.org/3/tutorial/index.html)
- [Python standard library reference](https://docs.python.org/3/library/index.html)