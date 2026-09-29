local M = {}

-- Previewer for GAP files, mirroring ~/.config/ranger/scope.sh

function M:peek(job)
	local start_line = job.skip + 1
	local end_line = job.skip + job.area.h

	local child = Command("pygmentize")
		:arg("-f")
		:arg("terminal256")
		:arg("-O")
		:arg("style=monokai")
		:arg("-l")
		:arg("gap")
		:arg(tostring(job.file.path))
		:stdout(Command.PIPED)
		:stderr(Command.PIPED)
		:spawn()
	if not child then
		return
	end

	local output = child:wait_with_output()
	if not output or not output.status.success then
		return
	end

	local lines = {}
	for l in output.stdout:gmatch("[^\n]*") do
		lines[#lines + 1] = l
	end
	if lines[#lines] == "" then
		table.remove(lines)
	end

	local sliced = {}
	for i = start_line, math.min(end_line, #lines) do
		sliced[#sliced + 1] = lines[i]
	end

	local text = ui.Text.parse(table.concat(sliced, "\n"))
	ya.preview_widget(job, text:area(job.area))
end

function M:seek(job)
	local h = cx.active.current.hovered
	if not h or h.url ~= job.file.url then
		return
	end

	local step = math.floor(job.units)
	local new_skip = math.max(0, job.skip + step)
	ya.emit("peek", { new_skip, only_if = job.file.url })
end

return M
