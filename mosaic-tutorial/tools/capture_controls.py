"""Record the four looping clips on the Controls slide, plus the chat still used
on the Runtime Architecture slide.

    python tools/capture_controls.py

Each clip isolates one control. The keys it uses are drawn as a keycap strip
along the bottom of the frame, and the key lights up on the frame it is pressed.

- controls-navigate.gif   arrow keys walking and turning inside one room
- controls-open.gif       Space on a closed door
- controls-pickup.gif     Tab on a key, then Tab on a real victim (green flash)
- controls-advice.gif     Alt: the chat panel shows "thinking", then the reply
- chat-advice.png         the chat panel holding that reply

The teammate is ReliableTeammate from labs/advisor.py, the class the "Customize
the AI teammate" slide shows, so the reply is what that code actually says about
this building. It is wrapped with a short delay only so the GUI's real
"thinking..." state is visible, as it would be while a hosted model answers.

Each clip searches seeds until its situation occurs in the starting room (a
closed door within reach, a key next to a victim, ...). Level generation is not
bit-reproducible, so the chosen seed is printed rather than fixed.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "labs"))
from _capture_common import (  # noqa: E402
    ASSETS, GAME, VICTIM, FrozenClock, build_study_env, door_state, is_door, is_key,
    keycap_strip, passable, save_gif, surface_to_image, turns_to, walk_to, DIRS,
)

import random  # noqa: E402

import pygame  # noqa: E402
from advisor import ReliableTeammate  # noqa: E402
from minigrid.core.actions import Actions  # noqa: E402
from mosaic.gui.feedback import EdgeVignette  # noqa: E402
from mosaic.gui.main import SAREnvGUI  # noqa: E402
from PIL import Image  # noqa: E402

OUT_PX = 320             # edge of the square world clips
PRESS_MS = 420           # frame with the key lit
STEP_MS = 260            # an unlit walking frame
HOLD_MS = 1100           # still frame so the result reads
FLASH_TICK_MS, FLASH_SHOW_MS = 50, 100   # vignette at half speed, as in gameplay.gif
ARROW = {Actions.left: "←", Actions.forward: "↑", Actions.right: "→"}
# Chat panel region of the 1200x800 compositor output: panel title and the
# first lines of the reply.
CHAT_BOX = (800, 400, 1200, 610)


class SlowTeammate(ReliableTeammate):
    """ReliableTeammate with a hosted model's latency."""

    def query(self, prompt):
        time.sleep(1.3)
        return super().query(prompt)


class Recorder:
    """One mission, one GUI, and the frames recorded from it."""

    def __init__(self, seed, teammate=None):
        self.clock = FrozenClock()
        pygame.time.get_ticks = self.clock  # chat panel blink + "thinking" dots
        self.env = build_study_env()
        self.gui = SAREnvGUI(
            self.env, config={"fullscreen": False, "max_time": 5},
            vignette=EdgeVignette(GAME, clock_ms=self.clock),
            llm_client=teammate or ReliableTeammate(reliability=1.0, seed=0),
            prompt_builder=json.dumps,
        )
        random.seed(seed)
        obs, _ = self.env.reset(seed=seed)
        self.gui.user.obs = obs
        self.gui.user.total_reward = 0.0
        self.frames = []           # (full RGB frame, lit key or None, duration ms)
        self.cells = []            # tiles the clip must keep in frame

    @property
    def obs(self):
        return self.gui.user.obs

    def room(self, pos=None):
        return self.env.room_from_pos(*(pos or self.env.agent_pos))

    def grab(self, lit=None, ms=STEP_MS, tick=None):
        self.gui.chat_panel.poll_llm(self.gui.user)
        surface = self.gui._build_combined_surface(self.env.render())
        self.frames.append((surface_to_image(surface), lit, ms))
        self.clock.ms += ms if tick is None else tick
        self.cells.append(tuple(self.env.agent_pos))

    def act(self, action, lit=None, record=True):
        self.gui.user.step(action)
        events = (self.gui.user.last_info or {}).get("events", [])
        if not record:
            return
        if not events:
            self.grab(lit, PRESS_MS if lit else STEP_MS)
            return
        self.gui.vignette.trigger(events)
        flash = max(self.gui.vignette._duration_ms, 1)
        self.grab(lit, FLASH_SHOW_MS, FLASH_TICK_MS)
        for _ in range(flash // FLASH_TICK_MS):
            self.grab(None, FLASH_SHOW_MS, FLASH_TICK_MS)

    def world_clip(self, keys, pad=1, min_tiles=5):
        """Square crop of the game viewport around every recorded cell, scaled
        to OUT_PX, with the keycap strip drawn in."""
        x0, y0, x1, y1 = self.env.camera.get_visible_bounds(self.env.width, self.env.height)
        tile = GAME / (x1 - x0)
        xs = [c[0] for c in self.cells]
        ys = [c[1] for c in self.cells]
        side = max(max(xs) - min(xs), max(ys) - min(ys)) + 1 + 2 * pad
        side = min(max(side, min_tiles), x1 - x0)
        cx, cy = (min(xs) + max(xs) + 1) / 2, (min(ys) + max(ys) + 1) / 2
        bx = min(max(cx - side / 2, x0), x1 - side)
        by = min(max(cy - side / 2, y0), y1 - side)
        box = tuple(int(round(v)) for v in (
            (bx - x0) * tile, (by - y0) * tile, (bx - x0 + side) * tile, (by - y0 + side) * tile))
        frames = [keycap_strip(f.crop(box).resize((OUT_PX, OUT_PX), Image.LANCZOS), keys, lit)
                  for f, lit, _ in self.frames]
        return frames, [ms for *_, ms in self.frames]


def room_paths(obs, room_of):
    """Shortest walkable path from the agent to every floor cell of its room."""
    grid, start = obs["grid"], (obs["agent_x"], obs["agent_y"])
    home = room_of(start)
    paths, frontier = {start: [start]}, [start]
    while frontier:
        nxt = []
        for x, y in frontier:
            for dx, dy in DIRS:
                cell = (x + dx, y + dy)
                if cell in paths or not passable(grid[cell[1]][cell[0]]) or room_of(cell) is not home:
                    continue
                paths[cell] = paths[(x, y)] + [cell]
                nxt.append(cell)
        frontier = nxt
    return paths


def along(obs, path):
    """Turn/forward actions that follow a path of cells."""
    actions, facing = [], obs["agent_dir"]
    for cur, nxt in zip(path, path[1:]):
        want = DIRS.index((nxt[0] - cur[0], nxt[1] - cur[1]))
        actions += turns_to(facing, want)
        actions.append(Actions.forward)
        facing = want
    return actions


def navigate(seed):
    rec = Recorder(seed)
    best = None
    for cell, path in room_paths(rec.obs, rec.room).items():
        acts = along(rec.obs, path)
        if not (6 <= len(acts) <= 9):
            continue
        if Actions.left in acts and Actions.right in acts and acts.count(Actions.forward) >= 3:
            best = acts
            break
    if best is None:
        return None
    rec.grab(None, HOLD_MS)
    for action in best:
        rec.act(action, ARROW[action])
        rec.grab(None, 180)
    rec.grab(None, HOLD_MS)
    return rec.world_clip(["←", "↑", "→"])


def open_door(seed):
    rec = Recorder(seed)
    acts, door = walk_to(rec.obs, lambda c: is_door(c) and door_state(c) == 1)
    if door is None or len(acts) > 14:
        return None
    approach = 3  # record the last few moves so the clip shows the walk up
    for action in acts[:-approach]:
        rec.act(action, record=False)
    home = rec.room()
    rec.grab(None, 700)
    for action in acts[-approach:]:
        rec.act(action)
        if rec.room() is not home:
            return None
    rec.cells.append(door)
    rec.grab(None, 700)
    rec.act(Actions.toggle, "Space")
    rec.grab(None, 900)
    if rec.room(door) is home:  # step into the open doorway if the view stays put
        rec.act(Actions.forward)
    rec.grab(None, HOLD_MS)
    return rec.world_clip(["Space"], min_tiles=5)


def pick_up(seed):
    rec = Recorder(seed)
    acts, key = walk_to(rec.obs, is_key)
    if key is None or len(acts) > 20:
        return None
    for action in acts:
        rec.act(action, record=False)
    home = rec.room()
    rec.cells.append(key)
    rec.grab(None, HOLD_MS)
    rec.act(Actions.pickup, "Tab")
    rec.grab(None, 700)
    acts, victim = walk_to(rec.obs, lambda c: c == VICTIM)
    if victim is None or len(acts) > 7 or rec.room(victim) is not home:
        return None
    for action in acts:
        rec.act(action)
        if rec.room() is not home:
            return None
    rec.cells.append(victim)
    rec.grab(None, 500)
    rec.act(Actions.pickup, "Tab")
    rec.grab(None, HOLD_MS)
    return rec.world_clip(["Tab"])


def advice(seed):
    rec = Recorder(seed, teammate=SlowTeammate(reliability=1.0, seed=0))
    probe = ReliableTeammate(reliability=1.0)
    reply = probe.query(json.dumps(rec.obs))
    if not probe.log or probe.log[0]["steps"] < 2:  # not a victim right beside the agent
        return None
    rec.grab(None, HOLD_MS)
    rec.gui.user.ask_llm_async()                  # what pressing Alt does
    rec.grab("Alt", PRESS_MS, 400)
    while rec.gui.user.llm_thread is not None and rec.gui.user.llm_thread.is_alive():
        rec.grab(None, 400, 400)
        time.sleep(0.4)
    for _ in range(3000 // 200 + 1):              # reply arrives, panel blinks for 3 s
        rec.grab(None, 200, 200)
    rec.grab(None, 1600)
    frames, durations = [], []
    for full, lit, ms in rec.frames:
        chat = full.crop(CHAT_BOX)
        canvas = Image.new("RGB", (chat.width, chat.height + 56), (20, 20, 24))
        canvas.paste(chat, (0, 0))
        frames.append(keycap_strip(canvas, ["Alt"], lit))
        durations.append(ms)
    still = rec.frames[-1][0].crop(CHAT_BOX)
    still.save(ASSETS / "chat-advice.png")
    return frames, durations, reply


def first_working(fn, name, seeds=range(1, 80)):
    for seed in seeds:
        result = fn(seed)
        if result is not None:
            print(f"{name}: seed {seed}")
            return result
    sys.exit(f"{name}: no seed in {seeds} produced the situation")


def main():
    only = sys.argv[1:]  # e.g. `capture_controls.py advice` re-records one clip
    for name, fn in [("controls-navigate", navigate), ("controls-open", open_door),
                     ("controls-pickup", pick_up)]:
        if only and name.split("-")[1] not in only:
            continue
        frames, durations = first_working(fn, name)
        kb = save_gif(ASSETS / f"{name}.gif", frames, durations)
        print(f"  wrote {name}.gif  {len(frames)} frames  {sum(durations) / 1000:.1f} s  {kb:.0f} KB")
    if only and "advice" not in only:
        return
    frames, durations, reply = first_working(advice, "controls-advice")
    kb = save_gif(ASSETS / "controls-advice.gif", frames, durations)
    print(f"  wrote controls-advice.gif  {len(frames)} frames  {kb:.0f} KB  reply: {reply!r}")
    print("  wrote chat-advice.png")
    pygame.quit()


if __name__ == "__main__":
    main()
