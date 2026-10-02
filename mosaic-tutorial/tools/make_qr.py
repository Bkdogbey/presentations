"""Draw the QR codes on the slides.

    python tools/make_qr.py

Writes assets/qr-notebook.png (the tutorial's Jupyter server, where the
companion notebook runs; on the Part Two and Part Four dividers) and
assets/qr-paper.png (the slides of the lab's SMC 2026 paper, on the "MOSAIC in
a Study" slide). Dark squares on white with a quiet border,
because inverted codes scan badly. Needs `segno` (`pip install segno`).
To point a code somewhere else, change its address below and rerun.
"""
import pathlib

import segno

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"
CODES = {
    "qr-notebook.png": "https://jupyter.ihuman-lab.work",
    "qr-paper.png": "https://ihuman-lab.github.io/presentations/ieee-smc-eo/ieee-smc-eo.html",
}


def main():
    for name, address in CODES.items():
        code = segno.make(address, error="m")
        code.save(str(ASSETS / name), scale=12, border=4, dark="#252525", light="#ffffff")
        print(f"wrote {name}  {code.symbol_size(scale=12, border=4)[0]} px  ->  {address}")


if __name__ == "__main__":
    main()
