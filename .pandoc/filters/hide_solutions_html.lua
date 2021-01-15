package.path = '/home/zack/.pandoc/filters/?.lua;'..package.path
require "utilities"

local hide_proofs = false

-- Hide solution environments in HTML output using <details> <summary> ... construct
if FORMAT:match 'html' then

  function enable_hide_proofs(meta)
    if meta["hide_proofs"] ~= nil then
      hide_proofs = true
    end
  end

  function hide_solutions(el)
      --print("Is proof? " .. tostring( has_value(el.classes, "proof")))
      --print("Hide proofs?" .. tostring( hide_proofs))
      if has_value(el.classes, "solution") or (has_value(el.classes, "proof") and hide_proofs) then
      --el.classes[#el.classes+1] = "alert"
      --el.classes[#el.classes+1] = "alert-info"
      --el.classes[#el.classes+1] = "proofenv"
      table.insert(
        el.content, 1,
        pandoc.RawBlock("html", "<details><summary><i>(Click to expand)</i></summary>")
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

  -- Run in this order.
  return {
    { Meta = enable_hide_proofs },  -- (1)
    { Div = hide_solutions }     -- (2)
  }
end
