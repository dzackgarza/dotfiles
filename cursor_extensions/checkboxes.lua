function Plain(el)
  if #el.content >= 3 and el.content[1].t == 'Str' and (el.content[1].text == '[ ]' or el.content[1].text == '[x]' or el.content[1].text == '[X]') then
    local checkbox
    if el.content[1].text == '[ ]' then
      checkbox = pandoc.Str('☐')
    else
      checkbox = pandoc.Str('☑')
    end
    -- Remove the [ ] or [x] and replace with checkbox
    local rest = {}
    for i = 2, #el.content do
      table.insert(rest, el.content[i])
    end
    -- If next is a Space, remove it
    if rest[1] and rest[1].t == 'Space' then
      table.remove(rest, 1)
    end
    table.insert(rest, 1, checkbox)
    return pandoc.Plain(rest)
  end
end

function Para(el)
  -- Same as Plain, but for Para blocks
  if #el.content >= 3 and el.content[1].t == 'Str' and (el.content[1].text == '[ ]' or el.content[1].text == '[x]' or el.content[1].text == '[X]') then
    local checkbox
    if el.content[1].text == '[ ]' then
      checkbox = pandoc.Str('☐')
    else
      checkbox = pandoc.Str('☑')
    end
    local rest = {}
    for i = 2, #el.content do
      table.insert(rest, el.content[i])
    end
    if rest[1] and rest[1].t == 'Space' then
      table.remove(rest, 1)
    end
    table.insert(rest, 1, checkbox)
    return pandoc.Para(rest)
  end
end