"""Capture the three camera strategies from the actually running game.

    python tools/capture_camera_views.py

Builds ONE mission, plays a few moves, then re-renders that single frozen world
through each camera via env.switch_camera(). Building three envs will not do:
level generation retries on "connect_all failed", and each retry consumes RNG,
so three separately seeded builds drift into three different buildings.

Saves the game viewport exactly as the player sees it -- the same 800px surface
the GUI composites, same smoothscale, same vignette layer.

Needs a MOSAIC checkout (MOSAIC_SRC below) and its runtime deps. Runs headless
through SDL's dummy video driver, so no window appears.
"""
import os
import pathlib
import sys

# Set MOSAIC_SRC to point at another checkout (e.g. on Windows).
MOSAIC_SRC = os.environ.get("MOSAIC_SRC", "/home/bennett/Research/mosaic/src")
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, MOSAIC_SRC)

import pygame  # noqa: E402
from experiment.placers import LavaRiskVictimPlacer, SectorSpreadLavaPlacer  # noqa: E402
from mosaic.core.camera import AgentConeCamera, AgentFOVCamera, EdgeFollowCamera  # noqa: E402
from mosaic.gui.main import SAREnvGUI  # noqa: E402
from mosaic.sar.env import build_sar_env  # noqa: E402
from mosaic.sar.placers import LockedRoomPlacer  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"
SEED = 11
GAME = 800
# A few moves off the spawn tile. Chosen by sweeping short sequences and keeping
# the one whose cone view is least degenerate -- face a wall and AgentConeCamera
# legitimately shows almost nothing, which reads as a broken image on a slide.
WARMUP = [2, 2, 1, 2, 2]

# Deliberately calmer than configs/experiment.yaml: at 6 real + 12 decoy victims
# per room the frame is so busy that the camera difference stops being the thing
# you notice, which is the whole point of the slide.
MISSION = dict(
    num_rows=3,
    num_cols=3,
    room_size=10,
    real_victims=2,
    fake_victims=2,
    lava_per_room=4,
    locked_room_prob=0.5,
)

CAMERAS = [
    ("cam-follow", EdgeFollowCamera),
    ("cam-room", AgentFOVCamera),
    ("cam-cone", AgentConeCamera),
]


def build():
    env = build_sar_env(
        screen_size=GAME,
        num_rows=MISSION["num_rows"],
        num_cols=MISSION["num_cols"],
        room_size=MISSION["room_size"],
        victim_placer=LavaRiskVictimPlacer(
            num_real_victims=MISSION["real_victims"],
            num_fake_victims=MISSION["fake_victims"],
        ),
        lava_placer=SectorSpreadLavaPlacer(lava_per_room=MISSION["lava_per_room"]),
        locked_room_placer=LockedRoomPlacer(
            locked_room_prob=MISSION["locked_room_prob"]
        ),
        camera_strategy=EdgeFollowCamera(),
    )
    gui = SAREnvGUI(env, config={"fullscreen": False, "max_time": 5})
    env.reset(seed=SEED)
    for action in WARMUP:
        env.step(action)
    return env, gui


def capture(env, gui, stem, camera_cls):
    camera = camera_cls()
    env.switch_camera(camera)
    if hasattr(camera, "reset"):
        camera.reset()
    surface = gui._build_combined_surface(env.render())
    view = surface.subsurface(pygame.Rect(0, 0, GAME, GAME)).copy()
    out = OUT / f"{stem}-live.png"
    pygame.image.save(view, str(out))
    print(f"wrote {out.name}")


if __name__ == "__main__":
    env, gui = build()
    for stem, cls in CAMERAS:
        capture(env, gui, stem, cls)
    pygame.quit()
