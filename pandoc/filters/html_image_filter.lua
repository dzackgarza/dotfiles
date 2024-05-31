package.path = '/home/dzack/.pandoc/filters' .. package.path
require "utilities"

function Image (el)
  tprint(el)
  table.insert(
    el.content, 1,
    pandoc.RawBlock("html", '<figure>')
  )
  table.insert(
    el.content,
    pandoc.RawBlock("html", '<span class="marginnotes">')
  )
  table.insert(
    el.content,
    elem.caption
  )
  table.insert(
    el.content,
    pandoc.RawBlock("html", '</span>')
  )
  ril = pandoc.RawInline('html', '<p style="text-align:center;"> <img class="tikz" src="' .. fname .. '"></p>')
  return el
end
