# MOSAIC Tutorial — Before You Arrive

**IEEE SMC 2026 · Bellevue, WA · two-hour hands-on tutorial**

**You do not need to install anything.** The whole tutorial runs in your browser,
on the tutorial's Jupyter server: the game is drawn on the server and shown in
the notebook, and the keys you press go back to it.

## What you need

- A laptop with a current browser (Chrome, Firefox, Edge, or Safari) and Wi-Fi
- The password you were given for the tutorial server
- No API key, no Python, no Git

## Before the session (two minutes)

1. Open <https://jupyter.ihuman-lab.work>.
2. Sign in with your password.
3. Open `02_mosaic_human_ai.ipynb`. If it asks for a kernel, choose **Python (smc)**.
4. Run the first code cell and then the cells of Step 1, each with `Shift+Enter`.

✓ **Checkpoint** — Step 1 prints `game config: {...}` and `mission: pick up all 8
victims`, and no cell shows red error text. If so, you are ready; you can close the
notebook. If not, tell a helper when you arrive.

In the session, open the same notebook. Wherever a cell opens a game, **click the
picture first**, then use the keys: arrows turn and walk, `Space` opens a door,
`E` (or `Tab`) picks up a key or rescues the victim in front of you, `Q` (or `Alt`)
asks the AI teammate. Press **Stop** to end a game and see your score.

## If something does not work

| Symptom | Fix |
| --- | --- |
| The server does not open | Check your Wi-Fi, then ask a helper. Share a neighbor's screen meanwhile. |
| `No module named 'mosaic'` | Wrong kernel: pick **Python (smc)** at the top right of the notebook. |
| `No module named 'live_play'` | `live_play.py` is not in the same folder as the notebook. Ask a helper. |
| The picture does not move | Click the picture once, then press the keys. |
| A blank picture | Run the cell again and wait a second. |
| The page asks you to sign in again | Sign in; your work is kept. |

## Optional: run it on your own laptop

Only if you want to work offline or take it home. You need Python **3.10 or 3.11**
(3.12 and newer are not supported) and Git. The game is drawn off-screen and shown
in the notebook, so no display setup is needed.

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

Choose either `venv` or Conda, not both. Your prompt should now start with
`(mosaic_env)`. On Ubuntu, if you see `ensurepip is not available`, run
`sudo apt install python3-venv`, delete `mosaic_env`, and repeat.

Then, from the `mosaic` folder:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip uninstall -y pygame
python -m pip install --force-reinstall "pygame-ce>=2.5.2"
python -m pip install matplotlib scipy pandas pylsl pyxdf
python -m pip install ipywidgets ipyevents notebook
python -c "import mosaic.sar.env, mosaic.gui.main; print('MOSAIC ready')"
```

The check prints a `pygame-ce` banner, then `MOSAIC ready`. The two `pygame` lines
are a workaround: MOSAIC's `pyproject.toml` declares plain `pygame`, but its
interface (`pygame_gui`) needs `pygame-ce`, and both install into the same folder.
Without them the import fails with
`ImportError: cannot import name 'DIRECTION_LTR' from 'pygame'`.
`--force-reinstall` is required: uninstalling `pygame` deletes files `pygame-ce`
shares, and a plain `pip install pygame-ce` then repairs nothing. A line saying
`mosaic 0.1.0 requires pygame` is harmless.

Open the notebook from its own folder, because it reads `config.yaml` from there:

```bash
cd notebooks
python -m jupyter notebook 02_mosaic_human_ai.ipynb
```

If Jupyter asks for a kernel, choose **Python 3 (ipykernel)**. The notebook folder
holds the files it needs: `02_mosaic_human_ai.ipynb`, `config.yaml`,
`live_play.py`, `lsl_tools.py` and `leaderboard.py`.

| Symptom | Fix |
| --- | --- |
| `ImportError: cannot import name 'DIRECTION_LTR'` | You skipped the two `pygame` lines. |
| `AttributeError: module 'pygame' has no attribute 'surface'` | You ran them without `--force-reinstall`. Rerun with the flag. |
| `ModuleNotFoundError: No module named 'mosaic'` | The environment is not active, or `pip install -e .` did not finish. |
| `No module named 'ipyevents'` | `python -m pip install ipywidgets ipyevents`, then restart Jupyter. |
| The picture never appears | Run the first code cell first, then the game cell; check the browser console for widget errors. |
| Hangs forever after you changed a setting | `locked_room_prob` is `1.0`. Every room locked leaves no solvable layout. Use `0.9` or less. |
| `AttributeError: 'FullviewCamera' object has no attribute 'reset'` | Known bug, same for `AgentCenteredCamera`. Build levels with `AgentFOVCamera`, `AgentConeCamera`, or the default; use the other two only with `switch_camera`. |
| `python --version` shows 3.12 or newer | Recreate the environment with Python 3.10 or 3.11. |

## Links

- Repository — <https://github.com/iHuman-Lab/mosaic>
- Tutorial materials — <https://github.com/iHuman-Lab/presentations/tree/main/mosaic-tutorial>
- Documentation — <https://ihuman-lab.github.io/mosaic/>
