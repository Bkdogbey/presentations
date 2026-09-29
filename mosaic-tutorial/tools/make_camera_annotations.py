"""Annotate the three camera renders so their difference reads from a distance.

    python tools/make_camera_annotations.py

Each render gets a white ring on the agent and a dashed orange outline of the
room the agent is standing in. Side by side that shows the moving viewport
spilling past the room, the room camera matching it exactly, and the cone
camera covering less than it.

Runs on the live captures from capture_camera_views.py. Tile sizes differ per
camera because each one crops a different number of tiles into the same 800px
surface: the follow camera shows 8x8, the room and cone cameras show 10x10.
Re-derive these if the capture settings change.
"""
import pathlib

from PIL import Image, ImageDraw

ORANGE = (236, 103, 44)
WHITE = (255, 255, 255)
SIZE = 800
ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"

# (stem, tile px, agent tile (col, row), room rect in tiles (c0, r0, c1, r1))
VIEWS = [
    # the room runs off the right and bottom of an 8x8 window, so the box is clipped
    ("cam-follow", 100, (3, 1), (1, 1, 8, 8)),
    ("cam-room", 80, (3, 1), (1, 1, 9, 9)),
    # same room box, but only the forward wedge of it is lit
    ("cam-cone", 80, (3, 1), (1, 1, 9, 9)),
]


def _dashed_rect(draw, box, color, width=4, dash=16, gap=11):
    x0, y0, x1, y1 = box

    def run(a, b, horizontal, fixed):
        pos = a
        while pos < b:
            end = min(pos + dash, b)
            line = [(pos, fixed), (end, fixed)] if horizontal else [(fixed, pos), (fixed, end)]
            draw.line(line, fill=color, width=width)
            pos = end + gap

    run(x0, x1, True, y0)
    run(x0, x1, True, y1)
    run(y0, y1, False, x0)
    run(y0, y1, False, x1)


def annotate(stem, tile, agent_tile, room_tiles):
    image = Image.open(ASSETS / f"{stem}-live.png").convert("RGB")
    draw = ImageDraw.Draw(image)

    c0, r0, c1, r1 = room_tiles
    box = (
        c0 * tile + 3,
        r0 * tile + 3,
        min(c1 * tile, SIZE) - 3,
        min(r1 * tile, SIZE) - 3,
    )
    _dashed_rect(draw, box, ORANGE, width=5, dash=20, gap=13)

    col, row = agent_tile
    cx, cy = col * tile + tile / 2, row * tile + tile / 2
    radius = tile * 0.54
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline=WHITE, width=6)

    out = ASSETS / f"{stem}-annot.png"
    image.save(out)
    print(f"wrote {out.name}")


if __name__ == "__main__":
    for stem, tile, agent, room in VIEWS:
        annotate(stem, tile, agent, room)
