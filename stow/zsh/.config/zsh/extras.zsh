#!/usr/bin/env zsh
#
# Additional Zsh configurations and customizations
# ---------------------------------------------

# =============================================================================
# Path Modifications
# =============================================================================

# Add local binaries to PATH
path=(
    $HOME/.local/bin
    $HOME/.cabal/bin
    $HOME/bin
    $HOME/.jenv/bin
    $HOME/anaconda3/bin
    $HOME/anaconda/bin
    $DOTFILES_ROOT/bin
    $path
)

export PATH

# Initialize jenv if available
if command -v jenv >/dev/null; then
    eval "$(jenv init -)"
fi

# Initialize rbenv if available
if command -v rbenv >/dev/null; then
    eval "$(rbenv init - zsh)"
fi

# =============================================================================
# Shell Options
# =============================================================================

# Better history handling
setopt extended_history       # Record timestamp and duration
setopt hist_ignore_dups      # Don't record duplicate entries
setopt hist_ignore_all_dups  # Remove older duplicate entries
setopt hist_find_no_dups     # Don't show duplicates in search
setopt hist_save_no_dups     # Don't write duplicate entries to history
setopt share_history         # Share history between sessions
setopt hist_reduce_blanks    # Remove superfluous blanks

# Navigation and completion
setopt auto_cd               # Change directory without 'cd' command
setopt auto_pushd            # Make cd push the old directory onto the directory stack
setopt pushd_ignore_dups     # Don't push multiple copies of the same directory

# =============================================================================
# Enhanced Standard Zsh Completion (Canonical approach)
# =============================================================================

# Enable better completion menu
zstyle ':completion:*' menu select
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=*' 'l:|=* r:|=*'

# Group completions by type
zstyle ':completion:*' group-name ''
zstyle ':completion:*:descriptions' format '%B%d%b'
zstyle ':completion:*:warnings' format 'No matches for: %d'

# Better directory completion
zstyle ':completion:*:cd:*' ignore-parents parent pwd
zstyle ':completion:*:cd:*' special-dirs true
zstyle ':completion:*' squeeze-slashes true

# Smart case-insensitive completion
zstyle ':completion:*' completer _complete _match _approximate
zstyle ':completion:*:match:*' original only
zstyle ':completion:*:approximate:*' max-errors 1 numeric

# Use arrow keys to navigate completion menu
bindkey '^[[A' up-line-or-search
bindkey '^[[B' down-line-or-search
setopt pushd_minus           # Swap the meaning of '+' and '-' when used with a number
setopt complete_in_word      # Allow completion from within a word
setopt always_to_end         # Move cursor to end of word after completion
setopt menu_complete         # Insert first match immediately

# Other useful options
setopt aliases              # Enable aliases in non-interactive shells
setopt completealiases      # Better alias completion
setopt nobanghist           # Disable ! history expansion
setopt interactive_comments # Allow comments in interactive shells
setopt extended_glob        # Enable extended globbing
setopt no_beep              # Disable beeping
setopt no_flow_control      # Disable flow control (^S/^Q)

# =============================================================================
# Key Bindings
# =============================================================================

# Better history search
autoload -U up-line-or-beginning-search
autoload -U down-line-or-beginning-search
zle -N up-line-or-beginning-search
zle -N down-line-or-beginning-search

# Bind up/down arrows for history search
bindkey '^[[A' up-line-or-beginning-search
bindkey '^[OA' up-line-or-beginning-search
bindkey '^[[B' down-line-or-beginning-search
bindkey '^[OB' down-line-or-beginning-search

# Word navigation (Ctrl+left/right)
bindkey '^[[1;5D' backward-word
bindkey '^[[1;5C' forward-word

# Home/End keys
bindkey '^[[H' beginning-of-line
bindkey '^[[F' end-of-line
bindkey '^[[3~' delete-char

# Ensure Ctrl+R triggers history search regardless of keymap or plugin state
if (( $+functions[fzf-history-widget] )); then
    bindkey '^R' fzf-history-widget
    bindkey -M viins '^R' fzf-history-widget
else
    bindkey '^R' history-incremental-search-backward
    bindkey -M viins '^R' history-incremental-search-backward
fi

# =============================================================================
# Completion System
# =============================================================================
# NOTE: compinit already loaded in ~/.zshrc

# Enable bash completion compatibility (only if not already loaded)
if ! functions -S bashcompinit >/dev/null 2>&1; then
    autoload -U +X bashcompinit && bashcompinit
fi

# Completion settings
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*' group-name ''
zstyle ':completion:*:descriptions' format '%B%d%b'

# Cache completions
zstyle ':completion:*' use-cache on
zstyle ':completion:*' cache-path ${XDG_CACHE_HOME:-$HOME/.cache}/zsh/completion-cache

# Command not found hook
if [[ -r '/usr/share/doc/pkgfile/command-not-found.zsh' ]]; then
    source '/usr/share/doc/pkgfile/command-not-found.zsh'
fi

# =============================================================================
# Startup Commands
# =============================================================================

# Function to run startup commands after instant prompt is ready
function _run_startup_commands() {
    # Only run in interactive shells
    if [[ -o interactive ]]; then
        # Show hostname with figlet if available
        if command -v figlet >/dev/null; then
            echo -n "\n"
            hostname | figlet -k
        fi

        # Show fortune with custom cowsay if available
        if command -v fortune >/dev/null; then
            # Set custom cowpath if it exists
            [[ -d "${DOTFILES_ROOT:-$HOME/dotfiles}/zsh/cows" ]] && \
                export COWPATH=${COWPATH}:${DOTFILES_ROOT:-$HOME/dotfiles}/zsh/cows
            
            echo -n "\n"
            if command -v tewisay >/dev/null && command -v lolcat >/dev/null; then
                fortune -a | tewisay -f kingslime | lolcat
            elif command -v cowsay >/dev/null; then
                if command -v lolcat >/dev/null; then
                    fortune -a | cowsay -f $(ls /usr/share/cowsay/cows/ 2>/dev/null | shuf -n1) | lolcat 2>/dev/null || \
                    fortune -a | cowsay
                else
                    fortune -a | cowsay
                fi
            else
                fortune -a
            fi
        fi

        # Show current date and time
        echo -e "\nToday is $(date '+%A, %B %d, %Y %H:%M:%S')\n"
    fi
}

# Run startup commands after instant prompt is ready
if [[ -n "${ZSH_VERSION}" && "${ZSH_VERSION}" != "" ]]; then
    autoload -Uz add-zsh-hook
    add-zsh-hook precmd _run_startup_commands
    # Only run once
    add-zsh-hook -d precmd _run_startup_commands
fi

# =============================================================================
# Additional Zinit Plugins
# =============================================================================

# Load additional zsh plugins if zinit is installed
if [[ -f "$HOME/.zinit/bin/zinit.zsh" ]]; then
    # Load zsh-history-substring-search
    zinit light zsh-users/zsh-history-substring-search
    
    # Bind keys for history-substring-search
    bindkey '^[[A' history-substring-search-up
    bindkey '^[OA' history-substring-search-up
    bindkey '^[[B' history-substring-search-down
    bindkey '^[OB' history-substring-search-down
    
    # Load additional completions
    zinit light zsh-users/zsh-completions
    
    # Load syntax highlighting (if not already loaded)
    if ! zinit list | grep -q "zsh-syntax-highlighting"; then
        zinit light zsh-users/zsh-syntax-highlighting
    fi
fi

# =============================================================================
# Environment-Specific Settings
# =============================================================================

# Load machine-specific settings if they exist
[[ -f ~/.zshrc.local ]] && source ~/.zshrc.local
[[ -f ~/.config/zsh/local.zsh ]] && source ~/.config/zsh/local.zsh
