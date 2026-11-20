-------------
-- LAYOUTS --
-------------
-- Named tiling layouts for the layout picker. Hyprland exposes these as
-- `lua:<name>`, so a workspace rule can select one directly.
--
-- `ctx.area` is the monitor work area after gaps_out. `target:place` sets the
-- logical box and does not add gaps, so each cell is inset by half of gaps_in.

local function gap_half()
    local gaps = hl.get_config("general:gaps_in")
    if type(gaps) == "table" then
        local g = tonumber(gaps.left) or tonumber(gaps.top) or 0
        return math.max(0, math.floor(g / 2))
    end
    return 5
end

local function place(target, box)
    local g = gap_half()
    target:place({
        x = box.x + g,
        y = box.y + g,
        w = math.max(1, box.w - 2 * g),
        h = math.max(1, box.h - 2 * g),
    })
end

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

            place(target, {
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
            place(target, {
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
            place(target, {
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
            place(ctx.targets[1], ctx.area)
            return
        end

        if n == 2 then
            local w = ctx.area.w / 2
            place(ctx.targets[1], { x = ctx.area.x, y = ctx.area.y, w = w, h = ctx.area.h })
            place(ctx.targets[2], { x = ctx.area.x + w, y = ctx.area.y, w = w, h = ctx.area.h })
            return
        end

        local left_n = math.floor((n - 1) / 2)
        local right_n = n - 1 - left_n
        local center_w = ctx.area.w * 0.5
        local side_w = (ctx.area.w - center_w) / 2

        place(ctx.targets[1], {
            x = ctx.area.x + side_w,
            y = ctx.area.y,
            w = center_w,
            h = ctx.area.h,
        })

        for i = 1, left_n do
            local h = ctx.area.h / left_n
            place(ctx.targets[1 + i], {
                x = ctx.area.x,
                y = ctx.area.y + (i - 1) * h,
                w = side_w,
                h = h,
            })
        end

        for i = 1, right_n do
            local h = ctx.area.h / right_n
            place(ctx.targets[1 + left_n + i], {
                x = ctx.area.x + side_w + center_w,
                y = ctx.area.y + (i - 1) * h,
                w = side_w,
                h = h,
            })
        end
    end,
})
