return {
    "nvimdev/lspsaga.nvim",
    event = "LspAttach",
    dependencies = {
        "nvim-treesitter/nvim-treesitter", -- improves finder previews
        "nvim-tree/nvim-web-devicons", -- optional but we already use icons
    },
    opts = {
        code_action = {
            num_shortcut = true,
            show_server_name = true,
        },
        lightbulb = {
            enable = true,
            enable_in_insert = false,
            sign = true,
            virtual_text = false,
        },
        ui = {
            code_action = "QF",
            border = "rounded",
        },
    },
}
