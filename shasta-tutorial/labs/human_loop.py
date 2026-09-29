"""A human in the loop, without the GUI: drive SHaSTA through SwarmCommander.

    python labs/human_loop.py

`shasta gui` is a thin window on top of `SwarmCommander`, which has no display
dependency. Anything that can call its methods can be the "human": a scripted
operator (this file), an AI advisor, or your own interface (a web page, a
joystick, VR). Replace `operator()` with your own decision-maker.
"""

from shasta.actors import UAV, UGV
from shasta.config import load_config
from shasta.env import ShastaEnv
from shasta.experiments import GoToNodeExperiment
from shasta.interaction import Mission, SwarmCommander

# --- EDIT ME --------------------------------------------------------------
MAP_NAME = "buffalo-small"
N_TARGETS = 2
SEED = 0                     # same seed, same target nodes every run
MAX_STEPS = 5000
HEADLESS = True              # False shows the pybullet 3D window (still no GUI panel)
# ---------------------------------------------------------------------------

config = load_config(headless=HEADLESS)
config["experiment"] = {"map_to_use": MAP_NAME, "type": GoToNodeExperiment}

groups = {0: [UAV() for _ in range(4)], 1: [UGV() for _ in range(3)]}
env = ShastaEnv(config, groups)
commander = SwarmCommander(env, Mission.random(env.core.get_map(), N_TARGETS, seed=SEED))


def operator(commander):
    """The decision-maker. Here: send each group to a different target, once."""
    targets = commander.mission.targets
    for i, group_id in enumerate(commander.groups):
        commander.send(group_id, targets[i % len(targets)])


operator(commander)          # <- the human's orders

while not commander.mission.is_over(commander.step_count) and commander.step_count < MAX_STEPS:
    commander.update()       # advance the swarm one tick

for step, text in commander.events:
    print(f"step {step:4d}  {text}")
print(f"score: {commander.mission.score}/{len(commander.mission.targets)} targets")
env.close()
