set nocompatible
filetype plugin on
set termguicolors     " enable true colors support

call plug#begin('~/.vim/plugged')
Plug 'vim-pandoc/vim-pandoc-syntax'
"
Plug 'MarcWeber/vim-addon-mw-utils'
Plug 'tomtom/tlib_vim'

Plug 'vim-voom/VOoM'
let g:voom_tab_key = "<c-a>"
let g:voom_return_key = '<c-a>'

"""""""" Ultisnips 
Plug 'sirver/ultisnips'
let g:UltiSnipsExpandTrigger = '<nop>'
let g:UltiSnipsJumpForwardTrigger = '<c-j>'
let g:UltiSnipsJumpBackwardTrigger = '<c-k>'
let g:UltiSnipsRemoveSelectModeMappings = 0
let g:UltiSnipsSnippetDirectories=["/home/zack/dotfiles/snippets"]
let g:UltiSnipsEditSplit="horizontal"
"""""""" Ultisnips + MuComplete Completion 


""""""""""" Autocomplete
Plug 'neoclide/coc.nvim', {'branch': 'release'}
let g:coc_config_home = "~/dotfiles"
let g:coc_global_extensions = [
      \ 'coc-vimtex',
      \ 'coc-snippets',
      \ 'coc-vimlsp',
      \ 'coc-dictionary',
      \ 'coc-word',
      \ 'coc-emoji',
      \ 'coc-spell-checker',
      \]

" Make tab select and jump through placeholders.
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
""""""""

""Snippets
"set noinfercase
set dictionary+=~/Notes/corpus.add
set dictionary+=~/Notes/mathdict.utf-8.add.spl
"set complete+=kspell
set spelllang=en
set spellfile=/home/zack/Notes/mathdict.utf-8.add

" Commands
" Nerdcommenter: toggle multiple lines as comments
Plug 'scrooloose/nerdcommenter'
"Plug 'Townk/vim-autoclose'
Plug 'ferrine/md-img-paste.vim'
let g:mdip_imgdir = 'figures'
Plug 'godlygeek/tabular'
Plug 'dhruvasagar/vim-table-mode'

" See contents of register with " or @ or Ctrl-R
Plug 'junegunn/vim-peekaboo'

" Layout and Functionality
Plug 'scrooloose/nerdtree'
" Hides "Press ? for help"
let NERDTreeMinimalUI = 1
let NERDTreeDirArrows = 1

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

call plug#end()

" Keyboard Shortucts
let mapleader=","
command! W w
command! Wq wq
command! Q q 
command! Qa qa 
nnoremap <CR> :noh<CR><CR>
noremap <silent> <Leader>n :NERDTreeToggle<CR>
nnoremap <Leader>c :let &cole=(&cole == 2) ? 0 : 2 <bar> echo 'conceallevel ' . &cole <CR>
nnoremap <silent> [[ ?^\#<CR>
nnoremap <silent> ]] /^\#<CR>
nmap <silent> <leader>p :call mdip#MarkdownClipboardImage()<CR>

" Pandoc-specific setup.
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
  autocmd BufWinEnter,WinEnter term://* if winnr("$") == 3  | qa | endif
 
  call s:pandocSyntax()
endfunction
function s:pandocSyntax()
  set filetype=markdown.pandoc 
  setlocal spell
  " Extra Syntax
  syntax match DZGConceal /:::/ conceal cchar=―
  syntax match DZGConceal /\\hfill/ conceal cchar=―

  " Theorem Environments
  syn region DZGEnvironments start="{." end="}" transparent contains=DZGMathResults,DZGMathThms,DZGMathNames

  syn keyword DZGMathResults contained proposition corollary example problem solution
  hi def link DZGMathResults Statement 

  syn keyword DZGMathThms contained theorem definition proof
  hi def link DZGMathThms Special

  syntax match DZGMathNames /title=/ contained conceal cchar= 
  "source /home/zack/dotfiles/vim/tex_conceal.vim
endfunction
au VimEnter *.md call s:markdownSetup()
au BufNewFile,BufFilePre,BufRead *.md call s:pandocSyntax()


colorscheme afterglow
"colorscheme flattened_light

set nobackup                      " Turn backup off (store everything in version control)
set nowb
set noswapfile
set mouse=a                     " Allow mouse selection


"""------  Generic Behavior  ------
" Use spaces instead of tabs (necessary for haskell/ghc)
set tabstop=2     " Inserts 2 spaces when tab key is pressed.
set softtabstop=2 " Deletes 2 spaces (simulates deleting a tab)
set shiftwidth=2  " Inserts 2 spaces for auto-indentation.
set expandtab     " Insert spaces whenever tab key is pressed.
set shiftround    " Round indent to nearest 'shiftwidth' multiple
syntax on
set number
set encoding=utf-8
let &termencoding=&encoding
set conceallevel=1

" Persistent Undo
let s:undoDir = "/tmp/.undodir_" . $USER
if !isdirectory(s:undoDir)
    call mkdir(s:undoDir, "", 0700)
endif
let &undodir=s:undoDir
set undofile


" Return to last edit position when opening files
augroup last_edit
  autocmd!
  autocmd BufReadPost *
       \ if line("'\"") > 0 && line("'\"") <= line("$") |
       \   exe "normal! g`\"" |
       \ endif
augroup END


" No spellchecking fullstops without capitalization
set spellcapcheck=
set ignorecase
set smartcase
""""""""""""" < \Spelling and Grammar > """"""""""""""""""

command! -nargs=1 -complete=file
         \ StartAsync call jobstart(expand(<f-args>), {
         \    'on_exit': { j,d,e ->
         \       execute('echom "['.<f-args>.'] command finished with exit status '.d.'"', '')
         \    }
         \ })


"autocmd BufLeave,VimLeave *.md !pkill zathura

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

function! StartPreview2()
  belowright split 
  resize 5 
  term vimpreview.sh -f "%:p" 
  execute "normal! G"
  wincmd p
endfunction
nnoremap <silent> <Leader>lpp :call StartPreview2()<CR>


function! s:CleanPreview()
  !notify-send "Vim" "Exiting.." --urgency=critical --expire-time=2000
  silent !pkill qutebrowser
  silent !lsof $(pwd) | grep inotify | awk '{print $2}' | xargs kill -9
endfunction
autocmd BufWinLeave,VimLeave *.md call s:CleanPreview()
" Automatically start preview?
"autocmd VimEnter *.md call StartPreview()
"autocmd CursorHold,CursorHoldI *.md update
"set updatetime=5000

"set title
"set titlestring=%{hostname()}\ \ %F\ \ %{strftime('%Y-%m-%d\ %H:%M',getftime(expand('%')))}

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
iabbrev ie i.e.
iabbrev eg e.g.
iabbrev aka a.k.a.
iabbrev Neron Néron
iabbrev abelain abelian
iabbrev noetherian Noetherian
iabbrev artinian Artinian

" Escape terminal
tnoremap <Esc> <C-\><C-n>
tnoremap <M-[> <Esc>
tnoremap <C-v><Esc> <Esc>

autocmd bufenter * if (winnr("$") == 2 && exists("b:NER3Tree") && b:NERDTree.isTabTree()) | qa | endif

" Highlight current line.
set cursorline
autocmd BufEnter * setlocal cursorline
autocmd BufEnter * :hi CursorLine   cterm=NONE ctermbg=239 ctermfg=NONE
hi NonText ctermbg=none
hi Normal guibg=NONE ctermbg=NONE
hi clear Conceal

set relativenumber

au FileType voomtree syntax match someCustomes /\$\\work\$/ conceal cchar=🚩
au FileType voomtree syntax match someCustomes /\$\\done\$/ conceal cchar=✨

" Disable Ex mode
map q: <Nop>
nnoremap Q <nop>

" Always center cursorline
set scrolloff=999
let g:markdown_folding = 1
set foldcolumn=3
set foldlevel=2

augroup remember_folds
  autocmd!
  autocmd BufWinLeave *.md mkview
  autocmd BufWinEnter *.md silent! loadview
augroup END


nnoremap <silent> <Leader>gs :call ToggleLatexMathMode()<CR>

function! ToggleLatexMathMode()
    " Get the current line and check if we find an expression surrounded by $ signs
    let l=getline('.')
    let inline=match(l, '\$[^$]\+\$')

    " Inline to block
    if (inline >= 0)
        " Get the expression
        let l=matchstr(l, '\$[^$]\+\$')
        " Remove the surrounding $ signs
        let expr=substitute(l, '\$', '', 'g')
        " Remove the expression from the line
        execute 's/\%' . inline  . 'c.\{' . ( len(l)+1 ) . '}//'
        " Append the delimitors and the expression without $ signs
        call append(line('.'), '\]')
        call append(line('.'), expr)
        call append(line('.'), '\[')
        " Format to get the right indentation
        normal! =}
    endif
endfunction

nnoremap <Leader>o o<Esc>
nnoremap <Leader>O O<Esc>
inoremap <c-s> <End>
nnoremap <c-s> <End>

" Ctrl-Space mode to save
nnoremap <c-space> <Esc>:w<CR>i
inoremap <c-space> <Esc>:w<CR>i
" Save every time a new line is put in
"inoremap <CR> <CR><Esc>:wa<CR>i
"nnoremap <c-q> :wqa<CR>
"inoremap <c-q> <Esc>:wqa<CR>
nnoremap ZZ :wqa<CR>

