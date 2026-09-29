local M = {}

-- Previewer for NumPy .npy files, mirroring ~/.config/ranger/scope.sh

function M:peek(job)
	local start_line = job.skip + 1
	local end_line = job.skip + job.area.h

	local home = os.getenv("HOME") or "/home/dzack"
	local script = home .. "/.config/yazi/plugins/npy.yazi/npy_preview.py"

	local child = Command("python3")
		:arg(script)
		:arg(tostring(job.file.path))
		:arg(tostring(start_line))
		:arg(tostring(end_line))
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
