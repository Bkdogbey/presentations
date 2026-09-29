"""Shared pieces of the headless capture scripts in this folder.

Every capture builds the same mission `python -m experiment.main` builds, drives
it with a scripted breadth-first walk over the observed grid, and grabs frames
from the real GUI compositor (or, for the camera clips, from the camera
strategies directly). Runs through SDL's dummy video driver, so no window
appears. Needs a MOSAIC checkout at MOSAIC_SRC and its runtime deps.
"""
import collections
import os
import pathlib
import sys

# Set MOSAIC_SRC to point at another checkout (e.g. on Windows).
MOSAIC_SRC = os.environ.get("MOSAIC_SRC", "/home/bennett/Research/mosaic/src")
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, MOSAIC_SRC)

import numpy as np  # noqa: E402
import pygame  # noqa: E402
import yaml  # noqa: E402
from experiment.placers import LavaRiskVictimPlacer, SectorSpreadLavaPlacer  # noqa: E402
from minigrid.core.actions import Actions  # noqa: E402
from mosaic.core.camera import AgentFOVCamera  # noqa: E402
from mosaic.sar.env import build_sar_env  # noqa: E402
from mosaic.sar.placers import LockedRoomPlacer  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"
GAME = 800  # game viewport edge in px, as in experiment.main

# Grid codes from mosaic/sar/observations.py.
EMPTY, WALL, LAVA, VICTIM, FAKE = 0, 1, 4, 5, 6
DOOR_BASE, KEY_BASE = 10, 30
# MiniGrid direction vectors, indexed by agent_dir.
DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

ORANGE = (236, 103, 44)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
if not os.path.exists(FONT):  # not Linux: the bold sans pygame ships with
    FONT = os.path.join(os.path.dirname(pygame.__file__), "freesansbold.ttf")


class FrozenClock:
    """pygame.time.get_ticks stand-in whose value we advance by hand."""

    def __init__(self):
        self.ms = 0

    def __call__(self):
        return self.ms


def is_door(code):
    return DOOR_BASE <= code < DOOR_BASE + 18


def door_state(code):
    """0 = open, 1 = closed, 2 = locked (observations.py encoding)."""
    return (code - DOOR_BASE) % 3


def is_key(code):
    return KEY_BASE <= code < KEY_BASE + 6


def passable(code):
    """Walkable floor: empty cells and open doors. Lava, walls, keys, victims,
    and closed or locked doors are out — targets are approached from an
    adjacent cell."""
    if code == EMPTY:
        return True
    if is_door(code):
        return door_state(code) == 0
    return False


def route_to(grid, start, is_target, min_leg=0):
    """Breadth-first search to a cell adjacent to the nearest tile for which
    is_target(code) is true, skipping targets fewer than min_leg moves away.
    Returns (path_of_cells, target_cell) or (None, None)."""
    h, w = len(grid), len(grid[0])
    prev = {start: None}
    queue = collections.deque([start])
    while queue:
        cell = queue.popleft()
        x, y = cell
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < w and 0 <= ny < h) or (nx, ny) in prev:
                continue
            if is_target(grid[ny][nx]):
                path = [cell]
                while prev[path[0]] is not None:
                    path.insert(0, prev[path[0]])
                if len(path) > min_leg:
                    return path, (nx, ny)
                continue
            if passable(grid[ny][nx]):
                prev[(nx, ny)] = cell
                queue.append((nx, ny))
    return None, None


def turns_to(cur_dir, want_dir):
    """Fewest left/right actions to face want_dir."""
    delta = (want_dir - cur_dir) % 4
    if delta == 0:
        return []
    if delta == 1:
        return [Actions.right]
    if delta == 3:
        return [Actions.left]
    return [Actions.right, Actions.right]


def walk_to(obs, is_target, min_leg=0):
    """Actions that walk next to the nearest matching tile and face it.
    Returns (actions, target_cell) or ([], None)."""
    start = (obs["agent_x"], obs["agent_y"])
    path, target = route_to(obs["grid"], start, is_target, min_leg)
    if path is None:
        return [], None
    actions, cur, facing = [], start, obs["agent_dir"]
    for nxt in path[1:]:
        want = DIRS.index((nxt[0] - cur[0], nxt[1] - cur[1]))
        actions += turns_to(facing, want)
        actions.append(Actions.forward)
        cur, facing = nxt, want
    actions += turns_to(facing, DIRS.index((target[0] - cur[0], target[1] - cur[1])))
    return actions, target


def plan(obs, target, min_leg=0):
    """Action list that walks to the nearest `target` tile and picks it up."""
    actions, cell = walk_to(obs, lambda code: code == target, min_leg)
    return actions + [Actions.pickup] if cell else []


def build_study_env(camera=None):
    """The mission experiment.main builds, with counts from configs/experiment.yaml."""
    with open(pathlib.Path(MOSAIC_SRC).parent / "configs/experiment.yaml") as fh:
        game = yaml.safe_load(fh).get("game", {})
    return build_sar_env(
        screen_size=GAME,
        num_rows=3,
        num_cols=3,
        room_size=10,
        victim_placer=LavaRiskVictimPlacer(
            num_real_victims=game.get("num_real_victims", 6),
            num_fake_victims=game.get("num_fake_victims", 12),
        ),
        lava_placer=SectorSpreadLavaPlacer(lava_per_room=game.get("lava_per_room", 8)),
        locked_room_placer=LockedRoomPlacer(locked_room_prob=0.5),
        camera_strategy=camera or AgentFOVCamera(),
    )


def surface_to_image(surface):
    raw = pygame.surfarray.array3d(surface).transpose(1, 0, 2)
    return Image.fromarray(raw.astype(np.uint8))


def save_gif(path, frames, durations, palette=96):
    """Quantize RGB frames and write a looping GIF with per-frame durations."""
    quant = [f.quantize(colors=palette, method=Image.MEDIANCUT) for f in frames]
    quant[0].save(path, save_all=True, append_images=quant[1:],
                  duration=durations, loop=0, optimize=True)
    return path.stat().st_size / 1024


def keycap_strip(img, keys, lit=None, height=56):
    """Draw a row of keycaps along the bottom of img; the key named `lit`
    glows orange. Returns a new image."""
    img = img.copy()
    draw = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    draw.rectangle((0, h - height, w, h), fill=(20, 20, 24, 215))
    font = ImageFont.truetype(FONT, int(height * 0.42))
    pad, gap = 10, 10
    widths = [max(height - 2 * pad, draw.textlength(k, font=font) + 24) for k in keys]
    x = (w - (sum(widths) + gap * (len(keys) - 1))) / 2
    for key, kw in zip(keys, widths):
        box = (x, h - height + pad, x + kw, h - pad)
        on = key == lit
        draw.rounded_rectangle(box, radius=7,
                               fill=ORANGE + (255,) if on else (60, 60, 68, 255),
                               outline=(255, 255, 255, 230 if on else 90), width=2)
        draw.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), key, font=font,
                  fill=(255, 255, 255) if on else (190, 190, 196), anchor="mm")
        x += kw + gap
    return img
