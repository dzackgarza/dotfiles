function parHaskell() {
	ghc -O2 --make $1 -threaded -rtsopts;
}

#export JAVA_HOME='/usr/libexec/java_home'



# SSH Shortcuts
alias tpd='ssh zgarza@zgarza.tinyprints.com'
alias droplet='ssh root@104.131.9.12'
alias berkeley='ssh -XC -c blowfish-cbc,arcfour cory.eecs.berkeley.edu -l cs70-awu'


# Dev Specific
alias l="ls"

alias getqueries="cat ~/.config/calibre/server_access_log.txt| grep -o -E 'query=[^ ]+' | sed 's/query=//' | sed 's/\"//' | sed 's/^[ \t]*//' | sort | uniq"

alias ls='ls --color=auto'

alias pbcopy='xsel --clipboard --input';
alias pbpaste='xsel --clipboard --output';
