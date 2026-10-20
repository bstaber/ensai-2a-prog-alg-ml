# Session 1 instructor guide

This guide runs the three-hour Python and NumPy bridge for mathematically trained students with prior programming experience. It covers the timed core of the single session deck, slides 1–53 (the appendix, slides 54–75, is reference-only and excluded from the 180-minute clock).

## Before students arrive

Complete these checks before the live three-hour block:

1. Run `uv sync --locked` from the repository root.
2. Run the README smoke test.
3. Execute `notebooks/session01_solution.ipynb` from a clean kernel.
4. Open `notebooks/session01_starter.ipynb` and confirm its setup cells run.
5. Open the rendered deck (`docs/session01.html`) and verify the regression plot is visible.
6. Put the starter notebook URL or repository path where students can copy it.

Environment troubleshooting is not part of the 180-minute schedule. Pair a student with a working neighbor if an unresolved setup problem appears during class.

## Exact 180-minute run sheet

| Clock | Minutes | Material | Instructor action | Learner evidence |
|---|---:|---|---|---|
| 00:00–00:10 | 10 | Slides 1–4 · Introduction | State the audience contract, run the one-minute shape diagnostic on slide 1, then cover outcomes, schedule, and assessment constraints. Confirm setup is already complete. | Students predict `(50, 1)` and `(50, 50)`, then can name the six outcomes and exercise checkpoints. |
| 00:10–00:35 | 25 | Slides 5–23 · Python | Move quickly: this is a refresher. Pause for predictions on list aliasing, `range`, `zip`, and invalid function inputs. The appendix at the end of the deck is not taught live. | Students answer the inline output/contract questions before code is revealed. |
| 00:35–00:50 | 15 | Slides 24–27 · Python | Launch the MSE pair exercise, reveal the hint only at the timed cue, then debrief with the solution and checklist. | Both supplied assertions pass; empty and mismatched inputs raise `ValueError`. |
| 00:50–01:15 | 25 | Slides 28–38 · NumPy | Require a shape prediction before every expression. Use hand gestures or board axes for `axis=0` and `axis=1`. | Students state each output shape before execution. |
| 01:15–01:30 | 15 | Slides 39–43 · NumPy | Run the row-centering exercise. Offer pairwise distances only to fast finishers. Debrief shape, axis, and `keepdims`. | Shape checks pass and each row mean is numerically zero. |
| 01:30–01:40 | 10 | Break | Stop on time. Keep the regression notebook ready for the restart. | — |
| 01:40–02:00 | 20 | Slides 44–47 · Regression + solution-notebook Python baseline | Re-establish the shared dataset. Trace model → fit → predict → evaluate. Connect the formula to the prepared pure-Python baseline; only MSE was student-authored earlier. | Students can identify slope, intercept, residual, MSE, and baseline. |
| 02:00–02:30 | 30 | Slides 48–50 · Regression + starter notebook | Launch the NumPy regression exercise. Give the two staged hints at 10 and 20 minutes; reveal the solution only after checks. | Correct shapes, finite coefficients, and model MSE below baseline. |
| 02:30–02:40 | 10 | Slide 51 · Regression + solution notebook | Compare with `lstsq`, inspect the plot, discuss tolerance, then preview held-out validation. | Coefficients agree within `1e-12`; students explain why no explicit inverse is needed. |
| 02:40–02:50 | 10 | Slide 52 · Regression | Students answer individually before pair discussion. Do not show slide 53 early. | Six short answers sampling function writing, vectorization, reproducibility, shapes, evaluation, and verification. |
| 02:50–02:55 | 5 | Slide 53 · Regression | Reveal answers, restate the complete workflow, and bridge to the next session. | Students can narrate fit → predict → evaluate → verify. |
| 02:55–03:00 | 5 | Protected contingency | Absorb normal delays or questions. Do not schedule new material here. | Prepared content has already finished. |

**Rehearsal target:** finish all prepared content, including the summary, by 02:55. The final five minutes are protected contingency with no planned slide or activity.

## Exercise protocols

### Python MSE: 15 minutes

- **Launch, 2 minutes:** point students to the starter function contract and two assertions.
- **Pair work, 7 minutes:** require input validation as well as the nominal calculation.
- **Hint at minute 5 of the block:** use `zip`, square each difference, and divide by the number of targets.
- **Debrief, 4 minutes:** reveal the solution; ask why the length check must occur before `zip`.
- **Transition, 2 minutes:** connect the list implementation to element-wise array arithmetic.

Expected evidence:

```python
assert mse_py([1.0, 2.0], [1.0, 2.0]) == 0.0
assert mse_py([1.0, 3.0], [2.0, 1.0]) == 2.5
```

Empty and unequal inputs must raise `ValueError`.

### NumPy row centering: 15 minutes

- **Launch, 2 minutes:** students write input and desired output shapes before code.
- **Pair work, 7 minutes:** core task is row centering only.
- **Hint at minute 5 of the block:** `axis=1, keepdims=True`.
- **Debrief, 4 minutes:** identify the consumed axis and retained length-one axis.
- **Transition, 2 minutes:** show pairwise broadcasting only if time remains.

Required checks:

```python
assert row_means.shape == (3, 1)
assert centered.shape == points.shape
assert np.allclose(centered.mean(axis=1), 0.0)
```

Fast-finisher evidence: pairwise squared distances have shape `(3, 3)`, are symmetric, non-negative, and have a zero diagonal.

### NumPy regression: 30 minutes

- **Launch, 3 minutes:** restate the three-function contract and expected shapes.
- **Work to minute 10:** validate shapes and center arrays.
- **First hint:** expose `x_centered` and `y_centered`.
- **Work to minute 20:** compute slope and intercept.
- **Second hint:** expose covariance-over-variance and the intercept formula.
- **Final 10 minutes:** complete prediction, MSE, baseline, and invalid-input checks.
- **Stop at 30 minutes:** continue with the supplied solution rather than consuming the debrief block.

Expected nominal values:

```text
slope      2.5242
intercept  0.5373
model MSE  2.2939
baseline   51.4769
```

Required invalid cases: empty arrays, unequal shapes, 2-D inputs, and constant `x`.

## Checks for understanding

Ask for an answer before revealing or executing code:

- **Python:** What does assignment copy, the list or the reference? Why can `zip` hide a length mismatch? Where must validation occur?
- **NumPy:** What is the output shape? Which axis is consumed? Which length-one axis enables broadcasting? Does this operation share memory?
- **Regression:** Can students write the vectorized prediction function? Which values are learned during fit? Why must predictions match target shape? What do the explicit RNG, baseline, and `lstsq` checks establish?

Use the regression mini-assessment as the final individual check. Collect or inspect answers before showing slide 53.

## If timing slips

Cut in this order:

1. a non-outcome Python teaching slide (Strings, Tuples, Dictionaries, Sets, or Classes). Mention it in one line, then move on rather than dropping it entirely. These are reference-quality material that do not serve the six learning outcomes;
2. the NumPy pairwise-distance fast-finisher extension;
3. discussion of view/copy edge cases beyond the displayed examples;
4. extra plot interpretation beyond fit versus baseline;
5. audience questions that can be deferred to the break or after class.

Do not compensate by speaking faster. Do not cut the ten-minute break, regression exercise checks, mini-assessment, or final workflow summary. If rehearsal exceeds 175 minutes before contingency, remove optional discussion rather than compressing exercises.
