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

-- Shared compilation core: given full LaTeX source, compile to PDF then SVG.
-- Returns (svg_path, pdf_path) or (nil, nil) on failure.
local function run_pdflatex_and_convert(tex_source, tmp_prefix, hash)
  local svg_path = svg_dir .. "/dzgtikz-" .. hash .. ".svg"
  local pdf_path = svg_dir .. "/dzgtikz-" .. hash .. ".pdf"

  local sf = io.open(svg_path, "r")
  if sf then sf:close() end
  local pf = io.open(pdf_path, "r")
  if pf then pf:close() end
  if sf and pf then
    return svg_path, pdf_path
  end

  os.execute("mkdir -p " .. svg_dir)

  local tmp = "/tmp/" .. tmp_prefix .. "-" .. hash
  os.execute("mkdir -p " .. tmp)
  local tex_path = tmp .. "/tikz.tex"

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

-- Compile a tikz snippet (e.g. \begin{tikzcd}...) by wrapping in standalone template.
-- Returns (svg_path, pdf_path) or (nil, nil) on failure.
local function compile_tikz(source)
  local hash = pandoc.sha1(source)
  local tex_source = tikz_doc_template:gsub("__TIKZ_CONTENT__", source)
  return run_pdflatex_and_convert(tex_source, "tikzcd", hash)
end

-- Compile a full tikz document (from ```tikz code block) directly, no template.
-- Returns (svg_path, pdf_path) or (nil, nil) on failure.
local function compile_tikz_document(source)
  local hash = pandoc.sha1(source)
  return run_pdflatex_and_convert(source, "tikzfull", hash)
end

-- Shared helpers for building output from a compiled SVG/PDF pair.
local function make_latex_output(pdf_path, is_tikzcd)
  local base = pdf_path:gsub("%.pdf$", "")
  if is_tikzcd then
    return "\\begin{figure}[H]\n\\centering\n\\includesvg[width=\\columnwidth]{" .. base .. "}\n\\end{figure}"
  else
    return "\\begin{figure}\n\\centering\n\\includesvg[width=\\columnwidth]{" .. base .. "}\n\\end{figure}"
  end
end

local function make_html_output(svg_path, css_class)
  local f = io.open(svg_path, "r")
  assert(f, "tikzcd.lua: SVG file missing after compilation: " .. svg_path)
  local svg_content = f:read("*a")
  f:close()

  local svg_tag = svg_content:match("<svg[^>]*>.-</svg>")
  if not svg_tag then
    svg_tag = svg_content
  end

  local html = '<div style="text-align:center;">'
    .. '<span class="' .. css_class .. '">'
    .. svg_tag
    .. '</span>'
    .. '</div>'
  return pandoc.Para(pandoc.RawInline('html', html))
end

if FORMAT:match 'latex' or FORMAT:match 'pdf' or FORMAT:match 'markdown' then
  function RawBlock(el)
    local is_tikzcd = starts_with('\\begin{tikzcd}', el.text)
    local is_tikzpic = starts_with('\\begin{tikzpicture}', el.text)
    if not is_tikzcd and not is_tikzpic then
      return el
    end

    local _, pdf_path = compile_tikz(el.text)
    assert(pdf_path, "tikzcd.lua: compilation failed for tikz block")

    el.text = make_latex_output(pdf_path, is_tikzcd)
    return el
  end

  function CodeBlock(el)
    if not el.classes:includes("tikz") then
      return el
    end

    local _, pdf_path = compile_tikz_document(el.text)
    assert(pdf_path, "tikzcd.lua: compilation failed for tikz code block")

    return pandoc.RawBlock('latex', make_latex_output(pdf_path, false))
  end
end

if FORMAT:match 'html' then
  function RawBlock(el)
    local is_tikzcd = starts_with('\\begin{tikzcd}', el.text)
    local is_tikzpic = starts_with('\\begin{tikzpicture}', el.text)
    if not is_tikzcd and not is_tikzpic then
      return el
    end

    local svg_path, _ = compile_tikz(el.text)
    assert(svg_path, "tikzcd.lua: compilation failed for tikz block")

    local css_class = "tikzcd"
    if not is_tikzcd then
      css_class = "tikzpic"
    end

    return make_html_output(svg_path, css_class)
  end

  function CodeBlock(el)
    if not el.classes:includes("tikz") then
      return el
    end

    local svg_path, _ = compile_tikz_document(el.text)
    assert(svg_path, "tikzcd.lua: compilation failed for tikz code block")

    return make_html_output(svg_path, "tikzcode")
  end
end
