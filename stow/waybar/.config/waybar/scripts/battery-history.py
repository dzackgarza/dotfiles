#!/usr/bin/env python3
import csv
import logging
import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

import gi

gi.require_version("Gdk", "3.0")
gi.require_version("GtkLayerShell", "0.1")
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gio, GLib, Gtk, GtkLayerShell


LOG_PATH = Path(os.path.expanduser("~/.local/state/waybar/battery-history.log"))
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
LOGGER = logging.getLogger(__name__)


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
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_can_focus(True)
        self.add_events(Gdk.EventMask.KEY_PRESS_MASK | Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect("key-press-event", self.on_key_press)
        self.connect("button-press-event", self.on_button_press)
        self.connect("focus-out-event", self.on_focus_out)

        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_namespace(self, "waybar-battery-history")
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.TOP)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, True)
        GtkLayerShell.set_exclusive_zone(self, -1)
        GtkLayerShell.set_keyboard_mode(self, GtkLayerShell.KeyboardMode.ON_DEMAND)
        self.position_below_pointer()

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

    def on_key_press(self, _window: Gtk.Window, event: Gdk.EventKey) -> bool:
        if event.keyval == Gdk.KEY_Escape:
            self.close()
            return True
        return False

    def on_button_press(self, _window: Gtk.Window, event: Gdk.EventButton) -> bool:
        if event.button != 1:
            return False
        allocation = self.get_allocation()
        if not (0 <= event.x <= allocation.width and 0 <= event.y <= allocation.height):
            self.close()
            return True
        return False

    def on_focus_out(self, _window: Gtk.Window, _event: Gdk.EventFocus) -> bool:
        self.close()
        return False

    def show(self) -> None:
        super().show()
        self.present()
        self.grab_focus()
        Gtk.grab_add(self)

    def close(self) -> None:
        if Gtk.grab_get_current() is self:
            Gtk.grab_remove(self)
        self.destroy()

    def position_below_pointer(self) -> None:
        display = Gdk.Display.get_default()
        if display is None:
            raise RuntimeError("No GDK display available")
        _screen, pointer_x, pointer_y = (
            display.get_default_seat().get_pointer().get_position()
        )
        monitor = display.get_monitor_at_point(pointer_x, pointer_y)
        if monitor is None:
            raise RuntimeError("No monitor found under pointer")
        geometry = monitor.get_geometry()
        popup_width = 680
        left = max(
            geometry.x + 8,
            min(pointer_x - popup_width // 2, geometry.x + geometry.width - popup_width - 8),
        )
        GtkLayerShell.set_monitor(self, monitor)
        GtkLayerShell.set_margin(self, GtkLayerShell.Edge.TOP, pointer_y - geometry.y + 8)
        GtkLayerShell.set_margin(self, GtkLayerShell.Edge.LEFT, left - geometry.x)

    def refresh(self) -> None:
        try:
            self.samples = charge_history(self.range_seconds)
            LOGGER.info(
                "Rendering %s samples for %ss range",
                len(self.samples),
                self.range_seconds,
            )
            input_path = Path(self.tempdir.name) / "history.csv"
            output_path = Path(self.tempdir.name) / "history.png"
            with input_path.open("w", newline="") as stream:
                writer = csv.writer(stream)
                writer.writerow(("timestamp", "percentage"))
                writer.writerows((sample.timestamp, sample.percentage) for sample in self.samples)
            result = subprocess.run(
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
            if result.stdout:
                LOGGER.info("R output: %s", result.stdout.strip())
            if result.stderr:
                LOGGER.warning("R warnings: %s", result.stderr.strip())
            if not output_path.is_file() or output_path.stat().st_size == 0:
                raise RuntimeError("R completed without producing a graph image")
            self.image.set_from_file(str(output_path))
            self.error.set_text("")
            LOGGER.info("Rendered graph image: %s bytes", output_path.stat().st_size)
        except (OSError, RuntimeError, GLib.Error, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            LOGGER.exception("Battery history render failed")
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
