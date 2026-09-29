"""Animate the three camera strategies on one walk, for the Camera Views slide.

    python tools/capture_camera_gifs.py

Builds ONE mission and walks the agent through a door into the next room. Every
step is rendered through all three cameras (EdgeFollowCamera, AgentFOVCamera,
AgentConeCamera) by calling each camera's get_crop() on the same world state,
exactly as SARLevelGen.get_camera_view() does. The world never forks, so the
three clips show the same walk and stay in step: every clip has the same frame
count and frame timing, and the deck restarts them together on slide entry.

Each frame carries the annotations of the still versions: a white ring on the
agent and a dashed orange outline of the room it is standing in, both computed
per frame from camera.get_visible_bounds().

Writes assets/cam-follow-walk.gif, cam-room-walk.gif, cam-cone-walk.gif.
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _capture_common import (  # noqa: E402
    ASSETS, GAME, door_state, is_door, save_gif, walk_to,
)
from make_camera_annotations import ORANGE, WHITE, _dashed_rect  # noqa: E402

from experiment.placers import LavaRiskVictimPlacer, SectorSpreadLavaPlacer  # noqa: E402
from minigrid.core.actions import Actions  # noqa: E402
from mosaic.core.camera import AgentConeCamera, AgentFOVCamera, EdgeFollowCamera  # noqa: E402
from mosaic.sar.env import build_sar_env  # noqa: E402
from mosaic.sar.placers import LockedRoomPlacer  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

OUT_PX = 400
STEP_MS = 340
HOLD_MS = 1000
CAMERAS = [
    ("cam-follow-walk", EdgeFollowCamera),
    ("cam-room-walk", AgentFOVCamera),
    ("cam-cone-walk", AgentConeCamera),
]


def build(seed):
    # Calmer than configs/experiment.yaml, as in capture_camera_views.py: a busy
    # room hides the thing the slide is about, which is what each camera shows.
    env = build_sar_env(
        screen_size=GAME, num_rows=3, num_cols=3, room_size=10,
        victim_placer=LavaRiskVictimPlacer(num_real_victims=2, num_fake_victims=2),
        lava_placer=SectorSpreadLavaPlacer(lava_per_room=4),
        locked_room_placer=LockedRoomPlacer(locked_room_prob=0.5),
        camera_strategy=AgentFOVCamera(),
    )
    random.seed(seed)
    obs, _ = env.reset(seed=seed)
    return env, obs


def script(env, obs):
    """Walk to the nearest unlocked door, open it if needed, and go through."""
    acts, door = walk_to(obs, lambda c: is_door(c) and door_state(c) in (0, 1), min_leg=3)
    if door is None or not 3 <= len(acts) <= 12:
        return None
    if door_state(obs["grid"][door[1]][door[0]]) == 1:
        acts.append(Actions.toggle)
    return acts + [Actions.forward] * 4


def render(env, camera):
    """One annotated frame of what `camera` shows right now."""
    room = env.room_from_pos(*env.agent_pos)
    crop = camera.get_crop(
        grid=env.grid, agent_pos=env.agent_pos, agent_dir=env.agent_dir, room=room,
        grid_width=env.width, grid_height=env.height, step_count=env.step_count, env=env,
    )
    img = Image.fromarray(crop).resize((OUT_PX, OUT_PX), Image.LANCZOS)
    x0, y0, x1, y1 = camera.get_visible_bounds(env.width, env.height)
    tile = OUT_PX / (x1 - x0)
    draw = ImageDraw.Draw(img)
    (rx, ry), (rw, rh) = room.top, room.size
    box = ((rx + 1 - x0) * tile + 2, (ry + 1 - y0) * tile + 2,
           (rx + rw - 1 - x0) * tile - 2, (ry + rh - 1 - y0) * tile - 2)
    box = (max(box[0], 2), max(box[1], 2), min(box[2], OUT_PX - 2), min(box[3], OUT_PX - 2))
    _dashed_rect(draw, box, ORANGE, width=3, dash=12, gap=8)
    ax, ay = env.agent_pos
    cx, cy = (ax - x0 + 0.5) * tile, (ay - y0 + 0.5) * tile
    r = tile * 0.56
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=4)
    return img


def main():
    for seed in range(1, 120):
        env, obs = build(seed)
        acts = script(env, obs)
        if acts is None:
            continue
        cameras = [(stem, cls()) for stem, cls in CAMERAS]
        frames = {stem: [render(env, cam)] for stem, cam in cameras}
        rooms = {env.room_from_pos(*env.agent_pos)}
        for action in acts:
            env.step(action)
            rooms.add(env.room_from_pos(*env.agent_pos))
            for stem, cam in cameras:
                frames[stem].append(render(env, cam))
        if len(rooms) < 2:
            continue  # the walk must cross into the next room
        durations = [HOLD_MS] + [STEP_MS] * (len(acts) - 1) + [HOLD_MS + 600]
        print(f"seed {seed}: {len(acts)} steps")
        for stem, _ in cameras:
            kb = save_gif(ASSETS / f"{stem}.gif", frames[stem], durations, palette=64)
            print(f"  wrote {stem}.gif  {len(durations)} frames  {kb:.0f} KB")
        return
    sys.exit("no seed produced a walk through a door")


if __name__ == "__main__":
    main()
