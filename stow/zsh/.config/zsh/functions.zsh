# Custom Functions and Keybindings
# ----------------------------------

# NLSH Keybindings
if typeset -f nlsh-key-binding > /dev/null; then
  zle -N nlsh-key-binding
  bindkey "${terminfo[kcuu1]}" history-substring-search-up   # Up arrow
  bindkey "${terminfo[kcud1]}" history-substring-search-down # Down arrow
fi

zle -N nlsh-fzf-history-widget
bindkey '^G' nlsh-fzf-history-widget

