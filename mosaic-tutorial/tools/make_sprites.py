"""Render the single-tile game sprites used by the interface slide.

    python tools/make_sprites.py

Needs `minigrid` installed, plus a checkout of MOSAIC for the victim shapes
(Victim / FakeVictim are MOSAIC objects, not MiniGrid ones). Tiles are drawn at
4x and averaged down, so the diagonals stay smooth when the deck scales them.
"""
import importlib.util
import pathlib

import numpy as np
from minigrid.core.world_object import Door, Key, Lava
from minigrid.utils.rendering import (
    downsample,
    fill_coords,
    point_in_triangle,
    rotate_fn,
)
from PIL import Image

MOSAIC_OBJECTS = "/home/bennett/Research/mosaic/src/mosaic/sar/objects.py"
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "sprites"

SUPERSAMPLE = 4
TILE = 64
EXPORT = 256

spec = importlib.util.spec_from_file_location("sar_objects", MOSAIC_OBJECTS)
sar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sar)


def _blank():
    return np.zeros((TILE * SUPERSAMPLE, TILE * SUPERSAMPLE, 3), dtype=np.uint8)


def _save(img, name):
    img = downsample(img, SUPERSAMPLE).astype(np.uint8)
    OUT.mkdir(parents=True, exist_ok=True)
    Image.fromarray(img).resize((EXPORT, EXPORT), Image.LANCZOS).save(OUT / f"{name}.png")


def _object(obj, name):
    img = _blank()
    obj.render(img)
    _save(img, name)


def _health(level, name):
    """A real victim with its health bar showing, as the study reveals it while
    advice is on screen: the white bar's height is the victim's health."""
    victim = sar.Victim("up")
    victim.health = level
    victim.show_battery(3600)
    _object(victim, name)


def _agent(name):
    """MiniGrid draws the agent itself, so reproduce its triangle here."""
    img = _blank()
    triangle = point_in_triangle((0.12, 0.19), (0.87, 0.50), (0.12, 0.81))
    fill_coords(img, rotate_fn(triangle, cx=0.5, cy=0.5, theta=0.0), (255, 0, 0))
    _save(img, name)


if __name__ == "__main__":
    _agent("agent")
    _object(sar.Victim("up"), "victim-real")
    _object(sar.FakeVictim("left", "up"), "victim-decoy")
    _object(Lava(), "lava")
    _object(Door("blue", is_locked=True), "door-locked")
    _object(Door("green"), "door-closed")
    _object(Key("blue"), "key")
    for level in (1.0, 0.6, 0.25, 0.0):
        _health(level, f"health-{int(level * 100)}")
    print(f"wrote sprites to {OUT}")
