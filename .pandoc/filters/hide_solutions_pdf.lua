local system = require 'pandoc.system'
package.path = package.path .. ';' .. '/home/zack/.pandoc/filters/?.lua;'
require "utilities"

function debug_print(some_str)
  myf = io.open("/home/zack/lua_filters.log", "a")
  io.output(myf)
  io.write(some_str)
  io.write("\n")
  io.close(myf)
end
debug_print("Starting")

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
      if not ( 
        has_value(el.classes, "solution") 
        or has_value(el.classes, "proof") 
        or has_value(el.classes, "strategy")
        or has_value(el.classes, "concept")
      ) then
        return el
      end
      if not (kill_proofs) then
        return el
      end
    debug_print("Is proof? " .. tostring( has_value(el.classes, "proof")))
    debug_print("Hide proofs?" .. tostring( hide_proofs))
    debug_print("Is solution? " .. tostring( has_value(el.classes, "solution")))
    debug_print("Kill proofs?" .. tostring( kill_proofs))

    if has_value(el.classes, "solution")  then return pandoc.Para(pandoc.Emph {pandoc.Str "Solution omitted." })
    elseif has_value(el.classes, "proof")  then return pandoc.Para(pandoc.Emph {pandoc.Str "Proof omitted."})
    elseif has_value(el.classes, "strategy")  then return pandoc.Para(pandoc.Emph {pandoc.Str "Strategy omitted."})
    elseif has_value(el.classes, "concept")  then return pandoc.Para(pandoc.Emph {pandoc.Str "Concept review omitted."})
    else return el
    end

  end
  return {
    { Meta = enable_hide_proofs },  -- (1)
    { Div = kill_proofs_fn }     -- (2)
  }
end

