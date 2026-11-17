#!/usr/bin/env python3
import subprocess
import time
from dataclasses import dataclass

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


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


def charge_history() -> list[Sample]:
    output = subprocess.run(
        ["upower", "-i", battery_path()],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    lines = output.splitlines()
    try:
        start = next(
            index + 1
            for index, line in enumerate(lines)
            if line.strip() == "History (charge):"
        )
    except StopIteration as exc:
        raise RuntimeError("UPower did not provide charge history") from exc

    samples = []
    for line in lines[start:]:
        if line.strip().startswith("History ("):
            break
        fields = line.split()
        if len(fields) < 2:
            continue
        try:
            samples.append(Sample(float(fields[0]), float(fields[1])))
        except ValueError:
            continue
    return sorted(samples, key=lambda sample: sample.timestamp)


class HistoryWindow(Gtk.Window):
    def __init__(self) -> None:
        super().__init__(title="Battery history")
        self.set_default_size(680, 400)
        self.set_border_width(12)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.range_seconds = 3600
        self.samples: list[Sample] = []
        self.graph = Gtk.DrawingArea()
        self.graph.connect("draw", self.draw_graph)

        controls = Gtk.Box(spacing=6)
        for label, seconds in (("1h", 3600), ("3h", 10800), ("8h", 28800), ("1d", 86400)):
            button = Gtk.Button(label=label)
            button.connect("clicked", self.set_range, seconds)
            controls.pack_start(button, False, False, 0)

        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        layout.pack_start(controls, False, False, 0)
        layout.pack_start(self.graph, True, True, 0)
        self.add(layout)

        self.refresh()

    def refresh(self) -> None:
        try:
            self.samples = charge_history()
        except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
            self.samples = []
            self.graph.set_tooltip_text(str(exc))
        self.graph.queue_draw()

    def set_range(self, _button: Gtk.Button, seconds: int) -> None:
        self.range_seconds = seconds
        self.refresh()

    def draw_graph(self, _area: Gtk.DrawingArea, context) -> bool:
        allocation = self.graph.get_allocation()
        width, height = allocation.width, allocation.height
        context.set_source_rgb(0.12, 0.12, 0.15)
        context.paint()

        left, top, right, bottom = 52, 18, width - 18, height - 38
        context.set_source_rgb(0.32, 0.34, 0.4)
        context.set_line_width(1)
        for percentage in (0, 25, 50, 75, 100):
            y = bottom - (percentage / 100) * (bottom - top)
            context.move_to(left, y)
            context.line_to(right, y)
            context.stroke()
            context.move_to(8, y + 4)
            context.show_text(f"{percentage}%")

        cutoff = time.time() - self.range_seconds
        samples = [sample for sample in self.samples if sample.timestamp >= cutoff]
        if not samples:
            context.set_source_rgb(0.75, 0.75, 0.8)
            context.move_to(left + 12, (top + bottom) / 2)
            context.show_text("No UPower history for this range")
            return False

        start = cutoff
        end = time.time()
        context.set_source_rgb(0.45, 0.8, 0.55)
        context.set_line_width(2.5)
        for index, sample in enumerate(samples):
            x = left + ((sample.timestamp - start) / (end - start)) * (right - left)
            y = bottom - (sample.percentage / 100) * (bottom - top)
            if index == 0:
                context.move_to(x, y)
            else:
                context.line_to(x, y)
        context.stroke()

        if len(samples) == 1:
            sample = samples[0]
            x = left + ((sample.timestamp - start) / (end - start)) * (right - left)
            y = bottom - (sample.percentage / 100) * (bottom - top)
            context.move_to(x, y)
            context.line_to(right, y)
            context.stroke()
            context.arc(x, y, 4, 0, 2 * 3.141592653589793)
            context.fill()

        context.set_source_rgb(0.75, 0.75, 0.8)
        context.move_to(left, height - 12)
        context.show_text(f"Latest: {samples[-1].percentage:.0f}%")
        return False


def main() -> None:
    window = HistoryWindow()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
