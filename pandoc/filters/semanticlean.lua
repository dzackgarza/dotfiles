-- resources/filters/semanticlean.lua
-- A filter to semantically clean make4ht-MathJax HTML for GFM output.

function Span(el)
  -- 1. Handle identifiers (IDs) on spans
  -- make4ht uses Spans for both empty anchors and semantic containers (like subsectionHead)
  if el.identifier ~= "" then
    -- Detect bibliography items (usually prefixed with X in make4ht)
    -- and force a newline to prevent merged bibliography paragraphs.
    local prefix = ""
    if el.identifier:match("^X") then
      prefix = "\n\n"
    end
    
    local label = pandoc.RawInline('markdown', prefix .. ' {#' .. el.identifier .. '}')
    
    -- If the span is empty, just return the label
    local text = pandoc.utils.stringify(el)
    if text == "" or text:match("^%s*$") then
      return label
    end
    
    -- If the span has content, append the label to the content
    table.insert(el.content, label)
  end

  -- 2. Handle MathJax Inline (from make4ht mathjax option)
  if el.classes:includes('mathjax-inline') then
    -- make4ht mathjax output is typically \( math \) inside the span
    local content = pandoc.utils.stringify(el)
    -- Trim whitespace to ensure delimiters are at the ends
    content = content:gsub("^%s+", ""):gsub("%s+$", "")
    -- Remove the \( and \) delimiters if present
    content = content:gsub("^\\%(", ""):gsub("\\%)$", "")
    return pandoc.Math('InlineMath', content)
  end

  -- 2. Handle MathJax Display
  if el.classes:includes('mathjax-display') then
    local content = pandoc.utils.stringify(el)
    content = content:gsub("^%s+", ""):gsub("%s+$", "")
    -- Remove the \[ and \] delimiters if present
    content = content:gsub("^\\%[", ""):gsub("\\%]$", "")
    return pandoc.Math('DisplayMath', content)
  end

  -- 3. Handle Citations (strip span and potentially extra brackets)
  if el.classes:includes('cite') then
    -- make4ht gives brackets inside the cite span: [ [Ale02](#link), Sec. 3 ]
    local content = el.content
    if #content >= 1 then
      -- Strip leading [ from first element
      if content[1].t == "Str" then
        content[1].text = content[1].text:gsub("^%s*%[", "")
      end
      -- Strip trailing ] from last element
      if content[#content].t == "Str" then
        content[#content].text = content[#content].text:gsub("%]%s*$", "")
      end
    end
    return content
  end

  -- 4. Handle TOC Spans
  if el.classes:includes('sectionToc') or el.classes:includes('subsectionToc') then
    return el.content
  end

  -- 5. Handle Section Numbering (titlemark)
  -- We keep the content but strip the span, so '1. ' becomes part of the header text
  if el.classes:includes('titlemark') then
    return el.content
  end

  -- 6. Strip redundant spans (font changes, etc.) while keeping content
  -- (Optionally: filter specific classes if needed)
  return el.content
end

function Link(el)
  -- 1. Handle anchors (empty links with an ID)
  -- make4ht uses <a id="..."></a> for targets
  local text = pandoc.utils.stringify(el)
  if (text == "" or text:match("^%s*$")) and el.identifier ~= "" then
    -- Detect bibliography items (usually prefixed with X in make4ht)
    -- and force a newline to prevent merged bibliography paragraphs.
    local prefix = ""
    if el.identifier:match("^X") then
      prefix = "\n\n"
    end
    -- Convert to {#id} syntax for gfm output
    return pandoc.RawInline('markdown', prefix .. ' {#' .. el.identifier .. '}')
  end

  -- 2. Clean standard links (non-citations)
  -- Strip all attributes (id, class, etc.) to ensure pandoc converts to [text](url)
  el.attr = pandoc.Attr("", {}, {})
  return el
end

function Header(el)
  -- Manually append {#id} to the header text so the gfm writer preserves it
  if el.identifier ~= "" then
    table.insert(el.content, pandoc.RawInline('markdown', ' {#' .. el.identifier .. '}'))
  end
  return el
end

function Div(el)
  -- 1. Handle MathJax Display Blocks
  if el.classes:includes('mathjax-block') then
    local content = pandoc.utils.stringify(el)
    -- Trim whitespace to ensure delimiters are at the ends
    content = content:gsub("^%s+", ""):gsub("%s+$", "")
    -- Remove the \[ and \] delimiters if present
    content = content:gsub("^\\%[", ""):gsub("\\%]$", "")
    return pandoc.Para({pandoc.Math('DisplayMath', content)})
  end

  -- Strip other divs but keep content
  return el.content
end
