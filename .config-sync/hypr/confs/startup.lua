-------------
-- STARTUP --
-------------

local scripts_dir = os.getenv("HOME") .. "/.config/hypr/scripts"
local cursor = "layan-white-cursors"

-- `exec-once` = run only at compositor startup.
hl.on("hyprland.start", function()
    hl.exec_cmd("dbus-update-activation-environment --systemd DISPLAY HYPRLAND_INSTANCE_SIGNATURE WAYLAND_DISPLAY XDG_CURRENT_DESKTOP XDG_SESSION_TYPE && systemctl --user stop hyprland-session.target && systemctl --user start hyprland-session.target")
    hl.exec_cmd("hyprctl setcursor " .. cursor .. " 24")
    hl.exec_cmd(scripts_dir .. "/startup.sh & " .. scripts_dir .. "/polkit.sh")
    -- `ags run` builds every app to the one file $XDG_RUNTIME_DIR/ags.js (ags 3.1,
    -- cli/cmd/run.go getOutfile), so two concurrent runs can load the same app.
    -- Start window-ram only after control-panel's instance ("ags") is registered,
    -- which happens after its gjs has loaded that file.
    hl.exec_cmd(
        "waybar & hyprsunset & nm-applet & copyq & dropbox & bitwarden-desktop & "
            .. "ags run /home/dzack/dotfiles/ags/control-panel & "
            .. "{ timeout 30 sh -c 'until ags list | grep -qx ags; do sleep 0.2; done' "
            .. "&& ags run /home/dzack/dotfiles/ags/window-ram/app.tsx "
            .. "|| notify-send -u critical 'window-ram not started' 'control-panel did not register within 30 s'; }"
    )
    hl.exec_cmd("zotero", { workspace = "10" })
end)
