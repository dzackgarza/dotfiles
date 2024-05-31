local system = require 'pandoc.system'
package.path = '/home/dzack/.pandoc/filters' .. package.path
require "utilities"

local tikz_doc_template = [[
\documentclass{standalone}
\input{/home/dzack/.pandoc/custom/preamble_common}
\begin{document}
\nopagecolor
%s
\end{document}
]]


function RawBlock(el)
  if not starts_with('\\begin{tikzcd}', el.text) and not starts_with('\\begin{tikzpicture}', el.text) then
    return el
  end

  if FORMAT:match 'latex' or FORMAT:match 'pdf' or FORMAT:match 'markdown' then
    return pandoc.RawInline( "tex", "\\begin{center}\n" .. el.text .. "\n\\end{center}")
  end

  if not FORMAT:match 'html' then
    return el
  end

  -- Just drop SVG files directly in tmp directory.   
  local file_hash = pandoc.sha1(el.text);
  local temp_tex_doc = tikz_doc_template:format(el.text)

  local f = io.open('/tmp/tikz.tex', 'w')
  f:write(temp_tex_doc)
  f:close()

  local file1 = io.popen('tikz_to_svg.sh -f "/tmp/tikz.tex" -h "' . file_hash . '"')
  local output1 = file1:read('*all')
  local rc1 = {file1:close()}
  if not rc1[1] then
    print("Error on 1")
    printDebugInfo(rc1)
    return false
  end


  local fname = "/tmp/" .. pandoc.sha1(el.text) .. ".svg"

  if not file_exists(fname) then
    system.with_working_directory("/tmp", function()
      local f = io.open('/tmp/tikz.tex', 'w')
      f:write()
      f:close()
      -- 1: Latex -> PDF 
      cmd1 =  'pdflatex /tmp/tikz.tex'
      local file1 = io.popen(cmd1)
      local output1 = file1:read('*all')
      local rc1 = {file1:close()}
      if not rc1[1] then
        print("Error on 1")
        printDebugInfo(rc1)
        return false
      end
      -- 2: PDF -> SVG
      cmd2 = 'pdf2svg /tmp/tikz.pdf "' .. fname .. '"'
      local file2 = io.popen(cmd2)
      local output2 = file2:read('*all')
      local rc2 = {file2:close()}
      if not rc2[1] then
        print("Error on 2")
        printDebugInfo(rc2)
        return false
      end
      -- Success!
    end)
  end
  ril = pandoc.RawInline('html', '<p style="text-align:center;"> <img class="tikz" src="' .. fname .. '"></p>')
  return pandoc.Para(ril)
end
