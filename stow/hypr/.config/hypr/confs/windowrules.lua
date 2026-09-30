------------------
-- WINDOW RULES --
------------------
-- All rules are anonymous on purpose: named rules are evaluated before every
-- anonymous one, which would silently reorder this file. Keeping them anonymous
-- preserves the strict top-to-bottom order the .conf version relied on.

local cfg = require("confs/vars").cfg
local opacity = cfg.opacity_act .. " " .. cfg.opacity_deact

--------------------------------
-- TAGS --
--------------------------------

-- browser tags
hl.window_rule({ match = { class = "^([Ff]irefox|org.mozilla.firefox|[Ff]irefox-esr|[Ff]irefox-bin)$" }, tag = "+browser" })
hl.window_rule({ match = { class = "^([Gg]oogle-chrome(-beta|-dev|-unstable)?)$" }, tag = "+browser" })
hl.window_rule({ match = { class = "^(chrome-.+-Default)$" }, tag = "+browser" }) -- Chrome PWAs
hl.window_rule({ match = { class = "^([Cc]hromium)$" }, tag = "+browser" })
hl.window_rule({ match = { class = "^([Mm]icrosoft-edge(-stable|-beta|-dev|-unstable))$" }, tag = "+browser" })
hl.window_rule({ match = { class = "^([Bb]rave-browser(-beta|-dev|-unstable)?)$" }, tag = "+browser" })
hl.window_rule({ match = { class = "^([Tt]horium-browser|[Cc]achy-browser)$" }, tag = "+browser" })
hl.window_rule({ match = { class = "^(zen-alpha|zen)$" }, tag = "+browser" })

-- terminal
hl.window_rule({ match = { class = "^(Alacritty|kitty|kitty-dropterm)$" }, tag = "+terminal" })

-- file manager
hl.window_rule({ match = { class = "^([Tt]hunar|org.gnome.Nautilus|[Pp]cmanfm-qt)$" }, tag = "+file-manager" })

-- ide
hl.window_rule({ match = { class = "^(codium|codium-url-handler|VSCodium)$" }, tag = "+ide" })
hl.window_rule({ match = { class = "^(VSCode|code-url-handler|code)$" }, tag = "+ide" })
hl.window_rule({ match = { class = "^(jetbrains-.+)$" }, tag = "+ide" }) -- JetBrains IDEs

--------------
-- FLOATING --
--------------

hl.window_rule({ match = { class = "^(org.kde.polkit-kde-authentication-agent-1)$" }, float = true })
hl.window_rule({ match = { class = "^(xfce-polkit)$" }, float = true })
hl.window_rule({ match = { tag = "file-manager*", title = "(File Operation Progress)" }, float = true })
hl.window_rule({ match = { class = "([Tt]hunar)", title = "(Confirm to replace files)" }, float = true })
hl.window_rule({ match = { class = "^(pavucontrol|org.pulseaudio.pavucontrol)$" }, float = true })
hl.window_rule({ match = { class = "^(nwg-look|qt5ct|qt6ct|mpv)$" }, float = true })
hl.window_rule({ match = { class = "^(kitty)$", title = "(update)" }, float = true })
hl.window_rule({ match = { class = "^(kitty)$", title = "(yazi)" }, float = true })
hl.window_rule({ match = { class = "^(kitty)$", title = "(monitor)" }, float = true })
hl.window_rule({ match = { class = "^(kitty)$", title = "(browser)" }, float = true })
hl.window_rule({ match = { class = "^(kitty)$", title = "(floating)" }, float = true })
hl.window_rule({ match = { class = "^(file-roller|org.gnome.FileRoller)$" }, float = true }) -- archive manager
hl.window_rule({ match = { class = "^([Kk]vantummanager)$" }, float = true })
hl.window_rule({ match = { class = "^([Ll]xappearance)$" }, float = true })
hl.window_rule({ match = { class = "^(yad)$" }, float = true })
hl.window_rule({ match = { class = "^(eog)$" }, float = true })
hl.window_rule({ match = { class = "^([Tt]hunar)$" }, float = true })
hl.window_rule({ match = { class = "^([Gg]nome-disks)$" }, float = true })
hl.window_rule({ match = { class = "^(com.obsproject.Studio)$" }, float = true })
hl.window_rule({ match = { class = "^(org.kde.kcalc)$" }, float = true })
hl.window_rule({ match = { class = "^(org.telegram.desktop)$" }, float = true })
hl.window_rule({ match = { class = "^(org.kde.partitionmanager)$" }, float = true })
hl.window_rule({ match = { class = "^(org.kde.gwenview)$" }, float = true })
hl.window_rule({ match = { class = "^(org.gnome.Calendar)$" }, float = true })
hl.window_rule({ match = { class = "^(scratch-term)$" }, fullscreen = true })
hl.window_rule({ match = { class = "^(Alacritty)$", title = "^(btop)$" }, float = true })

hl.window_rule({ match = { title = "^(Authentication Required)$" }, float = true })
hl.window_rule({ match = { title = "^(Authentication Required)$" }, center = true })
hl.window_rule({ match = { class = "(codium|codium-url-handler|VSCodium)", title = "negative:(.*codium.*|.*VSCodium.*)" }, float = true })
hl.window_rule({ match = { class = "^(com.heroicgameslauncher.hgl)$", title = "negative:(Heroic Games Launcher)" }, float = true })
hl.window_rule({ match = { class = "^([Ss]team)$", title = "negative:^([Ss]team)$" }, float = true })
hl.window_rule({ match = { class = "([Tt]hunar)", title = "negative:(.*[Tt]hunar.*)" }, float = true })
hl.window_rule({ match = { class = "(xdg-desktop-portal-gtk)" }, float = true })
hl.window_rule({ match = { class = "(electron)", title = "(Add Folder to Workspace)" }, float = true })
hl.window_rule({ match = { title = "^(Add Folder to Workspace)$" }, float = true })
hl.window_rule({ match = { tag = "browser*", initial_title = "^(wants to open)$" }, float = true })
hl.window_rule({ match = { initial_title = "(Open Files)" }, float = true })

----------
-- SIZE --
----------

hl.window_rule({ match = { class = "^([Kk]vantummanager)$" }, size = { "60%", "80%" } })
hl.window_rule({ match = { class = "^([Ll]xappearance)$" }, size = { "60%", "80%" } })
hl.window_rule({ match = { class = "^(nwg-look)$" }, size = { "60%", "80%" } })
hl.window_rule({ match = { class = "^(eog)$" }, size = { "60%", "80%" } })
hl.window_rule({ match = { class = "^([Tt]hunar)$" }, size = { "60%", "80%" } })
hl.window_rule({ match = { class = "^([Tt]hunar)$", title = "(File Operation Progress)" }, size = { "20%", "40%" } })
hl.window_rule({ match = { class = "^([Tt]hunar)$", title = "(Confirm to replace files)" }, size = { "20%", "40%" } })
hl.window_rule({ match = { class = "^(xdg-desktop-portal-gtk)$" }, size = { "70%", "70%" } })
hl.window_rule({ match = { title = "(Kvantum Manager)" }, size = { "60%", "70%" } })
hl.window_rule({ match = { class = "^(nwg-look|qt5ct|qt6ct|mpv)$" }, size = { "60%", "70%" } })
hl.window_rule({ match = { class = "^(pavucontrol|org.pulseaudio.pavucontrol)$" }, size = { "60%", "70%" } })
hl.window_rule({ match = { class = "^(kitty)$", title = "(update)" }, size = { "60%", "70%" } })
hl.window_rule({ match = { class = "^(kitty)$", title = "(yazi)" }, size = { "60%", "60%" } })
hl.window_rule({ match = { class = "^(kitty)$", title = "(monitor)" }, size = { "50%", "55%" } })
hl.window_rule({ match = { class = "^(kitty)$", title = "(browser)" }, size = { "50%", "60%" } })
hl.window_rule({ match = { class = "^(kitty)$", title = "(floating)" }, size = { "70%", "80%" } })
hl.window_rule({ match = { class = "^(com.obsproject.Studio)$" }, size = { "50%", "80%" } })
hl.window_rule({ match = { class = "^(org.telegram.desktop)$" }, size = { "60%", "80%" } })
hl.window_rule({ match = { class = "^(org.kde.gwenview)$" }, size = { "60%", "80%" } })
hl.window_rule({ match = { class = "^(org.kde.partitionmanager)$" }, size = { "50%", "60%" } })
hl.window_rule({ match = { class = "^(org.kde.kcalc)$" }, size = { "30%", "55%" } })
hl.window_rule({ match = { class = "^(xfce-polkit)$" }, size = { "30%", "20%" } })
hl.window_rule({ match = { class = "^(org.gnome.Calendar)$" }, size = { "60%", "80%" } })
hl.window_rule({ match = { class = "^(Alacritty)$", title = "^(btop)$" }, size = { "90%", "80%" } })
hl.window_rule({ match = { class = "^(chromium)$" }, size = { "100%", "90%" } })

--------------
-- POSITION --
--------------

hl.window_rule({ match = { class = "([Tt]hunar)", title = "(File Operation Progress)" }, center = true })
hl.window_rule({ match = { class = "([Tt]hunar)", title = "(Confirm to replace files)" }, center = true })
hl.window_rule({ match = { class = "^(nwg-look)$" }, center = true })
hl.window_rule({ match = { class = "^(qt5ct)$" }, center = true })
hl.window_rule({ match = { class = "^(lxappearance)$" }, center = true })
hl.window_rule({ match = { class = "^(yad)$" }, center = true })
hl.window_rule({ match = { class = "^(kitty)$", title = "(yazi|update|browser)" }, center = true })
hl.window_rule({ match = { class = "^(gnome-calendar)$" }, center = true })
hl.window_rule({ match = { class = "^(Alacritty)$", title = "^(btop)$" }, center = true })
hl.window_rule({ match = { class = "^(chromium)$" }, center = true })

-------------
-- OPACITY --
-------------

hl.window_rule({ match = { tag = "ide*" }, opacity = opacity })
hl.window_rule({ match = { tag = "terminal*" }, opacity = opacity })
hl.window_rule({ match = { tag = "file-manager*" }, opacity = opacity })
hl.window_rule({ match = { tag = "browser*" }, opacity = "1.0 " .. cfg.opacity_deact })

------------------------
-- OPEN IN WORKSPACES --
------------------------

hl.window_rule({ match = { tag = "ide*" }, workspace = "3 silent" })
hl.window_rule({ match = { class = "^(com.obsproject.Studio)$" }, workspace = "3 silent" })
hl.window_rule({ match = { class = "^(Zotero)$" }, workspace = "10 silent" })
hl.window_rule({ match = { class = "^(com.chatonsteroids.app)$" }, workspace = "10 silent" })
hl.window_rule({ match = { class = "^([Zz]ettlr(-[Pp]andoc)?)$" }, workspace = "8 silent" })

-- prevent new windows from stealing focus
hl.window_rule({ match = { class = ".*" }, no_initial_focus = true })
hl.window_rule({ match = { class = "^(kitty)$", initial_title = "^(main)$" }, no_initial_focus = false })

hl.workspace_rule({
    workspace = "special:exposed",
    gaps_out = 60,
    gaps_in = 30,
    border_size = 5,
    no_border = false,
    no_shadow = true,
})

hl.workspace_rule({
    workspace = "special:kitty-scratch",
    on_created_empty = "kitty --class scratch-term -e tmux new-session -A -s scratch",
})
hl.workspace_rule({
    workspace = "special:btop",
    on_created_empty = "alacritty --title btop -e btop",
})
hl.workspace_rule({
    workspace = "special:chromium",
    on_created_empty = "chromium",
})

-----------------
-- LAYER RULES --
-----------------

hl.layer_rule({ match = { namespace = "notifications" }, blur = true })
hl.layer_rule({ match = { namespace = "rofi" }, blur = true })
hl.layer_rule({ match = { namespace = "rofi" }, ignore_alpha = 0 })
hl.layer_rule({ match = { namespace = "notifications" }, ignore_alpha = 0 })
hl.layer_rule({ match = { namespace = "logout_dialog" }, blur = true })
hl.layer_rule({ match = { namespace = "swaync-control-center" }, blur = true })
hl.layer_rule({ match = { namespace = "swaync-notification-window" }, blur = true })
hl.layer_rule({ match = { namespace = "swaync-control-center" }, ignore_alpha = 0 })
hl.layer_rule({ match = { namespace = "swaync-notification-window" }, ignore_alpha = 0 })

hl.layer_rule({ match = { namespace = "code" }, blur = true })
hl.layer_rule({ match = { namespace = "code-oss" }, blur = true })
hl.layer_rule({ match = { namespace = "waybar" }, blur = true })

----------------
-- PDF BUCKET --
----------------

-- The bucket window takes focus when a capture opens its reader page.
dofile("/home/dzack/gitclones/math-pdf-reader/desktop/hyprland/pdf-bucket.lua")
