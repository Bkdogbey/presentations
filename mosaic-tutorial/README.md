# MOSAIC Tutorial — IEEE SMC 2026

A two-hour hands-on tutorial (plus a 15-minute break) introducing MOSAIC to HCI and human-factors
researchers, built on the iHuman Lab Quarto reveal.js template.

The narrative thread is human–AI teaming: MOSAIC is a configurable research
testbed for studying how humans and AI teammates collaborate during dynamic,
consequential tasks. Everything runs in the browser, on the tutorial's Jupyter
server: attendees open one notebook, `notebooks/02_mosaic_human_ai.ipynb` in the
MOSAIC repository, and play and change the mission in it. Nothing is installed on
their laptops; the install is a single appendix slide. The deck is four parts:

1. **Why MOSAIC** — the questions human–AI teaming research asks, why they need
   a configurable testbed, what MOSAIC is and how it works, search and rescue as
   the first testbed, and the teaming loop
2. **Open the notebook** — scan the QR code, sign in to the tutorial server, pick
   the kernel, run Step 1: the first level, built from `config.yaml`, and a checkpoint
3. **Experience the SAR mission** — the mission objective, the interface and what each
   tile means, victims and decoys, and the controls, then *Play It Yourself*
   (Step 2 of the notebook) and *No Human Required*: the same game, played by a random
   agent through the Gymnasium API, to show that RL agents can run it too. A 15-minute break follows
4. **Configure MOSAIC** — the notebook in four parts: 4.1 SAR (the building, what a
   level can contain, a decoy placer you write yourself, the camera, rewards), 4.2 GUI
   (the window and how it reaches the browser), 4.3 LLM (a stand-in teammate, and the
   two prompt styles), 4.4 Sensing (the observation, and recording game state and gaze;
   a presenter demo with a real eye tracker). The "Try it" slides are cells attendees run.
   No API key is used in the session

The appendix holds the install for a laptop, locked rooms, and the time limit. The
*Synchronized Record* slide after the eye-tracker demo shows a figure drawn from a
rehearsal recording.

## Contents

```
mosaic-tutorial/
├── mosaic-tutorial.qmd   # the deck — edit this (46 slides: 41 main, one of them the break + closing + 4 appendix)
├── theme.scss            # lab theme (template + team, fill-mode cards, horizontal flow,
│                         #   architecture diagram + .detached variant, annotated
│                         #   screenshots, .band notes, layer bands, you-are-here strip,
│                         #   .checkpoint callouts, dark-theme panel-tabset)
├── SETUP.md              # send to attendees before the session: nothing to install, plus the optional laptop install
├── RUNSHEET.md           # facilitator timings, cut list, expected failures
├── EYETRACKER_SETUP.md   # presenter only: machine setup for the slide 37 eye-tracker demo
├── assets/               # figures used in the deck
├── tools/                # scripts that draw the figures (see Assets)
└── labs/                 # side examples from the earlier, laptop-based version of the tutorial;
                          #   the deck no longer uses them (they patch src/experiment/), safe to delete
```

## The notebook

The session runs on `notebooks/02_mosaic_human_ai.ipynb` in the MOSAIC repository, with
four helpers next to it: `config.yaml` (the task as a text file), `leaderboard.py` (the shared leaderboard of Step 9, with `03_leaderboard.ipynb` to show it on the projector), `live_play.py` (shows
the game in the browser and takes the keys) and `lsl_tools.py` (recording and analysis).
Part Four of the deck is that notebook's Steps 1 to 9:

| Deck | Notebook |
| --- | --- |
| Part Two: your first level | Step 1: the config file and the environment |
| Part Three: play it yourself, and with no human | Step 2: actions, *Play it yourself*, and *No human needed* |
| 4.4 Sensing, the observation | Step 3: what the agent observes, and the five cameras |
| 4.2 GUI | Step 4: the human interface |
| 4.1 SAR: customize, placer, rewards | Step 5: what you can customize |
| 4.3 LLM: stand-in teammate, prompt styles | Step 6: the AI teammate |
| 4.4 Sensing: recording, live demo | Steps 7 and 8: record game state and gaze, then analyse it |
| The challenge (after 4.1) | Step 9: the same level for everyone, a prediction first, a random agent for comparison, and the leaderboard |

Change the notebook and the slides it feeds (the gallery and the chat screenshots)
together: `tools/capture_notebook_figures.py` runs the notebook's own cells.

## Render

```bash
quarto render mosaic-tutorial.qmd     # build once
quarto preview mosaic-tutorial.qmd    # live-reload while editing
```

Run both from this `mosaic-tutorial/` directory — the deck is not at the repository
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
| `gameplay.gif` | Captured by `tools/capture_gameplay.py` — the real GUI compositor driven by a scripted breadth-first walk (a real victim with a green flash, a decoy with a red flash, then another real victim; `SEED=9`, paced slower than live play) |
| `controls-*.gif`, `chat-advice.png` (no longer used by the deck) | Captured by `tools/capture_controls.py` — one clip per control (arrows, Space, Tab, Alt) with a keycap strip that lights on the pressed key; the advice clip and chat still use `ReliableTeammate` from `labs/advisor.py`; the deck shows them only as an illustration of the controls |
| `results/*.png`, `results/*.txt` | Captured by `tools/capture_config_results.py` — one before/after pair per Part Four setting, each rendered from the same seed with only the edited setting changed. The reward, time, mission-box, and chat crops (`scoring`, `time`, `panel`, `chatpair`) render the GUI at twice its size and crop inside each widget's frame, so they stay sharp at slide size |
| `results/customize-gallery.png`, `results/teammate-placeholder.png`, `results/teammate-sparse.png`, `results/teammate-detailed.png` | Drawn by `tools/capture_notebook_figures.py` by running the notebook's own cells (Step 5's five levels; Step 6's chat panel after one `Q`, for the placeholder and for the stand-in teammate under each prompt type). They need a MOSAIC checkout (`MOSAIC_REPO`) and only the public `mosaic` API |
| `results/gaze-record.png` | Drawn by `tools/make_gaze_figure.py` from the rehearsal recording of the slide 37 eye-tracker demo (LabRecorder `.xdf`): fixations on the screen's three areas, and one timeline of rescues and gaze area. Redraw it from the venue recording |
| `cam-*-walk.gif` | Captured by `tools/capture_camera_gifs.py` — one walk through a door rendered through all three cameras frame by frame, with the ring and room outline recomputed per frame; equal frame timing so the three play in step |
| `qr-notebook.png`, `qr-paper.png` | Drawn by `tools/make_qr.py` (needs `segno`): the tutorial's Jupyter server, where the companion notebook runs, on the Part Two and Part Four dividers, and the slides of the lab's SMC 2026 paper, on the *MOSAIC in a Study* slide. The addresses are at the top of the script |
| `logo.png`, `background.jpg` | iHuman Lab template |
| `team/*.jpg` | iHuman Lab website people page (`ihuman-lab.github.io/lab-website/people/`) |

`cam-full.png` introduces the search-and-rescue testbed in Part One.
`gui-screenshot-live.png` introduces the complete interface in Part Three.
The annotated `cam-*-annot.png` variants compare the three supported camera
choices in Part Three; the plain renders are kept as the unmarked originals.
`victims.png` shows the real and decoy victim shapes.


**About the older capture scripts.** `capture_interface.py`, `capture_first_frame.py`,
`capture_camera_views.py`, `capture_camera_gifs.py`, `capture_gameplay.py`,
`capture_controls.py` and `capture_config_results.py` build the lab's study mission from
`src/experiment/` in a MOSAIC checkout. They are only needed to redraw the images they
made; the slides themselves no longer run anything from `experiment/`. Redraw the two
new figures with:

```bash
MOSAIC_REPO=<checkout of iHuman-Lab/mosaic> python tools/capture_notebook_figures.py
```

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
python tools/capture_notebook_figures.py # Step 5's gallery and Step 6's chat screenshots (MOSAIC_REPO=...)
```

The capture scripts share `tools/_capture_common.py` (MOSAIC path, grid codes,
breadth-first routing, the study env builder, GIF writing). `gif-restart.html`
is included after the deck body and restarts a slide's clips when it opens.
`tools/check_eyetracker.py` is not a capture script: it checks the Tobii tracker
before the slide 37 demo (see `EYETRACKER_SETUP.md`).
`tools/make_gaze_figure.py <recording.xdf>` draws `results/gaze-record.png` for
slide 38 from the demo's LabRecorder file, with the notebook's own helpers
(`notebooks/lsl_tools.py` in the MOSAIC checkout). It is not in the list above
because it needs a recording; rerun it after the venue rehearsal.

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

1. Send `SETUP.md` to registrants at least a week out: it asks them to sign in to the
   tutorial server and run Step 1 once, which is the whole preparation.
2. Put the current notebook and its helpers on the server (see `RUNSHEET.md`) and run it
   top to bottom as an attendee. Load-test it with several simultaneous players.
3. Rehearse the eye-tracker demo end to end on the presenter laptop (`EYETRACKER_SETUP.md`):
   the route that uses the notebook has not been rehearsed yet.
4. Read `RUNSHEET.md`.

## Repo issues this tutorial exposed

Verified against a clean clone of `iHuman-Lab/mosaic` (`c571f94`) on Python
3.10.20; issues 1, 6 and 12 re-checked against `1018587` on Python 3.11.15.
The notebook works around the ones that affect it.

1. **`pygame` vs `pygame-ce`.** `pyproject.toml` declares `pygame`; `pygame_gui`
   requires `pygame-ce`. `pip install -e .` installs **both**, and `pygame` lands
   last, so the GUI dies with
   `ImportError: cannot import name 'DIRECTION_LTR' from 'pygame'`.
   Fix: depend on `pygame-ce>=2.5.2`. Not upstream as of `1018587`, so the
   laptop install (appendix slide) teaches the workaround from issue 2. Remove those
   two lines from the slide once the fix is merged.
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
6. **`tabulate` is required but undeclared.**
   `build_prompt()` → `_build_table()` calls `DataFrame.to_markdown()`, which
   needs `tabulate`. It is declared only in the fork `Bkdogbey/mosaic`, not in
   upstream `pyproject.toml` (`1018587`), so a real-LLM setup has to add it.
   Without it `Alt` replies "`Import tabulate` failed" for any non-dummy
   provider.
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
