return {
  "stevearc/aerial.nvim",
  dependencies = { "nvim-tree/nvim-web-devicons" },
  cmd = { "AerialToggle", "AerialOpen", "AerialNavToggle" },
  keys = {
    {
      ",o",
      function()
        require("aerial").toggle({ focus = true, direction = "float" })
      end,
      desc = "Aerial Outline (float)",
      silent = true,
    },
    { "<leader>an", "<cmd>AerialNavToggle<cr>", desc = "Aerial Nav", silent = true },
  },
  opts = {
    layout = {
      default_direction = "right",
      placement = "edge",
      width = 0.35,
      min_width = 40,
    },
    backends = { "lsp", "treesitter", "python" },
    filter_kind = {
      python = { "Class", "Function", "Method" },
      markdown = false,
    },
    manage_folds = false, -- handled by nvim-ufo
    link_folds_to_tree = true,
    link_tree_to_folds = true,
    show_guides = true,
  },
}
