# Eye-Tracker Demo: Machine Setup

A checklist for getting the presenter laptop ready for the live eye-tracking demo
(slide 37). Do the steps in order; each ends with a check. Allow 30 minutes on a
new machine. **Presenter only:** attendees do not need any of this.

The demo shows a Tobii eye tracker streaming gaze into the same recording as the
game, with the tutorial notebook (Step 7) running on **this laptop**, not on the
tutorial server: LSL streams are found on the local network, so the tracker and the
notebook have to be on one machine.

## What the machine needs

- **Python 3.10 exactly.** The Tobii SDK (`tobii-research` 2.1.0) is built only
  for Python 3.10, on Windows, macOS 14+, and Linux.
- The Tobii tracker on USB, mounted under the screen the game will run on.
- Internet for the installs. No API key.

## 1 · Tobii software (admin rights)

The tracker is a **Tobii Pro Spark**.

1. **Tobii Pro Spark runtime** (the driver), from
   <https://connect.tobii.com/s/spark-downloads>. Required: without it the
   tracker shows on USB but no software can find it.
2. **Tobii Pro Eye Tracker Manager.** Recommended: it tells the tracker where
   the screen is, and shows the volunteer's eyes in the tracking box.

On Ubuntu 22.04, with the runtime `.deb` downloaded:

```bash
sudo apt install ./TobiiProSpark_2.2.3.0_x64.deb
wget https://s3-eu-west-1.amazonaws.com/tobiipro.eyetracker.manager/linux/TobiiProEyeTrackerManager-2.7.2.deb
sudo apt install ./TobiiProEyeTrackerManager-2.7.2.deb
```

Unplug and replug the tracker, then open Eye Tracker Manager and set the
screen.

Without that, the tracker assumes a default screen position. If your mount is
different, gaze lands too high or too low: in rehearsal the default was in use
and gaze sat low on the screen.

✓ **Check:** the tracker appears in Eye Tracker Manager with its serial number.

## 2 · Code and environment

```bash
git clone https://github.com/iHuman-Lab/mosaic.git
conda create --name mosaic_tobii python=3.10 -y
conda activate mosaic_tobii
cd mosaic
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install tobii-research pylsl pyxdf matplotlib scipy pandas
python -m pip install ipywidgets ipyevents notebook
python -m pip uninstall -y pygame
python -m pip install --force-reinstall "pygame-ce>=2.5.2"
```

The last two lines must come last. Run them again if any later install puts
`pygame` back.

✓ **Check:**

```bash
python -c "import mosaic.gui.main, tobii_research, pylsl, ipyevents; print('demo ready')"
```

## 3 · Can the tracker see you?

From this `presentation/` folder, with the volunteer seated:

```bash
python tools/check_eyetracker.py
```

It prints the tracker and the screen position it assumes, then a line every
half second: both eyes, head position in the tracking box, distance, gaze on
screen.

✓ **Check:** both eyes show `yes` almost every line and valid gaze is 90% or
more. Sit **60 to 65 cm** from the screen; in rehearsal tracking was unbroken
there and patchy at 80 cm. Tilt the tracker until `x`, `y`, `z` are near 0.50.

## 4 · Calibrate

`notebooks/tobii_to_lsl.py` does **not** calibrate: the tracker uses whatever
calibration it already holds. Calibrate it in Tobii Eye Tracker Manager with the
volunteer seated, before you start. Without that, gaze can sit well off the screen.

## 5 · Run it

From the `mosaic` folder, with `mosaic_tobii` active. You need two terminals.

1. **Terminal 1, the gaze stream.** Give it the size of the screen the tracker
   sits under, in pixels, and leave it running:

   ```bash
   cd notebooks
   python tobii_to_lsl.py --width 1920 --height 1080
   ```

2. **Check the stream** (a third terminal, same environment):

   ```bash
   python -c "import pylsl; [print(s.name(), '|', s.type(), '|', s.nominal_srate(), 'Hz') for s in pylsl.resolve_streams(2)]"
   ```

   ✓ **Check:** `TobiiEyeTracker | Gaze | 60.0 Hz`.

3. **Terminal 2, the notebook.** In `notebooks/config.yaml` change the gaze source:

   ```yaml
   eye_tracker:
     source: live
   ```

   then start Jupyter from the `notebooks` folder and open the notebook:

   ```bash
   cd notebooks
   python -m jupyter notebook 02_mosaic_human_ai.ipynb
   ```

   Pick the **Python 3 (ipykernel)** kernel. Run the first code cell, the cells
   of Step 1, and Step 7's two cells.
4. **Play.** The volunteer clicks the game picture and plays; press **Stop** when
   the mission ends. Step 7 saves `mosaic_session.xdf`.
5. **Show both streams.** The notebook's Step 7 recorded exactly two: `TobiiEyeTracker`
   (gaze, 60 Hz) and `MOSAIC-State` (one marker per action). Run Step 8 to read the
   file back: it lists each stream with its sample count and time span, on one clock.
6. **Refresh slide 38:** from this folder, `python tools/make_gaze_figure.py <recording.xdf>`,
   then render the deck.

**Know this before you show the analysis.** Live gaze arrives in pixels of the whole
screen, but Step 7's gaze areas (game view, information panel, chat) are in pixels of
the game window, and in the browser the game is a small picture somewhere on the page.
So the dwell shares and heatmaps of Step 8 will not line up with the live gaze. Use
the demo to show two streams on one clock, and slide 38 (drawn from the rehearsal
recording) for what an analysis looks like.

## If something fails

| Symptom | Fix |
| --- | --- |
| `check_eyetracker.py` says no tracker found | Step 1: the runtime is missing, or replug the USB cable. |
| `tobii_to_lsl.py` finds no tracker | Same as above. |
| Both eyes rarely `yes`, or valid gaze well under 90% | Move to 60 to 65 cm and tilt the tracker towards the face (step 3). |
| Gaze is steady but always too low or too high | The tracker has the wrong screen position, or is not calibrated. Set the screen and calibrate in Eye Tracker Manager (steps 1 and 4). |
| The check in step 5 prints no `TobiiEyeTracker` | `tobii_to_lsl.py` is not running, or it is on another machine: LSL needs the same machine or network. |
| Step 7 stops with "No LSL streams found" | The stream was not running when you ran the setup cell. Start `tobii_to_lsl.py` first, then rerun it. |
| `cannot import name 'DIRECTION_LTR'` | Rerun the last two install lines of step 2. |
| `No module named 'ipyevents'` | `python -m pip install ipywidgets ipyevents`, then restart Jupyter. |
| The tracker fails on the day | Go to slide 38, which shows the rehearsal recording. |

## What was tested

The tracker side: Tobii Pro Spark on Ubuntu 22.04 (2 October 2026), steps 1 and 3,
and gaze streaming at 60 Hz.

**Not rehearsed in this form:** the notebook route above (steps 2, 4 and 5 with
`tobii_to_lsl.py` and Step 7 on the presenter laptop), so run it once end to end at the
venue before the session. Also untested: Eye Tracker Manager calibration, a second
screen or projector, and Windows or macOS. Seating and the tracker's screen position
decide the accuracy, so settle them there, not before.
