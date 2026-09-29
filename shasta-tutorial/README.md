# SHaSTA Tutorial

A hands-on introduction to [SHaSTA](https://doi.org/10.21203/rs.3.rs-4338790/v1) (Simulator for Human And Swarm Team Applications) for HCI and human-factors researchers, built on the iHuman Lab Quarto reveal.js template — structured the same way as [`mosaic-smc-tutorial`](../mosaic-smc-tutorial/), the sibling tutorial for MOSAIC.

The narrative thread is human–swarm teaming: SHaSTA is a pybullet-based testbed where UAV and UGV groups move in formation along real city street networks (built from OpenStreetMap), commanded by a human, a scripted policy, or an RL agent through one Gymnasium interface. The deck is four parts:

1. **Why SHaSTA** — the human–swarm teaming question, what SHaSTA is, how the OSM → OSM2World → pybullet → Gymnasium pipeline fits together, and the order/plan/execute/observe teaming loop
2. **Install SHaSTA** — the PyPI package isn't published yet, so this installs from a clone, then verifies with `shasta maps` and `shasta demo`
3. **Experience a mission** — no code: `shasta gui`, the controls table, and what the side panel shows
4. **Configure & extend** — the Python API (`ShastaEnv`, `load_config`, `GoToNodeExperiment`), three real gotchas found while building this tutorial, and writing your own experiment by subclassing `BaseExperiment`

## Team

SHaSTA is a joint project of Oklahoma State University (iHuman Lab) and the University at Buffalo. Slide 2 introduces Hemanth Manjunatha (OSU) and Ehsan T. Esfahani, Souma Chowdhury and Karthik Dantu (UB), and credits the other authors of the [SHaSTA paper](https://doi.org/10.21203/rs.3.rs-4338790/v1). Photos are in `assets/team/`; roles and photos were taken from public university pages and should be checked with each person.

## Status

This is a first working draft, not a rehearsed multi-hour workshop like the MOSAIC tutorial yet. Everything in the deck — every command, every code snippet, both lab scripts — was actually run against a clean editable install of SHaSTA while writing this, not just described from the README. What's *not* yet done:

- No `shasta gui` screenshots — the assets here are headless offscreen renders (`pybullet`'s software `TinyRenderer`, via `p.DIRECT`), which don't need a display but also don't show the actual GUI chrome (side panel, buttons, event log). Getting real GUI screenshots needs either a machine with a display or a virtual one (Xvfb) that wasn't available when this was built.
- No GIFs of an actual mission playing out (MOSAIC's tutorial has several, captured with dedicated `tools/capture_*.py` scripts against a running game — SHaSTA has no equivalent capture tooling yet).
- Not rehearsed against a live audience, so there's no `RUNSHEET.md` timing data from an actual run — the timings in `RUNSHEET.md` are estimates.
- `shasta fetch-osm` / `shasta build-map` (building a map of your own site) is described in the deck but not exercised here — it needs Java and network access to the Overpass API.

## Contents

```
shasta-tutorial/
├── shasta-tutorial.qmd   # the deck — edit this
├── theme.scss             # lab theme (unmodified from the templates repo)
├── README.md              # this file
├── SETUP.md               # send this to attendees before the session
├── RUNSHEET.md             # facilitator timings (estimated, not yet rehearsed)
├── assets/                 # figures used in the deck (team/ holds the portraits)
└── labs/                   # tested standalone scripts the deck points to
    ├── play.py               # a minimal mission with an EDIT ME block of knobs
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
| `swarm-topdown.png` | Same technique, top-down, captured a few steps into a `GoToNodeExperiment` mission — the small markers near the center-left are the UAV group. Used on the "Open the GUI" slide as a stand-in until a real `shasta gui` screenshot exists. |
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

1. Send `SETUP.md` to registrants ahead of time.
2. Re-run every command in Part 2 against the current `main` of the SHaSTA repo — issue 1 above (PyPI) may be resolved by then.
3. Read `RUNSHEET.md` — its timings are estimates, not yet validated against a live run; adjust after your first dry run.
4. Decide whether to attempt a real `shasta gui` screenshot session beforehand (needs a display or Xvfb) — Part 3 currently uses a headless render as a stand-in.
