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
