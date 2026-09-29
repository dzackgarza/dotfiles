return {
    "stevearc/conform.nvim",
    event = { "BufReadPre", "BufNewFile" },
    config = function()
        local conform = require("conform")

        conform.setup({
            formatters_by_ft = {
                javascript = { "prettier" },
                typescript = { "prettier" },
                javascriptreact = { "prettier" },
                typescriptreact = { "prettier" },
                svelte = { "prettier" },
                css = { "prettier" },
                html = { "prettier" },
                json = { "prettier" },
                yaml = { "prettier" },
                markdown = { "prettier" },
                graphql = { "prettier" },
                liquid = { "prettier" },
                lua = { "stylua" },
                python = { "autoflake", "isort", "black" },
            },
            formatters = {
                autoflake = {
                    inherit = true,
                    prepend_args = { "--remove-all-unused-imports", "--remove-unused-variables" },
                },
            },
            format_on_save = function(bufnr)
                -- disable autoformat-on-save for markdown (manual only via <leader>mp)
                if vim.bo[bufnr].filetype == "markdown" then
                    return
                end
                return {
                    lsp_fallback = true,
                    async = false,
                    timeout_ms = 1000,
                }
            end,
        })

        vim.keymap.set({ "n", "v" }, "<leader>mp", function()
            conform.format({
                lsp_fallback = true,
                async = false,
                timeout_ms = 1000,
            })
        end, { desc = "Format file or range (in visual mode)" })
    end,
}
