-- normalize.lua: Pandoc AST normalizations
--
-- Optional filter that normalizes AST constructs before the writer.
-- Currently handles: SoftBreak -> Space normalization (for writerd by
-- the AST comparator), and source-position attribute stripping.
--
-- Usage:
--   pandoc input.md --lua-filter normalize.lua -t json

-- Convert SoftBreak to Space
function SoftBreak()
  return pandoc.Space()
end

-- Strip source-pos attributes from all elements
local function strip_sourcepos(el)
  if el.attributes and el.attributes["source-pos"] then
    local attrs = {}
    for k, v in pairs(el.attributes) do
      if k ~= "source-pos" then
        attrs[k] = v
      end
    end
    el.attributes = attrs
  end
  return el
end

return {
  { SoftBreak = SoftBreak },
  { traverse = "topdown",
    CodeBlock = strip_sourcepos,
    Code = strip_sourcepos,
    Header = strip_sourcepos,
    Para = strip_sourcepos,
    Plain = strip_sourcepos,
    Div = strip_sourcepos,
    Span = strip_sourcepos,
    Link = strip_sourcepos,
    Image = strip_sourcepos,
    Figure = strip_sourcepos,
    Table = strip_sourcepos,
    Math = strip_sourcepos,
    RawBlock = strip_sourcepos,
    RawInline = strip_sourcepos,
  }
}
