"""Check the Tobii eye tracker before the slide 36 demo. Reads only; changes nothing.

    python tools/check_eyetracker.py            # 20 seconds
    python tools/check_eyetracker.py --seconds 60

Needs only `tobii-research` (Python 3.10). Prints what the tracker is and which
screen position it assumes, then a line every half second while the volunteer
sits and looks at the screen: are both eyes seen, where is the head in the
tracking box (0.50 is the middle on each axis), how far away, and is gaze
landing on the screen. Ends with the share of valid gaze.
"""

import argparse
import math
import statistics
import sys
import time

import tobii_research as tobii


def mean(a, b):
    vals = [v for v in (a, b) if v is not None and not math.isnan(v)]
    return sum(vals) / len(vals) if vals else float("nan")


def describe(tracker):
    print(f"Tracker   : {tracker.model}, serial {tracker.serial_number}")
    print(f"Gaze rate : {tracker.get_gaze_output_frequency():.0f} Hz")
    try:
        area = tracker.get_display_area()
    except tobii.EyeTrackerDisplayAreaNotValidError:
        print("Screen    : NOT SET on the tracker. Calibration will set a default.")
        return
    print(f"Screen    : {area.width:.0f} x {area.height:.0f} mm, "
          f"bottom edge {area.bottom_left[1]:.0f} mm above the tracker")
    print("            (measure your own screen: if these are wrong, gaze lands in the wrong place)")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seconds", type=float, default=20)
    args = parser.parse_args()

    trackers = tobii.find_all_eyetrackers()
    if not trackers:
        print("No tracker found. Check the USB cable and that the Tobii runtime is installed.")
        return 1
    tracker = trackers[0]
    describe(tracker)

    latest = {"guide": None}
    gaze_valid, distances = [], []

    def on_guide(data):
        latest["guide"] = data

    def on_gaze(data):
        latest["gaze"] = data
        gaze_valid.append(bool(data["left_gaze_point_validity"] or data["right_gaze_point_validity"]))

    tracker.subscribe_to(tobii.EYETRACKER_USER_POSITION_GUIDE, on_guide, as_dictionary=True)
    tracker.subscribe_to(tobii.EYETRACKER_GAZE_DATA, on_gaze, as_dictionary=True)

    readings = both = 0
    print("\n left  right |   x     y     z   | distance | gaze on screen")
    try:
        end = time.monotonic() + args.seconds
        while time.monotonic() < end:
            time.sleep(0.5)
            guide, gaze = latest["guide"], latest.get("gaze")
            if guide is None or gaze is None:
                print("  waiting for data ...")
                continue
            lv, rv = bool(guide["left_user_position_validity"]), bool(guide["right_user_position_validity"])
            lp, rp = guide["left_user_position"], guide["right_user_position"]
            x, y, z = (mean(lp[i] if lv else None, rp[i] if rv else None) for i in range(3))
            lz = gaze["left_gaze_origin_in_user_coordinate_system"][2] if gaze["left_gaze_origin_validity"] else None
            rz = gaze["right_gaze_origin_in_user_coordinate_system"][2] if gaze["right_gaze_origin_validity"] else None
            dist_cm = mean(lz, rz) / 10
            if not math.isnan(dist_cm):
                distances.append(dist_cm)
            on_screen = bool(gaze["left_gaze_point_validity"] or gaze["right_gaze_point_validity"])
            readings += 1
            both += lv and rv
            print(f"  {'yes' if lv else ' - '}   {'yes' if rv else ' - '}  | {x:4.2f}  {y:4.2f}  {z:4.2f} | "
                  f"{dist_cm:5.0f} cm | {'yes' if on_screen else 'no'}")
    finally:
        tracker.unsubscribe_from(tobii.EYETRACKER_USER_POSITION_GUIDE, on_guide)
        tracker.unsubscribe_from(tobii.EYETRACKER_GAZE_DATA, on_gaze)

    if not gaze_valid:
        print("\nThe tracker was found but sent no gaze samples.")
        return 1
    valid = 100 * sum(gaze_valid) / len(gaze_valid)
    print(f"\nBoth eyes seen : {100 * both / max(readings, 1):.0f}% of readings")
    print(f"Valid gaze     : {valid:.0f}% of {len(gaze_valid)} samples (aim for 90% or more)")
    if distances:
        print(f"Distance       : {statistics.median(distances):.0f} cm (60 to 65 cm tracked best in rehearsal)")
    return 0 if valid >= 90 else 2


if __name__ == "__main__":
    sys.exit(main())
