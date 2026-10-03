"""Figures drawn by running the tutorial notebook's own cells, so the slides show exactly what the notebook shows.

    SHASTA_REPO=<checkout of the SHaSTA repository> python tools/capture_notebook_figures.py

Runs `notebooks/01_shasta_hsi.ipynb` in a temporary copy of that folder (nothing is written to the checkout), plays a short session by sending
simulated mouse clicks to the interface, and writes to assets/:
    map-graph.png      Step 1: the street graph with numbered intersections
    world-3d.png       Step 3: the PyBullet world rendered in 3D, with the groups and their orders
    gaze-timeline.png  Step 8: gaze over time, with the operator's orders
    gaze-heatmap.png   Step 8: where the (synthetic) gaze went, and its fixations
    bellevue-map.png   Step 4: the interface on a map built from OpenStreetMap (needs Java and the network)

Needs the notebook's dependencies (shasta[gui], pylsl, pyxdf, matplotlib, pandas, ipywidgets, ipyevents) and runs headless.
"""
import contextlib
import io
import json
import os
import pathlib
import shutil
import sys
import tempfile
import time

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("MPLBACKEND", "Agg")

REPO = pathlib.Path(os.environ.get("SHASTA_REPO", "../shasta-ub")).resolve()
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"
if not (REPO / "notebooks" / "01_shasta_hsi.ipynb").exists():
    sys.exit(f"No notebook found under SHASTA_REPO={REPO}")

work = pathlib.Path(tempfile.mkdtemp(prefix="shasta-figures-"))
shutil.copytree(REPO / "notebooks", work, dirs_exist_ok=True)
os.chdir(work)
sys.path.insert(0, str(work))

cells = {c["id"]: "".join(c["source"]) for c in json.load(open("01_shasta_hsi.ipynb"))["cells"] if c["cell_type"] == "code"}
ns = {"__name__": "__main__", "display": lambda x: None}


def run(cell_id):
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(cells[cell_id], cell_id, "exec"), ns)


import live_play as live  # noqa: E402

captured = {}
original_play = live.play_shasta


def spy(gui, **kwargs):
    captured["gui"] = gui
    return original_play(gui, **kwargs)


live.play_shasta = spy

import world_view as _world_view  # noqa: E402

world_view_holder = {}
_original_world_run = _world_view.WorldView.run


def _spy_world_run(self):
    world_view_holder["view"] = self
    return _original_world_run(self)


_world_view.WorldView.run = _spy_world_run


def browser(gui, kind, native_xy=None, **extra):
    """An event as ipyevents delivers it: the position is in the picture as it is shown (800 px wide)."""
    shown = 800
    k = shown / gui.size[0]
    event = {"event": kind, "shiftKey": False, "ctrlKey": False, "altKey": False, "metaKey": False}
    if native_xy is not None:
        event.update(relativeX=native_xy[0] * k, relativeY=native_xy[1] * k, boundingRectWidth=shown,
                     boundingRectHeight=shown * gui.size[1] / gui.size[0])
    event.update(extra)
    return event


def play(orders=3):
    """Click a group's marker, a street node, and Enter, `orders` times, then press Stop."""
    time.sleep(1.5)
    session, gui = live._session, captured["gui"]
    commander = gui.commander
    nodes = list(commander.map.get_node_graph().nodes)

    def click(xy):
        session.on_mouse(browser(gui, "mousedown", xy, button=0))
        time.sleep(0.1)
        session.on_mouse(browser(gui, "mouseup", xy, button=0))
        time.sleep(0.25)

    for i in range(orders):
        group = i % len(commander.groups)
        click(tuple(int(v) for v in gui.view.to_screen(commander.status(group)["centroid"])[0]))
        click(tuple(int(v) for v in gui.view.to_screen(commander.map.get_cartesian_node_position(nodes[10 + 15 * i])[:2])[0]))
        session.on_key({"event": "keydown", "key": "Enter"})
        time.sleep(1.2)
    time.sleep(2.0)
    session.stop()
    time.sleep(1.0)


def capture_world():
    """Click the ground in the 3D view to order the selected group, wait for it to move, and save the frame."""
    import numpy as np
    from PIL import Image
    import world_view
    time.sleep(2.0)
    session = live._session
    view = world_view_holder["view"]
    width, height = view.size
    k = 800 / width
    matrix = view._view()
    visible = [n for n in view.nodes if (q := view.project(np.append(view.nodes[n], 0.0), matrix)) and 120 < q[0] < width - 120 and 120 < q[1] < height - 120]
    node = visible[len(visible) // 2]
    pixel = view.project(np.append(view.nodes[node], 0.0), matrix)
    for kind in ("mousedown", "mouseup"):
        session.on_mouse({"event": kind, "button": 0, "relativeX": pixel[0] * k, "relativeY": pixel[1] * k, "boundingRectWidth": 800,
                          "boundingRectHeight": 800 * height / width})
        time.sleep(0.15)
    time.sleep(3.0)
    Image.fromarray(session._frame).save(OUT / "world-3d.png")
    print("world-3d.png")
    session.stop()
    time.sleep(0.8)


def save(name, dpi=130):
    import matplotlib.pyplot as plt
    figure = plt.gcf()
    figure.patch.set_facecolor("#252525")
    for axis in figure.axes:
        axis.set_facecolor("#252525")
        axis.title.set_color("white")
        axis.xaxis.label.set_color("white")
        axis.yaxis.label.set_color("white")
        axis.tick_params(colors="white")
        for spine in axis.spines.values():
            spine.set_color("#888888")
        legend = axis.get_legend()
        if legend:
            legend.get_frame().set_facecolor("#333333")
            for text in legend.get_texts():
                text.set_color("white")
    figure.savefig(OUT / name, dpi=dpi, bbox_inches="tight", facecolor="#252525")
    plt.close("all")
    print(name)


if __name__ == "__main__":
    for cell_id in ("c002",):
        run(cell_id)
    open(os.environ["LSLAPICFG"], "a").write("\n[lab]\nKnownPeers = {127.0.0.1}\n")      # several LSL streams on one machine
    for cell_id in ("s1_map", "s1_plot"):
        run(cell_id)
    save("map-graph.png")
    for cell_id in ("s1_cfg", "s2_env", "s3_play"):
        run(cell_id)
        if cell_id == "s3_play":
            play(orders=1)
    run("s3_world")
    capture_world()
    for cell_id in ("s4_map", "s4_map_play"):                     # builds the map of downtown Bellevue, then plays on it
        run(cell_id)
    play(orders=2)
    from PIL import Image
    Image.fromarray(live._session._frame).save(OUT / "bellevue-map.png")
    print("bellevue-map.png")
    for cell_id in ("s7_setup", "s7_play"):
        run(cell_id)
    play(orders=4)
    for cell_id in ("s8_load", "s8_tables", "s8_time"):
        run(cell_id)
    save("gaze-timeline.png")
    for cell_id in ("s8_where",):
        run(cell_id)
    save("gaze-heatmap.png")
    shutil.rmtree(work, ignore_errors=True)
