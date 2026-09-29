# Setup — Before the SHaSTA Tutorial

Send this to registrants at least a few days ahead. Doing this in advance means the session starts with a working install instead of everyone debugging `pip` together.

## Requirements

- Python 3.9 or newer
- `git`
- About 10 minutes and a stable connection (the install pulls the SHaSTA map assets, which include some multi-MB city maps)

## Install

The PyPI package (`ihuman-shasta`) is not published yet, so install from a clone:

```bash
git clone <the shasta-ub repository URL>
cd shasta-ub
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[gui]"
```

`[gui]` adds the human interface (`shasta gui`) on top of the core simulator.

## Verify it worked

```bash
shasta maps
shasta demo
```

`shasta maps` should print a list of city names (`buffalo-small`, `chicago`, `new-york`, ...). `shasta demo` should print a series of `step ... centroids ...` lines and end with `All groups reached their targets after N steps.` — no window opens for this one.

Then try the interface itself:

```bash
shasta gui
```

A top-down map should open with a handful of blue and red markers on it. If it does, you're ready for the session — close it and see you there.

## If something goes wrong

- **`pip install` fails looking for `ihuman-shasta` on PyPI** — you're not installing from the clone; re-check you ran `pip install -e ".[gui]"` from inside the cloned `shasta-ub` directory (the `-e .` matters — it means "this local directory").
- **`shasta: command not found`** after install — make sure the virtual environment is activated (`source .venv/bin/activate`) in the same terminal you're running `shasta` from.
- **`shasta gui` doesn't open a window / errors about a display** — this needs a real display (not a pure SSH session without X forwarding, and not most cloud notebooks). If you're on such a setup, the headless commands (`shasta maps`, `shasta demo`, and the Python API) still work; message the organizers before the session so Part 3 can be adjusted for you.
- Anything else — bring it to the session; "my install is broken in a new way" is itself useful material for a hands-on tutorial.
