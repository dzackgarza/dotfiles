-- Reads hyprlang "$name = value" assignments out of the .conf files that are
-- still owned by shell scripts, so those scripts keep working unchanged:
--   scripts/settings.sh   sed-edits confs/configs.conf ($border, $rounding, ...)
--   scripts/theme_select.sh symlinks confs/themes/<Theme>.conf -> confs/decoration.conf
-- The five themes differ ONLY in these variables, so reading them is enough to
-- keep theme switching working without porting each theme to Lua.

---@param path string
---@return table<string, string|number>
local function read_vars(path)
    local vars = {}
    local f = io.open(path, "r")
    if not f then
        return vars
    end
    for line in f:lines() do
        local k, v = line:match("^%s*%$([%w_]+)%s*=%s*(.-)%s*$")
        if k then
            vars[k] = tonumber(v) or v
        end
    end
    f:close()
    return vars
end

local hypr = os.getenv("HOME") .. "/.config/hypr"

return {
    read_vars = read_vars,
    -- ponytail: no trailing-comment stripping; a "#" would also eat "#rrggbb"
    -- colors. Add it only if a value ever needs an inline comment.
    cfg = read_vars(hypr .. "/confs/configs.conf"),
    theme = read_vars(hypr .. "/confs/decoration.conf"),
}
