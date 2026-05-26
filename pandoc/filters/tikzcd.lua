local system = require 'pandoc.system'
local home = os.getenv("HOME")
package.path = package.path .. ';' .. home .. '/.pandoc/filters/?.lua;'
require "utilities"

-- Output directories
local pandoc_dir = os.getenv("PANDOC_DIR") or (home .. "/dotfiles/pandoc")
local figures_dir = os.getenv("FIGURES_DIR") or (home .. "/figures")
local svg_dir = os.getenv("SVG_DIR") or (figures_dir .. "/rendered")

local template_path = pandoc_dir .. "/templates/standalone-tikz.tex"
local template_file = io.open(template_path, "r")
if not template_file then
  error("tikzcd.lua: standalone template not found at " .. template_path)
end
local tikz_doc_template = template_file:read("*a")
template_file:close()

-- Compile tikz source to SVG + PDF, cache in svg_dir
-- Returns (svg_path, pdf_path) or (nil, nil) on failure
local function compile_tikz(source)
  local hash = pandoc.sha1(source)
  local svg_path = svg_dir .. "/dzgtikz-" .. hash .. ".svg"
  local pdf_path = svg_dir .. "/dzgtikz-" .. hash .. ".pdf"

  -- Return cached if both files exist
  local sf = io.open(svg_path, "r")
  if sf then sf:close() end
  local pf = io.open(pdf_path, "r")
  if pf then pf:close() end
  if sf and pf then
    return svg_path, pdf_path
  end

  os.execute("mkdir -p " .. svg_dir)

  local tmp = "/tmp/tikzcd-" .. hash
  os.execute("mkdir -p " .. tmp)
  local tex_path = tmp .. "/tikz.tex"

  local tex_source = tikz_doc_template:gsub("__TIKZ_CONTENT__", source)
  local f = io.open(tex_path, "w")
  f:write(tex_source)
  f:close()

  local cmd1 = "pdflatex -interaction=nonstopmode -output-directory=" .. tmp .. " " .. tex_path .. " 2>&1"
  local ok1 = os.execute(cmd1)
  if not ok1 then
    os.execute("rm -rf " .. tmp)
    return nil, nil
  end

  local tmp_pdf = tmp .. "/tikz.pdf"
  os.execute("cp " .. tmp_pdf .. " " .. pdf_path)
  local ok2 = os.execute("pdf2svg " .. tmp_pdf .. " " .. svg_path .. " >/dev/null 2>&1")
  os.execute("rm -rf " .. tmp)

  if not ok2 then
    return nil, pdf_path
  end

  return svg_path, pdf_path
end

if FORMAT:match 'latex' or FORMAT:match 'pdf' or FORMAT:match 'markdown' then
  function RawBlock(el)
    if not starts_with('\\begin{tikzcd}', el.text) and not starts_with('\\begin{tikzpicture}', el.text) then
      return el
    end

    local _, pdf_path = compile_tikz(el.text)
    assert(pdf_path, "tikzcd.lua: compilation failed for tikz block")

    local base = pdf_path:gsub("%.pdf$", "")
    if starts_with('\\begin{tikzpicture}', el.text) then
      el.text = "\\begin{figure}\n\\centering\n\\includesvg[width=\\columnwidth]{" .. base .. "}\n\\end{figure}"
    else
      el.text = "\\begin{figure}[H]\n\\centering\n\\includesvg[width=\\columnwidth]{" .. base .. "}\n\\end{figure}"
    end
    return el
  end
end

if FORMAT:match 'html' then
  function RawBlock(el)
    if not starts_with('\\begin{tikzcd}', el.text) and not starts_with('\\begin{tikzpicture}', el.text) then
      return el
    end

    local svg_path, _ = compile_tikz(el.text)
    assert(svg_path, "tikzcd.lua: compilation failed for tikz block")

    local f = io.open(svg_path, "r")
    assert(f, "tikzcd.lua: SVG file missing after compilation: " .. svg_path)
    local svg_content = f:read("*a")
    f:close()

    -- Extract the <svg> tag and its content
    local svg_tag = svg_content:match("<svg[^>]*>.-</svg>")
    if not svg_tag then
      svg_tag = svg_content
    end

    local css_class = "tikzcd"
    if starts_with('\\begin{tikzpicture}', el.text) then
      css_class = "tikzpic"
    end

    local html = '<div style="text-align:center;">'
      .. '<span class="' .. css_class .. '">'
      .. svg_tag
      .. '</span>'
      .. '</div>'
    return pandoc.Para(pandoc.RawInline('html', html))
  end
end
