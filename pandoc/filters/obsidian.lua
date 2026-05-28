-- Strip Obsidian wikilinks, %% comments, and bare #tag lines.
-- Pandoc 3.x API: tag/content/text instead of t/c.

local function starts_with(str, prefix)
  return str:sub(1, #prefix) == prefix
end

local function ends_with(str, suffix)
  return str:sub(-#suffix) == suffix
end

-- State for multi-word wikilinks and %% comments
local wiki_mode = false
local wiki_has_pipe = false
local wiki_pipe_text = ""
local wiki_buffer = {}
local in_comment = false

local function flush_wiki(result)
  if wiki_mode and #wiki_buffer > 0 then
    if wiki_has_pipe then
      table.insert(result, pandoc.Str(wiki_pipe_text))
    else
      table.insert(result, pandoc.Str(table.concat(wiki_buffer, " ")))
    end
  end
  wiki_mode = false
  wiki_has_pipe = false
  wiki_buffer = {}
  wiki_pipe_text = ""
end

-- Process a Str element's text for wikilinks, comments, tags.
-- Returns true if consumed (should not be added to result).
local function process_str(text, result)
  -- %% comment handling
  if starts_with(text, "%%") then
    local rest = text:sub(3)
    if in_comment then
      in_comment = false
      return true
    else
      in_comment = true
      local close = rest:find("%%")
      if close then
        in_comment = false
        local after = rest:sub(close + 2)
        if after ~= "" then
          process_str(after, result)
        end
      end
      return true
    end
  end

  if in_comment then
    if ends_with(text, "%%") then
      in_comment = false
    end
    return true
  end

  -- [[wikilink]] handling
  if starts_with(text, "[[") then
    local content = text:sub(3)
    local close = content:find("]]")
    if close then
      local inner = content:sub(1, close - 1)
      local pipe = inner:find("|")
      if pipe then
        table.insert(result, pandoc.Str(inner:sub(pipe + 1)))
      else
        table.insert(result, pandoc.Str(inner))
      end
      local after = content:sub(close + 2)
      if after ~= "" then
        if not process_str(after, result) then
          table.insert(result, pandoc.Str(after))
        end
      end
      return true
    else
      local pipe = content:find("|")
      if pipe then
        wiki_has_pipe = true
        wiki_pipe_text = content:sub(pipe + 1)
      else
        wiki_buffer = { content }
      end
      wiki_mode = true
      return true
    end
  end

  if wiki_mode then
    local close = text:find("]]")
    if close then
      local before = text:sub(1, close - 1)
      -- If pipe not yet found, scan buffer for one (pipe in later segment)
      if not wiki_has_pipe then
        for i, segment in ipairs(wiki_buffer) do
          local p = segment:find("|")
          if p then
            wiki_has_pipe = true
            wiki_pipe_text = segment:sub(p + 1)
            -- Remaining segments after the pipe are part of the display text
            for j = i + 1, #wiki_buffer do
              if wiki_buffer[j] ~= "" then
                wiki_pipe_text = wiki_pipe_text .. " " .. wiki_buffer[j]
              end
            end
            break
          end
        end
      end
      if wiki_has_pipe then
        -- Append the closing segment to the display text
        if wiki_pipe_text ~= "" then
          wiki_pipe_text = wiki_pipe_text .. " "
        end
        wiki_pipe_text = wiki_pipe_text .. before
        table.insert(result, pandoc.Str(wiki_pipe_text))
      else
        table.insert(wiki_buffer, before)
        table.insert(result, pandoc.Str(table.concat(wiki_buffer, " ")))
      end
      wiki_mode = false
      wiki_has_pipe = false
      wiki_buffer = {}
      local after = text:sub(close + 2)
      if after ~= "" then
        if not process_str(after, result) then
          table.insert(result, pandoc.Str(after))
        end
      end
      return true
    else
      if wiki_has_pipe then
        wiki_pipe_text = wiki_pipe_text .. " " .. text
      else
        table.insert(wiki_buffer, text)
      end
      return true
    end
  end

  -- Strip standalone #tags
  if text:match("^#[%w/]+$") then
    return true
  end

  return false
end

--- Process a list of Inline elements (Pandoc 3.x userdata).
local function process_inlines(inlines)
  local result = {}
  for _, il in ipairs(inlines) do
    if il.tag == "Str" then
      local consumed = process_str(il.text, result)
      if not consumed then
        flush_wiki(result)
        table.insert(result, il)
      end
    elseif il.tag == "Space" then
      if in_comment then
        -- skip
      elseif wiki_mode then
        -- space inside wikilink, just separator
      else
        flush_wiki(result)
        table.insert(result, il)
      end
    elseif il.tag == "SoftBreak" then
      if in_comment then
        -- skip
      else
        flush_wiki(result)
        table.insert(result, il)
      end
    else
      flush_wiki(result)
      table.insert(result, il)
    end
  end
  flush_wiki(result)
  return result
end

-- Drop metadata lines
function Para(el)
  local text = ""
  for _, il in ipairs(el.content) do
    if il.tag == "Str" then
      text = text .. il.text
    elseif il.tag == "Space" then
      text = text .. " "
    elseif il.tag == "SoftBreak" then
      text = text .. "\n"
    end
  end
  if starts_with(text, "Tags:") then return {} end
  if starts_with(text, "Refs:") then return {} end
  if text:match("^#[%w/]+") then return {} end

  el.content = process_inlines(el.content)
  return el
end

-- Strip markdown links whose targets are Obsidian page references (not URLs).
-- Converts [display text](page name) to plain "display text".
-- Obsidian page refs are either bare page names or file paths inside the vault.
local OBSIDIAN_VAULT_PREFIX = os.getenv("HOME") .. "/notes/"
local function is_obsidian_page_ref(target)
  -- Real URLs have a scheme
  if target:match("://") then return false end
  -- Mailto links
  if target:match("^mailto:") then return false end
  -- Anchor-only links
  if target:match("^#") then return false end
  -- Absolute paths under the Obsidian vault are resolved page refs
  if target:match("^" .. OBSIDIAN_VAULT_PREFIX) then return true end
  -- Relative paths with no extension and no scheme: Obsidian page refs
  if not target:match("://") and not target:match("%.[a-zA-Z]+$") and target:match("^[%w%s%%%-_]+$") then
    return true
  end
  return false
end

function Link(el)
  if is_obsidian_page_ref(el.target) then
    return el.content
  end
  return nil
end

function Header(el)
  el.content = process_inlines(el.content)
  return el
end

function Plain(el)
  el.content = process_inlines(el.content)
  return el
end
