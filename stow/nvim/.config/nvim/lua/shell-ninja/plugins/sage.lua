return {
    {
        "petRUShka/vim-sage",
        ft = { "sage", "spyx" },
        init = function()
            vim.filetype.add({
                extension = {
                    sage = "sage",
                    spyx = "sage",
                },
            })
        end,
        config = function()
            vim.treesitter.language.register("python", "sage")
        end,
    },
}
