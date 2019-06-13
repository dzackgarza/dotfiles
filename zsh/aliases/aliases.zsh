#function extract() {
  #if[ -f $1 ]; then
    #aunpack $1
  #else
    #echo "'$1' is not a valid file"
  #fi
#}


function mcd() {
	mkdir $1 && cd $1
}

# Dev Specific
alias ls="colorls"
alias ll="colorls -l"
#alias lsc="colorls"
alias mkdir="mkdir -p"

# Just git save everything
alias gsave="git add -A && git commit -m 'auto update' && git push origin master"

# Copy/paste piping
alias pbcopy='xsel --clipboard --input';
alias pbpaste='xsel --clipboard --output';

alias whatsmyip="curl ipinfo.io/ip"

function uninstall() {
  command -v yaourt >/dev/null 2>&1 && sudo yaourt -Rns "$1" --noconfirm;
}

function pinstall() {
  command -v yaourt >/dev/null 2>&1 && yaourt -S "$1" --noconfirm;
}

function researchnotes() {
  echo "Enter description for file name";
  read somefilename;
  todaydate=$(date +"%Y-%m-%d");
  basepath="/home/zack/Research/Notes/ReadingGeneral";
  fullname="$basepath/$todaydate $somefilename.md";
  echo "Creating file:\n$fullname\n";
  touch $fullname;
  vim $fullname;
}
