# Restart XMonad
alias xr="xmonad --recompile && xmonad --restart"

# SSH Targets
alias droplet='ssh root@104.131.9.12'
alias berkeley='ssh -XC -c blowfish-cbc,arcfour cory.eecs.berkeley.edu -l cs70-awu'

function build_ctags_php() {
	ctags -f ~/.vim/tags/myphpproject \
	--langmap="php:+.inc" -h ".php.inc" -R \
	--exclude='*.js' \
	--exclude='*.sql' \
	--totals=yes \
	--tag-relative=yes \
	--PHP-kinds=+cf-v \
	--regex-PHP='/abstract\s+class\s+([^ ]+)/\1/c/' \
	--regex-PHP='/interface\s+([^ ]+)/\1/c/' \
	--regex-PHP='/(public\s+|static\s+|abstract\s+|protected\s+|private\s+)function\s+\&?\s*([^ (]+)/\2/f/'
}

function py { 
	python3 $1; 
}

function parHaskell() { 
	ghc -O2 --make $1 -threaded -rtsopts; 
}

function mcd() {
	mkdir $1 && cd $1
}

# Copy to X-Window clipboard
alias cp="xclip -sel clip"

alias ls="ls --color=always"

alias mkdir="mkdir -p"
