import type { Accessor } from "ags"
import { Gtk } from "ags/gtk4"
import type { ToggleTileState } from "../services/control-center"

const ICON_SIZE = 22

function joinClasses(
  ...classes: Array<string | false | null | undefined>
): string {
  return classes.filter((value) => Boolean(value)).join(" ")
}

type ToggleTileProps = {
  iconOn: string
  iconOff: string
  state: Accessor<ToggleTileState>
  onToggle: () => Promise<boolean>
}

export function ToggleTile({
  iconOn,
  iconOff,
  state,
  onToggle,
}: ToggleTileProps) {
  return (
    <button
      class={state((value) =>
        joinClasses(
          "tile",
          "tile-toggle",
          value.active && "active",
          value.error && "error",
        ),
      )}
      hexpand
      halign={Gtk.Align.FILL}
      tooltipText={state((value) => value.detail)}
      onClicked={() => void onToggle()}
    >
      <box
        class="tile-content"
        orientation={Gtk.Orientation.HORIZONTAL}
        spacing={10}
        hexpand
        halign={Gtk.Align.FILL}
      >
        <image
          class="tile-icon"
          iconName={state((value) => (value.active ? iconOn : iconOff))}
          pixelSize={ICON_SIZE}
          valign={Gtk.Align.CENTER}
        />
        <box orientation={Gtk.Orientation.VERTICAL} spacing={4} hexpand>
          <label
            class="tile-line1"
            xalign={0}
            label={state((value) => value.line1)}
          />
          <label
            class="tile-line2"
            xalign={0}
            maxWidthChars={25}
            ellipsize={3}
            label={state((value) => value.line2)}
          />
        </box>
      </box>
    </button>
  )
}
