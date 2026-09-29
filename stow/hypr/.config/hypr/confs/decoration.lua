-------------------
-- LOOK AND FEEL --
-------------------
-- Values come from confs/configs.conf and confs/decoration.conf.
-- See confs/vars.lua for the file reader.

local vars = require("confs/vars")
local cfg, theme = vars.cfg, vars.theme

hl.exec_cmd("gsettings set org.gnome.desktop.interface icon-theme " .. theme.icon)
hl.exec_cmd("gsettings set org.gnome.desktop.interface gtk-theme " .. theme.theme)
hl.exec_cmd("gsettings set org.gnome.desktop.interface color-scheme " .. theme.color)

hl.config({
    general = {
        layout = "dwindle",
        gaps_in = cfg.inner_gap,
        gaps_out = cfg.outer_gap,
        border_size = cfg.border,
        col = {
            active_border = theme.activeCol,
            inactive_border = theme.inactiveCol,
        },
        resize_on_border = false,
        allow_tearing = false,
    },

    decoration = {
        rounding = cfg.rounding,
        rounding_power = 2,

        -- Per-tag opacity is applied in confs/windowrules.lua.
        fullscreen_opacity = 1.0,

        dim_strength = 0.1,
        dim_special = 0.8,

        shadow = {
            enabled = true,
            range = cfg.shadow_range,
            render_power = 4,
            color = theme.activeCol,
            color_inactive = theme.inactiveCol,
        },

        blur = {
            enabled = true,
            size = cfg.blur_size,
            passes = cfg.blur_pass,
            ignore_opacity = true,
            new_optimizations = true,
            special = true,
            popups = true,
        },
    },
})
