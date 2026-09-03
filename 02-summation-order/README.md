# 02 · Summation order

## Question
Does summing the same sequence of numbers in a different order change the
result? Why?

## Prediction
Even with the summation method held fixed, changing the positions of the numbers
causes shifts at the level of the fractional digits. The reason is the ulp
behaviour from the previous experiment: anything more than half an ulp away goes
to the next representable value up, anything less goes to the one below, and an
exact tie goes to the even one. If the fractional parts mostly sit close to the
value below, say 100.2 rounding down to 100, then I expect a linear decline in
the negative direction. If the opposite happens, I expect a linear but noisy line
in the positive direction. There will be noise either way, but the overall trend
should be visible from the majority.

Concretely:

- spread across many random shuffles of the same array (n = 1e6, sum ~5e5):
  half an ulp at this magnitude is 2.9e-11. If the rounding errors accumulate in
  one direction the spread should be around 2.9e-05; if they partly cancel it
  should be around 2.9e-08. I expect the first one.
- most accurate ordering, and why: TODO
- least accurate ordering, and why: TODO
- does the gap grow with n: linearly, so a 10x increase in n should give roughly
  a 10x wider spread.

## Setup

TODO

Environment: NumPy ?, Python ?. Data: `np.random.default_rng(?)`, ?

| label | how |
|---|---|
| TODO | TODO |

Run with `python deney.py`.

## Result

### TODO

| | | |
|---|---|---|
| | | |

### TODO

| | | |
|---|---|---|
| | | |

## What I got wrong

**1.** TODO

**2.** TODO

**3.** TODO

**Found by accident:** TODO

## Sources

Read after running the experiment, not before.

- TODO
- TODO