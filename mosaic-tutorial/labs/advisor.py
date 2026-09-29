"""Plug your own AI teammate into MOSAIC.

    python labs/advisor.py

A teammate is anything with `query(prompt) -> str`. That means the quality,
timing, and correctness of AI advice is an experimental variable you control
in a few lines of Python, with no changes to the environment.

ReliableTeammate is grounded in the real game state: it points the participant
at the nearest survivor they can actually reach. With probability
1 - reliability it points at the nearest decoy instead, so reliability is a
single number you can vary across trials to study trust and reliance.

It needs the whole observation rather than MOSAIC's text prompt, so pass
`prompt_builder=json.dumps` and the GUI hands it the observation as JSON.
"""
import json
import random

from mosaic.llm.client import LLMClient, ask
from mosaic.llm.pathfinding import query_all_objects
from mosaic.sar.observations import FAKE_VICTIM, VICTIM


def describe(obs, x, y, steps):
    """Radio-style sentence pointing the participant at tile (x, y)."""
    if steps == 0:
        return "There is a survivor right next to you."
    dx, dy = x - obs["agent_x"], y - obs["agent_y"]
    ns = "south" if dy > 0 else "north" if dy < 0 else ""
    ew = "east" if dx > 0 else "west" if dx < 0 else ""
    heading = "-".join(filter(None, [ns, ew]))
    unit = "step" if steps == 1 else "steps"
    return f"Survivor to the {heading}, about {steps} {unit} away."


class ReliableTeammate(LLMClient):
    """Points to the nearest reachable survivor — or, with probability
    1 - reliability, to the nearest decoy instead."""

    def __init__(self, reliability=0.8, seed=None):
        self.reliability = reliability
        self.rng = random.Random(seed)
        self.log = []  # one row per piece of advice, for analysis

    def query(self, prompt):
        obs = json.loads(prompt)  # prompt_builder=json.dumps
        honest = self.rng.random() < self.reliability
        target = VICTIM if honest else FAKE_VICTIM
        options = [(p.path_length, x, y)
                   for (x, y), p in query_all_objects(obs).items()
                   if p.reachable and obs["grid"][y][x] == target]
        if not options:
            return "No survivor in reach. Try the next room."
        steps, x, y = min(options)
        self.log.append({"honest": honest, "target": (x, y), "steps": steps})
        return describe(obs, x, y, steps)


if __name__ == "__main__":
    from mosaic.sar.env import build_sar_env
    from mosaic.sar.placers import VictimPlacer

    env = build_sar_env(screen_size=600, num_rows=2, num_cols=2, room_size=8,
                        victim_placer=VictimPlacer(num_real_victims=2))
    obs, _ = env.reset(seed=0)

    teammate = ReliableTeammate(reliability=0.7, seed=42)
    for _ in range(5):
        obs, reward, terminated, truncated, info = env.step(2)   # 2 = move forward
        print(ask(obs, teammate, prompt_builder=json.dumps))

    n_ok = sum(a["honest"] for a in teammate.log)
    print(f"\n{n_ok}/{len(teammate.log)} pieces of advice pointed at a real survivor")

    # To use it in the live game instead:
    #   from mosaic.gui.main import SAREnvGUI
    #   SAREnvGUI(env, config={"fullscreen": False},
    #             llm_client=teammate, prompt_builder=json.dumps).run()
