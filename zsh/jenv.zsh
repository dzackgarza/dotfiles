FOUND_JENV=0
jenvdirs=("$HOME/.jenv" "/usr/local/jenv" "/opt/jenv")

for jenvdir in "${jenvdirs[@]}" ; do
  if [ -d $jenvdir/bin -a $FOUND_JENV -eq 0 ] ; then
    FOUND_JENV=1
    export JENV_ROOT=$jenvdir
    export PATH=${jenvdir}/bin:$PATH
    eval "$(jenv init --no-rehash - zsh)"

    function jenv_prompt_info() {
        echo "$(jenv version-name)"
    }
  fi
done
unset jenvdir

if [ $FOUND_JENV -eq 0 ] ; then
  function jenv_prompt_info() { echo "system: $(java -version 2>&1 | cut -f 3 -d ' '|cut -f 2 -d '"'|head -n1)" }
fi
