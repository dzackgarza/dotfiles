import XMonad
import XMonad.Hooks.ManageDocks     -- For avoidStruts
import XMonad.Layout.NoBorders      -- Remove borders from fullscreen floats
import XMonad.Layout.Spacing        -- Bezel / Buffer between tiles
import XMonad.Util.EZConfig

import XMonad.Util.Scratchpad

import XMonad.Prompt
import XMonad.Prompt.Shell

import qualified XMonad.StackSet as W
import qualified Data.Map as M

import XMonad.Hooks.EwmhDesktops
import System.Exit (exitWith, ExitCode(ExitSuccess))

myTerminal = "lxterminal"

myWorkspaces = ["term", "web", "dev", "media", "stats", "chat", "???"]

myLayout = tiled ||| Mirror tiled ||| Full
    where
        tiled = Tall 1 (3/100) (3/5)

main =
  xmonad $ ewmh defaultConfig {
    terminal            = myTerminal
  , layoutHook          = spacing 5 $ avoidStruts $ smartBorders myLayout
  , workspaces          = myWorkspaces
  , borderWidth         = 1
  , normalBorderColor   = "#000000"
  , focusedBorderColor  = "#ff3300"
  , manageHook          = myManageHook
  , handleEventHook     = handleEventHook defaultConfig <+> fullscreenEventHook
  }
  `additionalKeys`
  [ ((mod4Mask .|. shiftMask, xK_q), killAndExit)     --Quit xmonad
  , ((mod4Mask, xK_Return)        , spawn myTerminal)
  , ((mod4Mask, xK_F2)            , shellPrompt myXPConfig)
  ]
    where
      killAndExit =
        io (exitWith ExitSuccess)

myManageHook = manageDocks <+> composeAll
  [ className =? "Tilda" --> doFloat
  ]

-- Prompt theme
myXPConfig :: XPConfig
myXPConfig = defaultXPConfig
	{ font              = dzenFont
	, bgColor           = colorBlack
	, fgColor           = colorWhite
	, bgHLight          = colorBlue
	, fgHLight          = colorBlack
	, borderColor       = colorGrayAlt
	, promptBorderWidth = 1
	, height            = panelHeight
	, position          = Top
	, historySize       = 100
	, historyFilter     = deleteConsecutive
	, autoComplete      = Nothing
	}

-- Colors, fonts and paths
dzenFont       = "-*-montecarlo-medium-r-normal-*-11-*-*-*-*-*-*-*"
colorBlack     = "#020202" --Background
colorBlackAlt  = "#1c1c1c" --Black Xdefaults
colorGray      = "#444444" --Gray
colorGrayAlt   = "#101010" --Gray dark
colorGrayAlt2  = "#404040"
colorGrayAlt3  = "#252525"
colorWhite     = "#a9a6af" --Foreground
colorWhiteAlt  = "#9d9d9d" --White dark
colorWhiteAlt2 = "#b5b3b3"
colorWhiteAlt3 = "#707070"
colorMagenta   = "#8e82a2"
colorBlue      = "#44aacc"
colorBlueAlt   = "#3955c4"
colorRed       = "#f7a16e"
colorRedAlt    = "#e0105f"
colorGreen     = "#66ff66"
colorGreenAlt  = "#558965"
panelHeight    = 16   --height of top and bottom panels
