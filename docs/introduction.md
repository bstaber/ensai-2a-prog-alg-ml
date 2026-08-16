---
theme: rose-pine
_class: lead
marp: true
paginate: true
size: 16:9
header: ENSAI · Algorithms and Programming in Python
markdown.marp.enableHtml: true
---

# Python and NumPy for machine learning

A three-hour bridge for students who already know basic programming, elementary linear algebra, means, and variances.

**Before class:** start the supplied environment and notebook successfully. This setup check is not part of the live three-hour schedule.

**Opening diagnostic · no code:** if `x.shape == (50,)`, what are the shapes of `x[:, None]` and `x - x[:, None]`?

---

## What you will be able to do

By the end of this session, you can:

1. write small Python functions with lists, loops, and comprehensions;
2. reason about NumPy **shapes**, **dtypes**, and **axes**;
3. vectorize a calculation instead of writing loops;
4. generate reproducible data with an explicit random-number generator;
5. **fit, predict, and evaluate** a univariate linear-regression model;
6. verify results with invariants and `numpy.linalg.lstsq`.

---

## Agenda · first 90 minutes

| Time | Activity |
|---|---|
| 00:00–00:10 | Outcomes, prerequisites, setup confirmation, diagnostic |
| 00:10–00:35 | Essential Python syntax |
| 00:35–00:50 | Guided Python micro-exercise |
| 00:50–01:15 | NumPy arrays, shapes, dtypes, indexing, reductions |
| 01:15–01:30 | Shape and broadcasting exercise |

Exercises are part of the schedule, not optional extras.

---

## Agenda · final 90 minutes

| Time | Activity |
|---|---|
| 01:30–01:40 | **Break** |
| 01:40–02:00 | Regression problem and pure-Python baseline |
| 02:00–02:30 | NumPy regression pair exercise |
| 02:30–02:40 | Debrief, `lstsq`, numerical practice, and next-step preview |
| 02:40–02:50 | Mini-assessment |
| 02:50–02:55 | Summary and bridge to the next lecture |
| 02:55–03:00 | **Contingency** |

**Total: 180 minutes; prepared content finishes by 02:55.**

---

## Course roadmap

1. Python, NumPy, SciPy, and linear regression
2. Ridge regression with GD, momentum/NAG, and SGD
3. Elastic Net with proximal gradient descent
4. Gaussian mixtures with projected gradient and EM
5. Reproducibility, metrics, and evaluation
6. Final exam

Today we stop after one complete, reproducible linear-regression workflow.

---

## Assessment

- **Duration:** three hours in class
- **Resources:** access to online documentation
- **Not allowed:** LLM assistance
- **Format:** one exercise closely related to class work

A typical exam asks you to adapt an optimization algorithm or apply the course methods to a real-world problem.
