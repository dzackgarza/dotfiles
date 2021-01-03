return {
  {
    Math = function (raw)
      if raw.text:match '\\coloneqq' and FORMAT:match 'html' then
        newstring = raw.text:gsub("\\coloneqq", "\\mathrel{\\vcenter{:}}=")
        return pandoc.Math(raw.mathtype, newstring)
      else
        return raw
      end
    end
  }
}
