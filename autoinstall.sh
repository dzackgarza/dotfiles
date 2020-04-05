#!/usr/bin/env bash
#
# bootstrap installs things.

DOTFILES_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# DOTFILES_ROOT=`dirname $SCRIPT_DIR`
echo "Using the following dotfiles root foler: $DOTFILES_ROOT"

set -e

echo ''

info () {
  printf "  [ \033[00;34m..\033[0m ] $1"
}

user () {
  printf "\r  [ \033[0;33m?\033[0m ] $1 "
}

success () {
  printf "\r\033[2K  [ \033[00;32mOK\033[0m ] $1\n"
}

fail () {
  printf "\r\033[2K  [\033[0;31mFAIL\033[0m] $1\n"
  echo ''
  exit
}

setup_gitconfig () {
  if ! [ -f $HOME/.gitconfig ]; then
    user ' - What is your github author email?'
    read -e git_authoremail
    ssh-keygen -t rsa -b 4096 -C $git_authoremail
    eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_rsa
    success 'gitconfig'
  fi
}


link_file () {
  local src=$1 dst=$2

  local overwrite= backup= skip=
  local action=

  if [ -f "$dst" -o -d "$dst" -o -L "$dst" ]
  then

    if [ "$overwrite_all" == "false" ] && [ "$backup_all" == "false" ] && [ "$skip_all" == "false" ]
    then

      local currentSrc="$(readlink $dst)"

      if [ "$currentSrc" == "$src" ]
      then

        skip=true;

      else

        user "File already exists: $(basename "$src"), what do you want to do? [s]kip, [S]kip all, [o]verwrite, [O]verwrite all, [b]ackup, [B]ackup all?"
        read -n 1 action

        case "$action" in
          o )
            overwrite=true;;
          O )
            overwrite_all=true;;
          b )
            backup=true;;
          B )
            backup_all=true;;
          s )
            skip=true;;
          S )
            skip_all=true;;
          * )
            ;;
        esac

      fi

    fi

    overwrite=${overwrite:-$overwrite_all}
    backup=${backup:-$backup_all}
    skip=${skip:-$skip_all}

    if [ "$overwrite" == "true" ]
    then
      rm -rf "$dst"
      success "removed $dst"
    fi

    if [ "$backup" == "true" ]
    then
      mv "$dst" "${dst}.backup"
      success "moved $dst to ${dst}.backup"
    fi

    if [ "$skip" == "true" ]
    then
      success "skipped $src"
    fi
  fi

  if [ "$skip" != "true" ]  # "false" or empty
  then
    ln -s "$1" "$2"
    success "linked $1 to $2"
  fi
}

install_dotfiles () {
  info 'installing dotfiles'

  local overwrite_all=false backup_all=false skip_all=false

  for src in $(find "$DOTFILES_ROOT" -maxdepth 2 -name '*.symlink')
  do
    dst="$HOME/.$(basename "${src%.*}")"
    link_file "$src" "$dst"
  done
  if [ ! -d $HOME/zsh-syntax-highlighting ]; then
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $HOME/zsh-syntax-highlighting
  fi
}

# Install Packagezs
# yaourt --needed --noconfirm -S - < packages.list
# todo: Install go and tewisay
if ! [[ $(awk -F: -v user="zack" '$1 == user {print $NF}' /etc/passwd) = $(which zsh) ]]; then
  chsh -s $(which zsh)
fi

# Install oh-my-zsh
if [ ! -d $HOME/.oh-my-zsh ]; then
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
fi

# Install antigen
curl -L git.io/antigen > antigen.zsh
#source ./antigen.zsh
success "Run 'source antigen.zsh' from zsh."

setup_gitconfig
install_dotfiles

info "Linking vim files.."
if [ ! -d $HOME/.vim ]; then
  ln -s $DOTFILES_ROOT/vim/vim $HOME/.vim
fi
success "Vim files linked."

info "Installing Vundle..."
if [ ! -d $HOME/.vim/bundle/Vundle.vim ]; then
  git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/Vundle.vim
fi
success "Vundle installed."

info "Installing Pathogen.."
mkdir -p ~/.vim/autoload ~/.vim/bundle
curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim
success "Pathogen installed."

info "Setting up vim.."
vim +PluginInstall +qall
success "Vim setup successful."

if [ ! -d $HOME/.fzf ]; then
  info "Installing fzf..."
  git clone --depth 1 https://github.com/junegunn/fzf.git $HOME/.fzf
  $HOME/.fzf/install
  success "fzf installed."
fi

if [ ! -d $HOME/.rvm ]; then
  info "Installing rvm..."
  gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
  \curl -sSL https://get.rvm.io | bash -s -- --ignore-dotfiles
  source $HOME/.rvm/scripts/rvm
  rvm install ruby --latest
  rvm --default use ruby
  gem install lolcat colorls
  info "rvm, ruby, and gems installed."
fi

if [ ! -d $HOME/.nvm ]; then
  info "Installing nvm..."
  mkdir $HOME/.nvm
  curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
  nvm install node
  npm install -g webpack eslint
  info "NVM, node, and global packages installed."
fi

echo ''
echo ' Installation Completed.'

xclip -sel clip < $HOME/.ssh/id_rsa.pub

echo 'SSH key copied to clipboard, go to Github to add.'
