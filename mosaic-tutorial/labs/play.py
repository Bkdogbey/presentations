"""Play your first rescue mission.

    python labs/play.py

Needs MOSAIC installed (`python -m pip install -e .` in the mosaic repo). No
PYTHONPATH, no config file, and no AI provider key.

Controls:  arrows = turn / move forward,  Space = open door,
           Tab = pick up a key or rescue a victim,  Left Shift = drop,
           Alt = request advice from the AI teammate,  Backspace = restart,
           F11 = fullscreen,  Esc = quit.

No teammate is attached below, so Alt replies "Currently, no commands are
available." See advisor.py for a teammate that gives real advice without a key.
"""
import random

from mosaic.gui.main import SAREnvGUI
from mosaic.sar.env import build_sar_env
from mosaic.sar.placers import LavaPlacer, LockedRoomPlacer, VictimPlacer

# ──────────────────────────── EDIT ME ────────────────────────────
# Every line below is a knob. Change one, rerun, see what it does.

SEED = None          # set to an int (e.g. 42) for the same building every time
NUM_ROWS = 2         # building is NUM_ROWS x NUM_COLS rooms      -> try 3
NUM_COLS = 2         #                                            -> try 3
ROOM_SIZE = 8        # tiles per room (interior = ROOM_SIZE - 2)  -> try 12
VICTIMS_PER_ROOM = 2 # NOTE: per ROOM, not total. 2x2 x 2 = 8 victims
LAVA_PER_ROOM = 2    # risk pressure                              -> try 6
LOCKED_ROOM_PROB = 0.5   # fraction of rooms locked               -> try 0.9
                         # (1.0 locks every room and hangs the generator)
MAX_TIME = 3         # wall-clock minutes before the mission fails
# ─────────────────────────── /EDIT ME ────────────────────────────

env = build_sar_env(
    screen_size=800,
    num_rows=NUM_ROWS,
    num_cols=NUM_COLS,
    room_size=ROOM_SIZE,
    victim_placer=VictimPlacer(num_real_victims=VICTIMS_PER_ROOM),
    lava_placer=LavaPlacer(lava_per_room=LAVA_PER_ROOM),
    locked_room_placer=LockedRoomPlacer(locked_room_prob=LOCKED_ROOM_PROB),
)

# Reproducibility needs BOTH seeds: env.reset() seeds the room/door skeleton,
# but the placers (victims, lava, keys) still draw from the global `random`.
if SEED is not None:
    random.seed(SEED)
    env.reset(seed=SEED)
else:
    env.reset()          # never skip this — the GUI needs a built world

SAREnvGUI(env, config={"fullscreen": False, "max_time": MAX_TIME}).run()
