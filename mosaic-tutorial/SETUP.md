# MOSAIC Tutorial — Attendee Setup

**IEEE SMC 2026 · Bellevue, WA · two-hour hands-on tutorial**

Please do this **before you arrive**. It takes about five minutes on conference
Wi-Fi and under a minute on a good connection.

## Requirements

- Python **3.10 or 3.11** (`python3 --version`). These are the supported
  tutorial versions; 3.12 and newer are not, so create your environment with
  3.11 if that is what your laptop ships.
- Git
- PowerShell, macOS Terminal, or any Linux shell
- A laptop with a real display — the game opens a window, so a remote/SSH-only
  machine or Colab will not work for the GUI
- No API key is required for the core tutorial. AI-teammate provider setup is optional.

## 1 · Clone and isolate

**macOS / Linux**

```bash
git clone https://github.com/iHuman-Lab/mosaic.git
cd mosaic
python3 -m venv mosaic_env
source mosaic_env/bin/activate
```

**Windows PowerShell**

```powershell
git clone https://github.com/iHuman-Lab/mosaic.git
cd mosaic
python -m venv mosaic_env
.\mosaic_env\Scripts\Activate.ps1
```

If PowerShell blocks the activation script:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\mosaic_env\Scripts\Activate.ps1
```

**Conda alternative on any platform**

```bash
git clone https://github.com/iHuman-Lab/mosaic.git
cd mosaic
conda create --name mosaic_env python=3.11 -y
conda activate mosaic_env
```

Choose either `venv` or Conda. Do not create both environments.

✓ **Checkpoint** — your prompt now starts with `(mosaic_env)`. If it does not, the
next step installs into the wrong Python.

> Ubuntu: if you see `ensurepip is not available`, run
> `sudo apt install python3-venv`, delete `mosaic_env`, and repeat.

## 2 · Install the package

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

```text
Successfully installed ... minigrid-3.1.0 mosaic-0.1.0 numpy-2.2.6
  pygame-2.6.1 pygame-ce-2.5.8 pygame_gui-0.6.14 ...
```

✓ **Checkpoint** — note that it installed **both** `pygame` and `pygame-ce`, and
`pygame` landed last. That is the bug the next step fixes.

## 3 · Fix the two packaging gaps

```bash
python -m pip uninstall -y pygame
python -m pip install --force-reinstall "pygame-ce>=2.5.2"
```

`--force-reinstall` is **required**. Uninstalling `pygame` deletes files from the
shared `pygame` namespace that `pygame-ce` also owns; a plain
`pip install pygame-ce` then reports "Requirement already satisfied" and repairs
nothing.

You may see `ERROR: mosaic 0.1.0 requires pygame, which is not installed.` —
**expected and harmless.** That is `pyproject.toml` naming the wrong package;
`pygame-ce` satisfies it in practice.

`tabulate` is the second gap: MOSAIC uses it to build the prompt for a real AI
teammate but does not declare it yet. The core tutorial does not need it. If
you plan to connect your own LLM, or `Alt` ever replies
`Import tabulate failed`, install it directly:

```bash
python -m pip install tabulate
```

✓ **Checkpoint**

```bash
python -c "from mosaic.gui.main import SAREnvGUI; print('GUI OK')"
```

```text
pygame-ce 2.5.8 (SDL 2.32.10, Python 3.10.20)
GUI OK
```

### Why any of this is necessary

MOSAIC's interface is built on `pygame_gui`, which requires **pygame-ce** (the
community edition). `pyproject.toml` declares plain `pygame`. Both install into
the same `pygame` namespace, and the loser gets shadowed. The symptom is an
import error at startup:

```
ImportError: cannot import name 'DIRECTION_LTR' from 'pygame'
```

This is a known packaging issue and will be resolved in the PyPI release.

## 4 · Verify

```bash
python -c "
from mosaic.sar.env import build_sar_env
from mosaic.sar.placers import VictimPlacer
env = build_sar_env(screen_size=600, num_rows=2, num_cols=2, room_size=8,
                    victim_placer=VictimPlacer(num_real_victims=2))
env.reset(seed=0)
print('MOSAIC OK —', env.get_mission_status())
"
```

Expected output:

```
MOSAIC OK — {'status': 'continue', 'saved_victims': 0, 'remaining_victims': 8}
```

Eight, not two: `num_real_victims` is **per room**, and a 2×2 building has four
rooms.

Lines reading `Timeout during mission generation: connect_all failed` or
`Sampling rejected: unreachable object at ...` may appear. Both are the level
generator retrying — warnings, not errors.

## 5 · Run MOSAIC

Keep `mosaic_env` active and stay in the cloned `mosaic` directory.

**macOS / Linux**

```bash
PYTHONPATH=src python -m experiment.main
```

**Windows PowerShell**

```powershell
$env:PYTHONPATH = "src"
python -m experiment.main
```

The Pygame interface opens fullscreen. Use the arrow keys to move, `Tab` to
rescue the victim you are facing, `F11` for a window (`fn`+`F11` on macOS, or set `fullscreen: false` in
`configs/experiment.yaml`), and `Esc` to quit. No
extra repository, notebook, or Python file is required.

> If you cloned before the fix landed, `git pull` first. Two imports were
> commented out in `src/experiment/main.py`, which made the runner exit with
> `NameError: name 'LavaRiskVictimPlacer' is not defined`.

## 6 · Get the two tutorial files

The session uses two small files from the tutorial repository: `advisor.py`
(in Part Four, when everyone swaps in a teammate that needs no key) and
`panel.py` (an optional appendix task). Download both from
<https://github.com/iHuman-Lab/presentations/tree/main/mosaic-tutorial/labs>
and save them into `src/experiment/` in your `mosaic` folder. The session shows
where they go when you reach those slides.

## 7 · Optional: the notebook

`notebooks/02_mosaic_human_ai.ipynb` is the take-home companion to the
session. It carries these install commands, shows each change the tutorial
makes to `main.py` (camera, rewards, feedback flash, AI teammate) in a cell,
lets you play the mission inside the notebook, and records game state together
with (synthetic) eye gaze. The session points to it but does not depend on it.
It draws off-screen, so it needs no window.

Attendees can run it with nothing to install on the tutorial's Jupyter server,
<https://jupyter.ihuman-lab.work>: sign in with your password and open
`02_mosaic_human_ai.ipynb`. To run it on your own laptop instead:

Save these two files into the `notebooks` folder, replacing the files of the
same name:
[02_mosaic_human_ai.ipynb](https://github.com/Bkdogbey/mosaic/raw/smc2026/notebooks/02_mosaic_human_ai.ipynb)
and [lsl_tools.py](https://github.com/Bkdogbey/mosaic/raw/smc2026/notebooks/lsl_tools.py).
Then add five packages and start Jupyter from the `notebooks` folder, because
the notebook reads `config.yaml` from there:

```bash
python -m pip install matplotlib scipy pylsl pyxdf notebook
cd notebooks
python -m jupyter notebook 02_mosaic_human_ai.ipynb
```

If Jupyter asks for a kernel, choose **Python 3 (ipykernel)**.

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| `ImportError: cannot import name 'DIRECTION_LTR'` | You skipped step 3. |
| `AttributeError: module 'pygame' has no attribute 'surface'` | You ran step 3 without `--force-reinstall`. Rerun it with the flag. |
| `ERROR: mosaic 0.1.0 requires pygame` | Harmless warning from step 3, not an error. Carry on. |
| PowerShell reports that `mosaic_env` could not be loaded | Run `.\mosaic_env\Scripts\Activate.ps1`; the leading `.\` is required. |
| `ensurepip is not available` | `sudo apt install python3-venv`, delete `mosaic_env`, remake it. |
| `ModuleNotFoundError: No module named 'mosaic'` | The virtual environment is not active, or `pip install -e .` did not finish. |
| Window appears and closes immediately | Run the command from a terminal and read the traceback. |
| `Timeout during mission generation` / `Sampling rejected` | Harmless warnings; the generator retries automatically. |
| Hangs forever with no window, after changing settings | You set `locked_room_prob=1.0`. Every room locked leaves no solvable layout and the generator retries forever. Use `0.9` or less. |
| `AttributeError: 'FullviewCamera' object has no attribute 'reset'` | Known bug; `AgentCenteredCamera` fails the same way. Use `AgentFOVCamera`, `AgentConeCamera`, or the default `EdgeFollowCamera`. |
| Nothing renders, or `pygame.error: No available video device` | You are on a headless or remote machine. Use a local laptop. |
| `Alt` replies `Currently, no commands are available.` | Expected. The runner attaches the keyless `dummy` teammate; a real provider is the optional extension. |
| `Missing optional dependency 'tabulate'` | `pip install tabulate` — normally installed with the package. |
| `NameError: name 'LavaRiskVictimPlacer' is not defined` | Your clone predates the fix. `git pull` in the `mosaic` directory. |
| `No module named 'experiment'` | Run from the repository root with `PYTHONPATH=src`. |
| Font warnings from `pygame_gui` | Harmless. |

If you are still stuck when you arrive, come to the front — we have helpers and a
pre-built environment on a spare machine.

## Links

- Repository — <https://github.com/iHuman-Lab/mosaic>
- Tutorial materials — <https://github.com/iHuman-Lab/presentations/tree/main/mosaic-tutorial>
- Documentation — <https://ihuman-lab.github.io/mosaic/>
