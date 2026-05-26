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
  },
  {
  Str = function (elem)
      if elem.text:match 'unanswered_questions' then
        newstring = elem.text:gsub("[()]?#unanswered_questions[)]?", "")
        return pandoc.Str(newstring)
      else
        return elem
      end
    end
  }
}
