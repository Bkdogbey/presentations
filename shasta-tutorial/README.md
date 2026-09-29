# SHaSTA Tutorial

A hands-on introduction to [SHaSTA](https://doi.org/10.21203/rs.3.rs-4338790/v1) (Simulator for Human And Swarm Team Applications) for HCI and human-factors researchers, built on the iHuman Lab Quarto reveal.js template — structured the same way as [`mosaic-smc-tutorial`](../mosaic-smc-tutorial/), the sibling tutorial for MOSAIC.

The narrative thread is human–swarm interaction (HSI): SHaSTA is a pybullet-based testbed where an operator commands UAV and UGV groups that move in formation along real city street networks, and where the operator's actions can be recorded on one clock with physiological data. The deck never treats the swarm as the point; the person is. It is four parts:

1. **Why human–swarm interaction** — the research question, the four dimensions a testbed has to vary (interface, AI, human factors, swarm), what SHaSTA is (its four components and the observe/decide/command/execute loop, on one slide)
2. **Install SHaSTA** — the PyPI package isn't published yet, so this installs from a clone, then verifies with `shasta maps` and `shasta demo`
3. **Put a human in the loop** — the built-in interface (`shasta gui`, its controls and side panel), `SwarmCommander` as the one seam that any operator (scripted, AI, or your own interface) plugs into, shown with a script that runs with only pybullet and no interface
4. **Measure the human, then extend** — Lab Streaming Layer (LSL): why it matters, logging operator events to an LSL stream and what a recorder sees, then the gotchas and writing your own experiment with `BaseExperiment`

## Team

SHaSTA is a joint project of Oklahoma State University (iHuman Lab) and the University at Buffalo. Slide 2 introduces Hemanth Manjunatha (OSU) and Ehsan T. Esfahani, Souma Chowdhury and Karthik Dantu (UB), and credits the other authors of the [SHaSTA paper](https://doi.org/10.21203/rs.3.rs-4338790/v1). Photos are in `assets/team/`; roles and photos were taken from public university pages and should be checked with each person.

## Status

This is a working draft, not a rehearsed multi-hour workshop like the MOSAIC tutorial yet. The commands and code in the deck were run against a clean editable install of SHaSTA (`pip install -e ".[gui]"`). What's *not* yet done:

- **LSL is not part of `ihuman-shasta`.** The paper describes an LSL layer (recording of operator inputs, mission events, EEG and eye tracking), but the released package contains no LSL code. Part 4 teaches the concept from the paper and shows a small add-on pattern, `labs/lsl_markers.py`, which forwards `SwarmCommander` events to an LSL marker stream. That script was run, and its output is what the "Log the Operator" slide shows. The recorder side (LabRecorder, the XDF file, analysis with `pyxdf`) and the EEG and eye-tracker streams are standard LSL tooling and were **not** exercised here.
- The interface screenshot (`assets/gui.png`) is a real capture of `shasta gui`: the window was driven offscreen with SDL's dummy video driver, given two orders, and the pygame surface saved. It shows a real mission mid-flight.
- The paper's own study used a pyglet interface; the interface shipped in this package is pygame-based.
- No GIFs of a mission playing out (MOSAIC's tutorial has several).
- Not rehearsed against a live audience; the timings in `RUNSHEET.md` are estimates.
- `shasta fetch-osm` / `shasta build-map` (building a map of your own site) is mentioned but not exercised here — it needs Java and network access to the Overpass API.

## Contents

```
shasta-tutorial/
├── shasta-tutorial.qmd   # the deck — edit this
├── theme.scss             # lab theme, plus team, card-grid and title-slide styles
├── README.md              # this file
├── SETUP.md               # send this to attendees before the session
├── RUNSHEET.md             # facilitator timings (estimated, not yet rehearsed)
├── assets/                 # figures used in the deck (team/ holds the portraits)
└── labs/                   # tested standalone scripts the deck points to
    ├── play.py               # a minimal mission with an EDIT ME block of knobs
    ├── human_loop.py         # a scripted operator driving SwarmCommander, no interface
    ├── lsl_markers.py        # the same loop, logging operator events to an LSL stream
    └── custom_experiment.py  # the smallest complete BaseExperiment subclass
```

## Render

```bash
quarto render shasta-tutorial.qmd     # build once
quarto preview shasta-tutorial.qmd    # live-reload while editing
```

Run both from this directory. Navigate with arrow keys, `f` for fullscreen, `s` for speaker notes.

## Assets

| File | Source |
| --- | --- |
| `world-angled.png` | A headless pybullet render (`getCameraImage` via `ER_TINY_RENDERER`, no display needed) of `buffalo-small`'s OSM2World mesh from an elevated angle. Used on the title slide and the "one real place" slide. |
| `world-overview.png` | The same map, top-down, wider frame. Not currently used in the deck — a spare in case you want a second establishing shot. |
| `swarm-topdown.png` | Same technique, top-down, captured a few steps into a `GoToNodeExperiment` mission. Not currently used in the deck. |
| `gui.png` | A real `shasta gui` capture (see Status). Used on the "Open the Interface" slide. |
| `team/*.jpg` | Portraits for the team slide, from public university pages. |
| `logo.png`, `background.jpg` | iHuman Lab template, unmodified. |

All three SHaSTA renders were captured with a short throwaway script (not checked in) that builds a `ShastaEnv`, steps it a few times, and calls `env.core.physics_client.getCameraImage(...)` directly — see the Configure & Extend part of the deck for the underlying API. Regenerating or adding more views just needs that same pattern with a different `cameraEyePosition`/`cameraTargetPosition`.

## Repo issues this tutorial exposed

Verified against a clean editable install (`pip install -e ".[gui]"`) of this checkout. The deck teaches around all of these.

1. **`ihuman-shasta` isn't on PyPI yet.** The main `README.md`'s `pip install "ihuman-shasta[gui]"` fails with "No matching distribution found." Install from a clone instead until this is published.
2. **The map-selection config key is one level deeper than you'd guess.** It's `config['experiment']['map_to_use']`, not `config['core']['map_name']` (which doesn't exist — `load_config()`'s default dict has no `'core'` key at all).
3. **Actors can't be reused across environments.** Building a second `ShastaEnv(config, groups)` with the same `groups` dict from an earlier one raises `ValueError: Cannot load an actor multiple times.` Build a fresh `groups` dict (fresh `UAV()`/`UGV()` instances) per environment.
4. **`GoToNodeExperiment.apply_actions` can raise `IndexError` intermittently.** Continuing to call `env.step(None)` after one group's path has emptied but the mission isn't yet globally complete (the other group hasn't arrived) sometimes hits `path[0]` on an empty list at `shasta/experiments.py:54`. Seen once in three otherwise-identical runs with two groups sent to the same target node — not yet root-caused as fully deterministic or reliably reproducible with a fixed seed. Sending groups to targets roughly the same distance away seems to avoid it in practice.
5. **`Mission.random(map, n, seed=...)`'s count should match your number of groups.** Passing `n=3` against an env with only two groups (as in the main README's `SwarmCommander` example) leaves the mission permanently incomplete — the third target is never assigned to a real group, so `mission.is_complete()` never returns `True` even after the groups you did send reach their targets.

## Before presenting

1. Send `SETUP.md` to registrants ahead of time (it includes the optional `pip install pylsl` for Part 4).
2. Re-run every command in Part 2 against the current `main` of the SHaSTA repo — issue 1 above (PyPI) may be resolved by then.
3. Read `RUNSHEET.md` — its timings are estimates, not yet validated against a live run; adjust after your first dry run.
4. Decide how to handle LSL: either keep the slides as a description of the paper's platform plus the add-on pattern, or add LSL to the SHaSTA repo first and update Part 4 to show the real thing.
5. If you can, run `labs/lsl_markers.py` beside a real LSL device and recorder once, so the "session" step is something you have seen work.
