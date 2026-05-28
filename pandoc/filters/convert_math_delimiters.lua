local function trim(text)
  return (text:gsub("^%s+", ""):gsub("%s+$", ""))
end

local function is_display_math(m)
  return m.mathtype == pandoc.DisplayMath or m.mathtype == "DisplayMath"
end

local function already_alignable(text)
  return text:match("^%s*\\begin%s*{%s*align%*?%s*}") ~= nil
end

local function alignment_environment(text)
  if text:find("\\label%s*{") then
    return "align"
  end
  return "align*"
end

local function alignable_display(text)
  local content = trim(text)
  if already_alignable(content) then
    return content
  end

  local env = alignment_environment(content)
  return "\\begin{" .. env .. "}\n" .. content .. "\n\\end{" .. env .. "}"
end

-- Specify delimiters for each type of output
function Math(m)
  -- For markdown->markdown cleaning
  if FORMAT:match "markdown" then
    if not is_display_math(m) then
      return pandoc.RawInline('markdown', '\\( ' .. m.text .. ' \\)')
    end
    return pandoc.RawInline('markdown', '\n' .. alignable_display(m.text) .. '\n')
  end 

  -- For Latex and HTML output
  if FORMAT:match "latex" or FORMAT:match "pdf" then
    if not is_display_math(m) then
      return m
      --return pandoc.RawInline('tex', '\\(' .. m.text .. '\\)')
    end
    return pandoc.RawInline('tex', '\n' .. alignable_display(m.text) .. '\n')
  end 

  if FORMAT:match "html" or FORMAT:match "html5" then
    if not is_display_math(m) then
      return m
    end
    return pandoc.RawInline('html', '\n<span class="math display">\n' .. alignable_display(m.text) .. '\n</span>')
  end 

end

-- Delete macro inclusions 
function RawBlock(el)
  if FORMAT:match "markdown" then
    if string.find(el.text, "newcommand") or string.find(el.text, "DeclareMath") then
      --print("Found newcommand")
      return pandoc.Para("")
    else
      return el
    end
  end
end
