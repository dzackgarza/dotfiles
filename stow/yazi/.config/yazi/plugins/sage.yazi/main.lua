local M = {}

function M:peek(job)
	local start_line = job.skip + 1
	local end_line = job.skip + job.area.h

	local child, err = Command("bat")
		:arg("--color=always")
		:arg("--style=plain")
		:arg("--language=python")
		:arg("--line-range")
		:arg(string.format("%d:%d", start_line, end_line))
		:arg(tostring(job.file.path))
		:stdout(Command.PIPED)
		:stderr(Command.PIPED)
		:spawn()

	if not child then
		return
	end

	local output, err = child:wait_with_output()
	if not output or not output.status.success then
		return
	end

	local text = ui.Text.parse(output.stdout)
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
