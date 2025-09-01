---
theme: gaia
class:
  - lead
marp: true
paginate: true
size: 16:9
header: ENSAI - 2A - Programmation algorithmique en Python - 2025/2026
# footer: 2025 - 2026
markdown.marp.enableHtml: true
---

<style>

img[alt~="center"] {
  display: block;
  margin: 0 auto;
}
blockquote {
  background: #ffedcc;
  border-left: 10px solid #d1bf9d;
  margin: 1.5em 10px;
  padding: 0.5em 10px;
}
blockquote:before{
  content: unset;
}
blockquote:after{
  content: unset;
}
</style>

### Algorithms and Programming in Python

Today:
1. Introduction: objectives, schedule & exam
2. Basics about Python & NumPy
3. Warm-up with linear regression

----

### Objectives

The objective is to implement a few optimization algorithms:

* Gradient descent (GD)
* Accelerated gardient descent (momentum, NAG)
* Proximal/projected gradient descent
* Stochastic gradient descent (SGD)
* ...

And develop good development practices in Python for ML.

----

### Schedule

* Basics about Python, NumPy & Scipy + linear regression ~ 3h
* Ridge regression (GD, NAG, SGD) ~ 3h
* Elastic-net (proximal gradient descent) ~ 3h
* Gaussian mixture model (projected gradient descent, EM) ~ 3h
* Reproductibility, metrics, and evaluation ~ 3h
* Exam ~ 3h

---

### Exam

* 3 hours in class
* Access to online documentation
* LLMs are forbidden, we're not here to learn vibe coding
* One exercise closely related to what we've done in class

**Example**
* A slighly different optimization algorithm
* Applying what we've done to a real world problem