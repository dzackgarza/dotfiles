-- normalize_displaymath.lua
-- Every Math(DisplayMath) and \begin{...}...\end{...} block gets its
-- delimiters on their own lines. If embedded in a Paragraph, the
-- paragraph is split so the block stands alone.

local function raw_displaymath(tex)
  local body = tex:match("^%s*(.-)%s*$")
  return pandoc.RawBlock("markdown", "\\[\n" .. body .. "\n\\]")
end

local function raw_latex_block(tex)
  -- Normalize: opening delimiter on own line, body, closing delimiter.
  local begin_pat = "^\\begin%b{}"
  local begin_start, begin_end = tex:find(begin_pat)
  if not begin_start then
    return pandoc.RawBlock("markdown", tex)
  end
  local end_start = tex:find("\\end%b{}$")
  if not end_start then
    return pandoc.RawBlock("markdown", tex)
  end
  local open_delim = tex:sub(begin_start, begin_end)
  local close_delim = tex:sub(end_start)
  local body = tex:sub(begin_end + 1, end_start - 1):match("^%s*(.-)%s*$")
  return pandoc.RawBlock("markdown", open_delim .. "\n" .. body .. "\n" .. close_delim)
end

local function is_latex_env(inline)
  return inline.t == "RawInline"
     and inline.format == "tex"
     and inline.text:match("^\\begin{")
     and inline.text:match("\\end{")
end

local function is_block_trigger(inline)
  return (inline.t == "Math" and inline.mathtype == "DisplayMath")
      or is_latex_env(inline)
end

local function render_block(inline)
  if inline.t == "Math" and inline.mathtype == "DisplayMath" then
    return raw_displaymath(inline.text)
  elseif is_latex_env(inline) then
    return raw_latex_block(inline.text)
  end
  return nil
end

local function split_para_on_blocks(inlines)
  local blocks = {}
  local current = {}

  for _, el in ipairs(inlines) do
    if is_block_trigger(el) then
      if #current > 0 then
        table.insert(blocks, pandoc.Para(current))
        current = {}
      end
      table.insert(blocks, render_block(el))
    else
      table.insert(current, el)
    end
  end

  if #current > 0 then
    table.insert(blocks, pandoc.Para(current))
  end

  return blocks
end

function Para(el)
  -- Standalone block: single child that is a trigger.
  if #el.content == 1 and is_block_trigger(el.content[1]) then
    return render_block(el.content[1])
  end

  -- Mixed: check if any child is a trigger.
  for _, inl in ipairs(el.content) do
    if is_block_trigger(inl) then
      return split_para_on_blocks(el.content)
    end
  end

  return nil  -- pass through
end
