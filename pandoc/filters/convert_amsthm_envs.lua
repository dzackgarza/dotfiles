-- Get the directory of this script to find utilities.lua relatively
local script_dir = debug.getinfo(1, "S").source:match("@(.*)[\\/]") or "."
package.path = package.path .. ';' .. script_dir .. '/?.lua;'
require "utilities"

-- In markdown, changes
--
-- :::{.theorem title="abcde" ref=:thm:123"} 
-- ...
-- :::
--
-- into 
--
-- \begin{theorem}["abcde"]
-- \label{thm:123}
-- ...
-- \end{theorem}
--
-- Supports math within the title. 

function Div(el)
  -- For markdown cleaning, just leave as-is
  if FORMAT:match 'markdown' then
    return el
  end
  --if FORMAT:match 'markdown' then
    --if el.attributes["title"]==nil then
      --return el
    --end
    --tprint(el)
    --print("---------------")
    --print(el.attributes["title"])
    --print("---------------")
    --local cont = pandoc.read(el.attributes["title"], "markdown")
    --tprint(cont)
    --print("---------------")
    --tprint(cont.blocks[1])
    --print("---------------")
    --newblock = pandoc.walk_block(cont.blocks[1], {
      --Math = function (m)
        --if m.mathtype == "InlineMath" then
          --m.text = '\\( ' .. m.text .. ' \\)'
          --return m
        --end
      --end
    --})
    --el.attributes["title"] = pandoc.utils.stringify(newblock)
    --tprint(el)
    --return el
  --end

  el.classes[#el.classes+1] = "proofenv" 

  -- Prepend to this blocks contents \begin{env}[...]\label{}...
  beginString = "\n\\begin{" .. el.classes[1] .. "}"

  if el.attributes["title"]~=nil then 
    beginString = beginString .. "[" .. el.attributes["title"] .. "]"
  end
  
  if el.attributes["ref"]~=nil then 
    beginString = beginString .. "\\label{" .. el.attributes["ref"] .. "}"
  end

  -- Prepend above string to open
  table.insert(
    el.content, 1,
    pandoc.RawBlock("latex", beginString)
  )

  -- Append at *end* of table to close
  table.insert(
      el.content,
      pandoc.RawBlock("latex", "\\end{" .. el.classes[1] .. "}")
    )

  return el
end

