# Run Sheet — SHaSTA Tutorial (Session 2: two hours)

The tutorial is **Closing the Human–AI Loop: Modular Architectures for Autonomous Teaming and Physiological Sensing**, a joint session by Oklahoma State
University and the University at Buffalo, in two sessions in Evergreen C. This deck is Session 2 (SHaSTA, 11:00 AM–1:00 PM). Session 1 (MOSAIC,
8:30–10:30 AM) has its own deck in `mosaic-tutorial/`.

The rendered deck has 33 slides: 29 in the main tutorial (one of them the break; slide 29 is the open discussion), the closing slide, and 3 appendix slides (the divider and two more).
Everything runs in the browser, on the tutorial's Jupyter server: attendees open `notebooks/01_shasta_hsi.ipynb` and command the swarm in it. Nobody
installs anything; the laptop install is one appendix slide. The timings are **estimates**, not yet validated against a live run.

## Before the room opens

- [ ] Render `shasta-tutorial.qmd` and open the HTML in a browser (`quarto render shasta-tutorial.qmd` from this folder).
- [ ] Test the deck at the projector's 16:9 resolution (authored at 1280×720).
- [ ] **The server (the tutorial depends on it).** Sign in as an attendee would and run the notebook top to bottom with the **Python (smc)** kernel. The
      environment needs `ihuman-shasta` (installed from a clone of the SHaSTA repository, with `[gui]`), `pylsl`, `pyxdf`, `pandas`, `matplotlib`. In the folder
      next to the notebook: `config.yaml`, `live_play.py`, `world_view.py`, `lsl_tools.py`. In the server's base Jupyter environment: `ipywidgets` and `ipyevents` (the picture and the
      input capture need their front-end extensions; reload the page after installing).
- [ ] **Test the mouse in a real browser.** The interface is mouse-driven: clicking a marker, clicking a street node, the **Send order** button, the wheel, a
      right-drag, Shift-click. The input was tested with simulated browser events against the real interface, not in a real browser, and it relies on the
      position fields that `ipyevents` reports. Check each of those in the browser you will use, and at the picture's shown size.
- [ ] **Load test.** Every attendee runs their own simulation and interface in their own kernel, and the picture travels through the tunnel at about 15 frames a
      second. Have several people play at once for several minutes and watch the server's CPU. If it struggles, lower `fps=` or `width=` in `play_shasta(...)`.
- [ ] Hub address `https://jupyter.ihuman-lab.work`: every registrant has an account and knows their password. Test the QR code (it is `assets/qr-notebook.png`).
- [ ] **Master copies and user copies.** The server holds one read-only master of each tutorial, in `/home/smc-tutorial/master/` (`mosaic/`, `shasta/`); only an admin changes it. Every user gets their own `~/mosaic` and `~/shasta` automatically when their Jupyter server starts, so nobody's edits reach anyone else. To publish a new version, change the master (`hub-setup/README.md` in the MOSAIC repository has the commands); users who have not edited get new helper `.py` files at their next login, and anyone can start over with `smc-sync --reset mosaic` in a terminal (their old folder is kept as a backup). 
- [ ] **What goes on the server.** The notebook and its helper files must be the current versions, together: `01_shasta_hsi.ipynb`, `config.yaml`, `live_play.py`,
      `world_view.py`, `lsl_tools.py`. An older `lsl_tools.py` stops Step 7 with `'MarkerOutlet' object has no attribute 'source_id'`. After replacing files, restart each kernel.
- [ ] Keep one laptop with the install of `SETUP.md` as a fallback for anyone who cannot reach the server.
- [ ] **No API keys in this session.** Nothing connects to a hosted model.
- [ ] **Building a map (Step 4, slide 20)** needs two things on the server: Java 11 or newer on the server (`sudo apt-get install -y default-jre-headless`; or the cell downloads one into each user's cache the first time), and outbound access to `overpass-api.de` (the roads and buildings) and to GitHub (the OSM2World tool, about 26 MB, downloaded once into `~/.cache/shasta`). The setup is written up in `notebooks/MAPS.md` of the SHaSTA repository. Run the cell once as a test user on the hub before the session. If the network is slow on the day, build `bellevue` once and let people reuse the `assets/bellevue` folder.
- [ ] Keep one rehearsal recording (an `.xdf`) in case the live recording in Step 7 fails.
- [ ] Appendix slide 33 (a real eye tracker on a laptop) uses `tobii_to_lsl.py` and `shasta_gui_lsl.py`, which have not been run against real hardware in
      this repository. Try them before you mention them.

## Timing

| Time | Slides | Block | Facilitator focus |
| --- | --- | --- | --- |
| 0:00–0:05 | 1–5 | Welcome | Title, the two sessions and the Wi-Fi, the Session 2 title, the team, the agenda. |
| 0:05–0:15 | 6–8 | Part One: why human–swarm interaction | Talk-through, no hands-on. "The Question" and its four cards carry the argument; "What Is SHaSTA" says plainly that LSL and physiological recording are in the paper and added as a layer in the notebook. |
| 0:15–0:25 | 9–12 | Part Two: open the notebook | Scan, sign in, pick the kernel, run Step 1 (the map and the config), checkpoint. |
| 0:25–1:05 | 13–20 | Part Three: put a human in the loop | Everyone commands the swarm in Step 3; the controls; `SwarmCommander` as the one seam; the same environment with no human (Gym API); the PyBullet world in 3D; everyone changes the mission in Step 4; then builds a map of anywhere from OpenStreetMap and plays on it. |
| 1:05–1:15 | 21 | Break | Ten minutes, slide 21 left up. Helpers fix anyone's kernel or picture. |
| 1:15–1:50 | 22–28 | Part Four: measure the human, then extend | Why LSL; logging the operator; everyone records a session in Step 7; the analysis in Step 8; the gotchas; building your own experiment (Step 5). |
| 1:50–1:58 | 29 | Open discussion | Three open questions, two minutes in pairs first, then the room. Questions 2 and 3 reach across to MOSAIC. |
| 1:58–2:00 | 30 | Closing | Thanks; slide 30 stays up; appendix as needed. |

## Part notes

- **Slide 2 (*Today's Sessions*)** shows both sessions, the room and the Wi-Fi: network `@Hyatt_Meeting`, password `SMC26`. Leave it up while people settle.
- **Slides 6–8 (Part One)**: the deck never treats the swarm as the point; the person is. Slide 8 is where you say plainly that today's `ihuman-shasta` ships the core and
  the interface, and that the LSL layer is `lsl_tools.py`, next to the notebook.
- **Slide 9 (Part Two divider)** carries a QR code to the tutorial's Jupyter server. **Slide 10** lists the four steps: go to the server, sign in, open
  `01_shasta_hsi.ipynb`, pick the kernel **Python (smc)**. The first code cell of the notebook must run first. **Slide 11** is Step 1: the map as a graph (the numbered
  circles are the nodes every order refers to) and `config.yaml`. **Slide 12** is the checkpoint; the usual problems are the kernel, a missing helper file, and the picture not
  receiving the mouse until it is clicked.
- **Slide 14 (*Play It Yourself*)**: Step 3's first cell. Give everyone several minutes of free play. They click the picture, click a group's marker, click a street node, press
  `Enter`, and press **Stop** to see the score. **Slide 15** is the controls, including shift-select, zoom and pan.
- **Slide 16 (*One Seam: SwarmCommander*)**: the interface is a thin window on `SwarmCommander`, which has no display; anything that can call it can be the human. Step 3's *No human
  needed* cell runs a scripted operator through it.
- **Slide 17 (*No Human Required*)**: SHaSTA is a Gymnasium environment, so `env.reset()` and `env.step({group: node})` run it with nobody at the keyboard, which is how a script or a
  reinforcement-learning agent would command the swarm. Step 2's cell does it. The tutorial does not train an agent.
- **Slide 18 (*The PyBullet World*)**: SHaSTA's physics is PyBullet, which runs in `DIRECT` mode with no window, and a whole trip across the map takes a fraction of a second of computing (Step 2 prints it).
  PyBullet can still render the 3D scene to an image (`getCameraImage`), so Step 3's *Interact with the PyBullet world* cell shows the 3D world in the browser: left-drag orbits, the wheel zooms, and a click on the
  ground becomes an order (the click is a ray, the ray meets the ground, the nearest street node goes to the selected group). The code is `world_view.py`, about a hundred lines. The 3D view runs at roughly
  ten frames a second on a laptop; lower `fps=` or `width=` in `play_world(...)` if it struggles.
- **Slide 19 (*What You Can Customize*)**: Step 4's build-your-own cell: vehicles, speed, targets, radius, time limit, seed. The operator's workload is the research variable.
- **Slide 20 (*Build a Map of Anywhere*)**: Step 4's second half. Two calls turn a bounding box (south, west, north, east) into a map: `fetch_osm` downloads the roads and buildings from OpenStreetMap and `build_map` makes the 3D mesh and the latitude/longitude table. It takes about ten seconds for downtown Bellevue (243 intersections), and then the same interface runs on it. Let people change the box to their own campus or city; right-clicking a point on openstreetmap.org shows its coordinates. Keep the box to a campus or a few blocks, up to about 2 km across. See the checklist for Java and network access.
- **Slide 23 (*Why LSL*)** and **slide 24 (*Log the Operator*)** carry the message of Part Four; the marker lines on slide 24 are real output from a short session in Step 7.
- **Slide 25 (*Record Your Own Session*)**: Step 7 has two cells. Everyone gives a few orders and presses **Stop**; `session.xdf` is saved next to the notebook. The gaze is synthetic: it looks
  at the target you just ordered, then follows the selected group. **Slide 26** is Step 8, drawn from the same kind of file.
- **Slide 27 (*Four Things That Will Trip You Up*)**: all four were hit while testing. Cheaper to show once than to answer one by one.
- **Slide 28 (*Build Your Own Experiment*)**: Step 5's `TargetCollector`; the table on the slide is the notebook's own output.
- **Slide 29 (*Open Discussion*)**: open on purpose, three questions rather than an agenda. Two minutes in pairs, then the room. Write down the *what is missing* answers.
- **Appendix**: slide 32 is the laptop install; slide 33 is a real eye tracker on a laptop, because a USB tracker cannot be plugged into the server and LSL finds streams on the
  local network.

## Expected problems

| Symptom | Response |
| --- | --- |
| The server does not open | Wi-Fi first, then a helper. Pair the attendee with a neighbor. |
| `ModuleNotFoundError: No module named 'shasta'` | Wrong kernel: pick **Python (smc)**. |
| `No module named 'live_play'` (or `lsl_tools`, `world_view`) | The helper file is not in the notebook's folder. Copy it there. |
| The picture does not respond | The picture needs a click first; then use the mouse and keys. |
| A click does nothing, or lands in the wrong place | Check the browser and the picture's shown size; report it, because this is the part that was only tested with simulated events. |
| A blank picture | Run the cell again and wait a second. A frozen picture: refresh the page and run from the first code cell. |
| A "Failed to load model class" message | `ipywidgets`/`ipyevents` are missing from the base Jupyter environment; install them there and reload the page. |
| The interface looks sluggish for everyone | The server or the tunnel is overloaded: lower `fps=` or `width=` in `play_shasta(...)` or `play_world(...)` (the 3D view renders on the CPU and is the slower of the two). |
| `ValueError: Cannot load an actor multiple times` | A `groups` dictionary was reused. Rerun the whole cell, not only its last line. |
| `IndexError` in `GoToNodeExperiment.apply_actions` mid-mission | Known intermittent bug (see `README.md`). Say so and move on. |
| `AttributeError: 'MarkerOutlet' object has no attribute 'source_id'` (Step 7) | An old `lsl_tools.py` is in the folder. Replace it and restart the kernel. |
| Step 7 stops with "No LSL streams found" | Restart the kernel and run Step 7's two cells again. |
| Step 8 stops with "This recording has no orders" | Step 7 was stopped before any order, or an old recording is being read. Rerun Step 7, give a few orders, press Stop. |
| Warnings or stray lines in the output | The first code cell silences them; run it first. They are harmless. |

## Cut list

If the session runs long:

1. Skip slide 19 (*What You Can Customize*) and let people change the numbers in their own time. Make slide 20 (*Build a Map of Anywhere*) a presenter demo: build Bellevue once on the projector, and let people try their own box in their own time.
2. Make the Step 5 experiment (slide 28) a presenter walk-through instead of a live try (the timetable already assumes this: it has 35 minutes, not 40).
3. Keep slides 16 and 17 to a minute each.
4. Shorten the analysis (slide 26) to the timeline figure.

Do **not** cut the LSL slides (23–25): they are the reason this tutorial is about human–swarm *interaction* rather than swarm simulation, or the *Four Things* slide (27).

## After the session

Note anything that did not match this run sheet (a different failure mode, a timing that was way off, a slide nobody needed), and fold it back into `README.md` and this file before the next run.
