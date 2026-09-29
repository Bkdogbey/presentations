"""Record a short gameplay loop as the animated GIF on the "run the mission" slide.

    python tools/capture_gameplay.py

Builds the same mission `python -m experiment.main` builds and drives the agent,
by breadth-first search over the observed grid, through a short script: rescue
the nearest real victim (green flash, +1), then the nearest decoy (red flash,
-1), then another real victim. Frames come from the real GUI compositor, so the
info panel, the chat panel and the vignettes are the ones attendees will see.

Pacing is slower than live play so a room can follow it: each move is held for
STEP_MS, each flash plays at half speed, and the result is held before the next
walk starts.

Two things are faked, both because we are not inside `gui.run()`:

- the vignette clock is a frozen counter we advance by hand, so each flash
  fades across several GIF frames instead of vanishing;
- the walk is scripted rather than typed.

Needs a MOSAIC checkout (MOSAIC_SRC in _capture_common.py) and its runtime deps. Runs headless
through SDL's dummy video driver, so no window appears.

Not bit-reproducible: level generation retries internally on "connect_all
failed" and each retry consumes RNG, so the same seed can lay out a different
building from run to run. Re-run until you get a clip that reads well.
"""
import collections
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _capture_common import (  # noqa: E402
    ASSETS, FAKE, GAME, VICTIM, FrozenClock, build_study_env, plan,
)

import numpy as np  # noqa: E402
import pygame  # noqa: E402
from mosaic.gui.feedback import EdgeVignette  # noqa: E402
from mosaic.gui.main import SAREnvGUI  # noqa: E402
from PIL import Image  # noqa: E402

OUT = ASSETS / "gameplay.gif"
SEED = int(os.environ.get("SEED", 7))
STEP_MS = 220            # display time of each move
FLASH_TICK_MS = 50       # vignette clock advance per flash frame ...
FLASH_SHOW_MS = 100      # ... shown for twice as long: flashes play at half speed
HOLD_MS = 900            # still frame after a flash, so the score change reads
MIN_LEG = 5              # skip targets closer than this many tiles, so the agent walks
MAX_STEPS = 70           # moves across the whole script; longer clips are rejected
SCALE = 0.44             # 1200x800 compositor output -> 528x352
PALETTE = 96             # GIF colours; the interface is mostly flat fills
SCRIPT = (VICTIM, FAKE, VICTIM)  # what to reach and pick up, in order


def main():
    clock = FrozenClock()
    vignette = EdgeVignette(GAME, clock_ms=clock)

    env = build_study_env()
    gui = SAREnvGUI(env, config={"fullscreen": False, "max_time": 5}, vignette=vignette)

    random.seed(SEED)
    obs, _ = env.reset(seed=SEED)
    gui.user.obs = obs
    gui.user.total_reward = 0.0

    frames, durations = [], []
    counts = collections.Counter()

    def capture(show_ms, tick_ms):
        surface = gui._build_combined_surface(env.render())
        raw = pygame.surfarray.array3d(surface).transpose(1, 0, 2)
        img = Image.fromarray(raw.astype(np.uint8))
        img = img.resize(
            (int(img.width * SCALE), int(img.height * SCALE)), Image.LANCZOS)
        frames.append(img.quantize(colors=PALETTE, method=Image.MEDIANCUT))
        durations.append(show_ms)
        clock.ms += tick_ms

    # Plan every leg up front against the live state, so a script that cannot
    # finish (no reachable decoy, too many steps) is rejected before rendering.
    capture(HOLD_MS, 0)
    steps = 0
    for target in SCRIPT:
        actions = plan(gui.user.obs, target, MIN_LEG)
        if not actions:
            sys.exit(f"seed {SEED}: no reachable target {target}; try another SEED")
        steps += len(actions)
        if steps > MAX_STEPS:
            sys.exit(f"seed {SEED}: script needs over {MAX_STEPS} steps; try another SEED")
        for action in actions:
            gui.user.step(action)
            events = (gui.user.last_info or {}).get("events", [])
            if not events:
                capture(STEP_MS, STEP_MS)
                continue
            vignette.trigger(events)
            counts.update(e["type"] for e in events)
            flash_ms = max(vignette._duration_ms, 1)
            for _ in range(flash_ms // FLASH_TICK_MS + 1):
                capture(FLASH_SHOW_MS, FLASH_TICK_MS)
            capture(HOLD_MS, 0)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        OUT, save_all=True, append_images=frames[1:],
        duration=durations, loop=0, optimize=True,
    )
    kb = OUT.stat().st_size / 1024
    print(f"wrote {OUT.name}  seed {SEED}  {steps} steps  {len(frames)} frames  "
          f"{sum(durations) / 1000:.1f} s  {dict(counts)}  {kb:.0f} KB")
    pygame.quit()


if __name__ == "__main__":
    main()
