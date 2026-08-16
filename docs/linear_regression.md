---
theme: rose-pine
_class: lead
marp: true
paginate: true
size: 16:9
header: ENSAI · Linear regression workflow
markdown.marp.enableHtml: true
---

# Linear regression · one complete workflow 📈

Model → fit → predict → evaluate → verify.

**20 minutes model + Python baseline · 30 exercise · 10 debrief · 10 check · 5 bridge · 5 contingency**

---

## Problem, data, and model

One reproducible dataset:

```python
import numpy as np

rng = np.random.default_rng(42)
x = rng.uniform(0.0, 10.0, size=50)
y = 1.0 + 2.5 * x + rng.normal(0.0, 2.0, size=x.shape)
```

Model one target from one feature:

$$
\hat y_i = b + a x_i
$$

Parameters: slope $a$, intercept $b$; residual: $e_i = y_i - \hat y_i$.

$$
\min_{a,b}\;\operatorname{MSE}=\frac{1}{n}\sum_{i=1}^{n}\left(y_i-(b+a x_i)\right)^2
$$

---

## Fit → predict → evaluate

```text
observations (x, y)
        │
        ▼
fit ──► parameters (slope, intercept)
        │
        ▼
predict(x) ──► predictions
        │
        ▼
evaluate(y, predictions) ──► MSE + checks
```

Compare against a mean-only baseline:

```python
baseline = np.full_like(y, y.mean())
```

Today, training MSE checks the implementation; it does **not** estimate generalization. Later: evaluation on held-out validation data.

---

## Prepared baseline · pure-Python fit

**Instructor walkthrough:** solution notebook §1. Population factors cancel:

```python
def fit_linear_py(x_values, y_values):
    if not x_values or len(x_values) != len(y_values):
        raise ValueError("x and y need equal non-zero lengths")
    x_mean = mean_py(x_values)
    y_mean = mean_py(y_values)
    numerator = sum(
        (x_i - x_mean) * (y_i - y_mean)
        for x_i, y_i in zip(x_values, y_values)
    )
    denominator = sum((x_i - x_mean) ** 2 for x_i in x_values)
    if denominator == 0.0:
        raise ValueError("x must vary")
    slope = numerator / denominator
    intercept = y_mean - slope * x_mean
    return slope, intercept
```

---

<!-- _class: exercise -->

## Exercise · NumPy fit–predict–evaluate

**Time:** 30 minutes · **Work:** pairs · **Notebook:** `session01_starter.ipynb`

Implement:

```text
fit_linear_numpy(x, y) -> (slope, intercept)
predict_numpy(x, slope, intercept) -> predictions
mse_numpy(y, predictions) -> mse
```

Completion checks:

```python
assert predictions_np.shape == y.shape == (50,)
assert np.isfinite([slope_np, intercept_np, mse_value_np]).all()
assert mse_value_np < mse_numpy(y, np.full_like(y, y.mean()))
```

Expected: slope ≈ `2.5242`, intercept ≈ `0.5373`, MSE ≈ `2.2939`.

Also test invalid inputs: empty, mismatched, 2-D, or constant `x`.

<!--
Presenter cue: spend 3 minutes launching. At minute 10 move to the first hint; at minute 20 reveal the parameter formulas. Stop at 30 minutes and continue with the supplied solution.
-->

---

<!-- _class: hint -->

## Staged hints

**After 10 minutes: shapes**

```python
x_centered = x - x.mean()
y_centered = y - y.mean()
```

**After 20 minutes: parameters**

```python
slope_np = np.mean(x_centered * y_centered) / np.mean(x_centered**2)
intercept_np = y.mean() - slope_np * x.mean()
```

**Final check**

The model MSE should beat the mean baseline MSE, approximately `51.4769`.

---

<!-- _class: solution -->

## Vectorized solution

```python
def fit_linear_numpy(x, y):
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    if x.ndim != 1 or y.ndim != 1 or x.shape != y.shape or x.size == 0:
        raise ValueError("x and y need equal non-zero 1D shapes")
    x_centered = x - x.mean()
    denominator = np.mean(x_centered**2)
    if denominator == 0.0:
        raise ValueError("x must vary")
    slope = np.mean(x_centered * (y - y.mean())) / denominator
    intercept = y.mean() - slope * x.mean()
    return float(slope), float(intercept)

slope_np, intercept_np = fit_linear_numpy(x, y)
predictions_np = intercept_np + slope_np * x
mse_value_np = np.mean((y - predictions_np) ** 2)
```

Result: `(slope, intercept, MSE) = (2.5242, 0.5373, 2.2939)`.

<!--
Debrief cue: check shapes, invalid inputs, and baseline comparison before discussing exact coefficients. Preserve the following 10-minute solver and numerical-practice block.
-->

---

<!-- _class: check -->

## Verify with a solver and a plot

![bg right:46% contain](assets/regression_workflow.png)

```python
design = np.column_stack([x, np.ones_like(x)])
(slope_ls, intercept_ls), *_ = np.linalg.lstsq(
    design, y, rcond=None
)

assert design.shape == (50, 2)
assert np.allclose(
    [slope_np, intercept_np],
    [slope_ls, intercept_ls],
    rtol=1e-12,
    atol=1e-12,
)
```

`lstsq` solves the least-squares problem directly. Do not form an explicit inverse just to obtain these coefficients.

A plot checks structure; numerical assertions check values.

---

<!-- _class: assessment -->

## Mini-assessment · 10 minutes

Answer individually before discussing:

1. Complete `def predict(x, slope, intercept): return ...`; for `x.shape == (50,)`, what is the output shape?
2. What is the shape of `column_stack([x, ones_like(x)])`, and why include ones?
3. What shape results from subtracting `(50, 1)` predictions from `(50,)` targets?
4. Why use `default_rng(42)`, and why compare MSE with a mean baseline?
5. Does a low training MSE prove good performance on unseen data?
6. What should agree with `lstsq`, and name one invariant to check first.

Be ready to justify each answer using shapes or the workflow contract.

<!--
Assessment cue: require individual answers before pair discussion. Do not reveal slide 10 early.
-->

---

<!-- _class: summary -->

## Answers and takeaways

1. `return intercept + slope * x`; output shape `(50,)`.
2. Design shape `(50, 2)`; the ones multiply the intercept.
3. Broadcasting produces `(50, 50)`, a silent and serious bug.
4. `default_rng(42)` reproduces data; the baseline tests value beyond one constant.
5. No. Generalization needs data not used for fitting.
6. Coefficients match `lstsq`; check shapes and finiteness first.

The complete workflow is:

```text
reproduce → validate → fit → predict → compare → verify/plot → interpret
```

Next: held-out validation, then optimization and regularization.
