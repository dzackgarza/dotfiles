-- lua/shell-ninja/core/autocmds.lua

local autocmd_group = vim.api.nvim_create_augroup("CustomPythonFolds", { clear = true })

vim.api.nvim_create_autocmd("BufReadPost", {
    pattern = "*.py",
    desc = "Apply code folds after reading Python file",
    callback = function()
        vim.schedule(function()
            vim.cmd("normal! zx") -- 'zx' opens all folds and then re-closes them to the default foldlevel
        end)
    end,
    group = autocmd_group,
})
