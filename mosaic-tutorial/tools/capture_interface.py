"""Capture the full interface with the edge vignette mid-flash.

    python tools/capture_interface.py

The vignette is a brief perimeter glow over the game viewport, keyed to SAR
events. It is the one part of the interface a still screenshot normally misses,
because it has usually faded by the time you press the shutter.

EdgeVignette takes its clock as an injectable callable, so instead of racing it
we hand it a frozen clock, trigger the event at t=0, and advance to the exact
peak of the fade envelope before compositing the frame.

Needs a MOSAIC checkout (MOSAIC_SRC below) and its runtime deps. Runs headless
through SDL's dummy video driver, so no window appears.

Not bit-reproducible: level generation retries internally on "connect_all
failed" and each retry consumes RNG, so the same seed can lay out a different
building from run to run. Re-run until you get one you like, and re-check the
.anno percentages on the interface slide if the panel layout ever shifts.
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
from mosaic.core.camera import AgentFOVCamera  # noqa: E402
from mosaic.gui.feedback import DEFAULT_VIGNETTE_STYLES, EdgeVignette  # noqa: E402
from mosaic.gui.main import SAREnvGUI  # noqa: E402
from mosaic.sar.env import build_sar_env  # noqa: E402
from mosaic.sar.placers import LockedRoomPlacer  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"
SEED = 11
GAME = 800
WARMUP = [2, 2, 1, 2, 2]

# Green "you rescued someone" flash: the positive event, and the one worth
# showing on a slide that is teaching people to read the screen.
EVENT = "victim_rescued"
# Where on the fade envelope to freeze. The envelope peaks at 0.125, but at full
# peak the tint floods the whole viewport and the tiles stop being readable --
# fine in motion, useless in a still. Just past halfway through the decay keeps
# an obvious perimeter glow while the world stays legible.
FLASH_PROGRESS = 0.45


class FrozenClock:
    """pygame.time.get_ticks stand-in whose value we set by hand."""

    def __init__(self):
        self.ms = 0

    def __call__(self):
        return self.ms


def main():
    clock = FrozenClock()
    vignette = EdgeVignette(GAME, clock_ms=clock)

    env = build_sar_env(
        screen_size=GAME,
        num_rows=3,
        num_cols=3,
        room_size=10,
        victim_placer=LavaRiskVictimPlacer(num_real_victims=2, num_fake_victims=2),
        lava_placer=SectorSpreadLavaPlacer(lava_per_room=4),
        locked_room_placer=LockedRoomPlacer(locked_room_prob=0.5),
        camera_strategy=AgentFOVCamera(),
    )
    gui = SAREnvGUI(env, config={"fullscreen": False, "max_time": 5}, vignette=vignette)
    env.reset(seed=SEED)
    for action in WARMUP:
        env.step(action)

    vignette.trigger([{"type": EVENT}])
    clock.ms = int(DEFAULT_VIGNETTE_STYLES[EVENT].duration * 1000 * FLASH_PROGRESS)

    surface = gui._build_combined_surface(env.render())
    out = OUT / "gui-screenshot-live.png"
    pygame.image.save(surface, str(out))
    print(f"wrote {out.name}  {surface.get_size()}")
    pygame.quit()


if __name__ == "__main__":
    main()
