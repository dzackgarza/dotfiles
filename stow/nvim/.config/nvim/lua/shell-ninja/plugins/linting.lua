return {
	"mfussenegger/nvim-lint",
	event = { "BufReadPre", "BufNewFile" },
	config = function()
		local lint = require("lint")

		lint.linters_by_ft = {
			javascript = { "eslint_d" },
			typescript = { "eslint_d" },
			javascriptreact = { "eslint_d" },
			typescriptreact = { "eslint_d" },
			python = { "pylint", "mypy" },
		}

		local mypy = lint.linters.mypy
		if mypy then
			mypy.args = {
				"--follow-imports=normal",
				"--python-version=3.13.7",
				"--show-column-numbers",
				"--show-error-end",
				"--hide-error-context",
				"--no-color-output",
				"--no-error-summary",
				"--no-pretty",
			}
		end

		local pylint = lint.linters.pylint
		if pylint then
			pylint.args = {
				"--prefer-stubs",
				"-f",
				"json",
				"--from-stdin",
				function()
					return vim.api.nvim_buf_get_name(0)
				end,
			}
		end

		local lint_augroup = vim.api.nvim_create_augroup("lint", { clear = true })

		vim.api.nvim_create_autocmd({ "BufEnter", "BufWritePost", "InsertLeave" }, {
			group = lint_augroup,
			callback = function()
				lint.try_lint()
			end,
		})

		vim.keymap.set("n", "<leader>l", function()
			lint.try_lint()
		end, { desc = "Trigger linting for current file" })
	end,
}
