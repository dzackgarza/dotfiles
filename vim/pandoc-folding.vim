" Smart Pandoc Folding with Beautiful Fold Text
" Features:
" - Headers and fenced divs are independent fold units
" - Smart fold text shows: icon + type + title + ID for fenced divs
" - Three fold text styles: smart (icons + full info), minimal (clean), default (vim default)
" - Key mappings: zf (fold current fenced div), <leader>ft (toggle fold text style)

" Configuration variables
let g:pandoc_folding_enabled = 1
let g:pandoc_fold_style = 'smart'  " Options: 'smart', 'minimal'

function! CustomPandocFold()
    let thisline = getline(v:lnum)
  let nextline = getline(v:lnum + 1)
  let prevline = getline(v:lnum - 1)

  " Handle markdown headers - these define the base fold structure
  let h = matchstr(thisline, '^#\+ \+')
  if !empty(h)
    return ">" . len(h)
  endif

  " Handle fenced div start - these are INDEPENDENT fold units
  if match(thisline, '^:::{\.') >= 0
    " Fenced divs get their own fold level, independent of headers
    " Find the deepest header level to nest properly
    let header_level = 0
    let line_num = v:lnum - 1
    while line_num > 0
      let check_line = getline(line_num)
      let header_match = matchstr(check_line, '^#\+ \+')
      if !empty(header_match)
        let header_level = len(header_match)
        break
      endif
      let line_num = line_num - 1
    endwhile

    " Fenced divs are always one level deeper than their containing header
    " But minimum level 1 if no header found
    let fold_level = max([header_level + 1, 1])
    return ">" . fold_level
  endif

  " Handle fenced div end - close the fold
  if match(thisline, '^:::$') >= 0
    " Find the matching start to determine fold level
    let start_line = v:lnum - 1
    let div_count = 1
    while start_line > 0 && div_count > 0
      let check_line = getline(start_line)
      if match(check_line, '^:::{\.') >= 0
        let div_count = div_count - 1
      elseif match(check_line, '^:::$') >= 0
        let div_count = div_count + 1
      endif
      let start_line = start_line - 1
    endwhile

    " Use the same level as the start
    let header_level = 0
    let line_num = start_line
    while line_num > 0
      let check_line = getline(line_num)
      let header_match = matchstr(check_line, '^#\+ \+')
      if !empty(header_match)
        let header_level = len(header_match)
        break
      endif
      let line_num = line_num - 1
    endwhile

    let fold_level = max([header_level + 1, 1])
    return "<" . fold_level
  endif

  " Default: inherit fold level from previous line
  return "="
endfunction

" Manual folding mode toggle
function! ToggleFoldingMode()
  if &foldmethod == 'expr'
    setlocal foldmethod=manual
    echo "Switched to manual folding mode"
  else
    setlocal foldmethod=expr
    setlocal foldexpr=CustomPandocFold()
    echo "Switched to expression folding mode"
  endif
endfunction

" Smart fenced div folding - works in both manual and expression mode
function! FoldCurrentFencedDiv()
  let current_line = line('.')
  let current_col = col('.')

  " Find the start of the current fenced div
  let start_line = current_line
  let found_start = 0

  " First, check if we're already on a fenced div start line
  if match(getline(current_line), '^:::{\.') >= 0
    let found_start = 1
  else
    " Search backward for fenced div start
    while start_line > 0
      let line_content = getline(start_line)
      if match(line_content, '^:::{\.') >= 0
        let found_start = 1
        break
      elseif match(line_content, '^:::$') >= 0
        " Hit another fenced div end, stop searching
        break
      endif
      let start_line = start_line - 1
    endwhile
  endif

  if !found_start
    echo "Not inside a fenced div"
    return
  endif

  " Find the matching end
  let end_line = start_line + 1
  let found_end = 0

  while end_line <= line('$')
    let line_content = getline(end_line)
    if match(line_content, '^:::$') >= 0
      let found_end = 1
      break
    elseif match(line_content, '^:::{\.') >= 0
      " Hit another fenced div start, this means no matching end
      break
    endif
    let end_line = end_line + 1
  endwhile

  if !found_end
    echo "Could not find matching fenced div end"
    return
  endif

  " Create the fold
  execute start_line . "," . end_line . "fold"
  echo "Folded fenced div from line " . start_line . " to " . end_line

  " Return cursor to original position
  call cursor(current_line, current_col)
endfunction

" Quick fold/unfold for fenced divs
function! ToggleCurrentFencedDiv()
  let current_line = line('.')

  " Check if current line is already folded
  if foldclosed(current_line) != -1
    " Unfold
    normal! zo
    echo "Unfolded fenced div"
  else
    " Fold
    call FoldCurrentFencedDiv()
  endif
endfunction

" (Fold setup moved to bottom of file)

function! SmartFoldText()
  let line = getline(v:foldstart)
  let folded_lines = v:foldend - v:foldstart + 1

  " Handle fenced div folds
  if match(line, '^:::{\.') >= 0
    return FormatFencedDivFold(line, folded_lines)
  endif

  " Handle header folds
  if match(line, '^#\+') >= 0
    return FormatHeaderFold(line, folded_lines)
  endif

  " Default formatting for other folds
  return FormatDefaultFold(line, folded_lines)
endfunction

function! FormatFencedDivFold(line, folded_lines)
  " Extract fenced div components
  let div_type = matchstr(a:line, '{\.\zs[^}#\s]*\ze')
  let div_id = matchstr(a:line, '#\zs[a-zA-Z0-9:_-]*\ze')

  " Fallback if div_type is empty
  if empty(div_type)
    let div_type = "block"
  endif

  " Look for title in the current line and next few lines
  let title = ""
  let max_search = min([v:foldend, v:foldstart + 10])

  " First try to get title from the same line (most common case)
  let title_match = matchstr(a:line, 'title="\zs[^"]*\ze"')
  if !empty(title_match)
    let title = title_match
  else
    " Also try single quotes on same line
    let title_match = matchstr(a:line, "title='\zs[^']*\ze'")
    if !empty(title_match)
      let title = title_match
    else
      " Search subsequent lines if not found on first line
      for line_num in range(v:foldstart + 1, max_search)
        let search_line = getline(line_num)
        let title_match = matchstr(search_line, 'title="\zs[^"]*\ze"')
        if !empty(title_match)
          let title = title_match
          break
        endif
        " Also try single quotes
        let title_match = matchstr(search_line, "title='\zs[^']*\ze'")
        if !empty(title_match)
          let title = title_match
          break
        endif
      endfor
    endif
  endif

  " Clean up title for display
  let clean_title = title
  if !empty(clean_title)
    let clean_title = CleanCitations(clean_title)
    let clean_title = substitute(clean_title, '\$\([^$]*\)\$', '\1', 'g')
    if clean_title =~ '^{.*}$'
      let clean_title = substitute(clean_title, '^{\(.*\)}$', '\1', '')
    endif
  endif

  " Choose icon based on div type
  let icon = GetDivIcon(div_type)

  " Calculate available width for content
  let available_width = &textwidth > 0 ? &textwidth : 80
  let fold_info = " (" . a:folded_lines . "L)"

  " Create aligned single-line display with smart truncation
  let type_field_width = 14  " icon + space + longest_type + colon + space
  let type_part = icon . " " . div_type
  let padding_needed = type_field_width - len(type_part) - 2  " -2 for ": "
  let padding = repeat(" ", max([0, padding_needed]))

  let line_start = type_part . padding . ": "

  " Calculate remaining space for title and ID
  let remaining_width = available_width - len(line_start) - len(fold_info) - 2

  " Smart content arrangement: prioritize title, add ID if space allows
  let content = ""
  if !empty(clean_title)
    if !empty(div_id)
      " Both title and ID - check if both fit
      let full_content = clean_title . " [#" . div_id . "]"
      if len(full_content) <= remaining_width
        let content = full_content
      else
        " Truncate title to make room for ID
        let id_part = " [#" . div_id . "]"
        let title_space = remaining_width - len(id_part)
        if title_space > 10  " Only truncate if we have reasonable title space
          let content = clean_title[:title_space-4] . "..." . id_part
        else
          " Not enough space for both - show only title
          let content = len(clean_title) <= remaining_width ? clean_title : clean_title[:remaining_width-4] . "..."
        endif
      endif
    else
      " Only title
      let content = len(clean_title) <= remaining_width ? clean_title : clean_title[:remaining_width-4] . "..."
    endif
  elseif !empty(div_id)
    " Only ID
    let content = "[#" . div_id . "]"
  endif

  " Assemble final line with proper spacing
  let result = line_start . content
  let current_length = len(result)

  if current_length < available_width - 10
    let fill_chars = available_width - current_length - len(fold_info)
    let result .= repeat(" ", max([1, fill_chars])) . fold_info
  else
    let result .= fold_info
  endif

  return result
endfunction

function! CleanCitations(text)
  let result = a:text

  " Handle \cite[optional]{reference} format
  " Pattern: \cite[anything]{anything}
  let cite_pattern = '\\cite\[\([^\]]*\)\]{\([^}]*\)}'
  while match(result, cite_pattern) >= 0
    let optional = substitute(result, '.*\\cite\[\([^\]]*\)\]{\([^}]*\)}.*', '\1', '')
    let reference = substitute(result, '.*\\cite\[\([^\]]*\)\]{\([^}]*\)}.*', '\2', '')
    let clean_cite = optional . ' (' . reference . ')'
    let result = substitute(result, cite_pattern, clean_cite, '')
  endwhile

  " Handle simple \cite{reference} format
  let simple_cite_pattern = '\\cite{\([^}]*\)}'
  while match(result, simple_cite_pattern) >= 0
    let reference = substitute(result, '.*\\cite{\([^}]*\)}.*', '\1', '')
    let clean_cite = '(' . reference . ')'
    let result = substitute(result, simple_cite_pattern, clean_cite, '')
  endwhile

  " Handle other common citation commands
  let result = substitute(result, '\\citep{\([^}]*\)}', '(\1)', 'g')
  let result = substitute(result, '\\citet{\([^}]*\)}', '\1', 'g')
  let result = substitute(result, '\\citeauthor{\([^}]*\)}', '\1', 'g')
  let result = substitute(result, '\\citeyear{\([^}]*\)}', '\1', 'g')

  return result
endfunction

function! GetDivIcon(div_type)
  let icons = {
    \ 'definition': '📚',
    \ 'theorem': '◆',
    \ 'proposition': '◇',
    \ 'lemma': '◯',
    \ 'corollary': '◈',
    \ 'proof': '∎',
    \ 'remark': '💭',
    \ 'example': '📝',
    \ 'question': '❓',
    \ 'strategy': '🎯',
    \ 'goal': '🎯',
    \ 'block': '📄'
    \ }

  " Always return an icon, even for unknown types
  let icon = get(icons, a:div_type, '📄')

  " Double-check we actually have an icon
  if empty(icon)
    let icon = '📄'
  endif

  return icon
endfunction

function! FormatHeaderFold(line, folded_lines)
  " Extract header level and text
  let header_level = len(matchstr(a:line, '^#\+'))
  let header_text = substitute(a:line, '^#\+\s*', '', '')

  " Choose icon based on header level
  let level_icons = ['📁', '📂', '📋', '📄', '📝', '📃']
  let icon = get(level_icons, header_level - 1, '📄')

  " Format with appropriate indentation
  let indent = repeat("  ", header_level - 1)
  let result = indent . icon . " " . header_text

  " Add fold info
  let available_width = &textwidth > 0 ? &textwidth : 80
  let current_length = len(result)
  if current_length < available_width - 10
    let fill_chars = available_width - current_length - 8
    let result .= repeat(" ", max([1, fill_chars])) . "(" . a:folded_lines . "L)"
  endif

  return result
endfunction

function! FormatDefaultFold(line, folded_lines)
  " Clean up the line and add fold info
  let clean_line = substitute(a:line, '^\s*', '', '')
  let clean_line = substitute(clean_line, '"\+', '', 'g')

  let available_width = &textwidth > 0 ? &textwidth : 80
  let max_text_width = available_width - 15

  if len(clean_line) > max_text_width
    let clean_line = clean_line[:max_text_width-3] . "..."
  endif

  let fill_chars = available_width - len(clean_line) - 8
  return clean_line . repeat(" ", max([1, fill_chars])) . "(" . a:folded_lines . "L)"
endfunction

" (Duplicate mappings and setup removed - consolidated at bottom)

" Toggle between fold text styles
function! ToggleFoldTextStyle()
  if g:pandoc_fold_style == 'smart'
    let g:pandoc_fold_style = 'minimal'
    setlocal foldtext=MinimalFoldText()
    echo "Switched to minimal fold text"
  else
    let g:pandoc_fold_style = 'smart'
    setlocal foldtext=SmartFoldText()
    echo "Switched to smart fold text"
  endif
  " Force redraw of folds
  normal! zx
endfunction

" (Multi-line folds removed - not supported by Vim/Neovim)

function! MinimalFoldText()
  let line = getline(v:foldstart)

  " For fenced divs, show just type and title
  if match(line, '^:::{\.') >= 0
    let div_type = matchstr(line, '{\.\zs[^}#\s]*\ze')
    let title = ""

    " Look for title
    let max_search = min([v:foldend, v:foldstart + 5])
    for line_num in range(v:foldstart, max_search)
      let search_line = getline(line_num)
      let title_match = matchstr(search_line, 'title="\zs[^"]*\ze"')
      if !empty(title_match)
        let title = title_match
        break
      endif
    endfor

    let clean_title = CleanCitations(title)
    let clean_title = substitute(clean_title, '\$\([^$]*\)\$', '\1', 'g')

    " Get icon for this div type
    let icon = GetDivIcon(div_type)

    " Use same alignment as SmartFoldText
    let type_field_width = 14
    let type_part = icon . " " . div_type
    let padding_needed = type_field_width - len(type_part) - 2
    let padding = repeat(" ", max([0, padding_needed]))

    let result = type_part . padding . ": "

    if !empty(clean_title)
      let result .= clean_title
    endif
    return result
  endif

  " For headers, show just the text
  if match(line, '^#\+') >= 0
    return substitute(line, '^#\+\s*', '', '')
  endif

  " Default: just the line
  return substitute(line, '^\s*', '', '')
endfunction

" Test current fold text
function! TestCurrentFoldText()
  let current_line = line('.')
  let fold_start = foldclosed(current_line)

  if fold_start == -1
    echo "No fold at current line"
    return
  endif

  " Temporarily set variables for testing
  let old_foldstart = get(v:, 'foldstart', 0)
  let old_foldend = get(v:, 'foldend', 0)

  let v:foldstart = fold_start
  let v:foldend = foldclosedend(current_line)

  echo "Fold text: " . SmartFoldText()

  let v:foldstart = old_foldstart
  let v:foldend = old_foldend
endfunction

" Debug icon display issues
function! DebugFoldIcons()
  let current_line = line('.')
  let line_content = getline(current_line)

  echo "=== Fold Icon Debug ==="
  echo "Line: " . current_line
  echo "Content: " . line_content

  if match(line_content, '^:::{\.') >= 0
    let div_type = matchstr(line_content, '{\.\zs[^}#\s]*\ze')
    echo "Detected div_type: '" . div_type . "'"
    echo "Icon for this type: '" . GetDivIcon(div_type) . "'"
    echo "Current fold text style: " . g:pandoc_fold_style

    let fold_start = foldclosed(current_line)
    if fold_start != -1
      echo "This line is folded, fold starts at: " . fold_start
      echo "Fold text would be: " . (g:pandoc_fold_style == 'minimal' ? 'MinimalFoldText()' : 'SmartFoldText()')
    else
      echo "This line is not currently folded"
    endif
  else
    echo "This line is not a fenced div start"
  endif
endfunction

" (Commands and mappings consolidated below)

" Set up folding and mappings
if get(g:, 'pandoc_folding_enabled', 1)
  " Use expression folding with our custom function
setlocal foldmethod=expr
setlocal foldexpr=CustomPandocFold()

  " Improve folding performance and behavior
  setlocal foldminlines=1
  setlocal foldnestmax=10

  " Set appropriate fold text style based on configuration
  if g:pandoc_fold_style == 'minimal'
    setlocal foldtext=MinimalFoldText()
  else
    setlocal foldtext=SmartFoldText()
  endif

  " Define commands
  command! -buffer ToggleFoldText call ToggleFoldTextStyle()
  command! -buffer TestFoldText call TestCurrentFoldText()
  command! -buffer DebugFoldIcons call DebugFoldIcons()

  " Core folding mappings
  nnoremap <buffer> zf :call FoldCurrentFencedDiv()<CR>
  nnoremap <buffer> zF :call FoldCurrentFencedDiv()<CR>

  " Fold text style controls
  nnoremap <buffer> <leader>ft :call ToggleFoldTextStyle()<CR>
  nnoremap <buffer> <leader>fm :call ToggleFoldingMode()<CR>

  " Debug and testing
  nnoremap <buffer> <leader>fT :call TestCurrentFoldText()<CR>
  nnoremap <buffer> <leader>fD :call DebugFoldIcons()<CR>

  " Fenced div-specific folding
  nnoremap <buffer> <leader>za :call ToggleCurrentFencedDiv()<CR>
  nnoremap <buffer> <leader>fd :call FoldCurrentFencedDiv()<CR>

  " Visual mode: create manual fold from selection (preserve original behavior)
  vnoremap <buffer> zf :<C-u>setlocal foldmethod=manual<CR>gv:fold<CR>

  " Quick folding operations
  nnoremap <buffer> <leader>zo :normal! zo<CR>
  nnoremap <buffer> <leader>zc :normal! zc<CR>
  nnoremap <buffer> <leader>zr :normal! zr<CR>

  " Navigation between fenced divs
  nnoremap <buffer> ]d /^:::{<CR>
  nnoremap <buffer> [d ?^:::{<CR>

  " Override global foldmethod for this filetype
  autocmd BufEnter <buffer> if &filetype =~ 'pandoc\|markdown' | setlocal foldmethod=expr foldexpr=CustomPandocFold() | endif
endif

