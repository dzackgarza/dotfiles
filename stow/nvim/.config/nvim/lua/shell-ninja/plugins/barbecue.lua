return {
    "utilyre/barbecue.nvim",
    name = "barbecue",
    event = { "BufReadPost", "BufNewFile" },
    dependencies = {
        "SmiteshP/nvim-navic",
        "nvim-tree/nvim-web-devicons",
    },
    opts = {
        create_autocmd = true,
    },
}
