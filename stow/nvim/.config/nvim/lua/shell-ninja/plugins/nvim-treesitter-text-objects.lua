local select_maps = {
    ["a="] = { "@assignment.outer", "Select outer part of an assignment" },
    ["i="] = { "@assignment.inner", "Select inner part of an assignment" },
    ["l="] = { "@assignment.lhs", "Select left hand side of an assignment" },
    ["r="] = { "@assignment.rhs", "Select right hand side of an assignment" },

    ["a:"] = { "@property.outer", "Select outer part of an object property" },
    ["i:"] = { "@property.inner", "Select inner part of an object property" },
    ["l:"] = { "@property.lhs", "Select left part of an object property" },
    ["r:"] = { "@property.rhs", "Select right part of an object property" },

    ["aa"] = { "@parameter.outer", "Select outer part of a parameter/argument" },
    ["ia"] = { "@parameter.inner", "Select inner part of a parameter/argument" },

    ["ai"] = { "@conditional.outer", "Select outer part of a conditional" },
    ["ii"] = { "@conditional.inner", "Select inner part of a conditional" },

    ["al"] = { "@loop.outer", "Select outer part of a loop" },
    ["il"] = { "@loop.inner", "Select inner part of a loop" },

    ["af"] = { "@call.outer", "Select outer part of a function call" },
    ["if"] = { "@call.inner", "Select inner part of a function call" },

    ["am"] = { "@function.outer", "Select outer part of a method/function definition" },
    ["im"] = { "@function.inner", "Select inner part of a method/function definition" },

    ["ac"] = { "@class.outer", "Select outer part of a class" },
    ["ic"] = { "@class.inner", "Select inner part of a class" },
}

local swap_next_maps = {
    ["<leader>na"] = "@parameter.inner",
    ["<leader>n:"] = "@property.outer",
    ["<leader>nm"] = "@function.outer",
}

local swap_previous_maps = {
    ["<leader>pa"] = "@parameter.inner",
    ["<leader>p:"] = "@property.outer",
    ["<leader>pm"] = "@function.outer",
}

-- key = { capture, description, query group }
local move_maps = {
    goto_next_start = {
        ["]f"] = { "@call.outer", "Next function call start" },
        ["]m"] = { "@function.outer", "Next method/function def start" },
        ["]c"] = { "@class.outer", "Next class start" },
        ["]i"] = { "@conditional.outer", "Next conditional start" },
        ["]l"] = { "@loop.outer", "Next loop start" },
        ["]s"] = { "@local.scope", "Next scope", "locals" },
        ["]z"] = { "@fold", "Next fold", "folds" },
    },
    goto_next_end = {
        ["]F"] = { "@call.outer", "Next function call end" },
        ["]M"] = { "@function.outer", "Next method/function def end" },
        ["]C"] = { "@class.outer", "Next class end" },
        ["]I"] = { "@conditional.outer", "Next conditional end" },
        ["]L"] = { "@loop.outer", "Next loop end" },
    },
    goto_previous_start = {
        ["[f"] = { "@call.outer", "Prev function call start" },
        ["[m"] = { "@function.outer", "Prev method/function def start" },
        ["[c"] = { "@class.outer", "Prev class start" },
        ["[i"] = { "@conditional.outer", "Prev conditional start" },
        ["[l"] = { "@loop.outer", "Prev loop start" },
    },
    goto_previous_end = {
        ["[F"] = { "@call.outer", "Prev function call end" },
        ["[M"] = { "@function.outer", "Prev method/function def end" },
        ["[C"] = { "@class.outer", "Prev class end" },
        ["[I"] = { "@conditional.outer", "Prev conditional end" },
        ["[L"] = { "@loop.outer", "Prev loop end" },
    },
}

return {
    "nvim-treesitter/nvim-treesitter-textobjects",
    branch = "main",
    dependencies = { "nvim-treesitter/nvim-treesitter" },
    event = "VeryLazy",
    config = function()
        require("nvim-treesitter-textobjects").setup({
            select = { lookahead = true },
            move = { set_jumps = true },
        })

        local select = require("nvim-treesitter-textobjects.select")
        for key, spec in pairs(select_maps) do
            vim.keymap.set({ "x", "o" }, key, function()
                select.select_textobject(spec[1], "textobjects")
            end, { desc = spec[2] })
        end

        local swap = require("nvim-treesitter-textobjects.swap")
        for key, capture in pairs(swap_next_maps) do
            vim.keymap.set("n", key, function()
                swap.swap_next(capture)
            end, { desc = "Swap " .. capture .. " with next" })
        end
        for key, capture in pairs(swap_previous_maps) do
            vim.keymap.set("n", key, function()
                swap.swap_previous(capture)
            end, { desc = "Swap " .. capture .. " with previous" })
        end

        local move = require("nvim-treesitter-textobjects.move")
        for fn, maps in pairs(move_maps) do
            for key, spec in pairs(maps) do
                vim.keymap.set({ "n", "x", "o" }, key, function()
                    move[fn](spec[1], spec[3] or "textobjects")
                end, { desc = spec[2] })
            end
        end

        local ts_repeat_move = require("nvim-treesitter-textobjects.repeatable_move")

        -- vim way: ; goes to the direction you were moving.
        vim.keymap.set({ "n", "x", "o" }, ";", ts_repeat_move.repeat_last_move)
        vim.keymap.set({ "n", "x", "o" }, ",", ts_repeat_move.repeat_last_move_opposite)

        vim.keymap.set({ "n", "x", "o" }, "f", ts_repeat_move.builtin_f_expr, { expr = true })
        vim.keymap.set({ "n", "x", "o" }, "F", ts_repeat_move.builtin_F_expr, { expr = true })
        vim.keymap.set({ "n", "x", "o" }, "t", ts_repeat_move.builtin_t_expr, { expr = true })
        vim.keymap.set({ "n", "x", "o" }, "T", ts_repeat_move.builtin_T_expr, { expr = true })
    end,
}
