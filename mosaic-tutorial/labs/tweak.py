"""Turn the knobs — the same mission, four different studies.

    python labs/tweak.py

Nothing here subclasses the environment. Every manipulation is an object
passed to the constructor.
"""
import random

from mosaic.core.camera import AgentConeCamera, AgentFOVCamera, CameraConfig
from mosaic.gui.main import SAREnvGUI
from mosaic.sar.actions import RescueAction, RescueRewards
from mosaic.sar.env import build_sar_env
from mosaic.sar.placers import LavaPlacer, LockedRoomPlacer, VictimPlacer

# 1. PLACERS — what goes in the world, and where
victims = VictimPlacer(num_real_victims=2)   # per ROOM, not total
lava = LavaPlacer(lava_per_room=4)
doors = LockedRoomPlacer(locked_room_prob=0.6)

# 2. CAMERA — how much of the world the participant can see
#    AgentFOVCamera   = the whole current room
#    AgentConeCamera  = only the forward visibility cone (harder, more search)
#    EdgeFollowCamera = the default; scrolls when the agent nears the edge
#
#    WARNING: FullviewCamera and AgentCenteredCamera raise AttributeError
#    today — PickupVictimEnv.reset() calls camera.reset(), which neither
#    class defines. Use one of the three above until that is fixed.
camera = AgentConeCamera(config=CameraConfig(tile_size=32))

# 3. ACTIONS + REWARDS — what a rescue is worth, and what a mistake costs
scoring = RescueAction(
    rewards=RescueRewards(
        real_victim_alive=+1.0,
        fake_victim=-1.0,       # cost of a false alarm -> raise it to shift criterion
        real_victim_dead=-2.0,  # cost of arriving too late
    )
)

env = build_sar_env(
    screen_size=800,
    num_rows=3,
    num_cols=3,
    room_size=8,
    victim_placer=victims,
    lava_placer=lava,
    locked_room_placer=doors,
    camera_strategy=camera,
    action=scoring,
)

# 4. OBSERVATIONS — what gets recorded every step. Subclass ObservationProcessor
#    to log whatever your analysis needs; the default GameObservation already
#    returns the full grid, agent pose, camera bounds, victim health and status.
random.seed(0)                 # placers use the global RNG ...
obs, _ = env.reset(seed=0)     # ... and env.reset() seeds the room skeleton
print("observation fields:", sorted(obs.keys()))
print("victims in this 3x3 building:", obs["remaining_victims"])
print("step budget:", obs["max_steps"])

if __name__ == "__main__":
    SAREnvGUI(env, config={"fullscreen": False}).run()
