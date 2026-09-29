# Custom Aliases
# ----------------

# --- General Aliases ---
alias vim="nvim" # Use Neovim instead of Vim.
alias r="yazi" # Alias for ranger file manager.
alias cp="cp -i" # Confirm before overwriting files with 'cp'.

# --- Tool-Specific Aliases ---
# exa (modern replacement for ls)
alias l='exa --long --header --icons --sort=type --color=always -al'
alias ll='exa -lgh --icons --color=always --sort=type'
alias la='exa -lgha --icons --color=always --sort=type'
alias tr='exa --tree --level 3 --icons'

# Search tools
alias agti"ag --noaffinity" # The Silver Searcher
alias re='rg --smart-case --no-heading --color=auto -C 2' # Ripgrep

# System tools
alias yay='yay --noconfirm'
alias diff='diff --color=auto'
alias ping="grc ping" # Ensure GRC is configured if this is used

alias qutebrowser="qutebrowser --restore mysession"
alias commits="git log --oneline | dmenu -l 20 | cut -d' ' -f1 | xargs -r git checkout"

alias paru="paru --color always"
