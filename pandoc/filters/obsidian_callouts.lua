local stringify = (require "pandoc.utils").stringify

function BlockQuote (el)
    local start = el.content[1]
    if (start.t == "Para" and start.content[1].t == "Str" and
        start.content[1].text:match("^%[!%w+%][-+]?$")) then
        local _, _, ctype = start.content[1].text:find("%[!(%w+)%]")
        el.content:remove(1)
        start.content:remove(1)
        -- Drop the leading space left by removing the "[!type]" token.
        while #start.content > 0 and start.content[1].t == "Space" do
            start.content:remove(1)
        end
        -- Emit the Obsidian-standard visible title element (a plain HTML title
        -- attribute is only a tooltip the reader never sees).
        local body = el.content
        body:insert(1, pandoc.Div({pandoc.Plain(start.content)}, {class = "callout-title"}))
        local div = pandoc.Div(body, {class = "callout"})
        div.attributes["data-callout"] = ctype:lower()
        div.attributes["title"] = stringify(start.content):gsub("^ ", "")
        return div
    else
        return el
    end
end
