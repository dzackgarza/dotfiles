-- Regression: pressing Super+N twice must stay on workspace N (binds.workspace_back_and_forth = 0).
-- Run inside the live compositor: hyprctl repl -- "$(cat confs/workspace_focus_test.lua)"
local focus = dofile(os.getenv("HOME") .. "/.config/hypr/confs/workspace_focus.lua")
local function active() return hl.get_active_monitor().active_workspace.id end
local start = active()

focus(2)()
focus(1)()
assert(active() == 1, "setup: expected workspace 1, got " .. active())
focus(1)()
local after_second_press = active()

focus(start)()
assert(after_second_press == 1, "second Super+1 on workspace 1 moved to workspace " .. after_second_press)
return "ok"
