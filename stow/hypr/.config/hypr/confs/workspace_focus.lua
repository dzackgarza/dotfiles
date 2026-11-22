-- Focus the Nth workspace of the current monitor (hyprsplit numbering).
--
-- hyprsplit's dsp.focus tests `hl.get_config("binds.workspace_back_and_forth")`
-- for truthiness. That call returns the number 0 when the option is off, and Lua
-- treats 0 as true, so repeated presses toggle to the previous workspace. This
-- is the same logic minus that check, so focusing the active workspace is a no-op.
local hs = require("hyprsplit")

return function(n)
    return function()
        local ws_string = hs.get_workspace_string(tostring(n))
        local ws = hl.get_workspace(ws_string)
        local monitor = hl.get_active_monitor()
        if ws and monitor and ws.monitor.id ~= monitor.id then
            hs.ensure_good_workspaces()
        end
        hl.dispatch(hl.dsp.focus({ workspace = ws_string, on_current_monitor = true }))
    end
end
