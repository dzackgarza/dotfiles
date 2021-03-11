package.path = '/home/zack/.pandoc/filters/?.lua;'..package.path

local system = require 'pandoc.system'

require "utilities"

local tikz_doc_template = [[
\documentclass{standalone}
\input{/home/zack/.pandoc/custom/preamble_common}
\begin{document}
\nopagecolor
%s
\end{document}
]]

if FORMAT:match 'latex' or FORMAT:match 'pdf' or FORMAT:match 'markdown' then
  function RawBlock(el)
    --tprint(el)
    if not starts_with('\\begin{tikzcd}', el.text) and not starts_with('\\begin{tikzpicture}', el.text) then
      --print("Doesn't start with tikzcd or tikzpicture")
      return el
    elseif starts_with('\\begin{tikzpicture}', el.text) then
      el.text = "\\begin{figure}\n\\centering\n\\resizebox{\\columnwidth}{!}{%\n" .. el.text .. "\n}\n\\end{figure}"
      return el
    else
      el.text = "\\begin{center}\n" .. el.text .. "\n\\end{center}"
      return el
    end
  end
end

if FORMAT:match 'html' then
  function RawBlock(el)
    if not starts_with('\\begin{tikzcd}', el.text) and not starts_with('\\begin{tikzpicture}', el.text) then
      return el
    end

    -- Just drop SVG files directly in tmp directory.   
    local fname = "/tmp/" .. pandoc.sha1(el.text) .. ".svg"

    if not file_exists(fname) then
      system.with_working_directory("/tmp", function()
        local f = io.open('/tmp/tikz.tex', 'w')
        f:write(tikz_doc_template:format(el.text))
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
    if starts_with('\\begin{tikzcd}', el.text) then
      ril = pandoc.RawInline('html', '<p style="text-align:center;"> <img class="tikzcd" src="' .. fname .. '"></p>')
    else
      ril = pandoc.RawInline('html', '<p style="text-align:center;"> <img class="tikzpic" src="' .. fname .. '"></p>')
    end
    return pandoc.Para(ril)
  end
end
