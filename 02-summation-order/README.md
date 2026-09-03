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
- most accurate ordering, and why: left blank. I did not commit to a direction
  before running, so this experiment cannot tell me whether I would have guessed
  it right.
- least accurate ordering, and why: left blank, same reason.
- does the gap grow with n: linearly, so a 10x increase in n should give roughly
  a 10x wider spread.

## Setup

Environment: NumPy 2.5.2, Python 3.12. Data: one array of 1e6 values from
`np.random.default_rng(42).random(1e6)`, uniform in [0, 1), sum around 5.0e5.
The array is generated once and never regenerated; only its order changes.

Every sum uses the same method, a Python loop accumulating into a single float64
running total. This is deliberate: `np.sum` uses pairwise summation, which would
change the algorithm as well as the order and make the two effects impossible to
separate.

| label | how |
|---|---|
| reference | `math.fsum` on the original array, exact to the last bit |
| shuffled | 100 permutations from `rng.permutation`, naive loop on each |
| ascending | `np.sort(x)`, naive loop |
| descending | `np.sort(x)[::-1]`, naive loop |

Run with `python deney.py`.

### Limitations

- One seed, one value of n. The claim about how the spread grows with n is not
  tested here; that would need the same measurement repeated at 1e5, 1e6, 1e7.
- 100 permutations out of 1e6! possible orderings. The measured spread is a
  lower bound on the true spread and will widen slightly with more runs.
- `np.sum` was not measured across permutations, so how much pairwise summation
  absorbs the ordering effect is still an open question.

## Result

### Distance from the exact sum

Reference (`math.fsum`): 500026.4761740889

| ordering | sum | distance from reference |
|---|---|---|
| ascending | 500026.4761740878 | 1.11e-09 |
| best of 100 shuffles | | 1.12e-08 |
| descending | 500026.4761740702 | 1.87e-08 |
| worst of 100 shuffles | | 3.56e-08 |

Ascending order wins by a factor of ten over the closest competitor. Descending
order is no better than shuffling; it sits in the middle of the random spread.

### Spread across shuffles, predicted against measured

| scenario | spread |
|---|---|
| errors accumulate in one direction (n x half ulp) | 2.91e-05 |
| errors partly cancel (sqrt(n) x half ulp) | 2.91e-08 |
| measured across 100 shuffles | 4.68e-08 |

The measurement lands on the cancellation scenario, three orders of magnitude
away from the accumulation scenario.

### Which side of the reference

The best and worst shuffled sums fall on opposite sides of the exact value: the
largest is 1.12e-08 above it, the smallest 3.56e-08 below it. The results
scatter around the true answer rather than drifting away from it.

## What I got wrong

**1. I predicted a one-directional drift and got a two-sided scatter.** My
prediction assumed the roundings would mostly go the same way, so the total would
creep steadily off in one direction and grow linearly with n. The shuffled sums
land on both sides of the exact value instead. Round-half-to-even is designed to
prevent exactly the bias I was predicting, and I had already written down why in
experiment 01 without connecting it to this.

**2. The magnitude followed from that mistake.** I predicted a spread around
2.9e-05 and measured 4.68e-08, roughly 1600 half-ulps rather than a million. If
errors partly cancel, the total error grows like sqrt(n), not n. The square root
I guessed at in experiment 01 belongs here.

**3. Order does matter, but far less than the method does.** In experiment 01,
switching from a naive loop to `np.sum` changed the error by four orders of
magnitude at n = 1e7. Here, reordering the same data under a fixed method moves
the answer by 1e-08. Both are the same underlying phenomenon, but they are not
the same size.

**4. Sorting ascending is the cheapest accuracy win available.** Keeping the
accumulator small for as long as possible keeps its ulp small, so the small
addends stay above half an ulp and survive instead of being rounded away.
Descending order does the opposite: the accumulator is large from the start and
the small values at the end get absorbed. This falls straight out of the half-ulp
rule from experiment 01, which means I could have predicted it and did not.

**Found by accident:** with the integer array I started with, [1..10] and
[10..100], every ordering gave a bit-identical result. Small integers are exactly
representable and their sums are too, so there is no rounding for the order to
interact with. The effect needs both inexact values and an accumulator large
enough relative to the addends.

## Sources

Read after running the experiment, not before.

- **Nicholas Higham, "Accuracy and Stability of Numerical Algorithms", chapter 4.**
  The main source for this experiment. Error bounds for summation, and why the
  sqrt(n) growth is the right expectation rather than n. Also covers why sorting
  ascending helps, which is the finding above stated as a theorem.
- **David Goldberg (1991), section 4.3, "Errors in Summation".** Short. The same
  ground as Higham but in a few pages, and continuous with what I already read
  for experiment 01.
- **Python `math.fsum` documentation, and Shewchuk's exact summation algorithm.**
  I used `fsum` as ground truth without knowing how it works. Worth understanding
  what makes it exact rather than just accurate.
- **Kahan summation algorithm.** Carried over from experiment 01 and still not
  implemented. It belongs here: it is the answer to the problem this experiment
  measured. Writing it and adding it as a fourth row is the natural next step.
