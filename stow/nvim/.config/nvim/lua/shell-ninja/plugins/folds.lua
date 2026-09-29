return {
    "kevinhwang91/nvim-ufo",
    event = "BufReadPost",
    dependencies = {
        "kevinhwang91/promise-async",
    },
    opts = {
        provider_selector = function(_, filetype, _)
            local ft_map = {
                python = { "treesitter", "indent" },
                markdown = { "treesitter", "indent" },
                vim = { "indent" },
            }
            return ft_map[filetype] or { "lsp", "indent" }
        end,
    },
    keys = {
        {
            "zR",
            function()
                require("ufo").openAllFolds()
            end,
            desc = "Open all folds",
        },
        {
            "zM",
            function()
                require("ufo").closeAllFolds()
            end,
            desc = "Close all folds",
        },
        {
            "zr",
            function()
                require("ufo").openFoldsExceptKinds()
            end,
            desc = "Open folds except imports/comments",
        },
        {
            "zm",
            function()
                require("ufo").closeFoldsWith()
            end,
            desc = "Close folds (depth 0)",
        },
        {
            "zp",
            function()
                local winid = require("ufo").peekFoldedLinesUnderCursor()
                if not winid then
                    vim.lsp.buf.hover()
                end
            end,
            desc = "Peek fold or hover",
        },
    },
}
