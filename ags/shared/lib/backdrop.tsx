import { Astal, Gdk, Gtk } from "ags/gtk4";
import app from "ags/gtk4/app";

/**
 * Create a full-screen transparent catcher window that closes a named panel
 * window on click-outside or Escape. Mirrors the pattern used in control-panel.
 *
 * Usage:
 *   const { sync } = makeBackdropCatcher("my-catcher", () => { win.visible = false })
 *   // then in the window's $ prop:
 *   $={(self) => sync(self)}
 */
export function makeBackdropCatcher(
  catcherName: string,
  onClose: () => void,
): { sync: (mainWindow: Gtk.Window) => void } {
  const { TOP, RIGHT, LEFT, BOTTOM } = Astal.WindowAnchor;

  const backdrop = (
    <box hexpand vexpand canTarget halign={Gtk.Align.FILL} valign={Gtk.Align.FILL} />
  ) as Gtk.Box;

  const click = Gtk.GestureClick.new();
  click.set_button(0);
  click.set_propagation_phase(Gtk.PropagationPhase.CAPTURE);
  click.connect("pressed", () => onClose());
  backdrop.add_controller(click);

  const escKey = Gtk.EventControllerKey.new();
  escKey.set_propagation_phase(Gtk.PropagationPhase.CAPTURE);
  escKey.connect("key-pressed", (_: unknown, keyval: number) => {
    if (keyval !== Gdk.KEY_Escape) return false;
    onClose();
    return true;
  });
  backdrop.add_controller(escKey);

  const catcher = new Astal.Window({
    name: catcherName,
    application: app,
    visible: false,
    anchor: TOP | RIGHT | LEFT | BOTTOM,
    layer: Astal.Layer.TOP,
    keymode: Astal.Keymode.ON_DEMAND,
    exclusivity: Astal.Exclusivity.IGNORE,
    child: backdrop,
  });

  return {
    sync(mainWindow: Gtk.Window): boolean {
      mainWindow.connect("notify::visible", () => {
        catcher.visible = mainWindow.visible;
        return true;
      });
      mainWindow.connect("destroy", () => {
        catcher.destroy();
        return true;
      });
      return true;
    },
  };
}
