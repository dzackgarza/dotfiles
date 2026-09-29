--------------
-- SETTINGS --
--------------

hl.config({
    input = {
        kb_layout = "us",
        kb_variant = "",
        kb_model = "",
        kb_options = "caps:swapescape", -- global caps/escape swap for all keyboards
        kb_rules = "",
        repeat_rate = 50,
        repeat_delay = 300,

        numlock_by_default = true,
        left_handed = false,
        follow_mouse = 1,
        float_switch_override_focus = false,

        touchpad = {
            disable_while_typing = true,
            natural_scroll = true,
            clickfinger_behavior = false,
            middle_button_emulation = true,
            tap_to_click = true,
            drag_lock = false,
        },

        sensitivity = 0, -- -1.0 - 1.0, 0 means no modification.
    },

    gestures = {
        workspace_swipe_distance = 400,
        workspace_swipe_invert = true,
        workspace_swipe_min_speed_to_force = 30,
        workspace_swipe_cancel_ratio = 0.5,
        workspace_swipe_create_new = true,
        workspace_swipe_forever = true,
    },

    misc = {
        disable_hyprland_logo = true,
        disable_splash_rendering = true,
        vrr = 2,
        mouse_move_enables_dpms = true,
        enable_swallow = false,
        focus_on_activate = false,
        initial_workspace_tracking = 0,
        middle_click_paste = false,
    },

    dwindle = {
        preserve_split = true, -- you probably want this
    },

    master = {
        new_status = "master",
    },

    binds = {
        workspace_back_and_forth = false,
        allow_workspace_cycles = true,
        pass_mouse_when_bound = false,
        movefocus_cycles_fullscreen = true,
    },

    -- Could help when scaling and not pixelating
    xwayland = {
        enabled = true,
        force_zero_scaling = true,
    },

    cursor = {
        sync_gsettings_theme = true,
        no_hardware_cursors = 2,
        enable_hyprcursor = true,
        warp_on_change_workspace = 2,
        no_warps = true,
    },
})

-- Three-finger left/right swipe changes workspace. The `gestures` block above
-- only tunes this gesture; the call below is what binds it.
hl.gesture({ fingers = 3, direction = "horizontal", action = "workspace" })
