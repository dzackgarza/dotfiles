return {
  "bassamsdata/namu.nvim",
  cmd = "Namu",
  keys = {
    { "<leader>ss", "<cmd>Namu symbols<cr>", desc = "Symbols (buffer)", silent = true },
    { "<leader>sw", "<cmd>Namu workspace<cr>", desc = "Symbols (workspace)", silent = true },
    { "<leader>sd", "<cmd>Namu diagnostics<cr>", desc = "Diagnostics picker", silent = true },
  },
  opts = {
    namu_symbols = {
      enable = true,
      options = {
        AllowKinds = {
          python = { "Class", "Function", "Method" },
        },
      },
    },
  },
}
