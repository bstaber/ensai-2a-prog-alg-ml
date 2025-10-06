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

### Too easy? Multidimensional linear regression (1/2) 🔥

We now have vectors $x_i \in \mathbb{R}^d$:

$$
y_i \approx w^\top x_i
$$

Objective:
$$
\min_w \ \|y - Xw\|_2^2
$$

Find the analytical solution for $w$ and implement it in Python.

Closed-form solution:

* $$\hat{w} = (X^\top X)^{-1} X^\top y$$

---

### Too easy? Multidimensional linear regression (2/2) 🔥

Add an intercept:

$$
y_i \approx w^\top x_i + b
$$

Find the analytical solution for $w$ and $b$, and implement it in Python.

Closed-form solution:

* Let $\tilde{X} = \begin{bmatrix} X & \mathbf{1} \end{bmatrix}$, $\tilde{w} = \begin{bmatrix} w \\ b \end{bmatrix}$.
* $$\hat{\tilde{w}} = (\tilde{X}^\top \tilde{X})^{-1} \tilde{X}^\top y$$

---

### A bit harder? Ridge regression 🔥🔥

We now **penalize large weights** to avoid overfitting:

$$
\mathcal{L}(w) = \frac{1}{n} \sum_i (y_i - w^\top x_i - b)^2 + \lambda \|w\|_2^2
$$

- Same idea: minimize the MSE  
- But now with a regularization term controlled by $\lambda$
- Find the analytical solution for $w$ and implement it

Closed-form solution:

* $$\hat{w} = (X^\top X + \lambda I)^{-1} X^\top y$$

---

# k-Means clustering
Pure Python vs NumPy implementation

---

### k-Means clustering from scratch 🔥🔥🔥

Iterate until convergence:

1) Initialize centers $(C \in \mathbb{R}^{k \times d}$ (random rows of $X$)
2) Assign:
$$
a_i = \arg\min_j \|x_i - c_j\|^2
$$
3) Update:
$$
c_j = \text{mean of } \{x_i : a_i = j\}
$$

Stop when assignments don't change or $\|C^{(t)} - C^{(t-1)}\|$ is small

---
