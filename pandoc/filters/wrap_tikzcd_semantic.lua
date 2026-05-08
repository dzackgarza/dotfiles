-- resources/filters/wrap_tikzcd_semantic.lua
-- Normalizes tikzcd environments by wrapping them in displaymath.

local function starts_with(start, str)
  return str:sub(1, #start) == start
end

function RawBlock(el)
  if el.format == 'latex' and starts_with('\\begin{tikzcd}', el.text) then
    -- Wrap in DisplayMath
    return pandoc.Para({pandoc.Math('DisplayMath', el.text)})
  else
    return el
  end
end
