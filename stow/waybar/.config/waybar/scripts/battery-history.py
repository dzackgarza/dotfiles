#!/usr/bin/env python3
import subprocess
import time
from dataclasses import dataclass

import gi
import matplotlib

matplotlib.use("GTK3Agg")
from matplotlib import dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg

gi.require_version("Gtk", "3.0")
from gi.repository import Gio, GLib, Gtk


@dataclass(frozen=True)
class Sample:
    timestamp: float
    percentage: float


def battery_path() -> str:
    devices = subprocess.run(
        ["upower", "-e"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    try:
        return next(
            device
            for device in devices
            if "battery" in device and "DisplayDevice" not in device
        )
    except StopIteration as exc:
        raise RuntimeError("No battery device found") from exc


def charge_history(timespan: int) -> list[Sample]:
    proxy = Gio.DBusProxy.new_sync(
        Gio.bus_get_sync(Gio.BusType.SYSTEM, None),
        Gio.DBusProxyFlags.NONE,
        None,
        "org.freedesktop.UPower",
        battery_path(),
        "org.freedesktop.UPower.Device",
        None,
    )
    result = proxy.call_sync(
        "GetHistory",
        GLib.Variant("(suu)", ("charge", timespan, max(1, timespan // 300))),
        Gio.DBusCallFlags.NONE,
        -1,
        None,
    )
    return [
        Sample(float(timestamp), float(percentage))
        for timestamp, percentage, _state in result.unpack()[0]
    ]


class HistoryWindow(Gtk.Window):
    def __init__(self) -> None:
        super().__init__(title="Battery history")
        self.set_default_size(680, 400)
        self.set_border_width(12)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.range_seconds = 3600
        self.samples: list[Sample] = []
        self.figure = Figure(figsize=(7, 4), dpi=100)
        self.figure.patch.set_facecolor("#1f1f26")
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvasGTK3Agg(self.figure)

        controls = Gtk.Box(spacing=6)
        for label, seconds in (("1h", 3600), ("3h", 10800), ("8h", 28800), ("1d", 86400)):
            button = Gtk.Button(label=label)
            button.connect("clicked", self.set_range, seconds)
            controls.pack_start(button, False, False, 0)

        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        layout.pack_start(controls, False, False, 0)
        layout.pack_start(self.canvas, True, True, 0)
        self.add(layout)

        self.refresh()

    def refresh(self) -> None:
        try:
            self.samples = charge_history(self.range_seconds)
        except (OSError, RuntimeError, GLib.Error, subprocess.CalledProcessError) as exc:
            self.samples = []
            self.axes.clear()
            self.axes.text(
                0.5,
                0.5,
                str(exc),
                ha="center",
                va="center",
                transform=self.axes.transAxes,
                color="#d8dee9",
            )
            self.canvas.draw_idle()
            return

        now = time.time()
        cutoff = now - self.range_seconds
        samples = [sample for sample in self.samples if sample.timestamp >= cutoff]

        self.axes.clear()
        self.axes.set_facecolor("#1f1f26")
        self.axes.tick_params(colors="#d8dee9", which="both")
        for spine in self.axes.spines.values():
            spine.set_color("#4c566a")
        self.axes.grid(True, color="#4c566a", alpha=0.35)
        self.axes.set_ylim(0, 100)
        self.axes.set_xlim(cutoff, now)
        self.axes.set_ylabel("Battery", color="#d8dee9")
        self.axes.yaxis.set_major_formatter(lambda value, _position: f"{value:.0f}%")
        self.axes.xaxis_date()
        self.axes.xaxis.set_major_locator(mdates.AutoDateLocator())
        self.axes.xaxis.set_major_formatter(mdates.ConciseDateFormatter(self.axes.xaxis.get_major_locator()))

        if samples:
            timestamps = [sample.timestamp for sample in samples]
            percentages = [sample.percentage for sample in samples]
            self.axes.plot(
                timestamps,
                percentages,
                color="#a3be8c",
                linewidth=2,
                marker="o",
                markersize=3,
            )
        else:
            self.axes.text(
                0.5,
                0.5,
                "No UPower history for this range",
                ha="center",
                va="center",
                transform=self.axes.transAxes,
                color="#d8dee9",
            )
        self.figure.tight_layout()
        self.canvas.draw_idle()

    def set_range(self, _button: Gtk.Button, seconds: int) -> None:
        self.range_seconds = seconds
        self.refresh()


def main() -> None:
    window = HistoryWindow()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
