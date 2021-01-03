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

" {{{ Boilerplate
set nocompatible
filetype plugin on
set termguicolors     " enable true colors support
" }}}

" {{{ Plugins
call plug#begin('~/.vim/plugged')
Plug 'vim-pandoc/vim-pandoc-syntax'
Plug 'MarcWeber/vim-addon-mw-utils'
Plug 'tomtom/tlib_vim'

Plug 'vim-voom/VOoM'
let g:voom_tab_key = "<c-q>"
let g:voom_return_key = '<c-q>'

" Automatically expand to math tex QUICKLY
Plug 'brennier/quicktex'

Plug 'lervag/vimtex'

"""""""" Ultisnips 
"Plug 'sirver/ultisnips'
"let g:UltiSnipsExpandTrigger = '<nop>'
"let g:UltiSnipsJumpForwardTrigger = '<c-p>'
"let g:UltiSnipsJumpBackwardTrigger = '<c-s-L>'
"let g:UltiSnipsRemoveSelectModeMappings = 0
"let g:UltiSnipsSnippetDirectories=["/home/zack/dotfiles/snippets"]
"let g:UltiSnipsEditSplit="horizontal"
""""""""""" Autocomplete
Plug 'neoclide/coc.nvim', {'branch': 'release'}
let g:coc_config_home = "~/dotfiles"
let g:coc_global_extensions = [
      \ 'coc-vimtex',
      \ 'coc-snippets',
      \ 'coc-dictionary',
      \ 'coc-word',
      \ 'coc-emoji',
      \ 'coc-spell-checker',
      \]

" use <tab> for trigger completion and navigate to the next complete item
"function! s:check_back_space() abort
  "let col = col('.') - 1
  "return !col || getline('.')[col - 1]  =~ '\s'
"endfunction

"inoremap <silent><expr> <Tab>
      "\ pumvisible() ? "\<CR>" :
      "\ <SID>check_back_space() ? "\<Tab>" :
      "\ coc#refresh()
"""""""""""""""""""""""""""""""""""""""""""""""""""

"""""coc-snippets test
" Use <C-l> for trigger snippet expand.
imap <C-l> <Plug>(coc-snippets-expand)

" Use <C-j> for jump to next placeholder, it's default of coc.nvim
let g:coc_snippet_next = '<c-e>'

" Use <C-k> for jump to previous placeholder, it's default of coc.nvim
let g:coc_snippet_prev = '<c-q>'

" Use <C-j> for both expand and jump (make expand higher priority.)
imap <C-j> <Plug>(coc-snippets-expand-jump)

inoremap <silent><expr> <TAB>
      \ pumvisible() ? coc#_select_confirm() :
      \ coc#expandableOrJumpable() ? "\<C-r>=coc#rpc#request('doKeymap', ['snippets-expand-jump',''])\<CR>" :
      \ <SID>check_back_space() ? "\<TAB>" :
      \ coc#refresh()

function! s:check_back_space() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction

let g:coc_snippet_next = '<tab>'
let g:coc_snippet_prev = '<s-tab>'

set dictionary+=~/Notes/corpus.add
set dictionary+=~/Notes/mathdict.utf-8.add.spl
"set complete+=kspell
set spelllang=en
set spellfile=/home/zack/Notes/mathdict.utf-8.add
""""""""

" Commands
" Nerdcommenter: toggle multiple lines as comments
Plug 'scrooloose/nerdcommenter'
"Plug 'Townk/vim-autoclose'
Plug 'ferrine/md-img-paste.vim'
let g:mdip_imgdir = 'figures'
Plug 'godlygeek/tabular'
Plug 'dhruvasagar/vim-table-mode'

" Layout and Functionality
Plug 'scrooloose/nerdtree'
" Hides "Press ? for help"
let NERDTreeMinimalUI = 1
let NERDTreeDirArrows = 1
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'

" Aesthetics
Plug 'flazz/vim-colorschemes'
Plug 'croaker/mustang-vim'
Plug 'tiagofumo/vim-nerdtree-syntax-highlight'
Plug 'ryanoasis/vim-devicons'
Plug 'romainl/flattened'
Plug 'rakr/vim-one'
" Searching
Plug 'mileszs/ack.vim'

" Close delimiters
"Plug 'Raimondi/delimitMate'
"let delimitMate_matchpairs = "{:}"
"let delimitMate_quotes = "\" `"

" Style
Plug 'amperser/proselint', {'rtp': 'plugins/vim/syntastic_proselint/'}
Plug 'scrooloose/syntastic'
let g:syntastic_markdown_checkers = ['proselint']
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*
let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 0
let g:syntastic_check_on_wq = 0
let g:syntastic_mode_map = { 'mode': 'passive', 'active_filetypes': [],'passive_filetypes': [] }

"Plug 'prabirshrestha/async.vim'
"Plug 'christianrondeau/vim-base64'

call plug#end()
" }}}

" {{{ Keyboard Shortcuts
let mapleader=","
command! W w
command! Wq wq
command! Q q 
command! Qa qa 
command! Wqa wqa
nnoremap <CR> :noh<CR><CR>
noremap <silent> <Leader>n :NERDTreeToggle<CR>
nnoremap <Leader>c :let &cole=(&cole == 2) ? 0 : 2 <bar> echo 'conceallevel ' . &cole <CR>
nnoremap <silent> [[ ?^\#<CR>
nnoremap <silent> ]] /^\#<CR>
nmap <silent> <leader>p :call mdip#MarkdownClipboardImage()<CR>

" Use arrow keys in wldmenu.
cnoremap <expr> <up> wildmenumode() ? "\<left>" : "\<up>"
cnoremap <expr> <down> wildmenumode() ? "\<right>" : "\<down>"
cnoremap <expr> <left> wildmenumode() ? "\<up>" : "\<left>"
cnoremap <expr> <right> wildmenumode() ? " \<bs>\<C-Z>" : "\<right>"

" {{{ Folds
" Jump to previous/next fold
nnoremap <silent> <leader>zj :call NextClosedFold('j')<cr>
nnoremap <silent> <leader>zk :call NextClosedFold('k')<cr>

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
" }}}

" {{{ Terminal buffers
" Escape terminal
tnoremap <Esc> <C-\><C-n>
tnoremap <M-[> <Esc>
tnoremap <C-v><Esc> <Esc>
" }}} 

" Disable Ex mode
map q: <Nop>
nnoremap Q <nop>


" Insert new lines in normal mode
nnoremap <Leader>o o<Esc>
nnoremap <Leader>O O<Esc>

" Write/quit in normal mode
nnoremap <Leader>w :wq<CR>

" Jump around in normal mode
"inoremap <c-]> <End><Esc>A
"nnoremap <c-]> <End><Esc>A
"inoremap <c-e> <Esc>f$a
"nnoremap <c-e> f$a
"inoremap <c-r> <Esc>f}a
"nnoremap <c-r> f}a
"inoremap <c-d> <Esc>2ji
"nnoremap <c-d> 2ji

" Ctrl-Space in any mode to save
nnoremap <c-space> :w<CR>o
inoremap <c-space> <Esc>:w<CR>o

" Save every time a new line is put in
"inoremap <CR> <CR><Esc>:wa<CR>i
"nnoremap <c-q> :wqa<CR>
"inoremap <c-q> <Esc>:wqa<CR>
nnoremap ZZ :wqa<CR>


" }}}

" {{{ Pandoc

" {{{ Default window settings when opening a new file.
function s:markdownSetup()
  " Open panes
  let s:current_win = winnr()
  " Open Nerdtree and hide it
  NERDTree | wincmd p | NERDTreeFind | wincmd p | NERDTreeToggle
  " Open Voom and split Nerdtree above it
  Voom pandoc
  sbuffer NERD_tree_1 |
  execute bufwinnr(s:current_win) . 'wincmd w'
  " Close Nerdtree if last buffer open
  autocmd BufWinEnter,WinEnter term://* if winnr("$") <= 3  | qa | endif
  autocmd BufWinEnter,WinEnter NERD_tree* if winnr("$") <= 3  | qa | endif
  "autocmd BufWinEnter,WinEnter *.md if winnr("$") <= 3  | qa | endif
  
  " Remap write/quit to close all terminals, nerdtree, voom, etc
  cnoreabbrev q q
  cnoreabbrev w wa
  cnoreabbrev wq wq
  call s:pandocSyntax()
endfunction
" }}}

" {{{ Pandoc PDF and HTML preview
function! StartPreview()
  belowright split 
  resize 5 
  term vimpreview.sh -f "%:p" -v
  execute "normal! G"
  wincmd p
endfunction
nnoremap <silent> <Leader>lp :call StartPreview()<CR>

function! StartPreview2()
  belowright split 
  resize 5 
  term vimpreview.sh -f "%:p" 
  execute "normal! G"
  wincmd p
endfunction
nnoremap <silent> <Leader>lpp :call StartPreview2()<CR>

function! StartPreview3()
  belowright split 
  resize 5 
  term pdfpreview.sh -f "%:p" -v
  execute "normal! G"
  wincmd p
endfunction
nnoremap <silent> <Leader>lo :call StartPreview3()<CR>

autocmd VimLeave *.md  silent! !pkill qutebrowser; pkill zathura; 

function! s:win_by_bufname(bufname)
	let bufmap = map(range(1, winnr('$')), '[bufname(winbufnr(v:val)), v:val]')
	let thewindow = filter(bufmap, 'v:val[0] =~ a:bufname')[0][1]
	execute thewindow 'wincmd w'
endfunction

function! s:fixResizing()
  call s:win_by_bufname('term')
  resize 5 
  wincmd p
endfunction

autocmd VimResized * call s:fixResizing()

" }}}

" {{{ Automatically start preview?
"autocmd VimEnter */section* call StartPreview()
"autocmd CursorHold,CursorHoldI *.md update
"set updatetime=300
" }}}

" {{{ Custom Pandoc Syntax and Conceals
function s:pandocSyntax()
  set filetype=markdown.pandoc 
  setlocal spell
  " Extra Syntax
  syntax match DZGConceal /:::/ conceal cchar=―
  syntax match DZGConceal /\\hfill/ conceal cchar=―

  " Theorem Environments
  syn region DZGEnvironments start="{." end="}" transparent contains=DZGMathResults,DZGMathThms,DZGMathNames

  syn keyword DZGMathResults contained proposition corollary example problem solution question remark warnings exercise slogan
  hi def link DZGMathResults Statement 

  syn keyword DZGMathThms contained theorem definition proof
  hi def link DZGMathThms Special

  syntax match DZGMathNames /title=/ contained conceal cchar= 
  "source /home/zack/dotfiles/vim/tex_conceal.vim
endfunction
au VimEnter *.md call s:markdownSetup()
au BufNewFile,BufFilePre,BufRead *.md call s:pandocSyntax()

" Add conceals to Voom pane
au FileType voomtree syntax match someCustomes /\$\\work\$/ conceal cchar=🚩
au FileType voomtree syntax match someCustomes /\$\\done\$/ conceal cchar=✨
" }}}
" }}}

" {{{ Aesthetics
colorscheme afterglow
"colorscheme flattened_light

" Use spaces instead of tabs (necessary for haskell/ghc)
set tabstop=2     " Inserts 2 spaces when tab key is pressed.
set softtabstop=2 " Deletes 2 spaces (simulates deleting a tab)
set shiftwidth=2  " Inserts 2 spaces for auto-indentation.
set expandtab     " Insert spaces whenever tab key is pressed.
set shiftround    " Round indent to nearest 'shiftwidth' multiple
syntax on
" Numbered lines
set number
" Actual line number on current line, otherwise relative line numbers above
" and below
set relativenumber
" Concleas
set conceallevel=1

" ? I forget
"set title
"set titlestring=%{hostname()}\ \ %F\ \ %{strftime('%Y-%m-%d\ %H:%M',getftime(expand('%')))}

" Highlight current line.
set cursorline
autocmd BufEnter * setlocal cursorline
autocmd BufEnter * :hi CursorLine   cterm=NONE ctermbg=239 ctermfg=NONE
hi NonText ctermbg=none
hi Normal guibg=NONE ctermbg=NONE
hi clear Conceal


" Always center cursorline
set scrolloff=999

" {{{ Folding
let g:markdown_folding = 1
set foldcolumn=3
set foldlevel=2

augroup remember_folds
  autocmd!
  autocmd BufWinLeave *.md mkview
  autocmd BufWinEnter *.md silent! loadview
augroup END
" }}}


" }}}

" {{{ Low-Level Vim Functionality
set nobackup                      " Turn backup off (store everything in version control)
set nowb
set noswapfile
set mouse=a                     " Allow mouse selection
set encoding=utf-8
let &termencoding=&encoding


" {{{ Persistent Undo
let s:undoDir = "/tmp/.undodir_" . $USER
if !isdirectory(s:undoDir)
    call mkdir(s:undoDir, "", 0700)
endif
let &undodir=s:undoDir
set undofile
" }}}

" {{{ Return to last edit position when opening files
augroup last_edit
  autocmd!
  autocmd BufReadPost *
       \ if line("'\"") > 0 && line("'\"") <= line("$") |
       \   exe "normal! g`\"" |
       \ endif
augroup END
" }}}

" {{{ Run command line jobs (!somescript) async?
command! -nargs=1 -complete=file
         \ StartAsync call jobstart(expand(<f-args>), {
         \    'on_exit': { j,d,e ->
         \       execute('echom "['.<f-args>.'] command finished with exit status '.d.'"', '')
         \    }
         \ })
" }}}


" }}}

" {{{ Prose Functionality

" {{{ Spellcheck
" No spellchecking fullstops without capitalization
set spellcapcheck=
set ignorecase
set smartcase
" }}}

" }}}

" {{{ Abbreviations
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
iabbrev nbhd neighborhood
iabbrev tp to
iabbrev Cech Čech
iabbrev corss cross
iabbrev Neron Néron
iabbrev abelain abelian
iabbrev noetherian Noetherian
iabbrev artinian Artinian
" }}}

" Quit is only Nerdtree + one other pane is open?
autocmd bufenter * if (winnr("$") == 2 && exists("b:NER3Tree") && b:NERDTree.isTabTree()) | qa | endif

" {{{ Quicktex (Prose)
let g:quicktex_tex = {
    \' '   : "\<ESC>:call search('<+.*+>')\<CR>\"_c/+>/e\<CR>",
    \'m'   : '\( <+++> \) <++>',
    \'M'   : "\\[\<CR><+++>\<CR>.\\]\<CR><++>",
    \'thm' : ":::{.theorem title=\"?\"}\<CR><+++>\<CR>:::",
    \'*'   : '*<+++>*<++>',
    \'**'   : '**<+++>**<++>',
\'Section       : Text Shortcuts'             : 'COMMENT',
    \'st'     : 'such that ',
    \'homo'   : 'homomorphism ',
    \'iso'    : 'isomorphism ',
    \'iff'    : 'if and only if ',
    \'wlog'   : 'without loss of generality ',
    \'Wlog'   : 'Without loss of generality, ',
    \'gset'   : '\(G\dash\)set ',
    \'rmod'   : '\(R\dash\)module ',
    \'ae'     : 'almost everywhere ',
    \'bd'     : 'boundary ',
    \'card'   : 'cardinality ',
    \'char'   : 'characteristic ',
    \'ker'    : 'kernel ',
    \'im'     : 'image ',
    \'def'    : 'define ',
    \'deg'    : 'degree ',
    \'det'    : 'determinant ',
    \'dim'    : 'dimension ',
    \'tf'     : 'the following: ',
    \'gal'    : 'Galois ',
    \'gcd'    : 'greatest common divisor ',
    \'int'    : 'interior ',
    \'ext'    : 'exterior ',
    \'lcm'    : 'least common multiple ',
    \'lim'    : 'limit ',
    \'resp'   : 'respectively ',  
    \'rhs'    : 'right-hand side ',
    \'lhs'    : 'left-hand side ',
    \'wts'    : 'want to show ',
    \'nts'    : 'need to show ',
    \'wrt'    : 'with respect to',
    \'tfae'   : 'the following are equivalent ',
    \'fd'     : 'finite-dimensional ',
    \'fg'     : 'finitely-generated',
    \'eg'     : 'e.g.',
    \'Eg'     : 'E.g.',
    \'ie'     : 'i.e.',
    \'Ie'     : 'I.e.',
    \'rep'    : 'representation ',
    \'comm'   : 'commutative ',
    \'inter'  : 'intersection ',
    \'ab'     : 'abelian ',
    \'cat'    : 'category ',
    \'mod'    : "\<BS>-module ",
    \'aka'    : 'a.k.a.'
\}

" }}}

" {{{ Quicktex (Math mode)
let g:quicktex_math = {
    \' '        : "\<ESC>:call search('<+.*+>')\<CR>\"_c/+>/e\<CR>",
\'Section       : Unsorted'             : 'COMMENT',
    \'in'       : '\in ',
    \'inv'      : '^{-1} ',
    \'sq'       : '^{2} ',
    \'sqrt'     : '\sqrt{<+++>} <++>',
    \'empty'    : '\emptyset',
    \'ex'       : '\exists ',
    \'eq'       : '= ',
    \'eqh'      : '\homotopic ',
    \'all'      : '\forall ',
    \'frac'     : '\frac{<+++>}{<++>} <++>',
    \'recip'    : '\frac{1}{<++>} <++>',
    \'kbar'     : '\bar{k} ',
    \'ksep'     : 'k^{s} ',
    \'limn'     : '\lim_{n\to\infty}',
    \'st'       : '\st ',
    \'le'       : '\leq ',
    \'ge'       : '\geq ',
    \'subs'     : '\subset ',
    \'subse'    : '\subseteq ',
    \'sups'     : '\supset ',
    \'supse'    : '\supseteq ',
    \'iso'      : '\cong ',
    \'ts'       : '\ts{ <+++> } <++>',
    \'text'     : '\text{ <+++> } <++>',
    \'iff'      : '\iff ',
    \'star' : "\<BS>^* ",
    \'suchthat' : '\text{ such that } ',
    \'lim'    : '\lim_{<+++>} <++>',
    \'converges'    : '\converges_{n\to\infty} ',
\'Section       : Short Symbols'             : 'COMMENT',
    \'>'        : '\mapsvia{<+++>} <++>',
    \'^'        : '^{<+++>} <++>',
    \'_'        : '_{<+++>} <++>',
    \'@'        : '\circ ',
    \'@@'       : '\infty ',
\'Section       : Greek Letters'             : 'COMMENT',
    \'a'        : '\alpha ',
    \'b'        : '\beta ',
    \'c'        : '\chi ',
    \'d'        : '\delta ',
    \'D'        : '\Delta ',
    \'e'        : '\epsilon ',
    \'f'        : '\varphi ',
    \'F'        : '\Phi ',
    \'g'        : '\gamma ',
    \'G'        : '\Gamma ',
    \'k'        : '\kappa ',
    \'i'        : '\iota ',
    \'l'        : '\lambda ',
    \'m'        : '\mu ',
    \'nu'       : '\nu ',
    \'na'       : '\nabla ',
    \'p'        : '\pi ',
    \'P'        : '\Pi ',
    \'ps'       : '\psi ',
    \'PS'       : '\Psi ',
    \'th'       : '\theta ',
    \'TH'       : '\Theta ',
    \'r'        : '\rho ',
    \'R'        : '\RR ',
    \'s'        : '\sigma ',
    \'S'        : '\Sigma ',
    \'tau'      : '\tau ',
    \'upsilon'  : '\upsilon ',
    \'Upsilon'  : '\Upsilon ',
    \'om'       : '\omega ',
    \'OM'       : '\Omega ',
    \'xi'       : '\xi ',
    \'XI'       : '\Xi ',
    \'x'        : '\cross ',
    \'zeta'     : '\zeta ',
    \'Zeta'     : '\Zeta ',
\'Section       : Mathcal'             : 'COMMENT',
    \'mca'      : '\mathcal{A} ',
    \'mcb'      : '\mathcal{B} ',
    \'mcc'      : '\mathcal{C} ',
    \'mcd'      : '\mathcal{D} ',
    \'mce'      : '\mathcal{E} ',
    \'mcf'      : '\mathcal{F} ',
    \'mcg'      : '\mathcal{G} ',
    \'mch'      : '\mathcal{H} ',
    \'mci'      : '\mathcal{I} ',
    \'mcj'      : '\mathcal{J} ',
    \'mck'      : '\mathcal{K} ',
    \'mcl'      : '\mathcal{L} ',
    \'mcm'      : '\mathcal{M} ',
    \'mcn'      : '\mathcal{N} ',
    \'mco'      : '\mathcal{O} ',
    \'mcp'      : '\mathcal{P} ',
    \'mcq'      : '\mathcal{Q} ',
    \'mcr'      : '\mathcal{R} ',
    \'mcs'      : '\mathcal{S} ',
    \'mct'      : '\mathcal{T} ',
    \'mcu'      : '\mathcal{U} ',
    \'mcv'      : '\mathcal{V} ',
    \'mcw'      : '\mathcal{W} ',
    \'mcx'      : '\mathcal{X} ',
    \'mcy'      : '\mathcal{Y} ',
    \'mcz'      : '\mathcal{Z} ',
\'Section       : Mathfrak'             : 'COMMENT',
    \'mfa'      : '\mathfrak{A} ',
    \'mfb'      : '\mathfrak{B} ',
    \'mfc'      : '\mathfrak{C} ',
    \'mfd'      : '\mathfrak{D} ',
    \'mfe'      : '\mathfrak{E} ',
    \'mff'      : '\mathfrak{F} ',
    \'mfg'      : '\mathfrak{G} ',
    \'mfh'      : '\mathfrak{H} ',
    \'mfi'      : '\mathfrak{I} ',
    \'mfj'      : '\mathfrak{J} ',
    \'mfk'      : '\mathfrak{K} ',
    \'mfl'      : '\mathfrak{L} ',
    \'mfm'      : '\mathfrak{M} ',
    \'mfn'      : '\mathfrak{N} ',
    \'mfo'      : '\mathfrak{O} ',
    \'mfp'      : '\mathfrak{P} ',
    \'mfq'      : '\mathfrak{Q} ',
    \'mfr'      : '\mathfrak{R} ',
    \'mfs'      : '\mathfrak{S} ',
    \'mft'      : '\mathfrak{T} ',
    \'mfu'      : '\mathfrak{U} ',
    \'mfv'      : '\mathfrak{V} ',
    \'mfw'      : '\mathfrak{W} ',
    \'mfx'      : '\mathfrak{X} ',
    \'mfy'      : '\mathfrak{Y} ',
    \'mfz'      : '\mathfrak{Z} ',
\'Section       : MathBB'             : 'COMMENT',
    \'mba'      : '\mathbb{A} ',
    \'mbb'      : '\mathbb{B} ',
    \'mbc'      : '\mathbb{C} ',
    \'mbd'      : '\mathbb{D} ',
    \'mbe'      : '\mathbb{E} ',
    \'mbf'      : '\mathbb{F} ',
    \'mbg'      : '\mathbb{G} ',
    \'mbh'      : '\mathbb{H} ',
    \'mbi'      : '\mathbb{I} ',
    \'mbj'      : '\mathbb{J} ',
    \'mbk'      : '\mathbb{K} ',
    \'mbl'      : '\mathbb{L} ',
    \'mbm'      : '\mathbb{M} ',
    \'mbn'      : '\mathbb{N} ',
    \'mbo'      : '\mathbb{O} ',
    \'mbp'      : '\mathbb{P} ',
    \'mbq'      : '\mathbb{Q} ',
    \'mbr'      : '\mathbb{R} ',
    \'mbs'      : '\mathbb{S} ',
    \'mbt'      : '\mathbb{T} ',
    \'mbu'      : '\mathbb{U} ',
    \'mbv'      : '\mathbb{V} ',
    \'mbw'      : '\mathbb{W} ',
    \'mbx'      : '\mathbb{X} ',
    \'mby'      : '\mathbb{Y} ',
    \'mbz'      : '\mathbb{Z} '
\}
" }}}

" {{{ Custom Functions
function ConvertOldMath()
    " Save cursor position
    let l:save = winsaveview()
    " Remove trailing whitespace
    %s/\\begin{align\*}/\\[/g
    %s/\\end{align\*}/\\]/g
    %s/\\begin{center}//g
    %s/\\end{center}//g
    %s/X\/k/X_{\/k}/g 
    %s/\/K/_{\/K}/g 
    %s/\/k/_{\/k}/g 
    " Move cursor to original position
    call winrestview(l:save)
    echo "Converted math"
endfunction


" Replace inline math $......$ with displaymath \[ ...... \]
nnoremap <silent> <Leader>gs F$lvt$"+dxF$xwi<cr><cr><Esc>ki\[<cr><esc>"+po.\]

"nnoremap <silent> <Leader>gt /$$<cr>Nhxxvtnhh"+dxxi\[<cr>.\]<esc>k"+p
"nnoremap <silent> <Leader>gl /\$\$<cr>Nxxvnh"+dxxi\[<cr>.\]<cr><esc>kk"+p
nnoremap <silent> <Leader>gl /\$\$<cr>NxxwvnB"+dknxxi\[<cr>.\]<cr><esc>kk:pu +<cr>

function CreateInkscape()
  let s:fig_dir = getcwd() . "/figures"
  silent exec '!mkdir -p "' . s:fig_dir . '"'
  let s:outfile= system('inkscape-figures.sh -d"' . s:fig_dir. '"')
  if v:shell_error == 1
    echo "Error: \n" . s:outfile
  else
    exe "normal! a" . s:outfile . "\<Esc>"
  endif
endfunction

nmap <silent> <leader>i :call CreateInkscape()<CR>

" }}}

" {{{ Notes 
"autocmd BufWritePost *note-*.md silent !buildNote.sh %:p
" }}}
