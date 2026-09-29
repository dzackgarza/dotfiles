return {
  {
    "glacambre/firenvim",
    build = ":call firenvim#install(0)",
    config = function()
      -- Optional: configure firenvim to not take over non-textareas
      -- vim.g.firenvim_config = {
      --   globalSettings = { alt = "all" },
      --   localSettings = {
      --     [".*"] = {
      --       selector = "textarea",
      --       takeover = "always",
      --     },
      --   },
      -- }
    end,
  },
}