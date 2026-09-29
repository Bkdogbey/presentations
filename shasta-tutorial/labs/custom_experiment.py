"""A minimal custom experiment — the four methods every experiment needs.

Run it with:

    python labs/custom_experiment.py

`GoToNodeExperiment` (shasta/experiments.py) does the same job in about 40
lines and is worth reading once you're past this. This file exists to show
the smallest possible version: one group, one fixed direction, done when a
step counter runs out. Swap in your own `apply_actions` / `get_done_status` /
`compute_reward` for your own task.
"""

import numpy as np
from gymnasium import spaces

from shasta.actors import UAV
from shasta.base_experiment import BaseExperiment
from shasta.config import load_config
from shasta.env import ShastaEnv


class FlyNorthExperiment(BaseExperiment):
    """Every actor in every group flies north at a fixed speed for N steps."""

    max_steps = 300
    speed = 2.0  # meters/step

    def __init__(self, config, core, experiment_config=None, *args, **kwargs):
        super().__init__(config, core, experiment_config, *args, **kwargs)
        self.step_count = 0

    def get_action_space(self):
        return spaces.Discrete(1)  # unused — this experiment ignores actions

    def get_observation_space(self):
        return spaces.Box(-np.inf, np.inf, shape=(3,), dtype=np.float64)

    def apply_actions(self, actions, core):
        self.step_count += 1
        for group_id in core.get_actor_groups():
            for actor in core.get_actors_by_group_id(group_id):
                pos, _ = actor.get_pos_and_orientation()
                actor.apply_action(pos + np.array([0, self.speed, 0]))

    def get_observation(self, observation, core):
        return {g: np.asarray(v) for g, v in observation.items()}, {}

    def get_done_status(self, observation, core):
        return self.step_count >= self.max_steps

    def compute_reward(self, observation, core):
        return 0.0


if __name__ == "__main__":
    config = load_config(headless=True)
    config["experiment"]["type"] = FlyNorthExperiment

    groups = {0: [UAV() for _ in range(3)]}
    env = ShastaEnv(config, groups)
    obs, info = env.reset()
    print("start centroid:", np.mean(obs[0], axis=0).round(1).tolist())

    terminated = False
    while not terminated:
        obs, reward, terminated, truncated, info = env.step(None)

    print("end centroid:  ", np.mean(obs[0], axis=0).round(1).tolist())
    env.close()
