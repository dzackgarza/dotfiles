import type { Accessor } from "ags"
import { Gtk } from "ags/gtk4"
import type { SliderState } from "../services/control-center"

const ICON_SIZE = 18

function joinClasses(...classes: Array<string | false | null | undefined>): string {
  return classes.filter((value) => Boolean(value)).join(" ")
}

type SliderRowProps = {
  icon: string
  state: Accessor<SliderState>
  onSetValue: (value: number) => Promise<void>
}

export function SliderRow({ icon, state, onSetValue }: SliderRowProps) {
  return (
    <box
      class={state((value) => joinClasses("slider-row", value.error && "error"))}
      orientation={Gtk.Orientation.HORIZONTAL}
      spacing={10}
      tooltipText={state((value) => value.error ?? "")}
    >
      <image class="slider-icon" iconName={icon} pixelSize={ICON_SIZE} />
      <slider
        value={state((value) => value.value)}
        min={0}
        max={1}
        hexpand
        sensitive={state((value) => !value.error)}
        onChangeValue={({ value }) => void onSetValue(value)}
      />
      <label class="slider-value" halign={Gtk.Align.END} label={state((value) => value.valueLabel)} />
    </box>
  )
}
