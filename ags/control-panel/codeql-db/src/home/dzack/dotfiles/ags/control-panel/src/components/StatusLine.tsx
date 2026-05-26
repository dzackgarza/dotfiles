import type { Accessor } from "ags";
import { Gtk } from "ags/gtk4";

const ICON_SIZE = 12;

type StatusLineProps = {
  icon: string;
  text: string | Accessor<string>;
};

export function StatusLine({ icon, text }: StatusLineProps) {
  return (
    <box class="status-subrow" orientation={Gtk.Orientation.HORIZONTAL} spacing={6}>
      <image class="status-subicon" iconName={icon} pixelSize={ICON_SIZE} />
      <label class="status-sub" xalign={0} label={text} />
    </box>
  );
}
