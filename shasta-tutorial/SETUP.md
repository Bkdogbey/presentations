# Before You Arrive — SHaSTA Tutorial

**IEEE SMC 2026 · Bellevue, WA · Session 2, 11:00 AM–1:00 PM · Evergreen C**

**You do not need to install anything.** The tutorial runs in your browser, on the tutorial's Jupyter server:
the simulation and the interface are drawn on the server and shown in the notebook, and your mouse and keys go back to it.

## What you need

- A laptop with a current browser (Chrome, Firefox, Edge, or Safari) and Wi-Fi
- The password you were given for the tutorial server
- No API key, no Python, no Git

## Before the session (two minutes)

1. Open <https://jupyter.ihuman-lab.work>.
2. Sign in with your password.
3. Open `01_shasta_hsi.ipynb`. If it asks for a kernel, choose **Python (smc)**.
4. Run the first code cell and then the cells of Step 1, each with `Shift+Enter`.

✓ **Checkpoint** — Step 1 prints the number of intersections and street segments of the map, draws it with numbered intersections, and no cell shows
red error text. If so, you are ready. If not, tell a helper when you arrive.

In the session, open the same notebook. Wherever a cell opens the interface, **click the picture first**, then use the mouse and the keys:
click a group's marker (or press `1`-`9`), click a street node, then `Enter` or the **Send order** button. The wheel zooms, a right-drag pans,
`Space` pauses. Press **Stop** to end and see how many targets you reached.

## If something does not work

| Symptom | Fix |
| --- | --- |
| The server does not open | Check your Wi-Fi, then ask a helper. Share a neighbor's screen meanwhile. |
| `No module named 'shasta'` | Wrong kernel: pick **Python (smc)** at the top right of the notebook. |
| `No module named 'live_play'` | `live_play.py` is not in the same folder as the notebook. Ask a helper. |
| The picture does not respond | Click the picture once, then use the mouse and keys. |
| A blank picture | Run the cell again and wait a second. |
| `Cannot load an actor multiple times` | Rerun the whole cell, not only its last line. |
| The page asks you to sign in again | Sign in; your work is kept. |

## Optional: run it on your own laptop

Only if you want to work offline or take it home. You need Python **3.9 or newer** and Git. The interface is drawn off-screen and shown in the notebook,
so no display setup is needed. The PyPI package is not published yet, so install from a clone.

**macOS / Linux**

```bash
git clone <the shasta-ub repository URL>
cd shasta-ub
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
git clone <the shasta-ub repository URL>
cd shasta-ub
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Then, from the `shasta-ub` folder:

```bash
python -m pip install -e ".[gui]"
python -m pip install pylsl pyxdf ipywidgets ipyevents notebook
cd notebooks
python -m jupyter notebook 01_shasta_hsi.ipynb
```

`[gui]` adds the human interface. Check the install with `shasta maps` (lists the maps) and `shasta demo` (a headless mission; it should end with
"All groups reached their targets"). `shasta gui` opens the interface in its own window. If Jupyter asks for a kernel, choose **Python 3 (ipykernel)**.

| Symptom | Fix |
| --- | --- |
| `pip install` fails looking for `ihuman-shasta` on PyPI | You are not installing from the clone. Run `pip install -e ".[gui]"` from inside `shasta-ub`. |
| `shasta: command not found` | Activate the virtual environment in the terminal you run `shasta` from. |
| `No module named 'ipyevents'` | `python -m pip install ipywidgets ipyevents`, then restart Jupyter. |
| The picture never appears | Run the first code cell first, then the interface cell; check the browser console for widget errors. |

If you are still stuck when you arrive, come to the front: we have helpers and a pre-built environment on a spare machine.
