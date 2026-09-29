"""Time-stamp the operator's actions with Lab Streaming Layer (LSL).

    pip install pylsl
    python labs/lsl_markers.py

The released `ihuman-shasta` package does not ship LSL support yet. This file
shows the pattern: after every `commander.update()`, forward the new
`SwarmCommander` events to an LSL marker stream. Any LSL recorder (LabRecorder)
then stores them next to EEG, eye tracking or any other stream on one clock.

To see it work without a recorder, this script also opens an LSL inlet on the
same stream and prints what arrives.
"""

import time

from pylsl import StreamInfo, StreamInlet, StreamOutlet, local_clock, resolve_byprop

from shasta.actors import UAV, UGV
from shasta.config import load_config
from shasta.env import ShastaEnv
from shasta.experiments import GoToNodeExperiment
from shasta.interaction import Mission, SwarmCommander

# --- 1. The marker stream: irregular rate, one string channel -------------------
info = StreamInfo(name="ShastaEvents", type="Markers", channel_count=1,
                  nominal_srate=0, channel_format="string", source_id="shasta-demo")
outlet = StreamOutlet(info)

# (Demo only: a recorder normally does this. We listen to our own stream.)
inlet = StreamInlet(resolve_byprop("name", "ShastaEvents", timeout=5)[0])
inlet.open_stream(timeout=5)     # connect now: LSL only delivers to connected consumers

# --- 2. The same headless setup as human_loop.py --------------------------------
config = load_config(headless=True)
config["experiment"] = {"map_to_use": "buffalo-small", "type": GoToNodeExperiment}
groups = {0: [UAV() for _ in range(4)], 1: [UGV() for _ in range(3)]}
env = ShastaEnv(config, groups)
commander = SwarmCommander(env, Mission.random(env.core.get_map(), 2, seed=0))

# --- 3. Forward every new event to LSL as it happens ----------------------------
sent = 0


def flush_events():
    global sent
    for _, text in commander.events[sent:]:
        outlet.push_sample([text])           # timestamped by LSL's clock
    sent = len(commander.events)


targets = commander.mission.targets
for i, group_id in enumerate(commander.groups):
    commander.send(group_id, targets[i % len(targets)])   # the operator's orders
flush_events()

while not commander.mission.is_over(commander.step_count) and commander.step_count < 5000:
    commander.update()
    flush_events()
env.close()

# --- 4. What a recorder would see -----------------------------------------------
time.sleep(0.5)
print(f"{'LSL time (s)':>14}  event")
while True:
    sample, stamp = inlet.pull_sample(timeout=0.2)
    if sample is None:
        break
    print(f"{stamp:14.3f}  {sample[0]}")
print(f"(now: {local_clock():.3f})")
inlet.close_stream()
