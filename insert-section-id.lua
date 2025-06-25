local header_stack = {}

function Header(el)
  local level = el.level
  local id = el.identifier or ""

  -- Update the header_stack at the current level
  header_stack[level] = id
  -- Remove deeper levels (headers below current level)
  for i = level + 1, #header_stack do
    header_stack[i] = nil
  end

  -- Collect all ancestor IDs (levels 1 to level-1)
  local ancestors = {}
  for i = 1, level - 1 do
    if header_stack[i] and header_stack[i] ~= "" then
      table.insert(ancestors, header_stack[i])
    end
  end

  -- Only proceed if current header has an ID
  if id ~= "" then
    local display_ids = ""
    if #ancestors > 0 then
      display_ids = table.concat(ancestors, "/") .. "/"
    end
    display_ids = display_ids .. id

    -- Append superscript with spacing, gray color, tiny, monospace, square brackets
    local latex = string.format("\\textsuperscript{\\,\\,\\textcolor{gray}{\\tiny\\texttt{[%s]}}}", display_ids)
    table.insert(el.content, pandoc.RawInline("latex", latex))
  end

  return el
end

