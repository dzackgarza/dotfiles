Take your dotfiles everywhere!

# How to Install
```
sudo apt-get install pacapt
git clone https://github.com/dzackgarza/dotfiles
cd dotfiles
sudo ./autoinstall.sh
```

# Dependencies
* pacapt (To abstract away the underlying package manager)

# What does this script install?
* zsh
* oh-my-zsh
* Many, many vim plugins

# Todo List
* Install packages automatically
  ** ruby
  ** python virtualenv
* Include fonts
* Fix HaskellConcealPlus vim plugin
* Fix prompt
* Fix LSCOLORS
* Fix vim's transparency issues
* cowsay: Could not find healy cowfile
* Install tmux
* Install ag
* Install xclip
* Fix vim autoindent for markdown files
* Fix antigen install issues, or install vim-apt
* Install dependencies
  * zsh
  * figlet
  * fortune
  * ruby
* Modify wizard to store git login information somewhere
  * See if github SSH key addition can be automated
* Move Vundle install out of vimrc? Maybe move to another package management system.

/root/.zshrc:source:18: no such file or directory: /root/.oh-my-zsh/oh-my-zsh.sh
/root/.zshrc:source:70: no such file or directory: /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
