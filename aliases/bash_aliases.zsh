alias tpd='ssh zgarza@zgarza.tinyprints.com'

alias syncjogl_fromdev='rsync -raz zgarza@zgarza.tinyprints.com:/opt/tinyprints/w2p-jogl /opt/tinyprints'

alias syncjogl_todev='rsync -raz /opt/tinyprints wqzgarza@zgarza.tinyprints.com:/opt/tinyprints/w2p-jogl'

function py { 
	python3 $1; 
}

function parHaskell() { 
	ghc -O2 --make $1 -threaded -rtsopts; 
}

export JAVA_HOME='/usr/libexec/java_home'

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
