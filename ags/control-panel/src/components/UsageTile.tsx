import type { Accessor } from "ags"
import { Gtk } from "ags/gtk4"
import type { UsageTileState } from "../services/control-center"

const ICON_SIZE = 22

function joinClasses(
  ...classes: Array<string | false | null | undefined>
): string {
  return classes.filter((value) => Boolean(value)).join(" ")
}

type UsageTileProps = {
  icon?: string
  iconFile?: string
  state: Accessor<UsageTileState>
}

export function UsageTile({ icon, iconFile, state }: UsageTileProps) {
  return (
    <box
      class={state((value) =>
        joinClasses("tile", "tile-usage", value.error && "error"),
      )}
      orientation={Gtk.Orientation.HORIZONTAL}
      spacing={10}
      hexpand
      halign={Gtk.Align.FILL}
      tooltipText={state((value) => value.detail)}
    >
      <image
        class="tile-icon"
        iconName={icon}
        file={iconFile}
        pixelSize={ICON_SIZE}
        valign={Gtk.Align.CENTER}
      />
      <box
        orientation={Gtk.Orientation.VERTICAL}
        spacing={4}
        hexpand
        halign={Gtk.Align.FILL}
      >
        <label
          class="tile-line1"
          xalign={0}
          label={state((value) => value.line1)}
        />
        <label
          class="tile-line2"
          xalign={0}
          label={state((value) => value.line2)}
        />
        <Gtk.ProgressBar
          fraction={state((value) => Math.min(Math.max(value.percent, 0), 1))}
        />
      </box>
    </box>
  )
}
