-- Pandoc Preview: sends buffer content to preview server on text change.
-- Activated only when PANDOC_PREVIEW_PORT env var is set.

local port = vim.env.PANDOC_PREVIEW_PORT
if not port then return end

port = tonumber(port)

local function send_buffer_update()
  local lines = vim.api.nvim_buf_get_lines(0, 0, -1, false)
  local body = table.concat(lines, '\n')
  if #body == 0 then return end

  local request = string.format(
    'POST /api/buffer-update HTTP/1.1\r\nHost: localhost:%d\r\nContent-Type: text/plain\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s',
    port, #body, body
  )

  local tcp = vim.loop.new_tcp()
  tcp:connect('127.0.0.1', port, function(err)
    if err then
      tcp:close()
      return
    end
    tcp:write(request, function()
      tcp:shutdown()
      tcp:close()
    end)
  end)
end

local timer = vim.loop.new_timer()

vim.api.nvim_create_autocmd({ 'TextChanged', 'TextChangedI' }, {
  callback = function()
    timer:stop()
    timer:start(200, 0, vim.schedule_wrap(send_buffer_update))
  end,
})

-- Send initial content after nvim finishes loading.
-- Use vim.schedule (not vim.defer_fn) to avoid races where the event loop
-- is blocked by terminal-DSR detection in PTY mode, which can delay
-- deferred functions by several seconds, by which time the current
-- buffer may have changed.
vim.api.nvim_create_autocmd('VimEnter', {
  once = true,
  callback = function()
    vim.schedule(send_buffer_update)
  end,
})
