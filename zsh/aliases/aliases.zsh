# Dev Specific
#alias ls="colorls"
#alias ll="colorls -l"
alias mkdir="mkdir -p"

# Just git save everything
alias gsave="git add -A && git commit -m 'auto update' && git push origin master"

# Copy/paste piping
alias pbcopy='xsel --clipboard --input';
alias pbpaste='xsel --clipboard --output';

alias whatsmyip="curl ipinfo.io/ip"

alias r.ranger='SHELL=/usr/local/bin/r.shell ranger'

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

function todaymd() {
  todaydate=$(date +"%Y-%m-%d");
  fullname="./$basepath/$todaydate.md";
  touch $fullname;
}

function cphist() {
  history 2 | tail -1 | awk '{ first=$1; $1=""; print $0; }' | pbcopy
}


alias f='source $DOTFILES_ROOT/bin/dmenu/faves_term.sh'

alias ag='ag --noaffinity'

alias vim=nvim
