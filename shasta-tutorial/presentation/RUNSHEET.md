# Run Sheet — SHASTA Tutorial

These timings are **estimates**, not yet validated against a live run (see `README.md`'s Status section) — do a full dry run yourself and adjust before presenting to a real audience. They assume attendees followed `SETUP.md` beforehand and arrive with a working install.

## Timing (approx. 50 minutes, 21 slides)

| Part | Slides | Time | What happens |
|---|---|---|---|
| 1. Why SHASTA | 6 | ~10 min | Talk-through, no hands-on. The full-bleed map slide is a good place to pause for questions — it's the most concrete "oh, I get it" moment before any code. |
| 2. Install SHASTA | 3 | ~10 min | Everyone runs `shasta maps` and `shasta demo` live. This is the first failure-prone checkpoint — see below. |
| 3. Experience a mission | 3 | ~10 min | Everyone runs `shasta gui` and sends at least one group somewhere. Let this run long if the room is engaged; it's the most memorable part. |
| 4. Configure & extend | 8 | ~15–20 min | Mix of talk-through (the gotchas slide) and live typing (the Python API snippet, then `labs/custom_experiment.py`). |
| Wrap-up | 1 | ~5 min | Point people at `labs/` and the main repo README. |

## Expected failures (and what to say)

These are the real issues in `README.md`'s "Repo issues this tutorial exposed" list, reframed as what you'll actually see happen in the room:

- **Someone's `pip install ihuman-shasta[gui]` fails** (they skipped `SETUP.md` or typo'd the clone-based install). Fix: `pip install -e ".[gui]"` from inside the cloned directory. Worth saying out loud before Part 2 starts, since it's the single most likely stumble.
- **`shasta demo` or `shasta gui` doesn't open / errors about a display** on a remote or headless machine. There's no in-session fix for this — point them at the Python API in Part 4, which works headless, and let them follow along by reading rather than typing during Part 3.
- **Someone tries `config['core']['map_name']`** while following along with Part 4 and gets a `KeyError`. This is gotcha #2 on the "trips you up" slide — if you see confused faces before you reach that slide, it's worth calling out early.
- **Someone reruns their script and hits `ValueError: Cannot load an actor multiple times.`** — almost always from reusing a Jupyter/REPL variable holding the old `groups` dict. Gotcha #2 on the same slide; tell people in a notebook to re-run the whole cell, not just the last line.
- **A `GoToNodeExperiment` mission occasionally crashes mid-loop with `IndexError`.** This is real and intermittent (issue 4 in the README) — if it happens live, don't panic-debug it; say "this is a known intermittent bug, see the README," and move on. Don't promise a fix on the spot.

## Cut list (if running short on time)

In order of what to drop first:

1. The "How It Fits Together" pipeline slide in Part 1 (nice context, not load-bearing).
2. `labs/custom_experiment.py` walk-through in Part 4 — mention it exists and point people to it afterward instead of live-coding it.
3. The "teaming loop" stats slide in Part 1 — fold its point into the spoken intro instead.

Do **not** cut the "Three Things That Will Trip You Up" slide — it's cheaper to show it once than to answer the same three questions individually while everyone's stuck.

## After the session

Note anything that didn't match this run sheet — a different failure mode, a timing that was way off, a slide nobody needed — and fold it back into `README.md` and this file before the next run, the same way this tutorial's own "issues exposed" list came from actually running everything once.
