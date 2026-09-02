# ml-experiments

100 self-directed experiments in machine learning and numerical computing.

Each one asks a question I cannot answer from memory, makes a prediction before
running anything, measures an answer, and records what I got wrong. The last part
is the point. An experiment where the prediction held taught me nothing; the ones
where it broke are why this repository exists.

## Structure

Each experiment lives in its own folder with the code and a README:

- **Question** — what I wanted to know
- **Prediction** — written before running the code, never edited afterwards
- **Setup** — data, parameters, random seed, how to reproduce
- **Result** — numbers and plots
- **What I got wrong** — the useful part
- **Sources** — read after the experiment, not before

Random seeds are fixed and recorded. Every number here should be reproducible.

## Progress

| # | Experiment | Status |
|---|---|---|
| 01 | Float32 vs float64 accumulation error | done |

## On AI assistance

The list of 100 questions was generated with an AI assistant. Everything after
that is mine to work out.

The code is written by hand. Experiment 01 is a partial exception: I was still
setting up the environment, and the naive-summation function came from an
assistant because I did not know the technique existed. The rest of that script
is mine, as is the debugging that made it run. Parts of its README were drafted
with assistance. From experiment 02 onward the code is entirely my own.

I do use an assistant for two things throughout: translating my notes from
Turkish into English, and catching grammar mistakes. The reasoning in "What I
got wrong" is mine in every case, written first in Turkish and then translated.