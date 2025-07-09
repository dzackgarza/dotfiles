-- Pandoc Lua filter: extract LaTeX environments and wrap as ```latex code blocks
function RawBlock(el)
  if el.format:match("tex") then
    -- Wrap LaTeX block environments in a code block
    return pandoc.CodeBlock(el.text, {class = "latex"})
  end
end

function RawInline(el)
  if el.format:match("tex") then
    -- Wrap inline LaTeX in a code block (rare, but for robustness)
    return pandoc.CodeBlock(el.text, {class = "latex"})
  end
end 