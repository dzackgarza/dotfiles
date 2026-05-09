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
  local envs = {
    theorem=true, lemma=true, proposition=true, corollary=true,
    proof=true, remark=true, definition=true, example=true,
    conjecture=true, claim=true, observation=true, question=true,
    problem=true, assumption=true, warning=true, exercise=true
  }
  
  local env = el.classes[1]
  if not (env and envs[env]) then
    return el
  end

  -- For markdown cleaning, just leave as-is
  if FORMAT:match 'markdown' then
    return el
  end

  if FORMAT:match 'latex' or FORMAT:match 'pdf' or FORMAT:match 'beamer' then
    local beginString = "\\begin{" .. env .. "}"
    if el.attributes["title"] ~= nil then 
      beginString = beginString .. "[" .. el.attributes["title"] .. "]"
    end
    if el.attributes["ref"] ~= nil then 
      beginString = beginString .. "\\label{" .. el.attributes["ref"] .. "}"
    end

    local out = {pandoc.RawBlock('latex', beginString)}
    for _, block in ipairs(el.content) do
      table.insert(out, block)
    end
    table.insert(out, pandoc.RawBlock('latex', "\\end{" .. env .. "}"))
    return out
  else
    -- For HTML and other formats, add proofenv class for CSS styling
    el.classes[#el.classes+1] = "proofenv" 
    return el
  end
end

