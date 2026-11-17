#!/usr/bin/env python3
import csv
import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

import gi

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
        self.tempdir = tempfile.TemporaryDirectory(prefix="waybar-battery-")
        self.image = Gtk.Image()
        self.error = Gtk.Label()
        self.error.set_line_wrap(True)
        self.error.set_xalign(0)

        controls = Gtk.Box(spacing=6)
        for label, seconds in (("1h", 3600), ("3h", 10800), ("8h", 28800), ("1d", 86400)):
            button = Gtk.Button(label=label)
            button.connect("clicked", self.set_range, seconds)
            controls.pack_start(button, False, False, 0)

        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        layout.pack_start(controls, False, False, 0)
        layout.pack_start(self.image, True, True, 0)
        layout.pack_start(self.error, False, False, 0)
        self.add(layout)

        self.refresh()

    def refresh(self) -> None:
        try:
            self.samples = charge_history(self.range_seconds)
            input_path = Path(self.tempdir.name) / "history.csv"
            output_path = Path(self.tempdir.name) / "history.png"
            with input_path.open("w", newline="") as stream:
                writer = csv.writer(stream)
                writer.writerow(("timestamp", "percentage"))
                writer.writerows((sample.timestamp, sample.percentage) for sample in self.samples)
            subprocess.run(
                [
                    "Rscript",
                    str(Path(__file__).with_name("battery-history.R")),
                    str(input_path),
                    str(output_path),
                    str(self.range_seconds),
                ],
                check=True,
                capture_output=True,
                text=True,
                env={**os.environ, "R_LIBS_USER": os.path.expanduser("~/R/x86_64-pc-linux-gnu-library/4.6")},
                timeout=30,
            )
            self.image.set_from_file(str(output_path))
            self.error.set_text("")
        except (OSError, RuntimeError, GLib.Error, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            self.image.clear()
            message = getattr(exc, "stderr", None) or str(exc)
            self.error.set_text(message.strip())

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
