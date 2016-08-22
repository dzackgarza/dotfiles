alias reload!='. ~/.zshrc'


alias syncjogl_fromdev='rsync -raz zgarza@zgarza.tinyprints.com:/opt/tinyprints/w2p-jogl /opt/tinyprints'

alias syncjogl_todev='rsync -raz /opt/tinyprints wqzgarza@zgarza.tinyprints.com:/opt/tinyprints/w2p-jogl'

function parHaskell() {
	ghc -O2 --make $1 -threaded -rtsopts;
}

#export JAVA_HOME='/usr/libexec/java_home'



# SSH Shortcuts
alias tpd='ssh zgarza@zgarza.tinyprints.com'
alias droplet='ssh root@104.131.9.12'
alias berkeley='ssh -XC -c blowfish-cbc,arcfour cory.eecs.berkeley.edu -l cs70-awu'


# Dev Specific
alias log='tail -f /var/log/tpsite/php.log'
alias l="ls"
alias sr='/etc/init.d/smb restart'

alias cdjogl='cd /opt/tinyprints/w2p-jogl/src/main/java/com/tinyprints/w2p/gl'
alias setjava8='export JAVA_HOME=/opt/jdk1.8.0_05; export JRE_HOME=/opt/jdk1.8.0_05/jre; export PATH=$PATH:/opt/jdk1.8.0_05/bin:/opt/jdk1.8.0_05/jre/bin:/opt/jdk1.8.0_05/bin:/opt/jdk1.8.0_05/jre/bin;    '
alias xvrestart='pkill Xvfb;export DISPLAY=:2; Xvfb :2 -screen 0 500x500x24 &'

alias qbuild-jogl='mvn clean install -T 3C -o -Dmaven.test.skip=true'
alias jbuildw2pjogl='cd /opt/tinyprints/w2p-jogl;/dist/apache-tomcat-7.0.29/bin/shutdown.sh;mvn clean install -T 4C -Pgenerate_font -o -Dmaven.test.skip=true;rm -rf /dist/apache-tomcat-7.0.29/webapps    /*;command cp -f target/web2print.war /dist/apache-tomcat-7.0.29/webapps/web2print.war;/dist/apache-tomcat-7.0.29/bin/startup.sh'
alias w2pbuild='cd /opt/tinyprints/web2print_trunk;/dist/apache-tomcat-7.0.29/bin/shutdown.sh;mvn clean install -T 4C -Pgenerate_font -o -Dmaven.test.skip=true;rm -rf /dist/apache-tomcat-7.0.29/webap    ps/*;command cp -f target/web2print.war /dist/apache-tomcat-7.0.29/webapps/web2print.war;/dist/apache-tomcat-7.0.29/bin/startup.sh'

alias permfix='sudo chown -R zgarza:zgarza /opt/tinyprints && find /opt/tinyprints/w2p-jogl -type f -perm 777 -print -exec chmod 755 {} \;'
alias crestart='/dist/apache-tomcat-7.0.29/bin/shutdown.sh && /dist/apache-tomcat-7.0.29/bin/startup.sh'

alias getqueries="cat ~/.config/calibre/server_access_log.txt| grep -o -E 'query=[^ ]+' | sed 's/query=//' | sed 's/\"//' | sed 's/^[ \t]*//' | sort | uniq"

alias ls='ls --color=auto'
