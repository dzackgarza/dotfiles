function jg () {
  curl -i -H "Accept: application/json" -H "Content-Type: application/json" "$1" -L
}

function jp () {
  curl --data "$1" "$2"
}

function parHaskell() {
	ghc -O2 --make $1 -threaded -rtsopts;
}

function mcd() {
	mkdir $1 && cd $1
}

# For xmonad tweaking
alias xr="xmonad --recompile && xmonad --restart"

# Dev Specific
alias ls="colorls"
alias l="colorls"
alias mkdir="mkdir -p"

# Just git save everything
alias gsave="git add -A && git commit -m 'auto update' && git push origin master"

# Copy/paste piping
alias pbcopy='xsel --clipboard --input';
alias pbpaste='xsel --clipboard --output';

# Directory jumping
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias .....="cd ../../../.."
alias gsave="git add -A && git commit -am Update && git push"

alias owp='"$(xclip -o | sed -E '\''s/\\/\//g'\'' | sed -E '\''s/X:/\/home\/zack\/onedrive/g'\'')"'
