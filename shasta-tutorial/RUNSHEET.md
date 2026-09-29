# Run Sheet — SHaSTA Tutorial

These timings are **estimates**, not yet validated against a live run (see `README.md`'s Status section) — do a full dry run yourself and adjust before presenting to a real audience. They assume attendees followed `SETUP.md` beforehand and arrive with a working install.

## Timing (approx. 50 minutes, 18 slides)

| Part | Slides | Time | What happens |
|---|---|---|---|
| Intro | 3 (title, team, agenda) | ~3 min | Introduce the joint OSU/UB team and the through-line: the *human* is the subject, the swarm is the apparatus. |
| 1. Why human–swarm interaction | 2 | ~8 min | Talk-through, no hands-on. "The Question" and its four cards carry the argument; "What Is SHaSTA" is where you say plainly that LSL and physiological recording are in the paper but added as a pattern in Part 4. |
| 2. Install SHaSTA | 1 | ~10 min | Everyone runs the clone steps, then `shasta maps` and `shasta demo` live. This is the first failure-prone checkpoint — see below. |
| 3. Put a human in the loop | 3 | ~12 min | Everyone runs `shasta gui` and sends at least one group somewhere. Then the pivot: `SwarmCommander` is the seam, and `labs/human_loop.py` runs the same mission with no interface. Let the interface part run long if the room is engaged. |
| 4. Measure the human, then extend | 4 | ~15 min | "Why LSL" and "Log the Operator" carry the message (run `labs/lsl_markers.py` live if pylsl is installed). The gotchas and `BaseExperiment` slides are talk-through; `labs/custom_experiment.py` is optional live typing. |
| Wrap-up | 1 | ~2 min | Point people at `labs/` and the main repo README. |

The four "Part" divider slides are not counted above; they take a few seconds each.

## Expected failures (and what to say)

These are the real issues in `README.md`'s "Repo issues this tutorial exposed" list, reframed as what you'll actually see happen in the room:

- **Someone's `pip install ihuman-shasta[gui]` fails** (they skipped `SETUP.md` or typo'd the clone-based install). Fix: `pip install -e ".[gui]"` from inside the cloned directory. Worth saying out loud before Part 2 starts, since it's the single most likely stumble.
- **`shasta demo` or `shasta gui` doesn't open / errors about a display** on a remote or headless machine. There's no in-session fix for this — point them at `labs/human_loop.py` in Part 3, which works with no display, and let them follow along by reading rather than typing during the interface slides.
- **Someone tries `config['core']['map_name']`** while following along and gets a `KeyError`. This is gotcha #1 on the "trips you up" slide — if you see confused faces before you reach that slide, it's worth calling out early.
- **Someone reruns their script and hits `ValueError: Cannot load an actor multiple times.`** — almost always from reusing a Jupyter/REPL variable holding the old `groups` dict. Gotcha #2 on the same slide; tell people in a notebook to re-run the whole cell, not just the last line.
- **`pip install pylsl` wasn't done, or LSL can't find the stream** (a firewall blocking discovery, or the outlet and inlet on different networks). Have people skip the live LSL run and read the recorded output on the "Log the Operator" slide instead. Say plainly that LSL is not in `ihuman-shasta` yet, so nobody goes looking for an LSL flag in the CLI.
- **A `GoToNodeExperiment` mission occasionally crashes mid-loop with `IndexError`.** This is real and intermittent (issue 4 in the README) — if it happens live, don't panic-debug it; say "this is a known intermittent bug, see the README," and move on. Don't promise a fix on the spot.

## Cut list (if running short on time)

In order of what to drop first:

1. The key table on "The Controls" slide — point people at `docs/human_interface.rst` instead.
2. `labs/custom_experiment.py` walk-through in Part 4 — mention it exists and point people to it afterward instead of live-coding it.
3. The "Options for your study" paragraph on "The Controls" — mention the flags when you demo the interface instead.

Do **not** cut the LSL slides — they are the reason this tutorial is about human–swarm *interaction* rather than swarm simulation — or the "Four Things That Will Trip You Up" slide, which is cheaper to show once than to answer individually while everyone's stuck.

## After the session

Note anything that didn't match this run sheet — a different failure mode, a timing that was way off, a slide nobody needed — and fold it back into `README.md` and this file before the next run, the same way this tutorial's own "issues exposed" list came from actually running everything once.
