return {
    "neovim/nvim-lspconfig",
    event = { "BufReadPre", "BufNewFile" },
    dependencies = {
        "hrsh7th/cmp-nvim-lsp",
        { "antosha417/nvim-lsp-file-operations", config = true },
        { "folke/neodev.nvim",                   opts = {} },
    },
    config = function()
        -- import mason_lspconfig plugin
        local mason_lspconfig = require("mason-lspconfig")

        -- import cmp-nvim-lsp plugin
        local cmp_nvim_lsp = require("cmp_nvim_lsp")
        local navic_ok, navic = pcall(require, "nvim-navic")
        local navic_preference = {
            basedpyright = 100,
            ty = 10,
        }
        local function should_override_navic(current, incoming)
            local current_score = navic_preference[current] or 0
            local incoming_score = navic_preference[incoming] or 0
            return incoming_score > current_score
        end
        local function attach_navic_once(client, bufnr)
            if not navic_ok or not client.server_capabilities.documentSymbolProvider then
                return
            end
            local ok, current = pcall(vim.api.nvim_buf_get_var, bufnr, "navic_client_name")
            if ok then
                if current == client.name then
                    return
                end
                if should_override_navic(current, client.name) then
                    pcall(vim.api.nvim_buf_del_var, bufnr, "navic_client_name")
                    pcall(vim.api.nvim_buf_del_var, bufnr, "navic_client_id")
                else
                    return
                end
            end
            navic.attach(client, bufnr)
        end

        local keymap = vim.keymap -- for conciseness

        vim.api.nvim_create_autocmd("LspAttach", {
            group = vim.api.nvim_create_augroup("UserLspConfig", {}),
            callback = function(ev)
                -- Buffer local mappings.
                -- See `:help vim.lsp.*` for documentation on any of the below functions
                local opts = { buffer = ev.buf, silent = true }

                -- set keybinds
                opts.desc = "Show LSP references"
                keymap.set("n", "gR", "<cmd>Telescope lsp_references<CR>", opts) -- show definition, references

                opts.desc = "Go to declaration"
                keymap.set("n", "gD", vim.lsp.buf.declaration, opts) -- go to declaration

                opts.desc = "Show LSP definitions"
                keymap.set("n", "gd", "<cmd>Telescope lsp_definitions<CR>", opts) -- show lsp definitions

                opts.desc = "Show LSP implementations"
                keymap.set("n", "gi", "<cmd>Telescope lsp_implementations<CR>", opts) -- show lsp implementations

                opts.desc = "Show LSP type definitions"
                keymap.set("n", "gt", "<cmd>Telescope lsp_type_definitions<CR>", opts) -- show lsp type definitions

                opts.desc = "See available code actions"
                keymap.set({ "n", "v" }, "<leader>ca", function()
                    local ok = pcall(vim.cmd, "Lspsaga code_action")
                    if not ok then
                        vim.lsp.buf.code_action()
                    end
                end, opts) -- prefer lspsaga UI for quick fixes, fallback to builtin

                opts.desc = "Smart rename"
                keymap.set("n", "<leader>rn", vim.lsp.buf.rename, opts) -- smart rename

                opts.desc = "Show buffer diagnostics"
                keymap.set("n", "<leader>D", "<cmd>Telescope diagnostics bufnr=0<CR>", opts) -- show  diagnostics for file

                opts.desc = "Show line diagnostics"
                keymap.set("n", "<leader>d", vim.diagnostic.open_float, opts) -- show diagnostics for line

                opts.desc = "Go to previous diagnostic"
                keymap.set("n", "[d", function()
                    vim.diagnostic.goto_prev({ float = true })
                end, opts)

                opts.desc = "Go to next diagnostic"
                keymap.set("n", "]d", function()
                    vim.diagnostic.goto_next({ float = true })
                end, opts)

                opts.desc = "Show documentation for what is under cursor"
                keymap.set("n", "K", function()
                    local ok, ufo = pcall(require, "ufo")
                    if ok then
                        local winid = ufo.peekFoldedLinesUnderCursor()
                        if winid then
                            return
                        end
                    end
                    vim.lsp.buf.hover()
                end, opts) -- show documentation for what is under cursor, but peek folds first when available

                opts.desc = "Restart LSP"
                keymap.set("n", "<leader>rs", ":LspRestart<CR>", opts) -- mapping to restart lsp if necessary

                if navic_ok and ev.data and ev.data.client_id then
                    local client = vim.lsp.get_client_by_id(ev.data.client_id)
                    if client then
                        attach_navic_once(client, ev.buf)
                    end
                end
            end,
        })

        -- used to enable autocompletion (assign to every lsp server config)
        local capabilities = cmp_nvim_lsp.default_capabilities()
        capabilities.textDocument.foldingRange = {
            dynamicRegistration = false,
            lineFoldingOnly = true,
        }

        -- Change the Diagnostic symbols in the sign column (gutter)
        vim.diagnostic.config({
            signs = {
                text = {
                    [vim.diagnostic.severity.ERROR] = " ",
                    [vim.diagnostic.severity.WARN] = " ",
                    [vim.diagnostic.severity.HINT] = "󰠠 ",
                    [vim.diagnostic.severity.INFO] = " ",
                },
            },
        })

        --Configure svelte server with custom settings
        --vim.lsp.config("svelte", {
        --cmd = { "svelte-language-server", "--stdio" },
        --filetypes = { "svelte" },
        --root_dir = vim.fs.dirname(vim.fs.find({ "package.json", "svelte.config.js" }, { upward = true })[1]),
        --settings = {},
        --on_attach = function(client, bufnr)
        --on_attach(client, bufnr)
        --vim.api.nvim_create_autocmd("BufWritePost", {
        --pattern = { "*.js", "*.ts" },
        --callback = function(ctx)
        --Here use ctx.match instead of ctx.file
        --client.notify("$/onDidChangeTsOrJsFile", { uri = ctx.match })
        --end,
        --})
        --end,
        --capabilities = capabilities,
        --})

        -- Configure emmet language server
        vim.lsp.config("emmet_ls", {
            cmd = { "emmet-ls", "--stdio" },
            filetypes = { "html", "typescriptreact", "javascriptreact", "css", "sass", "scss", "less", "svelte" },
            init_options = {
                html = {
                    options = {
                        ["bem.enabled"] = true,
                    },
                },
            },
            on_attach = on_attach,
            capabilities = capabilities,
        })

        -- Configure marksman for Markdown
        vim.lsp.config("marksman", {
            on_attach = on_attach,
            capabilities = capabilities,
        })

        -- Configure lua server (with special settings)
        --vim.lsp.config("lua_ls", {
        --cmd = { "lua-language-server" },
        --filetypes = { "lua" },
        --root_dir = vim.fs.dirname(vim.fs.find({ ".luarc.json", ".luarc.jsonc", ".git" }, { upward = true })[1]),
        --settings = {
        --Lua = {
        --make the language server recognize "vim" global
        --diagnostics = {
        --globals = { "vim" },
        --},
        --completion = {
        --callSnippet = "Replace",
        --},
        --},
        --},
        --on_attach = on_attach,
        --capabilities = capabilities,
        --})

        -- Configure basedpyright for Python
        vim.lsp.config("basedpyright", {
            cmd = { "basedpyright-langserver", "--stdio" },
            filetypes = { "python" },
            root_markers = {
                "pyproject.toml",
                "setup.py",
                "setup.cfg",
                "requirements.txt",
                "Pipfile",
                "pyrightconfig.json",
                ".git",
            },
            settings = {
                python = {
                    pythonPath = "/home/dzack/gitclones/sage/.venv/bin/python",
                },
                basedpyright = {
                    analysis = {
                        autoImportCompletions = true,
                        autoSearchPaths = true,
                        extraPaths = {
                            "/home/dzack/gitclones/sage/src",
                            "/home/dzack/gitclones/sage/.venv/lib/python3.13/site-packages",
                            "/home/dzack/gitclones/sage/build/cp313/src",
                        },
                        stubPath = "/home/dzack/gitclones/sage/typings",
                        diagnosticMode = "workspace",
                        typeCheckingMode = "all",
                        useLibraryCodeForTypes = true,
                        diagnosticSeverityOverrides = {
                            reportAny = "none",
                            reportExplicitAny = "none",
                            reportConstantRedefinition = "none",
                            reportUnusedFunction = "none",
                            reportUnusedImport = "none",
                            reportImplicitOverride = "none",
                            reportImplicitRelativeImport = "none",
                            reportWildcardImportFromLibrary = "none",
                            reportUnusedCallResult = "none"
                        }
                    },
                },
            },
            on_attach = on_attach,
            capabilities = capabilities,
        })

        vim.lsp.config("ty", {
            settings = {
                ty = {
                    -- ty language server settings go here
                },
            },
        })

        -- Enable each configured server
        vim.lsp.enable("ty")
        --vim.lsp.enable("svelte")
        --vim.lsp.enable("graphql")
        vim.lsp.enable("emmet_ls")
        vim.lsp.enable("marksman")
        vim.lsp.enable("basedpyright")
    end,
}
