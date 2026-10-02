# Eye-Tracker Demo: Machine Setup

A checklist for getting any machine ready for the live eye-tracking demo
(slide 33). Do the steps in order; each ends with a check. Allow 30 minutes on
a new machine.

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

Without that, MOSAIC's calibration gives the tracker a default: a screen whose
bottom edge is 95 mm above the tracker. If your mount is different, gaze lands
too high or too low. In rehearsal the default was in use and gaze sat low on
the screen.

✓ **Check:** the tracker appears in Eye Tracker Manager with its serial number.

## 2 · Code and environment

MOSAIC and the lab's `ixp` package go side by side in one folder.

```bash
git clone https://github.com/iHuman-Lab/mosaic.git
git clone https://github.com/iHuman-Lab/ixp.git
conda create --name mosaic_tobii python=3.10 -y
conda activate mosaic_tobii
cd mosaic
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install tobii-research pylsl
# Ubuntu 22.04 only: a ready-built wxPython, so PsychoPy does not compile it
python -m pip install https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-22.04/wxPython-4.2.1-cp310-cp310-linux_x86_64.whl
python -m pip install psychopy ray ujson "beartype>=0.18.5,<0.19" icontract "pydantic>=2.9,<3"
python -m pip install --no-deps --ignore-requires-python -e ../ixp
python -m pip install matplotlib scipy pyxdf notebook
python -m pip uninstall -y pygame
python -m pip install --force-reinstall --no-deps "pygame-ce>=2.5.2"
```

Three lines are deliberate:

- `--no-deps --ignore-requires-python` for `ixp`: it asks for Python 3.11, which
  the Tobii SDK cannot use, and it lists plain `pygame`, which breaks MOSAIC's
  window.
- `matplotlib scipy pyxdf notebook` are for reading the recording afterwards
  (step 5). The demo itself does not need them.
- The last two lines must come last. Run them again if any later install puts
  `pygame` back.

✓ **Check:**

```bash
ls src/experiment/eye_demo.py
python -c "import mosaic.gui.main, ixp.experiment, psychopy.visual, tobii_research, pylsl; print('demo ready')"
```

If `eye_demo.py` is missing, the checkout predates the demo runner.

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

## 4 · The demo runner

No edits. `src/experiment/eye_demo.py` registers the tracker, calibrates it,
and runs **one** two-minute mission with the keyless teammate (`SARGameDemo` in
`game.py`). The lab's study in `experiment.py` and `configs/experiment.yaml`
is left as it is.

One setting can matter: `display:` on the top line of
`configs/experiment.yaml` is the screen the calibration and the game open on
(`0` is the first). With a projector attached, set it to the screen the
tracker sits under.

## 5 · Run it

Start from the `mosaic` folder with `mosaic_tobii` active.

```bash
PYTHONPATH=src python -m experiment.eye_demo
```

Windows PowerShell: `$env:PYTHONPATH = "src"`, then `python -m experiment.eye_demo`.

1. **Calibration:** five dots. Keep the head still and look at the black
   centre of each dot until it disappears. `Space` accepts, `R` redoes. The
   terminal then prints a table: on each row `Avg pos` should be close to
   `Point`. If several rows are far off, run it again.
2. **Play:** one mission, at most two minutes. `Esc` ends it. `Alt` gets the
   keyless placeholder reply; no API key is used.
3. **Show both streams:** open LabRecorder and press *Update*. Or, in a second
   terminal (same environment) while the mission runs:

   ```bash
   python -c "import pylsl; [print(s.name(), '|', s.type(), '|', s.nominal_srate(), 'Hz') for s in pylsl.resolve_streams(2)]"
   ```

   ✓ **Check:** `TobiiEyeTracker | Gaze | 60.0 Hz` and `SARGame | GameState | 0.0 Hz`
   (0 means irregular: one sample per frame, about 30 a second).
4. **Record (optional):** in LabRecorder tick both streams, press *Start*, and
   *Stop* when the mission ends. It saves one `.xdf` file.
5. **Read the recording:** open `notebooks/02_mosaic_human_ai.ipynb`, go to
   Step 9, set `XDF_PATH` to the file and `SCREEN` to that screen's size in
   pixels, and run Step 9. It shows where the volunteer looked and what they
   looked at after each rescue.
6. **Refresh slide 34:** from this `presentation/` folder,
   `python tools/make_gaze_figure.py <recording.xdf>`, then render the deck.

## If something fails

| Symptom | Fix |
| --- | --- |
| `check_eyetracker.py` says no tracker found | Step 1: the runtime is missing, or replug the USB cable. |
| `No eye trackers found` when the demo starts | Same as above. |
| Both eyes rarely `yes`, or valid gaze well under 90% | Move to 60 to 65 cm and tilt the tracker towards the face (step 3). |
| Calibration table rows far from their `Point` | The volunteer looked away or moved. Redo it; check step 3 first. |
| Gaze is steady but always too low or too high | The tracker has the wrong screen position. Set the screen in Eye Tracker Manager (step 1). |
| `cannot import name 'DIRECTION_LTR'` | Rerun the last two install lines of step 2. |
| `No module named 'experiment'` | Run from the `mosaic` folder with `PYTHONPATH=src`. |
| `No module named 'ixp.experiment'` | `ixp` was cloned but not installed. Rerun its install line from step 2. |
| `Package 'ixp' requires a different Python` | The `--ignore-requires-python` flag is missing. |
| Imports pick up the wrong packages (machines with ROS, or packages in `~/.local`) | `conda env config vars set PYTHONNOUSERSITE=1 PYTHONPATH= -n mosaic_tobii`, then activate again. |
| Calibration opens on the wrong screen | Change `display:` in `configs/experiment.yaml`. |
| The tracker fails on the day | Go to slide 34, which shows the rehearsal recording. |

## What was tested

On Ubuntu 22.04 with a Tobii Pro Spark (2 October 2026): steps 2 to 5 as
written. The demo ran start to finish three times, both streams were recorded
on one clock (gaze at 60 Hz, game at 30 frames a second), and notebook Step 9
read the recording.

Not tested: Eye Tracker Manager (it was not installed, so the tracker ran on
the default screen position), a second screen or projector, starting and
stopping LabRecorder by hand (the rehearsal used its command-line recorder),
and Windows or macOS. In rehearsal valid gaze was 69% to 84% and calibration
was off by a few hundred pixels at some points, so settle seating and the
screen position at the venue before the session.
