---------------------------
-- ENVIRONMENT VARIABLES --
---------------------------

hl.env("HYPRCURSOR_THEME", "Bibata-Modern-Ice")
hl.env("HYPRCURSOR_SIZE", "24")
hl.env("SHELL", "/usr/bin/zsh")

hl.env("CLUTTER_BACKEND", "wayland")
hl.env("GDK_BACKEND", "wayland,x11")
hl.env("QT_AUTO_SCREEN_SCALE_FACTOR", "1")
hl.env("QT_QPA_PLATFORM", "wayland;xcb")
hl.env("QT_QPA_PLATFORMTHEME", "qt6ct")
hl.env("QT_SCALE_FACTOR", "1")
hl.env("QT_WAYLAND_DISABLE_WINDOWDECORATION", "1")
hl.env("XDG_CURRENT_DESKTOP", "Hyprland")
hl.env("XDG_SESSION_DESKTOP", "Hyprland")
hl.env("XDG_SESSION_TYPE", "wayland")

-- grimblast screenshot
-- Stops hyprpanel/hyprland from crashing when screenshotting with grimblast
hl.env("GRIMBLAST_HIDE_CURSOR", "0")

-- firefox
hl.env("MOZ_ENABLE_WAYLAND", "1")

-- electron >28 apps (may help)
hl.env("ELECTRON_OZONE_PLATFORM_HINT", "auto")
