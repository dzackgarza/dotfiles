-------------
-- LAYOUTS --
-------------
-- Named tiling layouts for the layout picker. Hyprland exposes these as
-- `lua:<name>`, so a workspace rule can select one directly.
--
-- `ctx.area` is the monitor work area after gaps_out. `target:place` sets the
-- logical box; Hyprland applies gaps_in when it draws the window, so adjacent
-- cells must share edges. Do not inset the boxes: a gap makes them
-- non-adjacent for `focus({ direction = ... })`, which only links boxes whose
-- edges touch within 2 px.

hl.layout.register("grid", {
    recalculate = function(ctx)
        local n = #ctx.targets
        if n == 0 then
            return
        end

        local cols = math.ceil(math.sqrt(n))
        local rows = math.ceil(n / cols)

        for i, target in ipairs(ctx.targets) do
            local row = math.floor((i - 1) / cols)
            local col = (i - 1) % cols
            local in_row = math.min(cols, n - row * cols)
            local w = ctx.area.w / in_row
            local h = ctx.area.h / rows

            target:place({
                x = ctx.area.x + col * w,
                y = ctx.area.y + row * h,
                w = w,
                h = h,
            })
        end
    end,
})

hl.layout.register("columns", {
    recalculate = function(ctx)
        local n = #ctx.targets
        if n == 0 then
            return
        end

        local w = ctx.area.w / n
        for i, target in ipairs(ctx.targets) do
            target:place({
                x = ctx.area.x + (i - 1) * w,
                y = ctx.area.y,
                w = w,
                h = ctx.area.h,
            })
        end
    end,
})

hl.layout.register("rows", {
    recalculate = function(ctx)
        local n = #ctx.targets
        if n == 0 then
            return
        end

        local h = ctx.area.h / n
        for i, target in ipairs(ctx.targets) do
            target:place({
                x = ctx.area.x,
                y = ctx.area.y + (i - 1) * h,
                w = ctx.area.w,
                h = h,
            })
        end
    end,
})

hl.layout.register("center", {
    recalculate = function(ctx)
        local n = #ctx.targets
        if n == 0 then
            return
        end

        if n == 1 then
            ctx.targets[1]:place(ctx.area)
            return
        end

        if n == 2 then
            local w = ctx.area.w / 2
            ctx.targets[1]:place({ x = ctx.area.x, y = ctx.area.y, w = w, h = ctx.area.h })
            ctx.targets[2]:place({ x = ctx.area.x + w, y = ctx.area.y, w = w, h = ctx.area.h })
            return
        end

        local left_n = math.floor((n - 1) / 2)
        local right_n = n - 1 - left_n
        local center_w = ctx.area.w * 0.5
        local side_w = (ctx.area.w - center_w) / 2

        ctx.targets[1]:place({
            x = ctx.area.x + side_w,
            y = ctx.area.y,
            w = center_w,
            h = ctx.area.h,
        })

        for i = 1, left_n do
            local h = ctx.area.h / left_n
            ctx.targets[1 + i]:place({
                x = ctx.area.x,
                y = ctx.area.y + (i - 1) * h,
                w = side_w,
                h = h,
            })
        end

        for i = 1, right_n do
            local h = ctx.area.h / right_n
            ctx.targets[1 + left_n + i]:place({
                x = ctx.area.x + side_w + center_w,
                y = ctx.area.y + (i - 1) * h,
                w = side_w,
                h = h,
            })
        end
    end,
})
