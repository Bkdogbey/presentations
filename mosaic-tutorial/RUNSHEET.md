# Facilitator Run Sheet — MOSAIC Tutorial (two hours, plus a 15-minute break)

The rendered deck has 44 slides: 39 in the main tutorial (one of them the break
slide after Part Three), a closing slide, and 4 appendix slides (the divider and
three more).

The tutorial is **Closing the Human–AI Loop: Modular Architectures for Autonomous
Teaming and Physiological Sensing**, a joint session by Oklahoma State University and
the University at Buffalo, in two sessions in Evergreen C. This deck is Session 1
(MOSAIC, 8:30–10:30 AM). Session 2 (SHaSTA, 11:00 AM–1:00 PM) has its own deck in
`shasta-tutorial/`.

Everything runs in the browser, on the tutorial's Jupyter server. Attendees open
one notebook, `notebooks/02_mosaic_human_ai.ipynb`, and play and change the mission
in it. Nobody installs anything; the laptop install is one appendix slide.

The main sequence runs in four parts: why MOSAIC exists, open the notebook,
experience one mission, then configure it in four parts: **SAR**, **GUI**, **LLM**,
and **Sensing**. Part Four follows the notebook's cells (its Steps 1 to 8).

## Before the room opens

- [ ] Render `mosaic-tutorial.qmd` and open the HTML in a browser (`quarto render
      mosaic-tutorial.qmd` from this folder).
- [ ] Test the deck at the projector's 16:9 resolution (authored at 1280×720).
- [ ] **The server (the tutorial depends on it).** Sign in as an attendee would and
      run the notebook top to bottom with the **Python (smc)** kernel. In the folder
      next to the notebook: `config.yaml`, `live_play.py`, `lsl_tools.py`. In the
      server's base Jupyter environment: `ipywidgets` and `ipyevents` (the picture and
      the key capture need their front-end extensions; reload the page after installing).
- [ ] **Load test.** Every player renders their own game in their own kernel and the
      picture travels through the tunnel to the browser (about 15 frames a second).
      Have several people play at once, for several minutes, and watch the server's CPU.
      If it struggles, lower `fps=` or `width=` in `play_mosaic(...)`, or `quality=`.
- [ ] **Keys.** In a real browser, check that arrows, `Space`, `Tab`/`E` and `Alt`/`Q`
      all reach the game. Some browsers keep `Tab` or `Alt` for themselves, which is why
      `E` and `Q` do the same jobs. Click the picture first.
- [ ] Hub address `https://jupyter.ihuman-lab.work`: every registrant has an account and
      knows their password. Test the QR codes (`tools/make_qr.py` to redraw them).
- [ ] **No API keys in this session.** Nothing connects to a hosted model. The teammate
      everyone hears from is the stand-in in Step 6, which answers in the style of its
      prompt.
- [ ] Keep one laptop with the install of `SETUP.md` as a fallback for anyone who
      cannot reach the server.
- [ ] Eye-tracker demo (slide 36), presenter laptop only: follow
      [EYETRACKER_SETUP.md](EYETRACKER_SETUP.md). It runs the notebook on that laptop
      with `eye_tracker: source: live` and `tobii_to_lsl.py`. **This route has not been
      rehearsed end to end:** do it once at the venue, with the projector attached.
      Run `python tools/check_eyetracker.py` first (both eyes seen, 90% valid gaze).
- [ ] Keep one rehearsal recording (an `.xdf`) on the laptop. Slide 37 (*The
      Synchronized Record*) shows a figure drawn from one, and Step 8 of the notebook
      reads the same kind of file. After the venue rehearsal, redraw the figure from
      that recording and render again: `python tools/make_gaze_figure.py <recording.xdf>`.
- [ ] **What goes on the server.** The notebook and its three helper files must be the
      current versions, together: `02_mosaic_human_ai.ipynb`, `config.yaml`,
      `live_play.py`, `lsl_tools.py`. Step 7 needs `lsl_tools.py` with the
      `MarkerOutlet.source_id` attribute; an older copy stops Step 7 with
      `'MarkerOutlet' object has no attribute 'source_id'`. After replacing files, restart
      each kernel. `tobii_to_lsl.py` is for the presenter laptop only.
- [ ] Shared server: Step 7 records only its own two LSL streams and closes them
      afterwards, so attendees on one server do not record each other.

## Timing

A proposal: the session runs 2:15 on the clock, two hours of content plus the break.
Part Two is short now (nothing to install), so the time goes to playing in Part Three
and to running the "Try it" cells in Part Four.

| Time | Slides | Block | Facilitator focus |
| --- | --- | --- | --- |
| 0:00–0:14 | 1–10 | Welcome, Part One: why MOSAIC | Title, sessions and Wi-Fi, the Session 1 title; then the field's questions, why they need a configurable testbed, what MOSAIC is, how it works, the task, the teaming loop. |
| 0:14–0:22 | 11–14 | Part Two: open the notebook | Scan, sign in, pick the kernel, run Step 1, checkpoint. |
| 0:22–0:47 | 15–21 | Part Three: experience | The mission, the interface and tiles, victims and decoys, the controls, then everyone plays Step 2, then the same game with no human. |
| 0:47–1:02 | 22 | Break | Fifteen minutes, slide 22 left up. Helpers fix anyone's sign-in or kernel. |
| 1:02–1:07 | 23–25 | Part Four: the map | The runtime, then the whole task as a few lines. |
| 1:07–1:19 | 26–28 | 4.1 SAR (building) | Build calls; what a level can contain; everyone writes a decoy placer's worth of settings and plays their own level. |
| 1:19–1:29 | 29–30 | 4.1 SAR (camera, rewards) | The three cameras; everyone changes a reward. |
| 1:29–1:33 | 31 | 4.2 GUI | The window and how it reaches the browser. |
| 1:33–1:51 | 32–34 | 4.3 LLM | The contract; everyone swaps in the stand-in teammate; the two prompt styles. |
| 1:51–2:09 | 35–37 | 4.4 Sensing | The observation; recording while you play; the live eye tracker; the recording it leaves. |
| 2:09–2:15 | 38–40 | Wrap-up | Where to go next, the invitation to the lab's paper, then questions; appendix as needed. |

The 2:09–2:15 wrap-up is the only slack. If a part runs long, use the cut list below.

## Opening notes (slides 1–3)

- Slide 1 is the title of the whole tutorial, with the organizers (Hemanth
  Manjunatha, Ehsan Esfahani, Elahe Oveisi, Kristian Dalland, Bennett Kwaku Dogbey)
  and both universities with their labs: the iHuman Lab (Oklahoma State University) and
  the Human in the Loop Systems Lab, HILS Lab (University at Buffalo).
- Slide 2 (*Today's Sessions*) shows the two sessions, the room and the Wi-Fi: network
  `@Hyatt_Meeting`, password `SMC26`. Leave it up while people settle and connect.
- Slide 3 is the Session 1 title: MOSAIC, with its full name.

## Part One notes (slides 4–10)

- There is no Part One divider — after the Session 1 title the deck goes straight into the
  lab and the motivation. The first part divider is slide 11.
- Part One runs why → what → how: the field's questions (3), why they need a
  configurable testbed (4), what MOSAIC is (5), how it works (6), then the task (7) and the
  teaming loop (8).
- Slide 5 names six questions human–AI teaming research asks, one theme per
  row: reliance (trust and reliance, decisions under pressure), what the person
  knows and can handle (situation awareness, cognitive state), and the AI side
  (AI teammate design — the lab's own none / GPT / Gemini comparison — and
  adaptive assistance). Its last line is the bridge: answering them means
  observing the interaction as it unfolds.
- Slide 6 argues for a configurable testbed without naming MOSAIC yet: four
  capabilities, 01–04, that one experiment needs and existing tools rarely
  combine. The slide leaves out what studies often do instead — say it: a single
  accept-or-reject judgment, an AI that stays fixed or shifts unpredictably, a
  new testbed for every question, separate systems on separate clocks.
- Slide 7 defines MOSAIC (Modular System for Adaptive Human–AI Collaboration)
  and answers slide 6 box for box, in the same positions: the task, a
  customizable teammate, conditions set per study, and one synchronized record.
- Slide 8 is the system overview: human, MOSAIC task, and AI teammate on top;
  study sensors, LSL, and session data underneath. Do not add the
  Gymnasium/MiniGrid detail here; it appears on Runtime Architecture (slide 24).
- Slide 9 introduces the task participants perform: search and rescue. The
  hook is that real victims and decoys look alike, so advice can help or mislead.
  Part Three teaches the rules.
- Slide 10 is the core claim of the tutorial. The teammate advises; the
  participant retains final action authority. Say it out loud.
- Keep Part One to fourteen minutes. Its purpose is to make the hands-on work
  meaningful, not to be complete.

## Part Two notes (slides 11–14): open the notebook

- Slide 11 (the divider) carries a QR code to the tutorial's Jupyter server, and
  slide 12 lists the four steps: go to the server, sign in, open
  `02_mosaic_human_ai.ipynb`, pick the kernel **Python (smc)**. Leave the divider up
  while people scan and sign in. The same code is on the Part Four divider (slide 23). To
  point the codes elsewhere, edit `tools/make_qr.py` and rerun.
- Slide 12 also names the four files in the folder (the notebook, `live_play.py`,
  `config.yaml`, `lsl_tools.py`). Its footnote points to the appendix for the laptop
  install: say that nobody needs it today.
- The first code cell of the notebook must run first: it silences warnings and
  sets pygame up to draw off-screen. After that, run cells in order with
  `Shift+Enter`.
- Slide 13 is the first cell group: `config.yaml` on the left, `build_sar_env` on the
  right. Say the sentence on the slide: the task is a text file. Counts are per room.
- Slide 14 is the only checkpoint before the break. Step 1 should print
  `game config: {...}` and `mission: pick up all 8 victims`. The recovery table covers
  the usual problems, in order of how often they happen: the kernel, a missing helper
  file, the picture not receiving keys, a blank picture, a signed-out page.
- Hold at slide 14 until most attendees have a level built. Helpers circulate.

## Part Three notes (slides 15–22): experience the mission

Almost no code in this part. Attendees play the baseline mission and learn to read it.

- Slide 16 states the objective: explore, tell real victims from decoys, decide
  who to rescue before time runs out. The clip is the real interface: one real
  victim (green flash, +1), one decoy (red flash, −1), then another real victim.
- Slide 17 reveals one region at a time — press forward five times. The
  screenshot is caught mid-flash, so the green glow around the game view is the
  edge vignette firing after a rescue — point at it. The legend on the right
  names every tile with its rule: lava ends the mission, a door opens with
  `Space`, a locked door needs the key of its color.
- Slide 18 labels the real-victim and decoy rows directly. Both are red T
  shapes; the decoy's stem is off-center. Point at one of each on screen. Real
  victims earn +1 and decoys cost −1 by default; Part Four changes both the number of
  decoys and the cost.
- Slide 19: each clip shows one action. `Tab` does both pickup and rescue on
  purpose; in the browser `E` does the same, and `Q` is `Alt`. The advice clip was
  recorded with a teammate that reads the map; the notebook's Step 2 game has the
  placeholder, which answers "Currently, no commands are available." — say that
  Step 6 changes that.
- Slide 20 sends everyone to the notebook: Step 2, the cell called *Play it
  yourself*. Give them several minutes of free play. They click the picture, move,
  open a door, pick up a key, rescue a victim, and press **Stop** to see the score.
- Slide 21 (*No Human Required*) is the point to land after everyone has played: MOSAIC is built on
  the Gymnasium (OpenAI Gym) API, so `env.reset()` and `env.step(action)` run the same game with
  nobody at the keyboard. Step 2's *No human needed* cell lets a random agent play a whole episode
  headless, in a fraction of a second. A learning agent uses the same loop with its own policy.
  Be clear that the tutorial does not train an agent. The observation is a richer dictionary than
  the declared `observation_space`, so an RL library that validates spaces needs a small wrapper.
- Slide 22 is the break: fifteen minutes. Leave the slide up. Send helpers to anyone
  who could not sign in or whose kernel is wrong. Before moving on, check that every
  game runs; anyone who lost their session reruns the notebook's first cells. Restart on
  time: Part Four has no slack to absorb a long break.

## Part Four notes (slides 23–38): configure MOSAIC

- Part Four follows the notebook in four parts: 4.1 SAR (the building, its contents,
  the camera, rewards), 4.2 GUI (the window), 4.3 LLM (who answers `Q`), 4.4 Sensing
  (what every step records). The strip at the top of each slide shows the part.
- Slide 24 (runtime architecture) maps the window to its four changeable parts plus
  Gymnasium/MiniGrid underneath. Slide 25 steps through the whole task as a few lines
  (press forward to move the highlight): SAR, GUI, LLM, then Sensing. It is
  assembled from the notebook's cells; it is a map, not a cell to copy.
- Each part opens with one slide (26, 31, 32, 35): the notebook code on the left,
  **three things to change** on the right, each as the setting and what it changes for
  the participant. The highlighted cards are the examples that follow. Keep each to about
  two minutes: name the three, then move on.
- Example slides share one layout: the task in one line, the code, Run, a question for
  the room, then on the next click the before/after from real MOSAIC. The pill at the
  start of each example's task line says who does it. **Try it** (25 the placer, 27
  rewards, 30 the stand-in teammate, 31 the prompt styles): everyone, live, in the
  notebook. **Presenter demo** (36 the eye tracker): you, on the projector.
- Slide 27 (*What You Can Customize*) is the gallery from Step 5: five levels, each
  changing one setting. It is drawn by `tools/capture_notebook_figures.py` from the
  notebook's own cells. Counts are per room, so totals grow with the building.
- Slide 28 (*Write Your Own Placer*) shows how little a placer is: one class, one method.
  The slide abridges the notebook's cell. Everyone changes `DECOYS` in Step 5's
  build-your-own cell and plays.
- Slide 29: the three clips are one walk rendered through three cameras. The notebook's
  Step 3 shows all five cameras. Use `FullviewCamera` and `AgentCenteredCamera` only with
  `switch_camera`: as the camera a level is built with, both raise `AttributeError` on env
  reset because they have no `reset()` method.
- Slide 30: `DECOY_COST` in Step 5's build-your-own cell is the knob. The score under the game
  when you press **Stop** includes it.
- Slide 32 and 33 (the teammate): the stand-in does not read the level; it answers in the
  style its prompt asks for with a fixed sentence. Say so: what it shows is the whole path.
  A real model replaces it by implementing the same method, `query`.
- Slide 34 (two prompt styles): both prompts describe the level in the same way and
  differ only in how the teammate should answer, one sentence or a short briefing. Everyone
  switches `PROMPT_TYPE` and presses `Q` again. Ask which style they would rather get under
  time pressure.
- Slide 35 (sensing) connects the observation (Step 3's live readout) to the recording
  (Step 7). In Step 7 the game calls a function after every action; that writes one
  marker per action to an LSL stream, and a second stream carries the gaze (synthetic in
  the notebook), recorded together to one XDF file.
- Slide 36 is the live eye-tracking demo, instructor-only, and the route is **not yet
  rehearsed** (see [EYETRACKER_SETUP.md](EYETRACKER_SETUP.md)). The notebook runs on the
  presenter laptop with the tracker. Seat the volunteer 60 to 65 cm from the screen, start
  `tobii_to_lsl.py`, run Step 7, press Stop. The point is two streams on one clock; do not
  show Step 8's dwell shares for this recording, because live gaze is in whole-screen
  pixels and the notebook's gaze areas are in game-window pixels. If the device fails, go
  straight to slide 37.
- Slide 37 (*The Synchronized Record*) shows the rehearsal recording: the fixations on
  the screen's three areas, and one timeline with the rescues and the area the gaze was in.
  Keep it to a minute. It is drawn by `tools/make_gaze_figure.py` and is also the fallback
  when the tracker fails. Its three rows are questions a researcher asks of such a
  record; the third (gaze after advice) needs a teammate that gives advice during the
  mission, which this recording does not have.
- Slide 38 (where to go next) is the code map. Point at `notebooks/` as the folder to
  copy for your own work.
- Slide 39 (*MOSAIC in a Study*) invites attendees to the lab's paper, MoA10.3:
  Monday October 5, 14:00–14:15, Grand C. It is the application of what they
  just configured. The slide says what the study did, not what it found; leave the
  results for the talk. The QR code opens the talk's slides. Check the time and room
  against the final program on the day.
- Appendix 42–44 hold the laptop install, and two more changes in the same layout: locked
  rooms and the time limit (at 0:00 the timer stops but the mission keeps going, which is
  expected).
- The closing slide (40) carries the two universities and the MOSAIC repository link.

## Expected problems

| Symptom | Response |
| --- | --- |
| The server does not open | Wi-Fi first, then a helper. Pair the attendee with a neighbor. |
| `ModuleNotFoundError: No module named 'mosaic'` | Wrong kernel: pick **Python (smc)**. |
| `No module named 'live_play'` (or `lsl_tools`) | The helper file is not in the notebook's folder. Copy it there. |
| The picture does not move | The picture needs a click first; then press the keys. |
| A key does nothing | `Tab` or `Alt` may be kept by the browser: use `E` or `Q`. |
| A blank picture | Run the cell again and wait a second. A frozen picture: refresh the page and run from the first code cell. |
| A "Failed to load model class" message | `ipywidgets`/`ipyevents` are missing from the base Jupyter environment; install them there and reload the page. |
| The game looks sluggish for everyone | The server or the tunnel is overloaded: lower `fps=` or `width=` in `play_mosaic(...)`. |
| `AttributeError: 'MarkerOutlet' object has no attribute 'source_id'` (Step 7) | An old `lsl_tools.py` is in the folder. Replace it and restart the kernel. |
| Step 8 stops with "This recording has no game states" | Step 7's game was stopped before any action, or an old recording is being read. Rerun Step 7, take some actions, press Stop. |
| Step 7 finds only one stream | LSL discovery can miss a stream; restart the kernel and run Step 7's two cells again. |
| Generation appears to hang after customization | `locked_room_prob` is at `1.0`. Use `0.9` or less. |
| More victims than expected | `num_real_victims` is per room; 2 per room across a 2×2 building is 8. |
| `AttributeError: 'FullviewCamera' object has no attribute 'reset'` | Known bug, same for `AgentCenteredCamera`. Use `AgentFOVCamera`, `AgentConeCamera`, or the default for a level; the other two only with `switch_camera`. |
| Warnings or `Sampling rejected` lines in the output | The first code cell silences them; run it first. They are harmless. |

## Cut list

If the session runs long:

1. In Part Three, explain slides 17–18 in one minute each.
2. Keep the part slides (26, 31, 32, 35) to a minute each.
3. Make the placer slide (28) a presenter walk-through instead of a live try.
4. Make the prompt-style switch (34) a presenter demo instead of a live try.
5. Drop the eye-tracker demo (36) if the device is not ready; show slide 37 instead.

Do not cut the checkpoint (14), the play slide (20), the three-cameras clip (29), or
the stand-in teammate (33): they are the parts every attendee does.

## Closing ask

Ask attendees to keep the notebook and try one change at home, and to open an issue
when something does not work for them. Concrete reports from new users are the most
useful outcome for the project after the tutorial.
