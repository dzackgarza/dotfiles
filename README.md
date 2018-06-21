Take your dotfiles everywhere!

# How to Install
```
sudo apt-get install pacapt
git clone --recursive -j8 git://github.com/dzackgarza/dotfiles.git
cd dotfiles
sudo ./autoinstall.sh
```

# Dependencies
* pacapt (If not on Arch, to abstract away the underlying package manager)

# What does this script install?
* Some OS packages (see packages.list)
* nvm for Node
* rvm for Ruby
* Some vim plugins

# Todo List
* Install packages automatically
  ** python virtualenv
* Include fonts
* Fix HaskellConcealPlus vim plugin
* Fix prompt
* Fix LSCOLORS
* Fix vim's transparency issues
* Fix vim autoindent for markdown files
* Modify wizard to store git login information somewhere
  * See if github SSH key addition can be automated
