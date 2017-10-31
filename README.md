Take your dotfiles everywhere!

# How to Install
```
sudo apt-get install pacapt
git clone --recursive -j8 git://github.com/dzackgarza/dotfiles.git
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
  ** ruby
  ** nvm
  ** python virtualenv
* Include fonts
* Fix HaskellConcealPlus vim plugin
* Fix prompt
* Fix LSCOLORS
* Fix vim's transparency issues
* Fix vim autoindent for markdown files
* Fix antigen install issues, or install vim-apt
* Install programming environments
* Modify wizard to store git login information somewhere
  * See if github SSH key addition can be automated
* Move Vundle install out of vimrc? Maybe move to another package management system.
