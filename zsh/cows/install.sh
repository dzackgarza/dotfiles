#!/usr/bin/zsh
if hash cowsay 2>/dev/null; then
  DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"
	sudo ln -s $DIR/healy.cow /usr/share/cows/healy.cow
	sudo chmod 644 /usr/share/cows/healy.cow
fi
