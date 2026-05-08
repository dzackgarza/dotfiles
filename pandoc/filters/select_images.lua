-- Lua filter to select appropriate image format
function Image(img)
  if FORMAT == 'latex' and img.src:match("%.svg$") then
    local pdf_src = img.src:gsub("%.svg$", ".pdf")
    img.src = pdf_src
    return img
  end
end
