"""Before/after images for the customize series: one pair per slide, showing
what each "Try it" edit changes on screen.

    MOSAIC_SRC=<checkout>/src python tools/capture_config_results.py

Each pair is rendered from the same seed with only the edited setting changed,
so the difference between the two images is the edit itself. Writes to
assets/results/:

- config-before/after.png    whole building, YAML counts 12/12/8 -> 2/2/2
- world-before/after.png     whole building, locked_room_prob 0.5 -> 0.9,
                             locked doors ringed in orange
- scoring-before/after.png   the REWARD metric after rescuing a decoy, default
                             rewards -> RescueRewards(fake_victim=-5.0), at 2x
- teammate-before.png        chat panel after Alt with the keyless dummy teammate
- teammate-*-msg.png         the chat message after Alt, dummy -> ReliableTeammate,
                             at 2x (run with `chatpair`)
- feedback-before/after.png  the decoy flash 0.3 s after the rescue, default
                             style -> VignetteStyle((200, 0, 0), 200, 1.5, "fade"),
                             same room: only the vignette is swapped
- data-fields.txt            what print(sorted(obs)) prints after env.reset()
- time-before/after.png      the TIME LEFT metric at the start, max_time 5 -> 2, at 2x
- panel-before/after.png     mission box, InfoPanel -> labs/panel.py's
                             NoProgressPanel (no "Remaining" count), at 2x
- nudge-before/after.png     chat panel after 10 turns and no Alt,
                             llm_nudge_interval 50 -> 10, with the
                             ReliableTeammate from labs/advisor.py attached
                             (the slide before keeps it)
- nudge-*-msg.png            the nudge pair cropped to the message box
- prompt-excerpt.txt         the start of what the teammate receives
                             (build_obs), trimmed to five columns

The view slide reuses cam-room-live.png / cam-cone-live.png from
capture_camera_views.py, which already differ only in the camera.

Every capture seeds Python's `random`, NumPy, and the env with the same seed
(the placers draw from the global RNGs), so both halves of a pair start from the
same building. The locked-room pair is the exception: the lock probability
changes how the building is generated (no seed in 1-59 kept the same doors at
0.5 and 0.9), so its two halves are two buildings. The slide quotes their
locked-door counts, so re-check them after re-running.
"""
import json
import os
import pathlib
import random
import sys
import time

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
from _capture_common import (  # noqa: E402
    ASSETS, FAKE, GAME, ORANGE, FrozenClock, plan, surface_to_image,
)

import numpy as np  # noqa: E402
import pygame  # noqa: E402
import yaml  # noqa: E402
from _capture_common import MOSAIC_SRC  # noqa: E402
from experiment.placers import LavaRiskVictimPlacer, SectorSpreadLavaPlacer  # noqa: E402
from mosaic.core.camera import AgentFOVCamera  # noqa: E402
from mosaic.gui.feedback import EdgeVignette, VignetteStyle  # noqa: E402
from mosaic.gui.main import SAREnvGUI  # noqa: E402
from mosaic.sar.actions import RescueAction, RescueRewards  # noqa: E402
from mosaic.sar.env import build_sar_env  # noqa: E402
from mosaic.sar.placers import LockedRoomPlacer  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

OUT = ASSETS / "results"
SEED = 11
CHAT_SEED = 2                  # the first ReliableTeammate reply is a direction and a distance
TILE = 24                      # whole-building renders: 28 tiles * 24 px
CHAT_BOX = (800, 400, 1200, 610)   # same crop as chat-advice.png
INFO_BOX = (800, 118, 1200, 212)   # info panel: the REWARD / TOTAL / TIME row
MISSION_BOX = (800, 34, 1200, 118) # info panel: the mission box alone

# Panel crops shown large on a slide render the GUI at twice experiment.main's
# size (the panel fonts scale with it), then crop inside each widget's frame.
UI = 2 * GAME
REWARD_CELL = (1618, 189, 1870, 323)   # the REWARD metric alone
TIME_CELL = (2138, 189, 2390, 323)     # the TIME LEFT metric alone
MISSION_CELL = (1618, 61, 2390, 177)   # the mission box, inside its frame
CHAT_MSG = (1609, 874, 2385, 986)      # the chat message area, inside its frame

with open(pathlib.Path(MOSAIC_SRC).parent / "configs/experiment.yaml") as fh:
    STOCK = yaml.safe_load(fh).get("game", {})
STOCK_COUNTS = dict(
    real=STOCK.get("num_real_victims", 6),
    fake=STOCK.get("num_fake_victims", 12),
    lava=STOCK.get("lava_per_room", 8),
)


def build(real, fake, lava, locked=0.5, size=GAME, **kwargs):
    """experiment.main's mission, with the edited knobs exposed."""
    return build_sar_env(
        screen_size=size,
        num_rows=3,
        num_cols=3,
        room_size=10,
        victim_placer=LavaRiskVictimPlacer(num_real_victims=real, num_fake_victims=fake),
        lava_placer=SectorSpreadLavaPlacer(lava_per_room=lava),
        locked_room_placer=LockedRoomPlacer(locked_room_prob=locked),
        camera_strategy=AgentFOVCamera(),
        **kwargs,
    )


def reset(env, seed=SEED):
    """env.reset() with the global RNGs the placers use seeded too."""
    random.seed(seed)
    np.random.seed(seed)
    return env.reset(seed=seed)


def whole_building(env, ring_locked=False):
    """Top-down render of every room; optionally ring each locked door."""
    base = env.unwrapped
    img = Image.fromarray(base.grid.render(TILE, base.agent_pos, base.agent_dir))
    locked = 0
    if ring_locked:
        draw = ImageDraw.Draw(img)
        for y in range(base.height):
            for x in range(base.width):
                cell = base.grid.get(x, y)
                if cell is not None and cell.type == "door" and cell.is_locked:
                    locked += 1
                    c = ((x + 0.5) * TILE, (y + 0.5) * TILE)
                    r = TILE * 0.95
                    draw.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r),
                                 outline=ORANGE, width=4)
    return img, locked


def world_pairs():
    env = build(**STOCK_COUNTS)
    reset(env)
    before, _ = whole_building(env)
    env = build(real=2, fake=2, lava=2)
    reset(env)
    after, _ = whole_building(env)
    before.save(OUT / "config-before.png")
    after.save(OUT / "config-after.png")
    print(f"config: stock {STOCK_COUNTS} -> 2/2/2")

    for prob, name in [(0.5, "before"), (0.9, "after")]:
        env = build(**STOCK_COUNTS, locked=prob)
        reset(env)
        img, locked = whole_building(env, ring_locked=True)
        img.save(OUT / f"world-{name}.png")
        print(f"world {name}: locked_room_prob={prob}, {locked} locked doors")


def gui_for(env, config=None, seed=SEED, **kwargs):
    gui = SAREnvGUI(env, config=config or {"fullscreen": False, "max_time": 5}, **kwargs)
    obs, _ = reset(env, seed)
    gui.user.obs = obs
    gui.user.total_reward = 0.0
    return gui


def scoring_pair():
    for name, kwargs in [
        ("before", {}),
        ("after", {"action": RescueAction(rewards=RescueRewards(fake_victim=-5.0))}),
    ]:
        clock = FrozenClock()
        env = build(**STOCK_COUNTS, size=UI, **kwargs)
        gui = gui_for(env, vignette=EdgeVignette(UI, clock_ms=clock))
        steps = plan(gui.user.obs, FAKE)
        assert steps, "no reachable decoy from the start"
        for action in steps:
            gui.user.step(action)
        gui.user._start_time = None           # timer reads max_time: only the reward differs
        surface = gui._build_combined_surface(env.render())
        surface_to_image(surface).crop(REWARD_CELL).save(OUT / f"scoring-{name}.png")
        print(f"scoring {name}: last_reward={gui.user.last_reward:+.1f}")


def teammate_before():
    clock = FrozenClock()
    pygame.time.get_ticks = clock          # chat blink runs off this clock
    env = build(**STOCK_COUNTS)
    gui = gui_for(env, vignette=EdgeVignette(GAME, clock_ms=clock))
    gui.user.ask_llm_async()               # what pressing Alt does
    while gui.user.llm_thread is not None and gui.user.llm_thread.is_alive():
        time.sleep(0.05)
    gui.chat_panel.poll_llm(gui.user)
    clock.ms += 5000                       # past the 3 s arrival blink
    gui.chat_panel.poll_llm(gui.user)
    surface = gui._build_combined_surface(env.render())
    surface_to_image(surface).crop(CHAT_BOX).save(OUT / "teammate-before.png")
    print(f"teammate before: {gui.user.last_llm_response!r}")


def teammate_pair():
    """The chat message after one Alt: the keyless dummy teammate, then
    labs/advisor.py's ReliableTeammate (at reliability 1.0, so the reply is
    the honest one). Same building for both."""
    sys.path.insert(0, os.path.join(HERE, "..", "labs"))
    from advisor import ReliableTeammate
    for name, kwargs in [("before", {}),
                         ("after", {"llm_client": ReliableTeammate(1.0),
                                    "prompt_builder": json.dumps})]:
        clock = FrozenClock()
        pygame.time.get_ticks = clock      # chat blink runs off this clock
        env = build(**STOCK_COUNTS, size=UI)
        gui = gui_for(env, seed=CHAT_SEED, vignette=EdgeVignette(UI, clock_ms=clock), **kwargs)
        gui.user.ask_llm_async()           # what pressing Alt does
        while gui.user.llm_thread is not None and gui.user.llm_thread.is_alive():
            time.sleep(0.05)
        gui.chat_panel.poll_llm(gui.user)
        clock.ms += 5000                   # past the 3 s arrival blink
        gui.chat_panel.poll_llm(gui.user)
        surface = gui._build_combined_surface(env.render())
        surface_to_image(surface).crop(CHAT_MSG).save(OUT / f"teammate-{name}-msg.png")
        print(f"teammate {name}: {gui.user.last_llm_response!r}")


def feedback_pair():
    styles = {"wrong_victim": VignetteStyle((200, 0, 0), 200, 1.5, "fade")}
    env = build(real=2, fake=2, lava=4)       # calm room so the flash reads
    gui = gui_for(env)
    frame = env.render()                      # one frame: only the flash differs
    for name, style_kw in [("before", {}), ("after", {"styles": styles})]:
        clock = FrozenClock()
        gui.vignette = EdgeVignette(GAME, clock_ms=clock, **style_kw)
        gui.vignette.trigger([{"type": "wrong_victim"}])
        clock.ms = 300
        surface = gui._build_combined_surface(frame)
        view = surface.subsurface(pygame.Rect(0, 0, GAME, GAME)).copy()
        surface_to_image(view).save(OUT / f"feedback-{name}.png")
        print(f"feedback {name}: frame at 0.3 s")


def data_fields():
    env = build(**STOCK_COUNTS)
    obs, _ = reset(env)
    text = str(sorted(obs))
    (OUT / "data-fields.txt").write_text(text + "\n", encoding="utf-8")
    print(f"data: {text}")


def time_pair():
    for name, minutes in [("before", 5), ("after", 2)]:
        env = build(**STOCK_COUNTS, size=UI)
        gui = SAREnvGUI(env, config={"fullscreen": False, "max_time": minutes})
        obs, _ = reset(env)
        gui.user.obs = obs
        gui.user.total_reward = 0.0
        gui.user.last_reward = 0.0
        surface = gui._build_combined_surface(env.render())
        surface_to_image(surface).crop(TIME_CELL).save(OUT / f"time-{name}.png")
        print(f"time {name}: max_time={minutes}")


def panel_pair():
    sys.path.insert(0, os.path.join(HERE, "..", "labs"))
    from panel import NoProgressPanel
    for name, kwargs in [("before", {}),
                         ("after", {"info_panel": NoProgressPanel(UI, UI // 2, UI // 2)})]:
        env = build(**STOCK_COUNTS, size=UI)
        gui = gui_for(env, **kwargs)
        surface = gui._build_combined_surface(env.render())
        surface_to_image(surface).crop(MISSION_CELL).save(OUT / f"panel-{name}.png")
        print(f"panel {name}")


def nudge_pair():
    sys.path.insert(0, os.path.join(HERE, "..", "labs"))
    from advisor import ReliableTeammate
    for name, every in [("before", 50), ("after", 10)]:
        clock = FrozenClock()
        pygame.time.get_ticks = clock
        env = build(**STOCK_COUNTS)
        gui = gui_for(env, config={"fullscreen": False, "max_time": 5,
                                   "llm_nudge_interval": every},
                      vignette=EdgeVignette(GAME, clock_ms=clock),
                      llm_client=ReliableTeammate(1.0), prompt_builder=json.dumps)
        for _ in range(10):                   # ten turns on the spot, no Alt
            gui.handle_user_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
            while gui.user.llm_thread is not None and gui.user.llm_thread.is_alive():
                time.sleep(0.05)
        gui.chat_panel.poll_llm(gui.user)
        clock.ms += 5000                      # past the 3 s arrival blink
        gui.chat_panel.poll_llm(gui.user)
        surface = gui._build_combined_surface(env.render())
        surface_to_image(surface).crop(CHAT_BOX).save(OUT / f"nudge-{name}.png")
        print(f"nudge {name}: llm_nudge_interval={every}, steps={gui.user.total_steps}")


def prompt_excerpt():
    from mosaic.llm.process_prompts import build_obs
    env = build(real=2, fake=2, lava=4)
    obs, _ = reset(env)
    lines = build_obs(obs).splitlines()
    keep = ["Object", "Direction", "Visible", "Reachable", "PathLength"]
    header = [c.strip() for c in lines[3].strip("|").split("|")]
    idx = [header.index(k) for k in keep]
    rows = [[c.strip() for c in ln.strip("|").split("|")] for ln in lines[5:11]]
    width = [max(len(keep[i]), *(len(r[j]) for r in rows)) for i, j in enumerate(idx)]
    fmt = lambda cells: "  ".join(c.ljust(w) for c, w in zip(cells, width)).rstrip()
    out = [lines[0], "", fmt(keep)] + [fmt([r[j] for j in idx]) for r in rows]
    text = "\n".join(out)
    (OUT / "prompt-excerpt.txt").write_text(text + "\n", encoding="utf-8")
    print(text)


def chat_crops():
    """The message box alone, so the reply stays legible when the image is
    shown at slide size. Runs on the chat images already written."""
    msg_box = (0, 44, 400, 116)
    for src, dst in [(OUT / "nudge-before.png", "nudge-before-msg.png"),
                     (OUT / "nudge-after.png", "nudge-after-msg.png")]:
        Image.open(src).crop(msg_box).save(OUT / dst)
        print(f"chat crop: {dst}")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    only = set(sys.argv[1:])
    for name, fn in [("world", world_pairs), ("scoring", scoring_pair),
                     ("teammate", teammate_before), ("chatpair", teammate_pair),
                     ("feedback", feedback_pair),
                     ("data", data_fields), ("time", time_pair), ("panel", panel_pair),
                     ("nudge", nudge_pair), ("prompt", prompt_excerpt),
                     ("chat", chat_crops)]:
        if not only or name in only:
            fn()
    pygame.quit()
