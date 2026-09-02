# 01 · Float32 vs float64 accumulation error

## Question
How far apart do float32 and float64 drift when summing the same
sequence of numbers, and how does the gap scale with the number of terms?

## Prediction
float32 stores fewer bits than float64, so every single addition carries a
small rounding error. My guess is that these errors accumulate and the gap
grows roughly with the square root of the number of terms, the way independent
errors usually add up. I am not confident about the reasoning here; I picked
the square root because errors that partly cancel each other tend to behave
that way, not because I derived it.

Concretely:
- at 1,000 terms: relative gap around 0.01%
- at 10,000,000 terms: relative gap around 1%
- growth: proportional to sqrt(n)

I expect the absolute difference to look large, but I am unsure whether the
relative difference stays small.

## Setup

NumPy 2.5.2, Python 3.12. Values drawn from `np.random.default_rng(42).random(n)`,
uniform in [0, 1). n from 1e3 to 1e8.

Three sums of the same data:

| label | how |
|---|---|
| reference | `x.astype(np.float64).sum()` |
| numpy f32 | `x.astype(np.float32).sum()` |
| naive f32 | Python loop accumulating into a single float32 running total |

Relative error is measured against the float64 reference.

Run with `python deney.py`.

## Result

### NumPy's sum in float32

| n | absolute error | relative error |
|---|---|---|
| 1e3 | 1.26e-05 | 2.53e-08 |
| 1e4 | 1.70e-04 | 3.41e-08 |
| 1e5 | 5.93e-04 | 1.18e-08 |
| 1e6 | 1.58e-02 | 3.17e-08 |
| 1e7 | 6.01e-02 | 1.20e-08 |
| 1e8 | 7.98e-01 | 1.60e-08 |

The absolute error grows, but only because the sum itself grows. The relative
error sits around 1e-08 across five orders of magnitude and shows no trend.

### Naive loop in float32

| n | naive sum | reference | relative error | growth vs previous |
|---|---|---|---|---|
| 1e3 | 497.178 | 497.178 | 6.39e-07 | |
| 1e4 | 4986.804 | 4986.798 | 1.14e-06 | 1.8x |
| 1e5 | 50109.828 | 50110.214 | 7.71e-06 | 6.8x |
| 1e6 | 499850.313 | 499843.328 | 1.40e-05 | 1.8x |
| 1e7 | 4999293.500 | 4999127.940 | 3.31e-05 | 2.4x |
| 1e8 | **16777216.000** | 50000751.202 | **6.64e-01** | 20063x |

Here the relative error does grow. Each row multiplies n by 10; sqrt(n) growth
would predict a factor of about 3.2 per row, linear growth a factor of 10. The
measured factors bounce between 1.8 and 6.8, averaging near the square root but
noisy, since each n is a single run with one seed.

The last row is a different kind of failure. The naive sum stops at exactly
16777216.0, which is 2^24, one third of the correct answer. It is not drifting;
it is stuck. Relative error jumps from 3e-05 to 0.66 in a single step.

### Why it stops at 2^24

The spacing between adjacent float32 values grows with magnitude:

| magnitude | spacing |
|---|---|
| 2^10 | 0.000122 |
| 2^20 | 0.125 |
| 2^23 | 1.0 |
| 2^24 | 2.0 |
| 2^25 | 4.0 |
| 2^30 | 128.0 |

Once the running total reaches 2^24, the next representable float32 is 2 away.
Every addend here is below 1, so each addition rounds straight back to the same
number and the total stops advancing. Verified directly:

```python
a = np.float32(2**24)
a + np.float32(1) == a          # True
a + np.float32(2) == a          # False
np.float32(2**25) + np.float32(2)   # 33554432.0, unchanged
```

At 2^25 the spacing is 4, so even adding 2 is absorbed. The threshold doubles
every time the magnitude doubles.

## What I got wrong

**1. The sqrt(n) prediction turned out roughly right, but not for what I was
measuring.** For the naive loop the growth does look close to a square root.
There was a lot of noise in it, and if I had collected many runs with different
seeds instead of one run per n, I expect it would have landed closer to sqrt(n).
For `np.sum` there is no growth at all, so my prediction was attached to the
wrong algorithm.

**2. The flat error has nothing to do with float32. It is a property of NumPy.**
I found this by comparing the naive loop against `np.sum`: same data, same
precision, same arithmetic, completely different error. The difference is in how
the sum is organised, not in how the numbers are stored.

**3. I thought 2^24 was a limit. It is not.** I believed it was a ceiling because
adding `np.float32(1)` to it returned the same number. What actually happens is
that the spacing between representable values has grown to 2 at that magnitude,
so anything smaller than that gets rounded away. Looking further up confirmed it:
at 2^25 the spacing is 4, and it keeps doubling as the magnitude doubles.

**4. I expected the error to degrade along a smooth line. It did not.** The
growth factors between consecutive rows came out as 1.8x, then 6.8x, then 1.8x,
then 2.4x. It is erratic rather than steady, at least with a single run per n.

**5. Found by accident:** while I thought I was testing float32, I was actually
still passing float64 to my naive loop. The Python loop returned a number ending
in 127 and `np.sum` returned one ending in 195, both starting with 497. Same
data, same type, same operation, different answers. As far as I understand, the
difference comes from NumPy summing in groups rather than one running total.

**6. I expected degradation to be gradual. It was a cliff** The first five rows live in the same world: relative error goes from 6.4e-07 to 3.3e-05, a factor of 50 across four orders of magnitude in n. Then one more step takes it to 0.66, a factor of twenty thousand. At n = 1e7 the naive loop is off by 0.003% and looks perfectly usable. At n = 1e8 it returns a third of the correct answer. Nothing in the earlier rows predicts this, because it is not the same failure: the sum hits 2^24 and stops moving. If I had only tested up to 1e7 I would have shipped
it. The error is silent either way, no exception and no warning, just a wrong number.

## Sources

Read after running the experiment, not before.

- **David Goldberg, "What Every Computer Scientist Should Know About
  Floating-Point Arithmetic"** (1991), sections on rounding error and on relative
  error and ulps. The "spacing" I measured with `np.spacing` is one ulp, and the
  fixed relative precision explains both the flat `np.sum` error and the 2^24
  wall.
- **IEEE 754 single-precision format.** 1 sign bit, 8 exponent bits, 23 stored
  fraction bits, 24 significant bits with the implicit leading one. 2^24 is where
  the integers stop being exactly representable.
- **NumPy `np.sum` documentation, Notes section**, and the NumPy 1.9 release
  notes, on pairwise summation. This is the source of finding 2.
- **Kahan summation algorithm.** A compensated summation method designed for
  exactly this problem. Not implemented here; a natural extension of this
  experiment.
