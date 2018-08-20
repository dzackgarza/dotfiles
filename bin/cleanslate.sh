#!/bin/bash

source "$DOTFILES_ROOT/.bash_colors";

if [[ -d ~/.rstudio-desktop ]]; then
  clr_green "Backing up and clearing rstudio sessions..";
  mv --backup=numbered ~/.rstudio-desktop ~/backup-rstudio-desktop/
fi

clr_green "Done!";
