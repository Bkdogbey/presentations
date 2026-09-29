"""Capture the first frame of the stock mission, as attendees see it at launch.

    python tools/capture_first_frame.py

The run-the-mission slide shows this as "you should see this", so it uses the
stock counts from configs/experiment.yaml (via build_study_env) and no warmup
steps: a crowded room, the full "Remaining" count, zero steps, no flash.
gui-screenshot-live.png stays on the interface slide, where a sparse room with
a flash reads better.
"""
import pygame

from _capture_common import ASSETS, build_study_env
from mosaic.gui.main import SAREnvGUI

SEED = 11


def main():
    env = build_study_env()
    gui = SAREnvGUI(env, config={"fullscreen": False, "max_time": 5})
    obs, _ = env.reset(seed=SEED)
    gui.user.obs = obs  # the info panel reads counts from here

    surface = gui._build_combined_surface(env.render())
    out = ASSETS / "gui-first-frame.png"
    pygame.image.save(surface, str(out))
    print(f"wrote {out.name}  {surface.get_size()}")
    pygame.quit()


if __name__ == "__main__":
    main()
