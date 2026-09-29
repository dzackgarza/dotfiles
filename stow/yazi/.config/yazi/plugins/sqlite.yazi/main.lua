local M = {}

-- Previewer for SQLite databases, mirroring ~/.config/ranger/scope.sh

local function query(db, sql)
	local child = Command("sqlite3")
		:arg(db)
		:arg(sql)
		:stdout(Command.PIPED)
		:stderr(Command.PIPED)
		:spawn()
	if not child then
		return nil
	end
	local output = child:wait_with_output()
	if not output or not output.status.success then
		return nil
	end
	return output.stdout:gsub("%s+$", "")
end

function M:peek(job)
	local db = tostring(job.file.path)
	local lines = { "=== Database Info ===" }

	local count = query(db, "SELECT 'Tables: ' || COUNT(*) FROM sqlite_master WHERE type='table';")
	if not count then
		return
	end
	lines[#lines + 1] = count

	local tables = query(db, "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
	if not tables then
		return
	end

	lines[#lines + 1] = ""
	lines[#lines + 1] = "=== Tables ==="
	for table in tables:gmatch("[^\n]+") do
		local rows = query(db, string.format('SELECT COUNT(*) FROM "%s";', table))
		lines[#lines + 1] = string.format("%s: %s rows", table, rows or "?")
	end

	local schema = query(db, ".schema")
	lines[#lines + 1] = ""
	lines[#lines + 1] = "=== Schema ==="
	if schema then
		for l in schema:gmatch("[^\n]+") do
			lines[#lines + 1] = l
		end
	end

	local text = ui.Text.parse(table.concat(lines, "\n"))
	ya.preview_widget(job, text:area(job.area))
end

return M
