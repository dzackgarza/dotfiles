function Math(el)
  if el.mathtype == pandoc.DisplayMath then
    if FORMAT:match 'html' then
      return pandoc.RawInline('html', '<span class="math display">\\begin{align*}\n' .. el.text .. '\\end{align*}</span>')
    else
      el.text = '\\begin{align*}\n' .. el.text .. '\\end{align*}'
      return el
    end
  end
end
end
