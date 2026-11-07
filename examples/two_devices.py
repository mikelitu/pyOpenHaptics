"""Plot two Touch devices; pass their configured Touch Setup names as arguments."""

import argparse
from contextlib import ExitStack

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import pyOpenHaptics.hd as hd
from pyOpenHaptics.hd_callback import hd_callback
from pyOpenHaptics.exceptions import DeviceInitException
from pyOpenHaptics.hd_device import HapticDevice


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("names", nargs=2, help="Two distinct Touch Setup device names")
    args = parser.parse_args()
    if args.names[0] == args.names[1]:
        parser.error("Specify two distinct device names")

    states = [None, None]

    def make_callback(index):
        @hd_callback
        def callback():
            # Publish a complete snapshot; draw only from the main thread.
            states[index] = (tuple(hd.get_transform()[3])[:3], hd.get_buttons())

        return callback

    fig = plt.figure(figsize=(10, 5))
    axes = [fig.add_subplot(1, 2, i + 1, projection="3d") for i in range(2)]
    points, labels = [], []
    for ax, name in zip(axes, args.names):
        ax.set(title=name, xlabel="X (mm)", ylabel="Y (mm)", zlabel="Z (mm)",
               xlim=(-250, 250), ylim=(-250, 250), zlim=(-250, 250))
        points.append(ax.plot([], [], [], "o", markersize=8)[0])
        labels.append(ax.text2D(0, 0.95, "Waiting for data...", transform=ax.transAxes))
    fig.tight_layout()

    def update(_frame):
        for index, point in enumerate(points):
            state = states[index]
            if state is None:
                continue
            (x, y, z), buttons = state
            point.set_data_3d([x], [y], [z])
            labels[index].set_text(
                f"XYZ: {x:.1f}, {y:.1f}, {z:.1f} mm\nButtons: {buttons:02b}"
            )

    try:
        with ExitStack() as stack:
            for index, name in enumerate(args.names):
                device = HapticDevice(make_callback(index), device_name=name)
                stack.callback(device.close)
            # Keep the animation alive until the window closes.
            animation = FuncAnimation(fig, update, interval=33, cache_frame_data=False)
            plt.show()
    except DeviceInitException as error:
        parser.exit(1, f"{error}\n")
    finally:
        plt.close(fig)


if __name__ == "__main__":
    main()
