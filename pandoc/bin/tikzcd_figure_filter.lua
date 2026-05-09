-- tikzcd_figure_filter.lua
--
-- A pandoc lua filter that finds all tikzcd environments and
-- wraps them in a LaTeX figure environment with \centering.
-- This ensures that TikZ diagrams are properly centered in the
-- final PDF output.

function RawBlock(el)
  -- Check if it's a TeX RawBlock and a tikzcd environment
  if el.format == 'tex' and el.text:match('^\\begin{tikzcd}') then
    -- Create the new LaTeX code with the figure wrapper.
    -- We use the [H] placement specifier from the 'float' package
    -- to ensure the figure is placed exactly here.
    local new_content = {
      '\\begin{figure}[H]',
      '\\centering',
      el.text,
      '\\end{figure}'
    }
    local new_latex = table.concat(new_content, '\n')

    -- Return a new RawBlock with the modified content
    return pandoc.RawBlock('tex', new_latex)
  end
  -- If not a tikzcd environment, return the element unchanged
  return el
end
