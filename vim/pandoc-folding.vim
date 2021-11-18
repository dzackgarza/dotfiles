function! CustomPandocFold()
  let h = matchstr(getline(v:lnum), '^#\+ \+')     
  if empty(h)       
    let thisline = getline(v:lnum)
    if match(thisline, '^\:\:\:{\.solution') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.concept') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.proposition') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.slogan') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.warnings') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.solution') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.exercise') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.example') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.remark') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.answer') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.question') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.conjecture') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.observation') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.theorem') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.proof') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.definition') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.fact') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.claim') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.corollary') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.problem') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.lemma') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:{\.strategy') >= 0
      return "a1"
    elseif match(thisline, '^\:\:\:$') >= 0
      return "s1"
    else
      return "="
    endif
  else       
    return ">" . len(h)     
  endif 
endfunction

setlocal foldmethod=expr
setlocal foldexpr=CustomPandocFold()

function! MyFoldText()
    let line = getline(v:foldstart)
    let folded_line_num = v:foldend - v:foldstart
    let line_text = substitute(line, '^"{\+', '', 'g')
    let fillcharcount = &textwidth - len(line_text) - len(folded_line_num)
    return line_text . repeat('.', fillcharcount) . repeat('-', 30) . ' (' . folded_line_num . ' L)'
endfunction
set foldtext=MyFoldText()

