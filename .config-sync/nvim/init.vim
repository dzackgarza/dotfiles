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
"let g:voom_tab_key = "<c-q>"
"let g:voom_return_key = '<CR>'

" Automatically expand to math tex QUICKLY
Plug 'dzackgarza/quicktex'

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
      \ 'coc-dictionary',
      \ 'coc-word',
      \ 'coc-emoji',
      \ 'coc-spell-checker',
      \]

imap <C-l> <Plug>(coc-snippets-expand)
inoremap <silent><expr> <NUL> coc#refresh()
inoremap <silent><expr> <Tab> pumvisible() ? coc#_select_confirm() : "\<C-g>u\<Tab>"
inoremap <expr> <cr> pumvisible() ? "<C-e><CR>" : "\<C-g>u\<CR>"

"""""coc-snippets test

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
"Plug 'amperser/proselint', {'rtp': 'plugins/vim/syntastic_proselint/'}
"Plug 'scrooloose/syntastic'
"let g:syntastic_markdown_checkers = ['proselint']
"set statusline+=%#warningmsg#
"set statusline+=%{SyntasticStatuslineFlag()}
"set statusline+=%*
"let g:syntastic_always_populate_loc_list = 1
"let g:syntastic_auto_loc_list = 1
"let g:syntastic_check_on_open = 0
"let g:syntastic_check_on_wq = 0
"let g:syntastic_mode_map = { 'mode': 'passive', 'active_filetypes': [],'passive_filetypes': [] }


call plug#end()
" }}}

" {{{ Keyboard Shortcuts

" {{{ Remaps
let mapleader=","
"command! W w
"command! Wq wq
"command! Q q 
"command! Qa qa 
"command! Wqa wqa
nnoremap <CR> :noh<CR><CR>
noremap <silent> <Leader>n :NERDTreeToggle<CR>
nnoremap <Leader>c :let &cole=(&cole == 2) ? 0 : 2 <bar> echo 'conceallevel ' . &cole <CR>
"nnoremap <silent> [[ ?^\#<CR>
nnoremap <silent> [[ ?^\:\:\:{<CR>
"nnoremap <silent> ]] /^\#<CR>
nnoremap <silent> ]] /^\:\:\:{<CR>
nmap <silent> <leader>p :call mdip#MarkdownClipboardImage()<CR>

" Use arrow keys in wldmenu.
cnoremap <expr> <up> wildmenumode() ? "\<left>" : "\<up>"
cnoremap <expr> <down> wildmenumode() ? "\<right>" : "\<down>"
cnoremap <expr> <left> wildmenumode() ? "\<up>" : "\<left>"
cnoremap <expr> <right> wildmenumode() ? " \<bs>\<C-Z>" : "\<right>"

" Disable Ex mode
map q: <Nop>
nnoremap Q <nop>

" Ctrl-Space in any mode to save
nnoremap <c-space> :w<CR>o
inoremap <c-space> <Esc>:w<CR>o

" Save every time a new line is put in
"inoremap <CR> <CR><Esc>:wa<CR>i
nnoremap ZZ :wqa<CR>

" }}}

" {{{ Leader Shortcuts
"
" Insert new lines in normal mode
nnoremap <Leader>o o<Esc>
nnoremap <Leader>O O<Esc>

" Write/quit in normal mode
nnoremap <Leader>w :w<CR>



nnoremap <silent> <leader>zj :call NextClosedFold('j')<cr>
nnoremap <silent> <leader>zk :call NextClosedFold('k')<cr>

nnoremap <silent> <Leader>lp :call StartPreview(1)<CR>
nnoremap <silent> <Leader>lpp :call StartPreview(2)<CR>
nnoremap <silent> <Leader>lo :call StartPreview(3)<CR>

nmap <silent> <leader>i :call CreateInkscape()<CR>

" Replace inline math $......$ with 
" \[ 
" ...... 
" .\]
nnoremap <silent> <Leader>gs F$xvt$"+dxi\[<cr><cr>.\]<Esc>k"+P
"nnoremap <silent> <Leader>gs F$lvt$"+dxF$xwi<cr><cr><Esc>ki\[<cr><esc>"+po.\]

" Replace inline math $......$ with \( ...... \)
nnoremap <silent> <Leader>gb F$xvt$"+dxi\(  \)<Esc>hh"+P

" Replace displaymath $$......$$ with displaymath \[ ...... \]
nnoremap <silent> <Leader>ga /\$\$<cr>Nxxwvnk$"+dknxxi\[<esc>"+p<esc>o.\]<esc>

" }}}

" {{{ Folds
" Jump to previous/next fold
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

" }}}

" {{{ Specific Filetype Commands
autocmd Filetype tmux setlocal foldmethod=marker
" }}}

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
  "autocmd BufWinEnter,WinEnter term://* if winnr("$") <= 3  | qa | endif
  "autocmd BufWinEnter,WinEnter NERD_tree* if winnr("$") <= 2  | qa | endif
  "autocmd BufWinEnter,WinEnter *VOOM* if winnr("$") <= 2  | qa | endif
  
  " Remap write/quit to close all terminals, nerdtree, voom, etc
  cnoreabbrev q q
  cnoreabbrev w wa
  cnoreabbrev wq wq
  call s:pandocSyntax()
  call FixResizing()
endfunction
" }}}

" {{{ Pandoc PDF and HTML preview
function! FixResizing()
  echo "Fixing resize"
  let windowNr = bufwinnr("term")
  if windowNr > 0
    execute windowNr 'wincmd w'
    resize 5 
    wincmd p
    redraw
  endif
endfunction

let g:previews_open = 0

function! StartPreview(preview_type)
  belowright split 
  resize 5 
  if a:preview_type == 1
    term vimpreview.sh -f "%:p" -v
    let g:previews_open = 1
  elseif a:preview_type == 2
    term vimpreview.sh -f "%:p" 
    let g:previews_open = 1
  elseif a:preview_type == 3
    term pdfpreview.sh -f "%:p" -v
    let g:previews_open = 2
  endif
  execute "normal! G"
  wincmd p
endfunction


autocmd VimResized * call FixResizing()

function! KillPreviews()
  if g:previews_open == 1
    silent exec "!pkill qutebrowser" 
  elseif g:previews_open == 2
    silent exec "!pkill zathura" 
  endif
endfunction

autocmd VimLeave *.md  call KillPreviews()

" }}}

" {{{ Automatically start preview?
"autocmd VimEnter */section* call StartPreview(1)
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

autocmd BufNewFile,BufRead *.tikz set syntax=tex


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
iabbrev tp to
iabbrev Cech Čech
iabbrev corss cross
iabbrev Neron Néron
iabbrev abelain abelian
iabbrev noetherian Noetherian
iabbrev artinian Artinian
iabbrev poincare Poincaré
iabbrev Poincare Poincaré
" }}}

" Quit is only Nerdtree + one other pane is open?
" autocmd bufenter * if (winnr("$") == 2 && exists("b:NER3Tree") && b:NERDTree.isTabTree()) | qa | endif

autocmd Filetype markdown.pandoc let g:enable_quicktex = 1
" See `~/.config/nvim/after/ftplugin/pandoc/quicktex_dict.vim`

" {{{ Custom Functions

" {{{ Converting Math
function ConvertOldMath()
    " Save cursor position
    let l:save = winsaveview()
    " Remove trailing whitespace
    %s/\\definedas/\\da/g
    %s/\\begin{align\*}/\\[/g
    %s/\\end{align\*}/\\]/g
    %s/\\begin{center}//g
    %s/\\end{center}//g
    "%s/X\/k/X_{\/k}/g 
    %s/\(\a\{1}\)\/\([kKS]\)/\1_{\/\2}/g
    %s/\(\a\{1}\)\/\(\\ell\)/\1_{\/\2}/g
    %s/\(\a\+\)_\(\w\+\)/\1_{\2}/g
    %s/\\red/\\mathrm{red}/g 
    %s/\\def/\\mathrm{def}/g 
    %s/\\obs/\\mathrm{obs}/g 
    %s/\\directlimit/\\directlim/g 
    " Move cursor to original position
    call winrestview(l:save)
    echo "Converted math"
endfunction



" }}}

" {{{ Inkscape and Xournal handling
function CreateInkscape()
  let s:fig_dir = getcwd() . "/figures"
  silent exec '!mkdir -p "' . s:fig_dir . '"'
  let s:outfile= system('inkscape-figures.sh -d"' . s:fig_dir. '"')
  if v:shell_error == 1
    echo "Error: \n" . s:outfile
  else
    echo s:outfile
    exe "normal! a" . s:outfile . "\<Esc>"
  endif
endfunction


" }}} 

function! SyntaxItem()
  return synIDattr(synID(line("."),col("."),1),"name")
endfunction
set statusline+=%{SyntaxItem()}

map <F6> :echo "hi<" . synIDattr(synID(line("."),col("."),1),"name") . '> trans<'
\ . synIDattr(synID(line("."),col("."),0),"name") . "> lo<"
\ . synIDattr(synIDtrans(synID(line("."),col("."),1)),"name") . ">"<CR>


" }}}

" {{{ Notes 
"autocmd BufWritePost *note-*.md silent !buildNote.sh %:p
" }}}
