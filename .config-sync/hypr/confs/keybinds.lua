--------------
-- KEYBINDS --
--------------

local hs = require("hyprsplit")

local mainMod = "SUPER"
local home = os.getenv("HOME")

-- Custom Variables
local scriptsDir = home .. "/.config/hypr/scripts"
local wallpaperSelect = scriptsDir .. "/WallpaperSelect.sh"
local terminal = "kitty"
local file_man = "dolphin"
local terminal_file_man = "yazi"
local rofi_emoji = scriptsDir .. "/rofi-emoji.sh"
local rofi_websites = home .. "/.config/hypr/confs/rofi-websites.sh"
local help = scriptsDir .. "/show-keybindings.sh"
local rofi_pdfs = home .. "/dotfiles/bin/dmenu/dmenuAllPDFs.sh"

local bind_actions = {}

local function register_bind(keys, dispatcher, flags, submap)
    local binding = hl.bind(keys, dispatcher, flags)
    local description = flags and flags.description

    if description then
        bind_actions[keys] = bind_actions[keys] or {}
        table.insert(bind_actions[keys], {
            description = description,
            dispatcher = dispatcher,
            submap = submap or "",
        })
    end

    return binding
end

_G.hypr_keybind_run = function(keys, description, submap)
    local actions = bind_actions[keys] or {}

    for _, action in ipairs(actions) do
        if action.description == description and action.submap == (submap or "") then
            if type(action.dispatcher) == "function" then
                return action.dispatcher()
            end
            return hl.dispatch(action.dispatcher)
        end
    end

    return { ok = false }
end

--------------------------------------
-- HYPRSPLIT: per-monitor workspaces --
--------------------------------------
-- Each monitor gets its own set of `num_workspaces` workspaces. The laptop is
-- listed first so it always owns 1-10; any other monitor is auto-assigned the
-- next block (11-20, 21-30, ...) no matter what it is or when it is plugged in.
hs.config({
    num_workspaces = 10,
    persistent_workspaces = true,
})
hs.monitor_priority({ "eDP-1" })

-- Native special-workspace scratchpads
local scratch_terminal = hl.dsp.workspace.toggle_special("kitty-scratch")
register_bind("F12", scratch_terminal, { description = "Toggle scratch terminal" })
-- Three-finger swipe up runs the same command as F12.
hl.gesture({ fingers = 3, direction = "up", action = function() hl.dispatch(scratch_terminal) end })
register_bind(mainMod .. " + F12", hl.dsp.workspace.toggle_special("btop"), { description = "Toggle btop scratchpad" })
register_bind("F11", hl.dsp.workspace.toggle_special("chromium"), { description = "Toggle Chromium scratchpad" })

-- Change Wallpaper
register_bind(mainMod .. " + SHIFT + W", hl.dsp.exec_cmd(wallpaperSelect .. " thm1"), { description = "Select wallpaper" })

-- Screenshot
register_bind("print", hl.dsp.exec_cmd(scriptsDir .. "/screenshot.sh"), { description = "Take screenshot" })

-- Key Binds Help
register_bind(mainMod .. " + SHIFT + h", hl.dsp.exec_cmd(help), { description = "Show keybinds" })

register_bind(mainMod .. " + Return", hl.dsp.exec_cmd(terminal .. " --title main"), { description = "Open terminal" })
register_bind(mainMod .. " + SHIFT + Return", hl.dsp.exec_cmd(scriptsDir .. "/script-launcher.sh"), { description = "Open command launcher" })
register_bind(mainMod .. " + W", hl.dsp.window.close(), { description = "Close active window" })
register_bind(mainMod .. " + E", hl.dsp.exec_cmd(file_man), { description = "Open file manager" })
register_bind(mainMod .. " + SHIFT + E", hl.dsp.exec_cmd(terminal .. " --title " .. terminal_file_man .. " -e " .. terminal_file_man), { description = "Open terminal file manager" })
register_bind(mainMod .. " + V", hl.dsp.window.float({ action = "toggle" }), { description = "Toggle floating layout" })
register_bind(mainMod .. " + Space", hl.dsp.window.fullscreen(), { description = "Toggle fullscreen layout" })
register_bind(mainMod .. " + A", hl.dsp.exec_cmd(rofi_pdfs), { description = "Search PDFs" })
register_bind(mainMod .. " + D", hl.dsp.exec_cmd(scriptsDir .. "/menu.sh || pkill rofi"), { description = "Open application menu" })
register_bind(mainMod .. " + SHIFT + D", hl.dsp.exec_cmd(rofi_emoji), { description = "Open emoji picker" })
register_bind(mainMod .. " + SHIFT + B", hl.dsp.exec_cmd(rofi_websites), { description = "Open website launcher" })
register_bind(mainMod .. " + SHIFT + P", hl.dsp.window.pseudo(), { description = "Toggle pseudotiling layout" })
register_bind(mainMod .. " + SHIFT + l", hl.dsp.exec_cmd("hyprlock"), { description = "Lock screen" })
register_bind(mainMod .. " + SHIFT + R", hl.dsp.exec_cmd('hyprctl reload && notify-send "Done" "Hyprland reload"'), { description = "Reload Hyprland" })

-- Cycle windows if floating bring to top
register_bind("ALT + tab", hl.dsp.window.cycle_next(), { description = "Cycle windows" })
register_bind("ALT + tab", hl.dsp.window.bring_to_top(), { description = "Raise selected window" })

register_bind(mainMod .. " + G", hl.dsp.group.toggle(), { description = "Toggle window group layout" })
register_bind(mainMod .. " + H", hl.dsp.exec_cmd(scriptsDir .. "/show-keybindings.sh"), { description = "Show keybinds" })
register_bind(mainMod .. " + M", hl.dsp.layout("splitratio 0.3"), { description = "Set layout split ratio" })
register_bind(mainMod .. " + SHIFT + I", hl.dsp.layout("togglesplit"), { description = "Toggle layout split direction" })
register_bind(mainMod .. " + P", hl.dsp.window.pseudo(), { description = "Toggle pseudotiling layout" })

-- Move focus with mainMod + arrow keys / hjkl
register_bind(mainMod .. " + left", hl.dsp.focus({ direction = "left" }), { description = "Focus left" })
register_bind(mainMod .. " + h", hl.dsp.focus({ direction = "left" }), { description = "Focus left" })
register_bind(mainMod .. " + right", hl.dsp.focus({ direction = "right" }), { description = "Focus right" })
register_bind(mainMod .. " + l", hl.dsp.focus({ direction = "right" }), { description = "Focus right" })
register_bind(mainMod .. " + up", hl.dsp.focus({ direction = "up" }), { description = "Focus up" })
register_bind(mainMod .. " + k", hl.dsp.focus({ direction = "up" }), { description = "Focus up" })
register_bind(mainMod .. " + down", hl.dsp.focus({ direction = "down" }), { description = "Focus down" })
register_bind(mainMod .. " + j", hl.dsp.focus({ direction = "down" }), { description = "Focus down" })

-- Move active window around current workspace with mainMod + SHIFT
register_bind(mainMod .. " + SHIFT + left", hl.dsp.window.move({ direction = "left" }), { description = "Move window left" })
register_bind(mainMod .. " + SHIFT + h", hl.dsp.window.move({ direction = "left" }), { description = "Move window left" })
register_bind(mainMod .. " + SHIFT + right", hl.dsp.window.move({ direction = "right" }), { description = "Move window right" })
register_bind(mainMod .. " + SHIFT + l", hl.dsp.window.move({ direction = "right" }), { description = "Move window right" })
register_bind(mainMod .. " + SHIFT + up", hl.dsp.window.move({ direction = "up" }), { description = "Move window up" })
register_bind(mainMod .. " + SHIFT + k", hl.dsp.window.move({ direction = "up" }), { description = "Move window up" })
register_bind(mainMod .. " + SHIFT + down", hl.dsp.window.move({ direction = "down" }), { description = "Move window down" })
register_bind(mainMod .. " + SHIFT + j", hl.dsp.window.move({ direction = "down" }), { description = "Move window down" })

-- Switch to / move a window to the Nth workspace OF THE CURRENT MONITOR
for i = 1, 10 do
    local key = i % 10 -- 10 maps to key 0
    register_bind(mainMod .. " + " .. key, hs.dsp.focus({ workspace = i }), { description = "Focus workspace " .. i })
    register_bind(mainMod .. " + SHIFT + " .. key, hs.dsp.window.move({ workspace = i, follow = true }), { description = "Move window to workspace " .. i })
end

-- Resize submap (similar to i3 resize mode)
register_bind(mainMod .. " + R", hl.dsp.submap("resize"), { description = "Enter layout resize mode" })
hl.define_submap("resize", function()
    register_bind(mainMod .. " + left", hl.dsp.window.resize({ x = -10, y = 0, relative = true }), { repeating = true, description = "Resize layout left" }, "resize")
    register_bind(mainMod .. " + right", hl.dsp.window.resize({ x = 10, y = 0, relative = true }), { repeating = true, description = "Resize layout right" }, "resize")
    register_bind(mainMod .. " + up", hl.dsp.window.resize({ x = 0, y = -10, relative = true }), { repeating = true, description = "Resize layout up" }, "resize")
    register_bind(mainMod .. " + down", hl.dsp.window.resize({ x = 0, y = 10, relative = true }), { repeating = true, description = "Resize layout down" }, "resize")
    register_bind(mainMod .. " + Return", hl.dsp.submap("reset"), { description = "Exit layout resize mode" }, "resize")
    register_bind(mainMod .. " + Escape", hl.dsp.submap("reset"), { description = "Exit layout resize mode" }, "resize")
end)

-- Move active window to a different monitor
register_bind(mainMod .. " + CTRL + SHIFT + right", hl.dsp.window.move({ monitor = "+1" }), { description = "Move window to next monitor" })
register_bind(mainMod .. " + CTRL + SHIFT + left", hl.dsp.window.move({ monitor = "-1" }), { description = "Move window to previous monitor" })

-- Cycle non-empty workspaces on the current monitor
register_bind(mainMod .. " + tab", hs.dsp.focus({ workspace = "m+1" }), { description = "Focus next workspace" })
register_bind(mainMod .. " + SHIFT + tab", hs.dsp.focus({ workspace = "m-1" }), { description = "Focus previous workspace" })

-- Multi-monitor housekeeping
-- Rescue windows stranded on a workspace whose monitor went away
register_bind(mainMod .. " + SHIFT + G", hs.dsp.grab_rogue_windows(), { description = "Recover windows from missing monitor" })
-- Swap the visible workspaces between this monitor and the next
register_bind(mainMod .. " + SHIFT + O", hs.dsp.workspace.swap_monitors({ monitor1 = "current", monitor2 = "+1" }), { description = "Swap workspaces with next monitor" })
