-- nvim-treesitter `main` branch: a parser installer plus queries.
-- Highlighting, folding and indenting are Neovim's own (:h treesitter-highlight).
local languages = {
    "bash",
    "c",
    "cmake",
    "css",
    "dockerfile",
    "gitignore",
    "go",
    "graphql",
    "groovy",
    "html",
    "java",
    "javascript",
    "json",
    "lua",
    "make",
    "markdown",
    "markdown_inline",
    "python",
    "regex",
    "sql",
    "terraform",
    "toml",
    "tsx",
    "typescript",
    "vim",
    "vimdoc",
    "yaml",
}

return {
    "nvim-treesitter/nvim-treesitter",
    branch = "main",
    lazy = false, -- main branch does not support lazy-loading
    build = ":TSUpdate",
    config = function()
        require("nvim-treesitter").install(languages)

        vim.api.nvim_create_autocmd("FileType", {
            group = vim.api.nvim_create_augroup("shell-ninja-treesitter", { clear = true }),
            callback = function(args)
                local lang = vim.treesitter.language.get_lang(args.match)
                if not (lang and vim.treesitter.language.add(lang)) then
                    return
                end
                -- ruby and sage keep their regex syntax alongside the parser
                vim.treesitter.start(args.buf, lang)
                vim.wo[0][0].foldexpr = "v:lua.vim.treesitter.foldexpr()"
                vim.wo[0][0].foldmethod = "expr"
                if args.match ~= "ruby" then
                    vim.bo[args.buf].indentexpr = "v:lua.require'nvim-treesitter'.indentexpr()"
                end
            end,
        })
    end,
}
