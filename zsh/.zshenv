export LANG=en_US.UTF-8
export LC_CTYPE=en_US.UTF-8

export EDITOR=nvim
export VISUAL=nvim
export PAGER=less
export SHELL=/bin/zsh
export TERM=xterm-256color
export JEKYLL_EDITOR=typora
export ZSH=$HOME/.oh-my-zsh

export DOTFILES_ROOT="$HOME/dotfiles"
export PATH="$DOTFILES_ROOT/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"

for d in $DOTFILES_ROOT/bin/*/; do
  PATH="$PATH:$d"
done

export BCAT_BROWSER=qutebrowser

export NOTES=$HOME/Notes
export PANDOC_DIR=$HOME/.pandoc
export PATH="$PANDOC_DIR/bin:$PATH"
export PANDOC_TEMPLATES=$PANDOC_DIR/pandoc-templates
export PANDOC_BIB=$NOTES/library.bib
export CUSTOM_TEX_DIR=$PANDOC_DIR/custom
export TEXINPUTS=.:$PANDOC_DIR/custom//:




if [ -e /home/zack/.nix-profile/etc/profile.d/nix.sh ]; then . /home/zack/.nix-profile/etc/profile.d/nix.sh; fi # added by Nix installer
