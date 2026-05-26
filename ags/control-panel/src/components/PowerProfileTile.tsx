import type { Accessor } from "ags";
import { Gtk } from "ags/gtk4";
import type { PowerProfile, PowerProfileState } from "../services/control-center";

const ICON_SIZE = 18;

function joinClasses(...classes: Array<string | false | null | undefined>): string {
  return classes.filter((value) => Boolean(value)).join(" ");
}

type PowerProfileTileProps = {
  state: Accessor<PowerProfileState>;
  onSetProfile: (profile: PowerProfile) => Promise<boolean>;
};

export function PowerProfileTile({ state, onSetProfile }: PowerProfileTileProps) {
  const options: Array<{ id: PowerProfile; icon: string; tooltip: string }> = [
    {
      id: "power-saver",
      icon: "xsi-power-profile-power-saver-symbolic",
      tooltip: "Power Saver",
    },
    {
      id: "balanced",
      icon: "xsi-power-profile-balanced-symbolic",
      tooltip: "Balanced",
    },
    {
      id: "performance",
      icon: "xsi-power-profile-performance-symbolic",
      tooltip: "Performance",
    },
  ];

  return (
    <box
      class={state((value) => joinClasses("tile", "tile-power", value.error && "error"))}
      orientation={Gtk.Orientation.HORIZONTAL}
      spacing={8}
      hexpand
      halign={Gtk.Align.FILL}
      tooltipText={state((value) => value.detail)}
    >
      {options.map((option) => (
        <button
          class={state((value) =>
            value.profile === option.id ? "tile-action active" : "tile-action",
          )}
          tooltipText={option.tooltip}
          sensitive={state((value) => !value.error)}
          onClicked={() => void onSetProfile(option.id)}
        >
          <image iconName={option.icon} pixelSize={ICON_SIZE} />
        </button>
      ))}
    </box>
  );
}
