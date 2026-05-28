-- normalize_fenced_divs.lua
-- Normalize fenced div layout: opening fence on own line, content
-- starts on next line, closing fence on own line. No depth-based
-- fence length growth.

function Div(el)
  local parts = {}
  for _, cls in ipairs(el.classes) do
    table.insert(parts, "." .. cls)
  end
  for k, v in pairs(el.attributes) do
    table.insert(parts, k .. '="' .. v .. '"')
  end
  if el.identifier ~= "" then
    table.insert(parts, "#" .. el.identifier)
  end
  local open_fence = ":::" .. table.concat(parts, " ")

  local body = pandoc.write(pandoc.Pandoc(el.content), "markdown+wikilinks_title_after_pipe", {wrap_text = "preserve"})
  -- Strip trailing whitespace/newlines from body
  body = body:gsub("%s+$", "")

  return pandoc.RawBlock("markdown", open_fence .. "\n" .. body .. "\n:::")
end
