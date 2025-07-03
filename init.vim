" vim: filetype=vim foldmethod=marker foldlevel=0 foldcolumn=3
"
" File:       init.vim (Neovim configuration)
" Github:     http://github.com/dzackgarza/dotfiles
" Maintainer:
"   _____       ______   ______   ______   __  __       ______   ______   ______  ______   ______
"  /\  __-.    /\___  \ /\  __ \ /\  ___\ /\ \/ /      /\  ___\ /\  __ \ /\  == \/\___  \ /\  __ \
"  \ \ \/\ \   \/_/  /__\ \  __ \\ \ \____\ \  _"-.    \ \ \__ \\ \  __ \\ \  __<\/_/  /__\ \  __ \
"   \ \____-     /\_____\\ \_\ \_\\ \_____\\ \_\ \_\    \ \_____\\ \_\ \_\\ \_\ \_\/\_____\\ \_\ \_\
"    \/____/     \/_____/ \/_/\/_/ \/_____/ \/_/\/_/     \/_____/ \/_/\/_/ \/_/ /_/\/_____/ \/_/\/_/
"
"　　 人　 　　　  　 人　 　　　  人　 　　　　 人
"　 ( ﾟーﾟ) 　 　  ( ﾟーﾟ) 　 　 ( ﾟーﾟ) 　 　 ( ﾟーﾟ)
"　  ￣￣　 　　　   ￣￣　　　　 ￣￣　 　　　 ￣￣
" ┏━━━━━━━━━━━━━━━━━━━━━┓━━━━━━━━━━━━━━━━━━━━━━━━┓
" ┃⇒ Attack             ┃ Items                 .┃
" ┃　Spells　　　       ┃ Equipment             .┃
" ┃　Skills 　　　      ┃ Psyche Up             .┃
" ┃　Defend 　　　      ┃ Flee                  .┃
" ┗━━━━━━━━━━━━━━━━━━━━━┛━━━━━━━━━━━━━━━━━━━━━━━━┛

" --- Core Settings & Boilerplate {{{
set nocompatible
filetype plugin on
syntax on
set termguicolors     " enable true colors support

set nobackup          " No backup files
set nowb
set noswapfile
set encoding=utf-8

set mouse=a           " Enable mouse support
set ignorecase        " Case-insensitive searching
set smartcase         " except when uppercase letters are used

" Indentation
set tabstop=2
set softtabstop=2
set shiftwidth=2
set expandtab
set shiftround

" Persistent Undo
let s:undoDir = "/tmp/.undodir_" . $USER
if !isdirectory(s:undoDir)
    call mkdir(s:undoDir, "", 0700)
endif
let &undodir=s:undoDir
set undofile
" }}}

" Use your custom wordlist for both completion and spell additions
set dictionary=~/dotfiles/dictionaries/corpus.add
set spellfile=~/dotfiles/dictionaries/corpus.add

" Use your comprehensive base dictionary for spell suggestions
set spelllang=en_us
set spell
set spellsuggest=best,9

" Tell Vim to look for .spl files in this directory as well
set runtimepath+=~/dotfiles/dictionaries

" Enable completion from dictionary and spell suggestions
set complete+=kspell

" Less aggressive spell checking for technical writing
set spellcapcheck=
set spelloptions=camel


" --- Plugins {{{
call plug#begin()

" Writing & Syntax
Plug 'vim-pandoc/vim-pandoc-syntax'
Plug 'MarcWeber/vim-addon-mw-utils' " Pandoc dependency
Plug 'tomtom/tlib_vim'             " Pandoc dependency
Plug 'lervag/vimtex'
Plug 'dzackgarza/quicktex'
Plug 'vim-voom/VOoM' " Outliner
Plug 'Raimondi/delimitMate'
Plug 'evansalter/vim-checklist'
Plug 'tpope/vim-commentary' " Replaces nerdcommenter for minimalism

" Autocompletion
Plug 'neoclide/coc.nvim', {'branch': 'release'}

" Fuzzy Finding
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'

" Aesthetics
Plug 'folke/tokyonight.nvim'
Plug 'ryanoasis/vim-devicons' " For VOoM and other UIs

call plug#end()
" }}}

" --- Plugin Configuration {{{

" CoC Configuration for Academic Mathematics Writing
let g:coc_config_home = "~/dotfiles"

" Essential extensions for math writing
let g:coc_global_extensions = [
      \ 'coc-vimtex',
      \ 'coc-dictionary',
      \ 'coc-word',
      \ 'coc-spell-checker',
      \ 'coc-snippets',
      \ 'coc-json',
      \ 'coc-sh',
      \]

" Project labels management for autocomplete - ASYNCHRONOUS
function! UpdateProjectLabels()
  " Asynchronous update to prevent blocking file operations
  if has('nvim') || has('job')
    " Use job control for async execution
    if has('nvim')
      call jobstart('find_project_labels.sh > ~/.cache/project-labels.txt 2>/dev/null', {
            \ 'on_exit': function('OnProjectLabelsUpdated')
            \ })
    else
      call job_start('find_project_labels.sh > ~/.cache/project-labels.txt 2>/dev/null', {
            \ 'exit_cb': function('OnProjectLabelsUpdated')
            \ })
    endif
  else
    " Fallback: background process (fire and forget)
    call system('find_project_labels.sh > ~/.cache/project-labels.txt 2>/dev/null &')
  endif
endfunction

function! OnProjectLabelsUpdated(...)
  " Called when async update completes
  if filereadable(expand('~/.cache/project-labels.txt'))
    let label_count = substitute(system('wc -l < ~/.cache/project-labels.txt'), '\n', '', 'g')
    echom "Project labels updated: " . label_count . " labels"
  endif
endfunction

" Update project labels on file saves with throttling (async, non-blocking)
let g:last_label_update = 0
autocmd BufWritePost *.md,*.tex,*.latex call AsyncUpdateLabelsThrottled()

function! AsyncUpdateLabelsThrottled()
  " Throttle updates to max once per 30 seconds
  let current_time = localtime()
  if (current_time - g:last_label_update) > 30
    let g:last_label_update = current_time
    call UpdateProjectLabels()
  endif
endfunction

" REMOVED: No longer block file opening with tag updates
" Only run lightweight cache check on first markdown/tex file in session
let g:labels_initialized = 0
autocmd FileType markdown,tex call InitProjectLabelsOnce()

function! InitProjectLabelsOnce()
  if !g:labels_initialized
    let g:labels_initialized = 1
    call InitProjectLabels()
  endif
endfunction

function! InitProjectLabels()
  " Lightweight initialization - just ensure cache directory exists
  " No blocking operations on file open
  call system('mkdir -p ~/.cache')

  " Only update if cache is missing or very old (>1 hour)
  let cache_file = expand('~/.cache/project-labels.txt')
  if !filereadable(cache_file) || (localtime() - getftime(cache_file)) > 3600
    call UpdateProjectLabels()
  endif
endfunction

" Manual label update command (synchronous for immediate feedback)
function! UpdateProjectLabelsSync()
  call system('mkdir -p ~/.cache')
  call system('find_project_labels.sh > ~/.cache/project-labels.txt 2>/dev/null')
  let label_count = substitute(system('wc -l < ~/.cache/project-labels.txt'), '\n', '', 'g')
  echo "Project labels updated: " . label_count . " labels"
endfunction

" Zotero integration functions
function! ZoteroSearch()
  " Interactive Zotero search - opens Zotero's search interface
  let api_call = 'http://127.0.0.1:23119/better-bibtex/cayw?format=cite&brackets=1'
  let ref = system('curl -s ' . shellescape(api_call))
  return substitute(ref, '\n', '', 'g')
endfunction

function! ZoteroSearch()
  " Interactive Zotero search - opens Zotero's search interface
  let api_call = 'http://127.0.0.1:23119/better-bibtex/cayw?format=cite&brackets=1&minimize=1'
  let ref = system('curl -s ' . shellescape(api_call))
  return substitute(ref, '\n', '', 'g')
endfunction

function! TestZoteroConnection()
  " Test if Zotero Better BibTeX is running
  let test_call = 'http://127.0.0.1:23119/better-bibtex/cayw?format=json'
  let response = system('curl -s -w "%{http_code}" -o /dev/null ' . shellescape(test_call))
  if response == '200'
    echo "Zotero Better BibTeX is running"
    return 1
  else
    echo "Zotero Better BibTeX not available (HTTP " . response . ")"
    return 0
  endif
endfunction

" Two-stage reference selection interface
function! SelectReferenceType()
  " First stage: Choose between internal labels or external citations
  let options = [
        \ 'INTERNAL: Cross-references (figures, tables, equations, sections)',
        \ 'EXTERNAL: Citations from Zotero library',
        \ 'TEST: Test Zotero connection'
        \ ]

  call fzf#run(fzf#wrap({
        \ 'source': options,
        \ 'sink': function('ProcessReferenceType'),
        \ 'options': ['--prompt=Reference Type> ', '--preview-window=hidden', '--height=40%'],
        \ 'down': '30%'
        \ }))
endfunction

function! ProcessReferenceType(selection)
  if a:selection =~ '^INTERNAL:'
    call InsertInternalReference()
  elseif a:selection =~ '^EXTERNAL:'
    call InsertExternalCitation()
  elseif a:selection =~ '^TEST:'
    call TestZoteroConnection()
  endif
endfunction

" Internal reference insertion (labels from project)
function! InsertInternalReference()
  let labels_file = expand('~/.cache/project-labels.txt')

  if !filereadable(labels_file)
    echo "No project labels found. Run :call UpdateProjectLabels() first."
    return
  endif

  let project_labels = readfile(labels_file)
  let formatted_labels = []

  for label in project_labels
    let clean_label = substitute(label, '^#', '', '')  " Remove # prefix
    let clean_label = substitute(clean_label, '\s*$', '', '')  " Trim whitespace
    call add(formatted_labels, clean_label . ' → \Cref{' . clean_label . '}')
  endfor

  if empty(formatted_labels)
    echo "No project labels available"
    return
  endif

  call fzf#run(fzf#wrap({
        \ 'source': formatted_labels,
        \ 'sink': function('ProcessInternalReference'),
        \ 'options': ['--prompt=Internal Ref> ', '--preview-window=hidden'],
        \ 'down': '40%'
        \ }))
endfunction

function! ProcessInternalReference(selection)
  " Extract label from selection and insert \Cref{label}
  let label = substitute(a:selection, ' →.*', '', '')
  let label = substitute(label, '\s*$', '', '')  " Trim whitespace
  execute 'normal! a\Cref{' . label . '}'
endfunction

" External citation insertion (Zotero)
function! InsertExternalCitation()
  echo "Opening Zotero search interface..."
  let citation = ZoteroSearch()

  if !empty(citation) && citation !~ '^$'
    execute 'normal! a' . citation
    echo "Citation inserted: " . citation
  else
    echo "No citation selected or Zotero not available"
  endif
endfunction

" Quick Zotero citation (bypass selection interface)
function! QuickZoteroCite()
  let citation = ZoteroCite()

  if !empty(citation) && citation !~ '^$'
    execute 'normal! a' . citation
    echo "Citation inserted: " . citation
  else
    echo "No citation selected or Zotero not available"
  endif
endfunction

" Auto-completion sources priority for math writing
autocmd FileType markdown,tex let b:coc_sources = [
      \ 'vimtex',
      \ 'dictionary',
      \ 'spell-checker',
      \ 'word',
      \ 'snippets'
      \]

" Better popup menu colors for readability
highlight PmenuSel ctermbg=blue ctermfg=white
highlight Pmenu ctermbg=gray ctermfg=black

" CoC settings via coc-settings.json equivalent
let g:coc_user_config = {
      \ 'suggest.autoTrigger': 'always',
      \ 'suggest.minTriggerInputLength': 0,
      \ 'suggest.timeout': 5000,
      \ 'suggest.enablePreview': v:true,
      \ 'suggest.maxCompleteItemCount': 50,
      \ 'suggest.triggerAfterInsertEnter': v:true,
      \ 'dictionary.enable': v:true,
      \ 'dictionary.priority': 50,
      \ 'dictionary.maxItemCount': 20,
      \ 'spell-checker.enableDictionaries': ['en', 'medical', 'mathematical'],
      \ 'vimtex.enabled': v:true,
      \ 'snippets.priority': 60,
      \ 'snippets.extends': {
      \   'markdown': ['tex'],
      \   'tex': ['markdown']
      \ }
      \}

" Project structure awareness
let g:coc_data_home = expand('~/.config/coc')
let g:python3_host_prog = '/usr/bin/python3'

" Optional: Auto-test Zotero connection on startup for tex/markdown files
" autocmd FileType markdown,tex silent! call TestZoteroConnection()

" delimitMate
let delimitMate_matchpairs = "{:},(:)"

" quicktex
autocmd Filetype markdown.pandoc let g:enable_quicktex = 1
" See `~/.config/nvim/after/ftplugin/pandoc/quicktex_dict.vim`

" fzf
if executable('ag')
  let $FZF_DEFAULT_COMMAND = 'ag -g ""'
endif

" }}}

" --- Aesthetics & UI {{{
colorscheme tokyonight-moon
set background=dark

" Line Numbers
set number
set relativenumber

" Cursor & Scrolling
set cursorline
set scrolloff=8 " Keep 8 lines visible above/below cursor

" Concealing for cleaner text - FIXED for better editing experience
set conceallevel=2
set concealcursor=    " CRITICAL: conceals disappear when cursor is on the line (enables proper editing)
hi clear Conceal
hi Normal guibg=NONE ctermbg=NONE

" Additional conceal settings for math files
autocmd FileType tex,markdown,pandoc setlocal concealcursor=
autocmd FileType tex,markdown,pandoc setlocal conceallevel=2

" Folding
set foldmethod=marker
set foldcolumn=3
set foldlevel=2
let g:markdown_folding = 1

" Statusline
set statusline=%F " Show file path
set statusline+= " " " Space
set statusline+=%{SyntaxItem()} " Show syntax group under cursor

" }}}

" --- Key Mappings {{{
let mapleader=","

" General Mappings
nnoremap <CR> :noh<CR><CR> " Clear search highlight with Enter
nnoremap Q <nop>           " Disable Ex mode
nnoremap ZZ :wqa<CR>       " Save and quit all

" Save buffer
nnoremap <c-space> :w<CR>o
inoremap <c-space> <Esc>:w<CR>o

" Terminal mappings
tnoremap <Esc> <C-\><C-n>

" FZF Mappings
nnoremap <C-p> :GitFiles<Cr>
nnoremap <C-f> :Ag<Cr>
nnoremap <silent> <Leader>f :Ag <C-R><C-W><CR> " Search for word under cursor

" Leader Mappings
nnoremap <Leader>w :w<CR>               " Write
nnoremap <Leader>o o<Esc>k              " Insert new line below
nnoremap <Leader>O O<Esc>j              " Insert new line above
" nnoremap <Leader>c :let &cole=(&cole == 2) ? 0 : 2<CR> " Toggle conceal
nnoremap <Leader>ll :let @+=expand("%:p")<CR> " Copy file path
nnoremap <leader>? :call ShowCustomCommands()<CR>  " Show all custom commands/shortcuts
nnoremap <leader>help :call ShowCustomCommands()<CR> " Show help popup
nnoremap <leader>fc :FixConceal<CR>     " Fix conceal rules
nnoremap <leader>dc :DebugConceal<CR>   " Debug conceal issues
nnoremap <leader>cc :let &cole=(&cole == 2) ? 0 : 2<CR> " Toggle conceal level
nnoremap <leader>vc :ValidateConceal<CR> " Validate conceal rules for conflicts
nnoremap <leader>tc :TestConcealFixes<CR> " Test conceal fixes with sample math

" Navigation
nnoremap <silent> [[ ?^\:\:\:{<CR> " Jump to previous pandoc divider
nnoremap <silent> ]] /^\:\:\:{<CR> " Jump to next pandoc divider
nnoremap <silent> <leader>zj :call NextClosedFold('j')<cr>
nnoremap <silent> <leader>zk :call NextClosedFold('k')<cr>

" Math Conversion Mappings
" Replace inline math $...$ with display math \[ ... \]
nnoremap <silent> <Leader>gs F$xvt$"+dxi\[<cr><cr>.\]<Esc>k"+P
" Replace inline math $...$ with \( ... \)
nnoremap <silent> <Leader>gb F$xvt$"+dxi\(  \)<Esc>hh"+P
" Replace displaymath $$...$$ with displaymath \[ ... \]
nnoremap <silent> <Leader>ga /\$\$<cr>Nxxwvnk$"+dknxxi\[<esc>"+p<esc>o.\]<esc>

" Workflow Mappings
nmap <silent> <leader>qp :call PasteQuiverDiagram()<CR>

" }}}

" --- Custom Functions {{{

" Jump between closed folds
function! NextClosedFold(dir)
    let cmd = 'norm!z' . a:dir
    let view = winsaveview()
    let [l0, l, open] = [0, view.lnum, 1]
    while l != l0 && open
        exe cmd
        let [l0, l] = [l, line('.')]
        let open = foldclosed(l) < 0
    endwhile
    if open
        call winrestview(view)
    endif
endfunction

" Custom Pandoc syntax highlighting and conceals - integrated with tex conceal rules
function! s:pandocSyntax()
  set filetype=markdown.pandoc
  setlocal spell

  " Ensure tex syntax is available for math zones
  runtime! syntax/tex.vim

  " Set up proper math zones that work with tex conceal rules
  " This allows the tex.vim conceal rules to work properly
  syn cluster texMathZoneGroup add=pandocLaTeXMathBlock,pandocLaTeXInlineMath

  " Fenced div conceals - minimal and non-conflicting
  syntax match DZGFenceConc /^:::/ conceal cchar=┌
  syntax match DZGFenceConc /^:::$/ conceal cchar=└

  " Title attribute concealing - fixed pattern
  syntax match DZGTitleConc /title=\"[^\"]*\"/ contained conceal
  syntax match DZGTitleConc /title='[^']*'/ contained conceal

  " Enhanced fenced div regions that preserve math zones
  syn region DZGFencedDiv start='^:::{' end='^:::$' transparent fold contains=DZGFenceDivAttrBlock,DZGMetaBlock,DZGFenceConc,pandocLaTeXMathBlock,pandocLaTeXInlineMath,@texMathZoneGroup
  syn region DZGFenceDivAttrBlock start='^:::{' end='^$\|^```\|}$\|^[^ .#]' keepend contains=DZGFenceConc,DZGFenceDivClassPrefix,DZGClassName,DZGTitleAttr,DZGTitlePrefix,DZGTitleValue,DZGIdDefPrefix,DZGIdDefValue,DZGIdThmPrefix,DZGIdThmValue,DZGIdRemPrefix,DZGIdRemValue,DZGClassAttr,DZGFenceDivAttrClose
  syn region DZGMetaBlock start='^```meta' end='^```$' keepend contains=@DZGYamlAll,DZGMetaDelimiter

  " Math regions that work with tex conceal - using pandoc's existing zones
  syn region DZGMathInline start='\$' end='\$' contained keepend
        \ contains=@texMathZoneGroup,texMathSymbol
  syn region DZGMathDisplay start='\$\$' end='\$\$' contained keepend
        \ contains=@texMathZoneGroup,texMathSymbol

  " Ensure LaTeX commands in fenced divs get proper highlighting
  syn match DZGLatexCmd '\\[a-zA-Z]*' contained contains=@texMathZoneGroup

  " Clean up other minor conceals
  syntax match DZGMiscConc /\\\\hfill/ conceal cchar=—

  " Highlight groups
  hi def link DZGFencedDiv Special
  hi def link DZGTitleConc Conceal
  hi def link DZGLatexCmd Statement
  hi def link DZGMiscConc Conceal

  " Make sure tex math symbols are properly highlighted
  hi def link texMathSymbol Identifier
  hi def link texBoldMathText Special

  " Conceal all of ':::{.' at the start of a fenced div attribute block
  syn match DZGFenceDivClassPrefix /^:::{\./ contained conceal cchar=╔
  " Conceal closing brace '}' with the same icon as closing ':::'
  syn match DZGFenceDivAttrClose /^}$/ contained conceal cchar=╚
  " Update attribute block region to include DZGFenceDivClassPrefix
  syn region DZGFenceDivAttrBlock start='^:::{' end='^$\|^```\|}$\|^[^ .#]' keepend contains=DZGFenceConc,DZGFenceDivClassPrefix,DZGClassName,DZGTitleAttr,DZGTitlePrefix,DZGTitleValue,DZGIdDefPrefix,DZGIdDefValue,DZGIdThmPrefix,DZGIdThmValue,DZGIdRemPrefix,DZGIdRemValue,DZGClassAttr,DZGFenceDivAttrClose
  " Remove old per-class dot conceal rules (DZGClassDefinitionDot, etc.) from contains

  " Highlight class names as Special
  hi def link DZGClassName Special
  hi def link DZGClassDefinitionDot Special
  hi def link DZGClassTheoremDot Special
  hi def link DZGClassLemmaDot Special
  hi def link DZGClassCorollaryDot Special
  hi def link DZGClassProofDot Special
  hi def link DZGClassRemarkDot Special
  hi def link DZGIdDefValue Identifier
  hi def link DZGIdThmValue Identifier
  hi def link DZGIdRemValue Identifier
  hi def link DZGTitleValue String
  hi def link DZGIdDefPrefix Special
  hi def link DZGIdThmPrefix Special
  hi def link DZGIdRemPrefix Special
  hi def link DZGMetaBlock Special
  hi def link DZGMetaDelimiter Comment
  hi def link yamlMappingKey Identifier
  hi def link yamlString String
  hi def link yamlFlowString String
  hi def link yamlComment Comment
  hi def link yamlBool Constant
  hi def link yamlNull Constant
  hi def link yamlInteger Number
  hi def link yamlFloat Float
  hi def link yamlKeyValueDelimiter Special

  runtime! syntax/yaml.vim
  syn cluster DZGYamlAll contains=@yamlBlockNode,yamlComment,yamlMappingKey,yamlString,yamlFlowString
  syn cluster DZGYamlAll add=yamlBool,yamlNull,yamlInteger,yamlFloat,yamlTimestamp
  syn cluster DZGYamlAll add=yamlBlockMappingKey,yamlFlowMappingKey,yamlKeyValueDelimiter
  syn cluster DZGYamlAll add=yamlBlockCollectionItemStart,yamlFlowIndicator

  syn match DZGMetaDelimiter /^```meta$/ contained conceal cchar=╔
  syn match DZGMetaDelimiter /^```$/ contained conceal cchar=╚
  syn region DZGMetaBlock start='^```meta$' end='^```$' keepend contains=@DZGYamlAll,DZGMetaDelimiter

  " Attribute tag matches for highlighting and conceal
  syntax match DZGTitleAttr /title=/ contained
  syntax match DZGTitlePrefix /title=/ contained conceal
  syntax match DZGTitleValue /"[^"]*"/ contained

  syntax match DZGIdDefPrefix /#def:/ contained conceal cchar=🏷️
  syntax match DZGIdDefValue /#def:\zs[a-zA-Z0-9_:-]\+/ contained
  syntax match DZGIdThmPrefix /#thm:/ contained conceal cchar=🏷️
  syntax match DZGIdThmValue /#thm:\zs[a-zA-Z0-9_:-]\+/ contained
  syntax match DZGIdRemPrefix /#rem:/ contained conceal cchar=🏷️
  syntax match DZGIdRemValue /#rem:\zs[a-zA-Z0-9_:-]\+/ contained
endfunction

" Paste image from clipboard (requires wl-paste for Wayland)
function! PasteImage()
  let this_file_dir = expand("%:p:h")
  let s = substitute(system("date '+%Y-%m-%d_%H-%M-%S' "), '\n\+$', '', '')
  let t = system("mkdir -p '".this_file_dir."/figures' && wl-paste > '".this_file_dir."/figures/".s.".png'")
  let md_text = "![](figures/" . s . ".png)"
  execute "normal! o".md_text
endfunction
nmap <silent> <leader>i :call CreateInkscape()<CR> " This seems to call a function not defined, keeping map for now
nmap <silent> <leader>p :call PasteImage()<CR>

" Paste Quiver diagram link
function! PasteQuiverDiagram()
  normal  "+pdd/end
  o pdwi> [Link to Diagram]( A) :w
endfunction

" Get citation from Zotero
"function! ZoteroCite()
  "let api_call = 'http://127.0.0.1:23119/better-bibtex/cayw?format=cite&brackets=1'
  "let ref = system('curl -s '.shellescape(api_call))
  "return ref
"endfunction
"inoremap <C-r> <C-r>=ZoteroCite()<CR>
"inoremap <expr> <c-x><c-m> fzf#vim#complete("find_all_latex_labels.sh")


" Legacy math conversion
function! ConvertOldMath()
    let l:save = winsaveview()
    %s/\\definedas/\\da/g
    %s/\\begin{align\*}/\\[/g
    %s/\\end{align\*}/\\]/g
    %s/\\begin{center}//g
    %s/\\end{center}//g
    %s/\(\a\{1}\)\/\([kKS]\)/\1_{\/\2}/g
    %s/\(\a\{1}\)\/\(\\ell\)/\1_{\/\2}/g
    %s/\(\a\+\)_\(\w\+\)/\1_{\2}/g
    %s/\\red/\\mathrm{red}/g
    %s/\\def/\\mathrm{def}/g
    %s/\\obs/\\mathrm{obs}/g
    %s/\\directlimit/\\directlim/g
    call winrestview(l:save)
    echo "Converted math"
endfunction

" For debugging syntax highlighting
function! SyntaxItem()
  return synIDattr(synID(line("."),col("."),1),"name")
endfunction

" Manual syntax reload for troubleshooting
function! ReloadPandocSyntax()
  call s:pandocSyntax()
  syntax sync fromstart
  echo "Pandoc syntax reloaded"
endfunction

" Command to reload syntax
command! ReloadSyntax call ReloadPandocSyntax()

" Show all custom mappings and functions from init.vim
function! ShowCustomCommands()
  let init_file = expand('~/.config/nvim/init.vim')
  let lines = readfile(init_file)
  let commands = []
  let current_section = ""

  for i in range(len(lines))
    let line = lines[i]
    let line_num = i + 1

    " Track sections from comments
    if line =~ '^" ---.*{{{$'
      let current_section = substitute(line, '^" --- \(.*\) {{{$', '\1', '')
      continue
    endif

    " Extract mappings
    if line =~ '^\s*[nvicosx]*noremap\|^\s*[nvicosx]*map\s'
      let mapping = substitute(line, '^\s*', '', '')
      let mapping = substitute(mapping, '\s*".*$', '', '') " Remove comments
      if mapping !~ '^\s*$' " Skip empty lines
        call add(commands, printf("%-12s │ %s │ Line %d", "MAPPING", mapping, line_num))
      endif
    endif

    " Extract function definitions
    if line =~ '^\s*function!\?\s\+\w'
      let func_name = substitute(line, '^\s*function!\?\s\+\([^(]*\).*', '\1', '')
      call add(commands, printf("%-12s │ %s │ Line %d", "FUNCTION", func_name, line_num))
    endif

    " Extract autocmd groups and autocmds
    if line =~ '^\s*augroup\s\+\w'
      let group_name = substitute(line, '^\s*augroup\s\+\(\w\+\).*', '\1', '')
      call add(commands, printf("%-12s │ %s │ Line %d", "AUTOCMD GRP", group_name, line_num))
    endif

    if line =~ '^\s*autocmd\s'
      let autocmd = substitute(line, '^\s*autocmd\s\+\(.\{0,50}\).*', '\1', '')
      call add(commands, printf("%-12s │ %s │ Line %d", "AUTOCMD", autocmd, line_num))
    endif

    " Extract let statements for important variables
    if line =~ '^\s*let\s\+g:'
      let var_name = substitute(line, '^\s*let\s\+\(g:[^=]*\).*', '\1', '')
      call add(commands, printf("%-12s │ %s │ Line %d", "VARIABLE", var_name, line_num))
    endif

    " Extract abbreviations
    if line =~ '^\s*iabbrev\s'
      let abbrev = substitute(line, '^\s*iabbrev\s\+\(\S\+\s\+\S\+\).*', '\1', '')
      call add(commands, printf("%-12s │ %s │ Line %d", "ABBREV", abbrev, line_num))
    endif
  endfor

  " Sort commands by type, then alphabetically
  call sort(commands)

  " Add header with counts
  let header = [
        \ "═══════════════════════════════════════════════════════════════",
        \ "                    NVIM CUSTOM COMMANDS & SHORTCUTS",
        \ "═══════════════════════════════════════════════════════════════",
        \ "Type         │ Command/Function/Mapping                 │ Location",
        \ "─────────────┼─────────────────────────────────────────┼─────────",
        \ ]

  let all_items = header + commands + [
        \ "─────────────┼─────────────────────────────────────────┼─────────",
        \ "💡 Press ENTER on any line to jump to that location in init.vim",
        \ "🔍 Type to search • ESC to close • Ctrl-C to cancel"
        \ ]

  call fzf#run(fzf#wrap({
        \ 'source': all_items,
        \ 'sink': function('GotoInitVimLine'),
        \ 'options': [
        \   '--prompt=nvim> ',
        \   '--header-lines=5',
        \   '--preview-window=hidden',
        \   '--height=80%',
        \   '--layout=reverse',
        \   '--border'
        \ ]
        \ }))
endfunction

" Jump to line in init.vim when selection is made
function! GotoInitVimLine(selection)
  " Extract line number from selection
  let line_match = matchstr(a:selection, 'Line \zs\d\+')
  if !empty(line_match)
    let init_file = expand('~/.config/nvim/init.vim')
    execute 'edit ' . init_file
    execute line_match
    normal! zz
    echo "Jumped to line " . line_match . " in init.vim"
  endif
endfunction

" }}}

" --- Autocommands {{{

" Remember last edit position
augroup last_edit
  autocmd!
  autocmd BufReadPost *
       \ if line("'\"") > 0 && line("'\"") <= line("$") |
       \   exe "normal! g`\"" |
       \ endif
augroup END

" Remember folds
augroup remember_folds
  autocmd!
  autocmd BufWinLeave *.md mkview
  autocmd BufWinEnter *.md silent! loadview
augroup END

" Force close terminal buffers on quit
autocmd QuitPre * call s:TermForceCloseAll()
function! s:TermForceCloseAll() abort
    let term_bufs = filter(range(1, bufnr('$')), 'getbufvar(v:val, "&buftype") == "terminal"')
    for t in term_bufs
            execute "bd! " t
    endfor
endfunction

" Filetype-specific settings - improved syntax and conceal handling
autocmd BufNewFile,BufRead *.md call s:pandocSyntax() | call LoadTexConcealRules()
autocmd BufNewFile,BufRead *.mdc call s:pandocSyntax() | call LoadTexConcealRules() | set filetype=markdown
autocmd BufNewFile,BufRead *.markdown call s:pandocSyntax() | call LoadTexConcealRules()
autocmd BufNewFile,BufRead *.sage set filetype=python
autocmd BufNewFile,BufRead *.g set filetype=gap | setlocal commentstring=#\\ %s | setlocal comments=:#
autocmd BufNewFile,BufRead *.tikz set syntax=tex

" Syntax reload on file type changes
autocmd FileType markdown,pandoc,markdown.pandoc call s:pandocSyntax() | call LoadTexConcealRules()

" Add conceals to Voom pane
au FileType voomtree syntax match someCustomes /\$\\work\$/ conceal cchar=🚩
au FileType voomtree syntax match someCustomes /\$\\done\$/ conceal cchar=✨

" When opening a markdown file, open the VOoM outliner
autocmd VimEnter *.md Voom pandoc

" }}}

" --- Abbreviations {{{
iabbrev impies implies
iabbrev keq leq
iabbrev suchtat suchthat
iabbrev pver over
iabbrev Rouche Rouché
iabbrev rouche rouché
iabbrev defineas definedas
iabbrev subet subset
iabbrev Etale Étale
iabbrev etale étale
iabbrev kapp kappa
iabbrev apha alpha
iabbrev variabel variable
iabbrev interset intersect
iabbrev lmabda lambda
iabbrev Wely Weyl
iabbrev rhi phi
iabbrev lamda lambda
iabbrev tp to
iabbrev Cech Čech
iabbrev corss cross
iabbrev Neron Néron
iabbrev abelain abelian
iabbrev noetherian Noetherian
iabbrev artinian Artinian
iabbrev poincare Poincaré
iabbrev Poincare Poincaré
iabbrev kahler kähler
iabbrev Kahler Kähler
iabbrev char ch
iabbrev detla delta
iabbrev Detla Delta
" }}}

" Enhanced CoC keybindings for academic writing
inoremap <silent><expr> <Tab>
      \ pumvisible() ? coc#_select_confirm() :
      \ coc#expandableOrJumpable() ? "\<C-r>=coc#rpc#request('doKeymap', ['snippets-expand-jump',''])\<CR>" :
      \ "\<Tab>"

" Better completion behavior for writing
inoremap <expr> <CR> pumvisible() ? coc#_select_confirm() : "\<CR>"
inoremap <silent><expr> <C-space> coc#refresh()

" Snippet expansion
imap <C-l> <Plug>(coc-snippets-expand)
let g:coc_snippet_next = '<Tab>'
let g:coc_snippet_prev = '<S-Tab>'

" Academic writing specific mappings
nnoremap <leader>pl :call UpdateProjectLabelsSync()<CR>
nnoremap <leader>zt :call TestZoteroConnection()<CR>

" Reference insertion keybindings
" Primary: Two-stage selection (internal vs external)
inoremap <C-r><C-r> <Esc>:call SelectReferenceType()<CR>
nnoremap <leader>ref :call SelectReferenceType()<CR>

" Quick access shortcuts
" Quick internal reference
inoremap <C-r><C-i> <Esc>:call InsertInternalReference()<CR>
nnoremap <leader>ri :call InsertInternalReference()<CR>

" Quick external citation
inoremap <C-r><C-e> <Esc>:call InsertExternalCitation()<CR>
nnoremap <leader>re :call InsertExternalCitation()<CR>

" Super quick Zotero (no interface, direct insertion)
inoremap <C-r><C-z> <C-r>=ZoteroCite()<CR>
nnoremap <leader>rz :call QuickZoteroCite()<CR>
" Ensure tex conceal rules are properly loaded
function! LoadTexConcealRules()
  if has('conceal')
    " Force load tex conceal rules
    runtime! after/syntax/tex.vim
    " Enable concealing for math symbols
    setlocal conceallevel=2
    setlocal concealcursor=    " FIXED: conceals disappear when cursor is on line
  endif
endfunction

" Legacy conceal commands removed - replaced with enhanced versions above

" Conceal debugging and management functions
command! FixConceal call FixConcealRules()
command! DebugConceal call DebugConcealUnderCursor()
command! ValidateConceal call ValidateConcealRules()

function! FixConcealRules()
  " Re-source syntax files to fix any conceal issues
  syntax clear
  if &filetype == 'tex' || &filetype == 'markdown' || &filetype == 'pandoc'
    runtime! syntax/tex.vim
    runtime! after/syntax/tex.vim
    setlocal concealcursor=
    setlocal conceallevel=2
    echo "Conceal rules reloaded and settings fixed"
  else
    echo "Not a tex/markdown file"
  endif
endfunction

function! DebugConcealUnderCursor()
  " Debug what's happening with conceals at cursor position
  let line_num = line('.')
  let col_num = col('.')
  let line_text = getline('.')

  echo "=== Conceal Debug ==="
  echo "Position: " . line_num . ":" . col_num
  echo "Line: " . line_text
  echo "Conceal level: " . &conceallevel
  echo "Conceal cursor: '" . &concealcursor . "'"
  echo "Syntax item: " . synIDattr(synID(line_num, col_num, 1), "name")

  " Check if this position is concealed
  let conceal_info = synconcealed(line_num, col_num)
  if conceal_info[0]
    echo "CONCEALED: '" . conceal_info[1] . "'"
  else
    echo "NOT CONCEALED"
  endif
endfunction

function! ValidateConcealRules()
  " Check for common conceal rule conflicts
  echo "=== Conceal Validation ==="

  " Check for empty cchar rules that might cause issues
  redir => syntax_output
  silent syntax list
  redir END

  let empty_conceal_count = 0
  for line in split(syntax_output, '\n')
    if match(line, 'conceal cchar=$') >= 0
      let empty_conceal_count += 1
      echo "WARNING: Empty conceal rule found: " . line
    endif
  endfor

  echo "Empty conceal rules found: " . empty_conceal_count
  echo "Current settings: conceallevel=" . &conceallevel . " concealcursor='" . &concealcursor . "'"

  if &concealcursor != ''
    echo "RECOMMENDATION: Set concealcursor= for better editing (currently: '" . &concealcursor . "')"
  endif
endfunction

" Test conceal fixes with sample math
command! TestConcealFixes call TestConcealFixes()
function! TestConcealFixes()
  echo "=== Testing Conceal Fixes ==="
  echo "1. Creating test buffer with math..."

  " Create a new buffer with test content
  tabnew
  setlocal filetype=markdown
  call setline(1, [
    \ '# Test Math Conceals',
    \ '',
    \ 'Test line: Given isotropic $H \subseteq A_L$, define $M_H = \{v \in L^* : v + L \in H\}$',
    \ '',
    \ 'More math: $\alpha + \beta = \gamma$ and $\ZZ \subseteq \RR$',
    \ '',
    \ 'Display math:',
    \ '$$\int_0^1 f(x) \, dx = \langle f, g \rangle$$'
    \ ])

  " Apply our conceal settings
  setlocal conceallevel=2
  setlocal concealcursor=

  " Load conceal rules
  call LoadTexConcealRules()

  echo "2. Test buffer created!"
  echo "3. Settings applied: conceallevel=" . &conceallevel . " concealcursor='" . &concealcursor . "'"
  echo ""
  echo "🧪 TEST INSTRUCTIONS:"
  echo "   • Move cursor to line 3 (the math line)"
  echo "   • Conceals should DISAPPEAR when cursor is on that line"
  echo "   • Move cursor away - conceals should reappear"
  echo "   • Try word navigation (w) - cursor should stay on correct characters"
  echo "   • Press i to enter insert mode - conceals should stay visible"
  echo "   • Press <leader>cc to toggle concealing completely"
  echo ""
  echo "📍 Place cursor on line 3 and test!"
endfunction

