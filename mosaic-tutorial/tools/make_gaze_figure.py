"""Draw the Synchronized Record figure from an eye-tracking demo recording.

    python tools/make_gaze_figure.py path/to/recording.xdf
    python tools/make_gaze_figure.py recording.xdf --screen 2560x1440

The recording is the LabRecorder file from the slide 37 demo (see
EYETRACKER_SETUP.md): gaze and game state on one clock. The figure shows where
the fixations fell on the screen's three areas, and one timeline with the
victims saved and the area the gaze was in. Writes
assets/results/gaze-record.png in the deck's dark style.

Reads the file with the notebook's own helpers (notebooks/lsl_tools.py in the
MOSAIC checkout at MOSAIC_SRC), so the numbers match notebook Step 8. Needs
matplotlib, scipy and pyxdf, not the game.
"""
import argparse
import os
import pathlib
import sys

# Set MOSAIC_SRC to point at another checkout (e.g. on Windows).
MOSAIC_SRC = os.environ.get("MOSAIC_SRC", "/home/bennett/Research/mosaic/src")
sys.path.insert(0, str(pathlib.Path(MOSAIC_SRC).parent / "notebooks"))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from lsl_tools import detect_fixations, gaze_area, load_streams, study_tables  # noqa: E402

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"

# The deck's surface and ink, and one colour per screen area (checked for
# colour-blind separation and contrast on this surface).
SURFACE, PANEL, HAIRLINE = "#252525", "#2e2e2e", "#4a4a4a"
INK, INK_2, MUTED = "#ffffff", "#c3c2b7", "#898781"
AREA = {"game": "#3987e5", "info": "#d95926", "chat": "#199e70"}
AREA_LABEL = {"game": "game view", "info": "info panel", "chat": "chat"}
ELSEWHERE = "#898781"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("xdf", type=pathlib.Path, help="LabRecorder file from the eye-tracking demo")
    parser.add_argument("--screen", default="1920x1080", help="size of the screen it was played on, in pixels")
    parser.add_argument("--out", type=pathlib.Path, default=ASSETS / "results" / "gaze-record.png")
    args = parser.parse_args()
    screen = tuple(int(v) for v in args.screen.lower().split("x"))

    gaze, rows = study_tables(load_streams(str(args.xdf)), screen)
    t0 = min(gaze["t"][0], rows[0]["t"])
    t = gaze["t"] - t0
    aois = rows[0]["aois"]
    states = pd.DataFrame([r for r in rows if r["event"] == "state"])
    states["t"] -= t0
    rescues = [r["t"] - t0 for r in rows if r["event"] == "rescue"]
    area = gaze_area(gaze, aois)
    valid = gaze["valid"]
    share = {name: float((area[valid] == name).mean()) for name in AREA}
    fixations = detect_fixations(gaze["t"], gaze["x"], gaze["y"])
    end = max(t[-1], states["t"].iloc[-1])

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "text.color": INK_2,
                         "axes.edgecolor": HAIRLINE, "axes.labelcolor": MUTED,
                         "xtick.color": MUTED, "ytick.color": MUTED, "axes.linewidth": 0.8})
    # Shown about 590 px wide on the slide, so type is set large: 11 pt here is about 14 px there.
    fig = plt.figure(figsize=(6.3, 3.7), dpi=200, facecolor=SURFACE)
    grid = fig.add_gridspec(3, 2, height_ratios=[2.2, 0.62, 0.24], width_ratios=[2.05, 1],
                            left=0.075, right=0.99, top=0.985, bottom=0.15, hspace=0.32, wspace=0.04)

    # Where the fixations fell on the screen.
    ax = fig.add_subplot(grid[0, 0])
    ax.set_facecolor(SURFACE)
    ax.add_patch(plt.Rectangle((0, 0), *screen, facecolor="#1c1c1c", edgecolor=HAIRLINE, linewidth=0.8))
    for name, (left, top, width, height) in aois.items():
        ax.add_patch(plt.Rectangle((left, top), width, height, facecolor=PANEL, edgecolor=HAIRLINE, linewidth=0.8))
        ax.text(left + 0.02 * screen[0], top + 0.035 * screen[1], AREA_LABEL[name], va="top", fontsize=10, color=INK_2)
    for f in fixations:
        name = next((n for n, (l, tp, w, h) in aois.items() if l <= f["x"] < l + w and tp <= f["y"] < tp + h), None)
        ax.scatter(f["x"], f["y"], s=26 + 260 * (f["end"] - f["start"]), color=AREA.get(name, ELSEWHERE),
                   alpha=0.8, edgecolors=PANEL, linewidths=1.0, zorder=3)
    ax.set_xlim(0, screen[0]); ax.set_ylim(screen[1], 0); ax.set_aspect("equal"); ax.axis("off")

    # Share of gaze per area: the legend, with the numbers.
    ax = fig.add_subplot(grid[0, 1]); ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.text(0.06, 0.94, "share of gaze", fontsize=10, color=MUTED, va="center")
    for row, name in enumerate(AREA):
        y = 0.76 - 0.19 * row
        ax.scatter(0.10, y, s=80, color=AREA[name], edgecolors=SURFACE, linewidths=1.0)
        ax.text(0.19, y, AREA_LABEL[name], fontsize=11, color=INK_2, va="center")
        ax.text(1.0, y, f"{share[name]:.0%}", fontsize=14, color=INK, va="center", ha="right", fontweight="bold")
    ax.text(0.06, 0.13, f"{len(fixations)} fixations\nbigger = longer", fontsize=10, color=MUTED, va="center", linespacing=1.4)

    # One clock: victims saved, and under it the area the gaze was in.
    ax = fig.add_subplot(grid[1, :]); ax.set_facecolor(SURFACE)
    steps_t = np.append(states["t"].to_numpy(), end)
    steps_v = np.append(states["saved_victims"].to_numpy(), states["saved_victims"].iloc[-1])
    ax.plot(steps_t, steps_v, drawstyle="steps-post", color=INK, linewidth=2, solid_capstyle="round")
    for when in rescues:
        ax.axvline(when, color=HAIRLINE, linewidth=0.8, zorder=1)
        saved = states.loc[states["t"] <= when + 1e-6, "saved_victims"].iloc[-1]
        ax.scatter(when, saved, s=34, color=INK, edgecolors=SURFACE, linewidths=1.2, zorder=4)
    ax.set_xlim(0, end); ax.set_ylim(-0.3, max(steps_v.max(), 1) + 0.45)
    ax.yaxis.get_major_locator().set_params(integer=True)
    ax.text(0.008, 0.97, "victims saved", transform=ax.transAxes, fontsize=10, color=MUTED, va="top")
    ax.tick_params(labelbottom=False, length=0, labelsize=10)
    ax.grid(axis="y", color="#383838", linewidth=0.8); ax.set_axisbelow(True)
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)

    strip = fig.add_subplot(grid[2, :], sharex=ax); strip.set_facecolor("#1c1c1c")
    for name, color in {**AREA, "elsewhere": ELSEWHERE}.items():
        strip.fill_between(t, 0, 1, where=(area == name), step="post", color=color, linewidth=0)
    for when in rescues:
        strip.axvline(when, color=INK, linewidth=0.8, zorder=3)
    strip.set_ylim(0, 1); strip.set_yticks([]); strip.set_ylabel("gaze", fontsize=10, rotation=0, ha="right", va="center")
    strip.set_xlabel("seconds  ·  gaps = eyes not tracked", fontsize=10); strip.tick_params(length=2, labelsize=10)
    for side in ("top", "right", "left"):
        strip.spines[side].set_visible(False)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, facecolor=SURFACE)
    print(f"wrote {args.out.name}  {end:.0f} s, {len(rescues)} rescues, valid gaze {valid.mean():.0%}, "
          + ", ".join(f"{AREA_LABEL[n]} {share[n]:.0%}" for n in AREA))


if __name__ == "__main__":
    main()
