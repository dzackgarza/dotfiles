----------------
-- ANIMATIONS --
----------------

hl.config({ animations = { enabled = true } })

hl.curve("overshot", { type = "bezier", points = { { 0.13, 0.99 }, { 0.29, 1.15 } } })
hl.curve("win", { type = "bezier", points = { { 0.15, 0.90 }, { 0.25, 1.2 } } })
hl.curve("wind", { type = "bezier", points = { { 0.05, 0.9 }, { 0.1, 1.05 } } })
hl.curve("winIn", { type = "bezier", points = { { 0.1, 1.1 }, { 0.1, 1.1 } } })
hl.curve("winOut", { type = "bezier", points = { { 0.3, -0.3 }, { 0, 1 } } })
hl.curve("liner", { type = "bezier", points = { { 1, 1 }, { 1, 1 } } })

hl.animation({ leaf = "windowsIn", enabled = true, speed = 5, bezier = "overshot", style = "slide" })
hl.animation({ leaf = "windowsOut", enabled = true, speed = 5, bezier = "overshot", style = "slide" })
hl.animation({ leaf = "windowsMove", enabled = true, speed = 5, bezier = "wind", style = "slide" })
hl.animation({ leaf = "border", enabled = true, speed = 1, bezier = "liner" })
hl.animation({ leaf = "fade", enabled = true, speed = 10, bezier = "default" })
hl.animation({ leaf = "workspaces", enabled = true, speed = 5, bezier = "overshot", style = "slide" })
hl.animation({ leaf = "layersIn", enabled = true, speed = 4, bezier = "overshot", style = "slide" })
hl.animation({ leaf = "layersOut", enabled = true, speed = 7, bezier = "overshot", style = "slide 10%" })
