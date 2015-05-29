import XMonad
import XMonad.Hooks.ManageDocks     -- For avoidStruts
import XMonad.Layout.NoBorders      -- Remove borders from fullscreen floats
import XMonad.Layout.Spacing        -- Bezel / Buffer between tiles

myWorkspaces = ["term", "web", "dev", "media", "stats", "chat", "???"]

myLayout = tiled ||| Mirror tiled ||| Full
    where
        tiled = Tall 1 (3/100) (3/5)

main =
    xmonad $ defaultConfig {
    terminal            = "lxterminal",
    modMask             = mod4Mask,
    layoutHook          = spacing 2 $ avoidStruts $ smartBorders myLayout,
    workspaces          = myWorkspaces,
    borderWidth         = 1,
    normalBorderColor   = "#000000",
    focusedBorderColor  = "#49455C"
    }
