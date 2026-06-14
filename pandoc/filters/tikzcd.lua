local system = require 'pandoc.system'
local home = os.getenv("HOME")
package.path = package.path .. ';' .. home .. '/.pandoc/filters/?.lua;'
require "utilities"

-- Logging helper: writes to stderr, no-op unless TIKZCD_DEBUG=1
local debug_mode = os.getenv("TIKZCD_DEBUG") == "1"
local function log(msg)
  if debug_mode then
    io.stderr:write("[tikzcd] " .. msg .. "\n")
  end
end

-- Output directories
local pandoc_dir = os.getenv("PANDOC_DIR") or (home .. "/dotfiles/pandoc")
local figures_dir = os.getenv("FIGURES_DIR") or (home .. "/figures")
local svg_dir = os.getenv("SVG_DIR") or (figures_dir .. "/rendered")

local template_path = pandoc_dir .. "/templates/standalone-tikz.tex"
local template_file = io.open(template_path, "r")
if not template_file then
  error("tikzcd.lua: standalone template not found at " .. template_path)
end
local tikz_doc_template_str = template_file:read("*a")
template_file:close()
local tikz_doc_template = pandoc.template.compile(tikz_doc_template_str)

-- Shared compilation core: given full LaTeX source, compile to PDF then SVG.
-- Returns (svg_path, pdf_path) or (nil, nil) on failure.
local function run_pdflatex_and_convert(tex_source, tmp_prefix, hash, doc_dir)
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

  local inputs_env = ""
  local styles_dir = pandoc_dir .. "/styles//"
  if doc_dir and doc_dir ~= "" then
    inputs_env = "TEXINPUTS=" .. doc_dir .. ":" .. styles_dir .. ":: "
  else
    inputs_env = "TEXINPUTS=" .. styles_dir .. ":: "
  end

  local cmd1 = inputs_env .. "pdflatex -interaction=nonstopmode -output-directory=" .. tmp .. " " .. tex_path .. " 2>&1"
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

local function resolve_inputs(text, base_dir, depth)
  if not depth then depth = 1 end
  if depth > 10 then
    log("resolve_inputs: max depth exceeded, potential circular input")
    return text
  end

  local count
  repeat
    count = 0
    text = text:gsub("\\input%s-{(.-)}", function(filename)
      count = count + 1
      local full_path = filename
      local is_absolute = filename:sub(1,1) == "/" or filename:match("^%a+:")
      if not is_absolute then
        full_path = base_dir .. "/" .. filename
      end

      local file = io.open(full_path, "r")
      if not file then
        -- If it doesn't end with .tikz or .tex, try appending extensions
        if not filename:match("%.%a+$") then
          file = io.open(full_path .. ".tikz", "r")
          if not file then
            file = io.open(full_path .. ".tex", "r")
          end
        end
      end

      if file then
        local content = file:read("*a")
        file:close()
        -- Recursively resolve inputs inside the loaded content
        return resolve_inputs(content, base_dir, depth + 1)
      else
        log("resolve_inputs: WARNING: could not open input file " .. filename)
        return "\\input{" .. filename .. "}"
      end
    end)
  until count == 0

  return text
end

-- Compile a tikz snippet (e.g. \begin{tikzcd}...) by wrapping in standalone template.
-- Returns (svg_path, pdf_path) or (nil, nil) on failure.
local function compile_tikz(source)
  local doc_path = os.getenv("PANDOC_DOC_PATH")
  local doc_dir = "."
  if doc_path and doc_path ~= "" then
    doc_dir = doc_path:match("(.+)[/\\]") or doc_dir
  end

  local resolved_source = resolve_inputs(source, doc_dir)
  local hash = pandoc.sha1(resolved_source)

  local tex_source = tikz_doc_template:gsub("__TIKZ_CONTENT__", resolved_source)

  log("compile_tikz: hash=" .. hash .. " source_length=" .. #resolved_source)
  if debug_mode then
    local preview = resolved_source:sub(1, 200):gsub("\n", "\\n")
    log("compile_tikz: source_preview: " .. preview)
  end
  return run_pdflatex_and_convert(tex_source, "tikzcd", hash, doc_dir)
end

-- Compile a full tikz document (from ```tikz code block) directly, no template.
-- Returns (svg_path, pdf_path) or (nil, nil) on failure.
local function compile_tikz_document(source)
  local doc_path = os.getenv("PANDOC_DOC_PATH")
  local doc_dir = "."
  if doc_path and doc_path ~= "" then
    doc_dir = doc_path:match("(.+)[/\\]") or doc_dir
  end

  local resolved_source = resolve_inputs(source, doc_dir)
  local hash = pandoc.sha1(resolved_source)
  return run_pdflatex_and_convert(resolved_source, "tikzfull", hash, doc_dir)
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

local function namespace_svg_ids(svg_tag, prefix)
  -- Prefix all id="..." and xlink:href="#..." to prevent cross-SVG ID collisions
  -- when multiple inline SVGs share one HTML document.
  local result = svg_tag:gsub('id="([^"]*)"', 'id="' .. prefix .. '-%1"')
  result = result:gsub('xlink:href="#([^"]*)"', 'xlink:href="#' .. prefix .. '-%1"')
  return result
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

  -- Namespace IDs using a short hash to prevent cross-SVG collisions
  local hash = pandoc.sha1(svg_tag):sub(1, 8)
  svg_tag = namespace_svg_ids(svg_tag, hash)

  local html = '<div style="text-align:center;">'
    .. '<span class="' .. css_class .. ' pandoc-preview-editable" data-edit-kind="' .. css_class .. '">'
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

    log("RawBlock: processing " .. (is_tikzcd and "tikzcd" or "tikzpicture") .. " block, length=" .. #el.text)
    local _, pdf_path = compile_tikz(el.text)
    if not pdf_path then
      log("RawBlock: compilation FAILED for block")
      assert(pdf_path, "tikzcd.lua: compilation failed for tikz block")
    end
    log("RawBlock: compiled to " .. pdf_path)

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
    local is_pdftex = el.text:match("\\input%s-{(.-%.pdf_tex)}")
    if not is_tikzcd and not is_tikzpic and not is_pdftex then
      return el
    end

    log("RawBlock (html): processing tikz/pdftex block, length=" .. #el.text)
    local svg_path, _ = compile_tikz(el.text)
    if not svg_path then
      log("RawBlock (html): compilation FAILED")
      assert(svg_path, "tikzcd.lua: compilation failed for block")
    end
    log("RawBlock (html): compiled to " .. svg_path)

    local css_class = "tikzcd"
    if is_pdftex then
      css_class = "pdftex"
    elseif not is_tikzcd then
      css_class = "tikzpic"
    end

    return make_html_output(svg_path, css_class)
  end

  function CodeBlock(el)
    if not el.classes:includes("tikz") then
      return el
    end

    log("CodeBlock (html): processing tikz code block, length=" .. #el.text)
    local svg_path, _ = compile_tikz_document(el.text)
    if not svg_path then
      log("CodeBlock (html): compilation FAILED")
      assert(svg_path, "tikzcd.lua: compilation failed for tikz code block")
    end
    log("CodeBlock (html): compiled to " .. svg_path)

    return make_html_output(svg_path, "tikzcode")
  end
end
