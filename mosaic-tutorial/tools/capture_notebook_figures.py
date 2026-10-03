"""Figures drawn by running the tutorial notebook's own cells, so the slides show exactly what the notebook shows.

    MOSAIC_REPO=<checkout of iHuman-Lab/mosaic> python tools/capture_notebook_figures.py

Writes to assets/results/:
    customize-gallery.png   Step 5: five levels, each changing one setting
    teammate-placeholder.png, teammate-sparse.png, teammate-detailed.png
                            Step 6: the chat panel after one `Q`, for the placeholder
                            teammate and for the stand-in teammate under each prompt type

Needs the notebook's dependencies (mosaic, matplotlib, pygame-ce, pygame_gui) and runs headless through SDL's dummy driver.
"""
import contextlib
import io
import json
import os
import pathlib
import sys
import time

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("MPLBACKEND", "Agg")

REPO = pathlib.Path(os.environ.get("MOSAIC_REPO", pathlib.Path(__file__).resolve().parents[3] / "mosaic"))
NOTEBOOK = REPO / "notebooks" / "02_mosaic_human_ai.ipynb"
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "results"

cells = {c["id"]: "".join(c["source"]) for c in json.loads(NOTEBOOK.read_text())["cells"]}
os.chdir(NOTEBOOK.parent)                       # the notebook reads config.yaml from its own folder
sys.path.insert(0, str(NOTEBOOK.parent))

ns = {"display": lambda *args, **kwargs: None}


def run(cell_id):
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(cells[cell_id], cell_id, "exec"), ns)


# the notebook's setup, config, helpers, our own placer, and the two prompt cells
for cell_id in ("c002", "c008", "c037", "cust_setup", "llm_prompt", "llm_client"):
    run(cell_id)

import numpy as np  # noqa: E402
import pygame  # noqa: E402
from mosaic.sar.env import build_sar_env  # noqa: E402

OUT.mkdir(exist_ok=True)


def gallery():
    """Step 5's five levels, redrawn larger for a slide: the notebook cell defines `variants` and `make_level`."""
    plt = ns["plt"]
    plt.rcParams.update({"text.color": "white", "axes.titlecolor": "white"})      # the slides are dark
    run("cust_gallery")
    plt.close("all")
    O, variants = ns["O"], ns["variants"]
    fig, axes = plt.subplots(1, len(variants), figsize=(14, 3.9))
    for ax, (title, changes) in zip(axes, variants.items()):
        env = ns["make_level"](**changes, seed=0)
        obs, _ = env.reset(seed=0)
        grid = np.array(obs["grid"])
        env.switch_camera(ns["FullviewCamera"]())                                  # the whole building
        ax.imshow(env.render()); ax.axis("off")
        ax.set_title(f"{title}\n{(grid == O.VICTIM).sum()} victims · {(grid == O.FAKE_VICTIM).sum()} decoys\n"
                     f"{(grid == O.LAVA).sum()} lava · {env.max_steps} steps", fontsize=13, linespacing=1.4)
    plt.tight_layout()
    plt.savefig(OUT / "customize-gallery.png", dpi=130, bbox_inches="tight", facecolor="#252525")
    plt.close("all")
    print("customize-gallery.png")


class Clock:
    """pygame.time.get_ticks stand-in that we advance by hand: the chat panel blinks when a reply arrives."""
    ms = 0

    def __call__(self):
        return self.ms


def chat(name, client, prompt_type):
    """The chat panel after one `Q`, rendered at twice the size so the text stays sharp on a slide."""
    clock = Clock()
    pygame.time.get_ticks = clock
    size = 1280
    ns["random"].seed(7)
    env = build_sar_env(screen_size=size, num_rows=2, num_cols=2, room_size=8,
                        victim_placer=ns["VictimsAndDecoys"](2, 2), lava_placer=ns["LavaPlacer"](lava_per_room=1),
                        locked_room_placer=ns["LockedRoomPlacer"](0.35), camera_strategy=ns["AgentFOVCamera"]())
    gui = ns["SAREnvGUI"](env, config={"fullscreen": False, "prompt_type": prompt_type}, llm_client=client)
    gui.user.obs, _ = env.reset(seed=7)
    gui.user.ask_llm_async()                    # what pressing Q does
    while gui.user.llm_thread is not None and gui.user.llm_thread.is_alive():
        time.sleep(0.05)
    gui.chat_panel.poll_llm(gui.user)
    clock.ms += 5000                            # past the arrival blink
    gui.chat_panel.poll_llm(gui.user)
    surface = gui._build_combined_surface(env.render())
    image = np.asarray(pygame.surfarray.array3d(surface)).swapaxes(0, 1)
    from PIL import Image
    x0, y0 = gui.game_size, gui.game_size // 2
    panel = Image.fromarray(image).crop((x0, y0 + 58, x0 + gui.panel_width, y0 + 250))      # just the message box
    panel.save(OUT / f"{name}.png")
    print(f"{name}.png  reply: {gui.user.last_llm_response!r}")


if __name__ == "__main__":
    gallery()
    chat("teammate-placeholder", ns["DummyLLMClient"](), "sparse")
    chat("teammate-sparse", ns["StandInTeammate"](), "sparse")
    chat("teammate-detailed", ns["StandInTeammate"](), "detailed")
    pygame.quit()
