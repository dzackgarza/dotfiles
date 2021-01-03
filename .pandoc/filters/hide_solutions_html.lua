-- Hide solution environments in HTML output using <details> <summary> ... construct
function Div(el)
  if (el.classes[1] == "solution" and FORMAT:match 'html5') then
    el.classes[#el.classes+1] = "alert"
    el.classes[#el.classes+1] = "alert-info"
    el.classes[#el.classes+1] = "proofenv"
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
  end
end

