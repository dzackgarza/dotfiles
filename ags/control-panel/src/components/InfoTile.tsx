import type { Accessor } from "ags"
import { Gtk } from "ags/gtk4"
import type { InfoTileState } from "../services/control-center"

const ICON_SIZE = 22

function joinClasses(...classes: Array<string | false | null | undefined>): string {
  return classes.filter((value) => Boolean(value)).join(" ")
}

type InfoTileProps = {
  icon: string
  state: Accessor<InfoTileState>
  onActivate?: () => Promise<void>
}

export function InfoTile({ icon, state, onActivate }: InfoTileProps) {
  const content = (
    <box
      class={state((value) => joinClasses("tile", "tile-info", value.error && "error"))}
      orientation={Gtk.Orientation.HORIZONTAL}
      spacing={10}
      hexpand
      halign={Gtk.Align.FILL}
      tooltipText={state((value) => value.detail)}
    >
      <image class="tile-icon" iconName={icon} pixelSize={ICON_SIZE} valign={Gtk.Align.CENTER} />
      <box orientation={Gtk.Orientation.VERTICAL} spacing={4} hexpand halign={Gtk.Align.FILL}>
        <label class="tile-line1" xalign={0} label={state((value) => value.line1)} />
        <label class="tile-line2" xalign={0} label={state((value) => value.line2)} />
      </box>
    </box>
  )

  if (!onActivate) return content

  return (
    <button class="tile-trigger" onClicked={() => void onActivate()} hexpand halign={Gtk.Align.FILL}>
      {content}
    </button>
  )
}
