# SHaSTA Tutorial

Session 2 of **Closing the Human–AI Loop: Modular Architectures for Autonomous Teaming and Physiological Sensing**, a joint tutorial by Oklahoma State University and the University at Buffalo at IEEE SMC 2026. A hands-on introduction to [SHaSTA](https://doi.org/10.21203/rs.3.rs-4338790/v1) (Simulator for Human And Swarm Team Applications) for HCI and human-factors researchers, built on the iHuman Lab Quarto reveal.js template. Session 1, [`mosaic-tutorial`](../mosaic-tutorial/), is the sibling tutorial for MOSAIC.

The narrative thread is human–swarm interaction (HSI): SHaSTA is a pybullet-based testbed where an operator commands UAV and UGV groups that move in formation along real city street networks, and where the operator's actions can be recorded on one clock with physiological data. The deck never treats the swarm as the point; the person is.

Everything runs in the browser, on the tutorial's Jupyter server: attendees open one notebook, `01_shasta_hsi.ipynb` in the SHaSTA repository, and command the swarm in it. Nothing is installed on their laptops; the install is a single appendix slide. The deck is four parts:

1. **Why human–swarm interaction** — the research question, the four dimensions a testbed has to vary (interface, AI, human factors, swarm), what SHaSTA is (its four components and the observe/decide/command/execute loop, on one slide)
2. **Open the notebook** — scan the QR code, sign in to the tutorial server, pick the kernel, run Step 1: the map as a street graph and the config file, then a checkpoint
3. **Put a human in the loop** — *Play It Yourself* (Step 3): the interface in the browser, with the mouse; the controls; `SwarmCommander` as the one seam any operator plugs into; *No Human Required*, the same environment through the Gym API (Step 2); *The PyBullet World*, the physics running with no window and rendered in 3D so you can interact with it (Step 3); *What You Can Customize* (Step 4); and *Build a Map of Anywhere* (Step 4), a map of any place from OpenStreetMap in a few seconds. A 10-minute break follows
4. **Measure the human, then extend** — Lab Streaming Layer (LSL): why it matters, logging the operator's orders, recording your own session (Step 7), analysing it (Step 8), the gotchas, and writing your own experiment with `BaseExperiment` (Step 5)

The appendix holds the install for a laptop, and how to record a real study with an eye tracker on the tracker's laptop.

## Contents

```
shasta-tutorial/
├── shasta-tutorial.qmd   # the deck — edit this (33 slides: 29 main, one of them the break + closing + 3 appendix)
├── theme.scss            # lab theme, plus team, card-grid and title-slide styles, and the code-card / task-split /
│                         #   numbered-step layouts copied from the MOSAIC tutorial's theme
├── README.md             # this file
├── SETUP.md              # send this to attendees before the session: nothing to install, plus the optional laptop install
├── RUNSHEET.md           # facilitator timings (estimated, not yet rehearsed)
├── assets/               # figures used in the deck (team/ holds the portraits)
├── tools/                # capture_notebook_figures.py draws the figures that come from the notebook
└── labs/                 # standalone scripts from the earlier, laptop-based version of the tutorial; the deck no longer
                          #   uses them (the notebook has their content), safe to delete
```

## The notebook

The session runs on `notebooks/01_shasta_hsi.ipynb` in the SHaSTA repository, with four helpers next to it: `config.yaml` (the simulation as a text file), `live_play.py`
(shows the pygame interface in the browser and passes the mouse and keys to it), `world_view.py` (the interactive 3D view of the PyBullet world) and `lsl_tools.py` (recording and analysis). `live_play.py` and
`lsl_tools.py` are the same files as in the MOSAIC tutorial's notebook folder. The deck follows the notebook's eight steps:

| Deck | Notebook |
| --- | --- |
| Part Two: your first map | Step 1: the map and the config file |
| Part Three: no human required | Step 2: actors, groups and the Gym API |
| Part Three: play it yourself, the PyBullet world, the seam | Step 3: human in the loop (the interface, the 3D world, then a scripted operator) |
| Part Three: what you can customize, build a map of anywhere | Step 4: what you can customize, then build a map of any place from OpenStreetMap |
| Part Four: build your own experiment | Step 5: write your own experiment |
| Part Four: why LSL | Step 6: LSL basics |
| Part Four: log the operator, record your own session | Step 7: record the operator and gaze |
| Part Four: analyse the recording | Step 8: analyse the recording |

The mouse input (a click on a marker or a street node, the Send button, the wheel, a right-drag, Shift-click) was tested with simulated browser events against the real
interface, and has **not** yet been tested in a real browser; see `RUNSHEET.md`.

## Team

SHaSTA is a joint project of Oklahoma State University (iHuman Lab) and the University at Buffalo. Slide 2 introduces Hemanth Manjunatha (OSU) and Ehsan T. Esfahani, Souma Chowdhury and Karthik Dantu (UB), and credits the other authors of the [SHaSTA paper](https://doi.org/10.21203/rs.3.rs-4338790/v1). Photos are in `assets/team/`; roles and photos were taken from public university pages and should be checked with each person.

## Status

A working draft, not yet rehearsed with an audience. The commands and code in the deck were run against a clean editable install of SHaSTA (`pip install -e ".[gui]"`), and every code
cell of the notebook was run headless with a simulated session. What is *not* yet done:

- **LSL is not part of `ihuman-shasta`.** The paper describes an LSL layer (recording of operator inputs, mission events, EEG and eye tracking), but the released package contains no LSL
  code. The notebook's `lsl_tools.py` is that layer: it forwards `SwarmCommander` events to an LSL marker stream, and records them with a gaze stream. In the notebook the gaze is
  synthetic; a real tracker, EEG and LabRecorder are standard LSL tooling and were **not** exercised here. `tobii_to_lsl.py` and `shasta_gui_lsl.py` (the real-study route, appendix slide 33)
  have not been run against real hardware in this repository.
- The interface screenshot (`assets/gui.png`) is a real capture of `shasta gui`: the window was driven offscreen with SDL's dummy video driver, given two orders, and the pygame surface saved.
- The paper's own study used a pyglet interface; the interface shipped in this package is pygame-based.
- No GIFs of a mission playing out (MOSAIC's tutorial has several).
- Not rehearsed against a live audience; the timings in `RUNSHEET.md` are estimates.
- Building a map of any place (Step 4, slide 20) runs `fetch_osm` and `build_map` from the notebook: it needs Java 11 or newer (the cell downloads one if there is none) and network access to the Overpass API and to GitHub (the OSM2World tool). It was tested end to end for downtown Bellevue (about ten seconds, calibration error under 0.01 m), not on the hub.

## Render

```bash
quarto render shasta-tutorial.qmd     # build once
quarto preview shasta-tutorial.qmd    # live-reload while editing
```

Run both from this directory. Navigate with arrow keys, `f` for fullscreen, `s` for speaker notes.

## Assets

| File | Source |
| --- | --- |
| `world-angled.png` | A headless pybullet render (`getCameraImage` via `ER_TINY_RENDERER`, no display needed) of `buffalo-small`'s OSM2World mesh from an elevated angle. Not used in the deck at the moment (the title slide is plain, to match the MOSAIC deck). |
| `world-overview.png` | The same map, top-down, wider frame. Not currently used in the deck — a spare in case you want a second establishing shot. |
| `swarm-topdown.png` | Same technique, top-down, captured a few steps into a `GoToNodeExperiment` mission. Not currently used in the deck. |
| `gui.png` | A real `shasta gui` capture (see Status). Used on the "Play It Yourself" slide. |
| `map-graph.png`, `world-3d.png`, `gaze-timeline.png`, `gaze-heatmap.png` | Drawn by `tools/capture_notebook_figures.py` by running the notebook's own cells: Step 1's street graph, Step 3's 3D PyBullet view (after a simulated click on the ground), and Step 8's gaze timeline and heatmap from a short simulated session with synthetic gaze. `gaze-heatmap.png` is not used in the deck at the moment. Needs a SHaSTA checkout (`SHASTA_REPO`) |
| `qr-notebook.png` | The tutorial's Jupyter server, where the notebook runs: same code as in the MOSAIC tutorial (drawn by its `tools/make_qr.py`) |
| `team/*.jpg` | Portraits for the team slide, from public university pages. |
| `logo.png`, `background.jpg` | iHuman Lab template, unmodified. |

All three SHaSTA renders were captured with a short throwaway script (not checked in) that builds a `ShastaEnv`, steps it a few times, and calls `env.core.physics_client.getCameraImage(...)` directly — see the Configure & Extend part of the deck for the underlying API. Regenerating or adding more views just needs that same pattern with a different `cameraEyePosition`/`cameraTargetPosition`.

Redraw the notebook figures with:

```bash
SHASTA_REPO=<checkout of the SHaSTA repository> python tools/capture_notebook_figures.py
```

It runs the notebook in a temporary copy of its folder, so nothing is written to the checkout.

## Repo issues this tutorial exposed

Verified against a clean editable install (`pip install -e ".[gui]"`) of this checkout. The deck teaches around all of these.

1. **`ihuman-shasta` isn't on PyPI yet.** The main `README.md`'s `pip install "ihuman-shasta[gui]"` fails with "No matching distribution found." Install from a clone instead until this is published.
2. **The map-selection config key is one level deeper than you'd guess.** It's `config['experiment']['map_to_use']`, not `config['core']['map_name']` (which doesn't exist — `load_config()`'s default dict has no `'core'` key at all).
3. **Actors can't be reused across environments.** Building a second `ShastaEnv(config, groups)` with the same `groups` dict from an earlier one raises `ValueError: Cannot load an actor multiple times.` Build a fresh `groups` dict (fresh `UAV()`/`UGV()` instances) per environment.
4. **`GoToNodeExperiment.apply_actions` can raise `IndexError` intermittently.** Continuing to call `env.step(None)` after one group's path has emptied but the mission isn't yet globally complete (the other group hasn't arrived) sometimes hits `path[0]` on an empty list at `shasta/experiments.py:54`. Seen once in three otherwise-identical runs with two groups sent to the same target node — not yet root-caused as fully deterministic or reliably reproducible with a fixed seed. Sending groups to targets roughly the same distance away seems to avoid it in practice.
5. **`Mission.random(map, n, seed=...)`'s count should match your number of groups.** Passing `n=3` against an env with only two groups (as in the main README's `SwarmCommander` example) leaves the mission permanently incomplete — the third target is never assigned to a real group, so `mission.is_complete()` never returns `True` even after the groups you did send reach their targets.

## Before presenting

1. Send `SETUP.md` to registrants ahead of time: it asks them to sign in to the tutorial server and run Step 1 once, which is the whole preparation.
2. Put the current notebook and its helpers on the server (see `RUNSHEET.md`) and run it top to bottom as an attendee. **Test the mouse in a real browser**, and load-test it with several simultaneous players.
3. Read `RUNSHEET.md`: its timings are estimates, not yet validated against a live run; adjust after your first dry run.
4. Decide how to handle LSL: the notebook shows the paper's pattern with synthetic gaze; if you can, try `tobii_to_lsl.py` and `shasta_gui_lsl.py` beside a real tracker and recorder once, so the real-study slide is something you have seen work.
