#! /bin/bash

cd $HOME/.dotfiles
git pull origin master
./script/boostrap
cp -f /root/.bashrc /home/zgarza/.bashrc
cp -f -R /root/.zsh* /home/zgarza/
cp -f /root/.bash_aliases /home/zgarza/.bash_aliases
cp -f -R /root/.vim* /home/zgarza/
chmod 777 -R /home/zgarza

