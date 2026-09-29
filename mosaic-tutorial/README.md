# MOSAIC Tutorial — IEEE SMC 2026

A two-hour hands-on tutorial introducing MOSAIC to HCI and human-factors
researchers, built on the iHuman Lab Quarto reveal.js template.

The narrative thread is human–AI teaming: MOSAIC is a configurable research
testbed for studying how humans and AI teammates collaborate during dynamic,
consequential tasks. The deck is four parts:

1. **Why MOSAIC** — the questions human–AI teaming research asks, why they need
   a configurable testbed, what MOSAIC is and how it works, search and rescue as
   the first testbed, and the teaming loop
2. **Install MOSAIC** — the dependency list, `venv` and Conda setup paths, an
   import checkpoint, and the first mission via `python -m experiment.main`
3. **Experience the SAR mission** — no code: the mission objective, the
   interface and what each tile means, victims and decoys, and the controls
4. **Configure MOSAIC** — a walk through `experiment/main.py`, the file
   attendees launched, in four parts: 4.1 SAR (the building, the camera,
   rewards), 4.2 GUI (the window and its feedback), 4.3 LLM (who answers `Alt`),
   4.4 Sensing (what every step records). Each part opens with one slide: the
   exact `main.py` lines and three things to change. One focused example
   follows: rewards and a keyless teammate (everyone tries), then the decoy
   flash, a real LLM, and a live eye tracker (presenter demos). Building
   settings and the observation-field print move to a notebook server (not
   built yet)

The appendix holds the other changes named on the part slides: locked rooms,
time limit, info panel, and what the teammate is told. A *Synchronized Record*
slide stays hidden until the eye-tracker rehearsal recording exists.

## Contents

```
presentation/
├── mosaic-tutorial.qmd   # the deck — edit this (39 slides: 33 main + closing + 5 appendix; one more hidden)
├── mosaic-tutorial.ipynb # optional development prototype; not required by attendees
├── theme.scss            # lab theme (template + team, fill-mode cards, horizontal flow,
│                         #   architecture diagram + .detached variant, annotated
│                         #   screenshots, .band notes, layer bands, you-are-here strip,
│                         #   .checkpoint callouts, dark-theme panel-tabset)
├── SETUP.md              # send this to attendees BEFORE the session
├── RUNSHEET.md           # facilitator timings, cut list, expected failures
├── assets/               # figures used in the deck
└── labs/                 # optional side examples; the deck itself runs experiment.main
    ├── play.py           # a minimal mission with an EDIT ME block of knobs
    ├── panel.py          # NoProgressPanel: the info panel without the "Remaining" count (appendix slide 38)
    ├── advisor.py        # ReliableTeammate: grounded advice with tunable reliability; no API key.
    │                     #   Slide 29 uses it; its result image is assets/chat-advice.png
    └── tweak.py          # all four injection points in one file
```

## Render

```bash
quarto render mosaic-tutorial.qmd     # build once
quarto preview mosaic-tutorial.qmd    # live-reload while editing
```

Run both from this `presentation/` directory — the deck is not at the repository
root, so `quarto render mosaic-tutorial.qmd` from one level up fails with
`ERROR: mosaic-tutorial.qmd not found`.

Navigate with arrow keys, `f` for fullscreen, `s` for speaker notes.

## Assets

| File | Source |
| --- | --- |
| `gui-screenshot-live.png` | Captured by `tools/capture_interface.py` with the edge vignette frozen mid-flash — the green perimeter glow is the one part of the interface a normal screenshot misses. A sparse room, used on the interface slide |
| `gui-first-frame.png` | Captured by `tools/capture_first_frame.py` — the stock mission's first frame (crowded room, full "Remaining" count, no flash), the "you should see this" image on the run-the-mission slide |
| `gui-screenshot.png`, `game-view.png` | MOSAIC docs; superseded by the live capture, kept for reference |
| `cam-*-live.png` | Captured from the running game by `tools/capture_camera_views.py` — one mission, one frozen frame, re-rendered through each camera with `env.switch_camera()` |
| `cam-*-annot.png` | The live captures with a white ring on the agent and a dashed outline of its room, so the camera difference is readable from the back of the room |
| `cam-follow.png`, `cam-room.png`, `cam-cone.png` | The earlier 512px renders, superseded by the live captures and kept for reference |
| `sprites/*.png` | Single tiles rendered from `minigrid` and MOSAIC's `Victim` / `FakeVictim` classes at 4x supersampling — the world legend on the interface slide, and `health-*.png`, a real victim with its health bar at 100/60/25/0% |
| `victims.png` | Generated from `Victim` / `FakeVictim` render coordinates — top row real, bottom row decoys |
| `gameplay.gif` | Captured by `tools/capture_gameplay.py` — the real GUI compositor driven by a scripted breadth-first walk (a real victim with a green flash, a decoy with a red flash, then another real victim; `SEED=9`, paced slower than live play), built from `configs/experiment.yaml` so it matches what `experiment.main` shows |
| `controls-*.gif`, `chat-advice.png` | Captured by `tools/capture_controls.py` — one clip per control (arrows, Space, Tab, Alt) with a keycap strip that lights on the pressed key; the advice clip and chat still use `ReliableTeammate` from `labs/advisor.py` |
| `results/*.png`, `results/*.txt` | Captured by `tools/capture_config_results.py` — one before/after pair per Part Four setting, each rendered from the same seed with only the edited setting changed. The reward, time, mission-box, and chat crops (`scoring`, `time`, `panel`, `chatpair`) render the GUI at twice its size and crop inside each widget's frame, so they stay sharp at slide size |
| `cam-*-walk.gif` | Captured by `tools/capture_camera_gifs.py` — one walk through a door rendered through all three cameras frame by frame, with the ring and room outline recomputed per frame; equal frame timing so the three play in step |
| `logo.png`, `background.jpg` | iHuman Lab template |
| `team/*.jpg` | iHuman Lab website people page (`ihuman-lab.github.io/lab-website/people/`) |

`cam-full.png` introduces the search-and-rescue testbed in Part One.
`gui-screenshot-live.png` introduces the complete interface in Part Three.
The annotated `cam-*-annot.png` variants compare the three supported camera
choices in Part Three; the plain renders are kept as the unmarked originals.
`victims.png` shows the real and decoy victim shapes.

Regenerate everything with the scripts in `tools/`, in this order:

```bash
python tools/capture_interface.py        # full interface, vignette mid-flash
python tools/capture_first_frame.py      # the stock first frame for the run slide
python tools/capture_camera_views.py     # play the mission, grab the three views
python tools/make_camera_annotations.py  # ring + room outline on those captures
python tools/make_sprites.py             # single tiles for the interface slide
python tools/capture_gameplay.py         # the animated clip on the mission slide
python tools/capture_controls.py         # one clip per control + the chat still
python tools/capture_camera_gifs.py      # the three synced camera walks
python tools/capture_config_results.py   # before/after pairs for the customize series
```

The capture scripts share `tools/_capture_common.py` (MOSAIC path, grid codes,
breadth-first routing, the study env builder, GIF writing). `gif-restart.html`
is included after the deck body and restarts a slide's clips when it opens.

All three need `minigrid` and a checkout of the MOSAIC repository; the capture
script additionally needs MOSAIC's runtime deps (`pygame-ce`, `pygame_gui`,
`gymnasium`) and runs headless via SDL's dummy driver. Each script takes the
MOSAIC path from a constant at the top of the file, or from the `MOSAIC_SRC`
environment variable when it is set (e.g. on Windows). With both `pygame` and
`pygame-ce` installed, `pygame_gui` fails to import; force-reinstall
`pygame-ce` as in `SETUP.md`.

Two things to know before regenerating:

- Do not rebuild the three camera views by constructing three environments. Level
  generation retries internally, each retry consumes RNG, and three separately
  seeded builds drift into three different buildings. Build one and switch the
  camera, which is what `capture_camera_views.py` does.
- For the same reason the captures are not bit-reproducible across runs: the same
  seed can lay out a different building. If the interface capture changes, re-check
  the `.anno` percentages on the interface slide against the new panel positions.

## Before presenting

1. Send `SETUP.md` to registrants at least a week out.
2. Re-verify every command in Part 2 against the current `main`. Part 2 now
   assumes MOSAIC depends on `pygame-ce` (issue 1 below) and that `Esc` exits
   cleanly (issue 13) — **both fixes must be merged before the tutorial**, or
   attendees hit `DIRECTION_LTR` on first run and a traceback on every `Esc`.
3. Merge this branch so `mosaic-tutorial/labs/` on `main` has `panel.py` and
   `advisor.py`; slides 29 and 38 send people to the repo for them.
4. Read `RUNSHEET.md`.

## Repo issues this tutorial exposed

Verified against a clean clone of `iHuman-Lab/mosaic` (`c571f94`) on Python
3.10.20. The deck currently teaches around all of these.

1. **`pygame` vs `pygame-ce`.** `pyproject.toml` declares `pygame`; `pygame_gui`
   requires `pygame-ce`. `pip install -e .` installs **both**, and `pygame` lands
   last, so the GUI dies with
   `ImportError: cannot import name 'DIRECTION_LTR' from 'pygame'`.
   Fix: depend on `pygame-ce>=2.5.2` (done in the local checkout, not yet
   upstream). **Required before the tutorial:** the deck no longer teaches a
   workaround.
2. **The obvious workaround for issue 1 does not work.**
   `pip uninstall -y pygame && pip install "pygame-ce>=2.5.2"` leaves pygame-ce
   *broken* — uninstalling `pygame` removes shared files from the namespace, and
   pip then reports "Requirement already satisfied" and repairs nothing. The
   symptom is `AttributeError: module 'pygame' has no attribute 'surface'`.
   `--force-reinstall` is required. Worth putting in the README until it is fixed.
3. **`env.reset(seed=N)` does not reproduce a world.** The placers use the global
   `random` module (`src/mosaic/sar/placers.py:1,42,102,103,130,131,153`) rather
   than the environment's seeded `np_random`. Only the room-and-door skeleton is
   seeded; victims, lava and keys are not. Calling `random.seed(N)` before
   `env.reset(seed=N)` is a working workaround, but reproducibility is a headline
   claim and should not need one. Fix: thread `self.np_random` through `Placer`.
4. **`FullviewCamera` and `AgentCenteredCamera` have no `reset()`.**
   `PickupVictimEnv.reset()` calls `self.camera.reset()` unconditionally, so
   passing either as `camera_strategy` raises `AttributeError`. Fix: add a no-op
   `reset()` to `CameraStrategy`.
5. **`locked_room_prob=1.0` hangs forever.** `LockedRoomPlacer` computes
   `n_locked = max(1, int(num_cols * num_rows * prob))`, so at `1.0` every room is
   locked, no solvable layout exists, and the level generator retries without a
   cap — the process never returns and no window opens. Reproduced on 2×2 at
   seeds 1, 2 and 3; `0.9` is fine. Fix: cap `n_locked` below the room count, or
   bound the retry loop and raise.
6. ~~**`tabulate` is required but undeclared.**~~ **Fixed upstream.**
   `build_prompt()` → `_build_table()` calls `DataFrame.to_markdown()`, which
   needs `tabulate`; it is now declared in `pyproject.toml`, so the deck does
   not install it separately.
7. **`experiment_main.py` does not exist.** `README.md`, `REFERENCE.md`,
   `docs/getting-started.md`, `docs/architecture.md` and `docs/experiment.md` all
   point at `python -m experiment.experiment_main`; the file is
   `src/experiment/experiment.py`.
8. **README quick-start does not run.** It calls
   `SAREnvGUI(env, fullscreen=False)`, but the constructor takes
   `config: dict` — the working form is `SAREnvGUI(env, config={"fullscreen": False})`.
   The clone URL is also still `github.com/yourusername/mosaic.git`.
9. **`docs/game-concept.md` documents keys that are not mapped.** It lists `W` for
   forward; `key_to_action` in `src/mosaic/gui/user.py` has no `W`. It also lists
   the decoy penalty as `-0.5`; `RescueRewards.fake_victim` defaults to `-1.0`.
10. **`requires-python = ">=3.8"`** is optimistic given the current dependency set;
   the docs say 3.9+ and we only test 3.10.
12. ~~**`python -m experiment.main` does not run at all.**~~ **Fixed locally, not
   yet upstream** (upstream `main` 1ba2268 still has the imports commented out).
   `src/experiment/main.py` had `from .llm import build_llm_client` and
   `from .placers import LavaRiskVictimPlacer, SectorSpreadLavaPlacer` commented
   out at lines 15–16 while still using all three names, so the script exited
   with `NameError: name 'LavaRiskVictimPlacer' is not defined` before building
   anything. The imports are restored, and `build_llm_client` now defaults to
   the keyless `dummy` provider instead of `openai`, so the runner needs no API
   key.
11. **The `cam_*` observation fields are camera-dependent.** `cam_top_x`,
   `cam_top_y`, `cam_view_w` and `cam_view_h` are only written when the camera has
   `_update_position` (i.e. `EdgeFollowCamera`). Analyses written against the
   default camera break silently under `AgentConeCamera`.
13. **`Esc` ends `experiment.main` in a traceback.** After the first mission
   closes, `main.py` runs a second block, `skip_run("run", "tutorial")`, which
   calls `pygame.display.Info()` after the GUI has called `pygame.quit()`:
   `pygame.error: video system not initialized`. Fix: set that block to
   `skip_run("skip", "tutorial")`. Done in the local checkout, not yet upstream.
