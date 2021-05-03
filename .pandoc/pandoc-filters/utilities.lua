-- Debugging: dump table contnts to a readable string.
function dump(o)
   if type(o) == 'table' then
      local s = '\n{ '
      for k,v in pairs(o) do
         if type(kG) ~= 'number' then k = '"'..k..'"' end
         s = s .. '['..k..'] = ' .. dump(v) .. ','
      end
      return s .. '} '
   else
      return tostring(o)
   end
end

-- Capitalize first letter of a string.
function firstToUpper(str)
    return (str:gsub("^%l", string.upper))
end

-- Print contents of `tbl`, with indentation.
-- `indent` sets the initial level of indentation.
function tprint (tbl, indent)
  if not indent then indent = 0 end
  for k, v in pairs(tbl) do
    formatting = string.rep("  ", indent) .. k .. ": "
    if type(v) == "table" then
      print(formatting)
      tprint(v, indent+1)
    elseif type(v) == 'boolean' then
      print(formatting .. tostring(v))      
    else
      print(formatting .. v)
    end
  end
end

-- get all lines from a file, returns an empty 
-- list/table if the file does not exist
function lines_from(file)
  if not file_exists(file) then return {} end
  lines = {}
  for line in io.lines(file) do 
    lines[#lines + 1] = line
  end
  return lines
end

function file_exists(name)
  local f = io.open(name, 'r')
  if f ~= nil then
    io.close(f)
    return true
  else
    return false
  end
end

function starts_with(start, str)
  return str:sub(1, #start) == start
end

function printDebugInfo(rc)
  print(dump(rc))
  lines = {}
  for line in io.lines('/tmp/tikz.tex') do 
    lines[#lines + 1] = line
  end
  for k,v in pairs(lines) do
    print(v)
  end
end

function has_value (tab, val)
  for index, value in ipairs(tab) do
    if value == val then
      return true
    end
  end

  return false
end
