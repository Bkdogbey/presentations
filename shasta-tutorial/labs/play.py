"""A minimal SHaSTA mission — run it, then edit the block below and run it again.

    python labs/play.py

Everything you're likely to want to change first lives in the EDIT ME block.
"""

import numpy as np

from shasta.actors import UAV, UGV
from shasta.config import load_config
from shasta.env import ShastaEnv
from shasta.experiments import GoToNodeExperiment

# --- EDIT ME --------------------------------------------------------------
MAP_NAME = "buffalo-small"   # `shasta maps` lists what's available
N_UAVS = 4                   # group 0: aerial vehicles
N_UGVS = 3                   # group 1: ground vehicles
TARGET_NODE = 5              # a map-graph node index (see the note below)
HEADLESS = True              # False opens the 3D pybullet window
# ---------------------------------------------------------------------------

config = load_config(headless=HEADLESS)
config["experiment"]["type"] = GoToNodeExperiment
config["experiment"]["map_to_use"] = MAP_NAME

groups = {
    0: [UAV() for _ in range(N_UAVS)],
    1: [UGV() for _ in range(N_UGVS)],
}

env = ShastaEnv(config, groups)
obs, info = env.reset()

# Map nodes are intersections of the OpenStreetMap street graph. Pick one from
# the graph itself rather than guessing an index, so this always targets a
# real node regardless of which map you set above:
node_ids = list(env.core.get_map().get_node_graph().nodes)
target = TARGET_NODE if TARGET_NODE in node_ids else node_ids[len(node_ids) // 2]

print(f"Sending {N_UAVS} UAVs and {N_UGVS} UGVs on {MAP_NAME} to node {target}...")
obs, reward, terminated, truncated, info = env.step({0: target, 1: target})

step = 0
while not terminated and step < 5000:
    obs, reward, terminated, truncated, info = env.step(None)
    step += 1
    if step % 100 == 0:
        centroids = {g: np.round(np.mean(v, axis=0)[:2], 1).tolist() for g, v in obs.items()}
        print(f"  step {step:4d}  centroids {centroids}")

print("Reached the target." if terminated else "Did not reach the target in time — try a different node.")
env.close()
