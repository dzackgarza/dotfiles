function dump(o)
   if type(o) == 'table' then
      local s = '{ '
      for k,v in pairs(o) do
         if type(k) ~= 'number' then k = '"'..k..'"' end
         s = s .. '['..k..'] = ' .. dump(v) .. ','
      end
      return s .. '} '
   else
      return tostring(o)
   end
end

-- Map the following syntax
-- {.someEnvName title="Some quoted name"}
-- to
-- \begin{someEnvName}[Some quoted name]
-- Supports math within the quoted name
function Div(el)

  if (el.classes[1] == "solution" and FORMAT=='html5') then
    
    el.classes[#el.classes+1] = "alert alert-info"
    table.insert(
      el.content, 1,
      pandoc.RawBlock("html", "<details><summary>Solution <i>(Click to expand)</i></summary>")
    )
    table.insert(
      el.content,
      pandoc.RawBlock("latex", "\\begin{solution}")
    )
    table.insert(
      el.content,
      pandoc.RawBlock("latex", "\\end{solution}")
    )
    table.insert(
      el.content,
      pandoc.RawBlock("html", "</details>")
    )
    return el
  else
    beginString = "\\begin{" .. el.classes[1] .. "}"
    if el.attributes["title"]~=nil then 
      beginString = beginString .. "[" .. el.attributes["title"] .. "]"
    end
    table.insert(
      el.content, 1,
      pandoc.RawBlock("latex", beginString)
    )
    table.insert(
      el.content,
      pandoc.RawBlock("latex", "\\end{" .. el.classes[1] .. "}")
    )
    return el
  end
end

-- Convert \[ ... \] to \begin{align*} ... \end{align*}
if FORMAT:match 'latex' or FORMAT:match 'pdf' then
  function Math (m)
    if m.mathtype == "DisplayMath" then
      return pandoc.RawInline('tex', '\n\\begin{align*}'.. m.text .. '\\end{align*}')
    else
      return m
    end
  end
end
