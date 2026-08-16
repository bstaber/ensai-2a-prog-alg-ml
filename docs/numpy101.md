---
theme: rose-pine
_class: lead
marp: true
paginate: true
size: 16:9
header: ENSAI · NumPy shape reasoning
markdown.marp.enableHtml: true
---

# NumPy shape reasoning 🔢

Arrays, axes, broadcasting, and checks for reliable numerical code.

**25 minutes teaching · 15 minutes guided practice**

---

## An array has a contract

```python
import numpy as np

values = np.array([2.0, 4.0, 8.0, 16.0])
```

Every array has:

```python
values.shape   # (4,)
values.ndim    # 1
values.dtype   # dtype('float64')
values.size    # 4
```

Before any calculation, ask: **What shape do I have? What shape do I need?**

---

## Create data with an explicit generator

```python
rng = np.random.default_rng(42)

x = rng.uniform(0.0, 10.0, size=50)
noise = rng.normal(0.0, 2.0, size=x.shape)
y = 1.0 + 2.5 * x + noise
```

```python
x.shape == y.shape == (50,)  # True
```

- One owned generator makes state and reproducibility visible.
- Calling `default_rng(42)` again restarts the same sequence.
- Use `rng.integers(0, 10, size=5)`, not a nonexistent module-level `np.random.integers(...)`.

---

## One dimension is not a row or column matrix

```python
vector = np.array([10.0, 20.0, 30.0])
row = vector[None, :]
column = vector[:, None]

vector.shape   # (3,)
row.shape      # (1, 3)
column.shape   # (3, 1)
```

These shapes carry different broadcasting and matrix-multiplication behavior.

A trailing comma matters: `(3,)` is a one-element tuple.

---

## Indexing can remove or preserve an axis

```python
matrix = np.array([
    [1.0, 2.0],
    [3.0, 4.0],
    [5.0, 6.0],
])

matrix[0].shape       # (2,)
matrix[0:1].shape     # (1, 2)
matrix[:, 0].shape    # (3,)
matrix[:, 0:1].shape  # (3, 1)
```

Integer indexing removes an axis. A length-one slice preserves it.

---

## Views and copies depend on the operation

Basic slicing usually shares data:

```python
view = matrix[:, :1]
np.shares_memory(matrix, view)  # True
```

Advanced indexing usually copies:

```python
copy = matrix[[0, 2]]
np.shares_memory(matrix, copy)  # False
```

`reshape` and `ravel` return views when possible, but may copy. Use `.copy()` when independence is required.

---

## Array arithmetic enables vectorization

```python
x = np.array([1.0, 2.0, 3.0])

x + 10.0  # array([11., 12., 13.])
x * x     # array([1., 4., 9.])
x**2      # array([1., 4., 9.])
```

A whole error calculation:

```python
squared_errors = (y - predictions) ** 2
mse = squared_errors.mean()
```

`*` is element-wise. Use `@` for matrix multiplication. Array expressions state the calculation and let NumPy run compiled numerical kernels.

---

## Reductions remove an axis

For `matrix.shape == (3, 2)`:

```python
matrix.mean()          # scalar
matrix.mean(axis=0)    # shape (2,): one mean per column
matrix.mean(axis=1)    # shape (3,): one mean per row
```

Think: **the named axis is consumed**.

```text
axis=0 ↓ combines rows     axis=1 → combines columns
```

Always connect an `axis` argument to the input and output shapes.

---

## `keepdims=True` preserves a length-one axis

```python
row_means = matrix.mean(axis=1, keepdims=True)

matrix.shape      # (3, 2)
row_means.shape   # (3, 1)
```

Now subtraction is unambiguous:

```python
centered = matrix - row_means
centered.shape  # (3, 2)
```

Without `keepdims=True`, `(3, 2) - (3,)` is not broadcastable.

---

## Broadcasting aligns trailing dimensions

Two dimensions are compatible when they are equal or one of them is `1`.

```text
(3, 2)
(3, 1)
------
(3, 2)  ✓
```

```text
(4, 1, 2)
(   3, 2)
---------
(4, 3, 2)  ✓
```

Broadcasting behaves as if length-one dimensions were repeated, usually without materializing those copies.

---

## Shape check · predict before running

For `points.shape == (3, 2)`, what are the shapes?

```python
points[0]
points[0:1]
points.mean(axis=0)
points.mean(axis=1, keepdims=True)
points[:, None, :]
points[None, :, :]
```

Answers:

```text
(2,)  (1, 2)  (2,)  (3, 1)  (3, 1, 2)  (1, 3, 2)
```

Which pair can broadcast to `(3, 3, 2)`?

---

<!-- _class: exercise -->

## Exercise · center every row

**Time:** 7 minutes coding · 15 minutes including launch and debrief · **Work:** pairs

```python
points = np.array([
    [0.0, 0.0],
    [1.0, 0.0],
    [1.0, 2.0],
])
```

Create `row_means` with shape `(3, 1)`, then create `centered` with shape `(3, 2)`, all without a Python loop.

```python
assert row_means.shape == (3, 1)
assert centered.shape == points.shape
assert np.allclose(centered.mean(axis=1), 0.0)
```

<!--
Presenter cue: spend 2 minutes launching, then 7 minutes on pair work. Require students to write the expected shapes before coding. Move to the hint after 3 minutes of coding.
-->

---

<!-- _class: hint -->

## Exercise hint

After three minutes:

1. Which axis contains the two coordinates of one row?
2. Which axis must the reduction consume?
3. Which length-one axis must remain for subtraction?

```python
row_means = points.mean(axis=..., keepdims=...)
centered = points - row_means
```

**Optional fast finisher:** use `points[:, None, :] - points[None, :, :]` and predict the resulting shape.

---

<!-- _class: solution -->

## Solution · row centering

```python
row_means = points.mean(axis=1, keepdims=True)
centered = points - row_means

assert row_means.shape == (3, 1)
assert centered.shape == points.shape
assert np.allclose(centered.mean(axis=1), 0.0)
```

- `axis=1` consumes the two-coordinate feature axis.
- `keepdims=True` retains a length-one axis, so subtraction broadcasts.
- The checks make the intended shapes and numerical invariant executable.

**Optional fast finisher:** continue with pairwise squared distances in the notebook only after these core checks pass.

<!--
Debrief cue: ask which axis was consumed and why keepdims preserves broadcastability. The pairwise extension is for fast finishers only.
-->

---

<!-- _class: check -->

## Numerical checks are part of the algorithm

```python
assert predictions.shape == y.shape
assert np.isfinite(predictions).all()
assert np.allclose(actual, expected, rtol=1e-12, atol=1e-12)
```

- Use `np.allclose`, not exact equality, for most floating-point results.
- Choose tolerances from the scale and precision of the problem.
- Make shape and finiteness failures immediate.
- Avoid an explicit matrix inverse when a solver such as `np.linalg.lstsq` expresses the problem directly.

---

<!-- _class: summary -->

## NumPy checklist for today

You can now:

- inspect `shape`, `ndim`, `dtype`, and `size`;
- preserve or remove axes intentionally;
- distinguish common views from copies;
- replace numerical loops with array expressions;
- explain reductions using input and output shapes;
- apply the trailing-dimension broadcasting rules;
- verify numerical results with shape, finiteness, and tolerance checks.

Next: use these tools to fit, predict, and evaluate linear regression.
