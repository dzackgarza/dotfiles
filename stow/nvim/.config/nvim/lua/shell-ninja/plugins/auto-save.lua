return {
    "Pocco81/auto-save.nvim",
    config = function()
        require("auto-save").setup({
            -- milliseconds between automatic saves
            debounce_delay = 50000,
        })
    end,
}
