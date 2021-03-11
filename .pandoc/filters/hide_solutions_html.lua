package.path = '/home/zack/.pandoc/filters/?.lua;'..package.path
require "utilities"

local hide_proofs = false
local kill_proofs = false

function enable_hide_proofs(meta)
  if meta["hide_proofs"] ~= nil then
    hide_proofs = true
  end
  if meta["kill_proofs"] ~= nil then
    kill_proofs = true
  end
end

if FORMAT:match "latex" or FORMAT:match "pdf" then
  function kill_proofs_fn(el)
    if has_value(el.classes, "solution") or (has_value(el.classes, "proof") and kill_proofs) then
      --print("Is proof? " .. tostring( has_value(el.classes, "proof")))
      --print("Hide proofs?" .. tostring( hide_proofs))
      --print("Is solution? " .. tostring( has_value(el.classes, "solution")))
      --print("Kill proofs?" .. tostring( kill_proofs))
      return pandoc.Para(pandoc.Str("Solution/proof omitted."))
    end
  end
  return {
    { Meta = enable_hide_proofs },  -- (1)
    { Div = kill_proofs_fn }     -- (2)
  }
end
  

-- Hide solution environments in HTML output using <details> <summary> ... construct
if FORMAT:match 'html' then
  function hide_solutions(el)
      --print("Is proof? " .. tostring( has_value(el.classes, "proof")))
      --print("Hide proofs?" .. tostring( hide_proofs))
      if has_value(el.classes, "solution") or (has_value(el.classes, "proof") and kill_proofs) then
        return pandoc.Emph("Solution/proof omitted")
      end
      if has_value(el.classes, "solution") or (has_value(el.classes, "proof") and hide_proofs) then
      --el.classes[#el.classes+1] = "alert"
      --el.classes[#el.classes+1] = "alert-info"
      --el.classes[#el.classes+1] = "proofenv"
      table.insert(
        el.content, 1,
        pandoc.RawBlock("html", "<details open><summary><i>(Click to expand)</i></summary>")
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
