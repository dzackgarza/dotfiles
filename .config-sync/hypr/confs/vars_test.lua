-- Self-check for the hyprlang $var reader. Run: lua confs/vars_test.lua
-- Fails loudly if the parser stops reading the files the shell scripts write.
local vars = dofile(os.getenv("HOME") .. "/.config/hypr/confs/vars.lua")

local tmp = os.tmpname()
local f = assert(io.open(tmp, "w"))
f:write("$opacity_act = 0.9\n")
f:write("  $rounding=8\n") -- leading space, no spaces around '='
f:write("$activeCol = rgba(b4b9bcFF)\n")
f:write("# $ignored = 1\n") -- comment line
f:write("general { gaps_in = 5 }\n") -- non-$ line
f:close()

local v = vars.read_vars(tmp)
os.remove(tmp)

assert(v.opacity_act == 0.9, "numeric value should be a number, got " .. tostring(v.opacity_act))
assert(v.rounding == 8, "must handle no spaces around '=', got " .. tostring(v.rounding))
assert(v.activeCol == "rgba(b4b9bcFF)", "string value mangled: " .. tostring(v.activeCol))
assert(v.ignored == nil, "commented-out vars must not be read")
assert(v.gaps_in == nil, "only $-prefixed assignments are vars")

-- The live files must actually yield the values the config depends on.
for _, k in ipairs({ "opacity_act", "opacity_deact", "rounding", "border", "inner_gap", "outer_gap", "blur_size", "blur_pass", "shadow_range" }) do
    assert(vars.cfg[k] ~= nil, "confs/configs.conf is missing $" .. k)
end
for _, k in ipairs({ "activeCol", "inactiveCol", "icon", "theme", "color" }) do
    assert(vars.theme[k] ~= nil, "confs/decoration.conf is missing $" .. k)
end

print("vars.lua OK")
