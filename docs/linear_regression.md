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

# Linear regression 📈
Pure Python vs NumPy implementation

---

## Problem setup

We want to fit a line:

$$ 
y = a x + b 
$$

Given data points $(x_i, y_i)$, find $a, b$ that minimize:

$$
\mathrm{MSE}(a, b) = \frac{1}{n} \sum_{i=1}^n (y_i - (a x_i + b))^2
$$

---

## Analytical solution

Optimal parameters are:

$$
a = \frac{\sum (x_i - \overline{x})(y_i - \overline{y})}{\sum (x_i - \overline{x})^2},
$$

and

$$
b = \overline{y} - a \overline{x}
$$

where $\overline{x}$ and $\overline{y}$ are the means of $X = (x_1, ..., x_n)$ and $Y = (y_1, ..., y_n)$.

---

## Pure Python approach: simulate toy data

Set some parameters:
```python
import random

n = 100
a_true, b_true = 2.0, 1.0
noise_std = 1.0
```

Create a simulated dataset:
```python
X_train = [random.uniform(0, 10) for _ in range(n)]
y_train = [a_true * x + b_true + random.gauss(0, noise_std) for x in X_train]
```

---


## Computing slope & intercept

Implement mean, variance, covariance manually:

```python
def mean(values):
    return sum(values) / len(values)

def covariance(x, y, x_mean, y_mean):
    return sum((xi - x_mean)*(yi - y_mean) for xi, yi in zip(x, y)) / len(x)

def variance(values, mean_value):
    return sum((v - mean_value)**2 for v in values) / len(values)

x_mean, y_mean = mean(X_train), mean(y_train)
a = covariance(X_train, y_train, x_mean, y_mean) / variance(X_train, x_mean)
b = y_mean - a * x_mean
```

---

## NumPy approach: generate toy data

Set some parameters
```python
np.random.seed(42)
n_samples = 50

true_a, true_b = 2.5, 1.0
```

Create toy dataset:
```python
x = np.random.uniform(0, 10, size=n_samples)
noise = np.random.normal(0, 2, size=n_samples)
y = true_a * x + true_b + noise
```

---

## NumPy implementation

Compute the solution using NumPy API:

```python
x_mean = np.mean(x)
y_mean = np.mean(y)

cov_xy = np.mean((x - x_mean) * (y - y_mean))
var_x = np.mean((x - x_mean) ** 2)

a = cov_xy / var_x
b = y_mean - a * x_mean
```

We only use the `np.mean` method, are there other ways?

---

## Visualizing the fit

Generate some test inputs
```python
x_test = np.linspace(0, 10, 100)
y_pred = a * x_test + b
```

Plot the result with `matplotlib`
```python
import matplotlib.pyplot as plt

plt.scatter(x, y, label="Noisy data")
plt.plot(x_test, true_a * x_test + true_b, color="green", linestyle="--", label="True line")
plt.plot(x_test, y_pred, color="red", label="Fitted line")
plt.legend()
```

---

### Too easy? Multidimensional linear regression 🔥

We now have vectors $x_i \in \mathbb{R}^d$:

$$
y_i \approx w^\top x_i + b
$$

- Still linear, but in higher dimensions  
- Same principle: minimize MSE  
- Solution uses **matrix algebra**.
- Find the analytical solution for $w$ and implement it in Python.

* $$\hat{w} = (X^\top X)^{-1} X^\top y$$

---

### A bit harder? Ridge regression 🔥🔥

We now **penalize large weights** to avoid overfitting:

$$
\mathcal{L}(w) = \frac{1}{n} \sum_i (y_i - w^\top x_i - b)^2 + \lambda \|w\|_2^2
$$

- Same idea: minimize the MSE  
- But now with a regularization term controlled by $\lambda$
- Find the analytical solution for $w$ and implement it

<p data-marpit-fragment>💡 Closed-form solution:</p>

<p data-marpit-fragment>
$$
\hat{w} = (X^\top X + \lambda I)^{-1} X^\top y
$$
</p>

---


## Summary

- Generated noisy toy data with a linear relationship  
- Implemented linear regression in two ways:
  - Pure Python (lists + loops)
  - NumPy (vectorized, analytical)  
- Derived slope & intercept from covariance and variance  
- Visualized fitted vs true line  
