-- Focus the Nth workspace of the current monitor (hyprsplit numbering).
local hs = require("hyprsplit")

return function(n)
    return hs.dsp.focus({ workspace = n })
end
