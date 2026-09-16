# NVM environment authority for zsh.
#
# Login shells source this before Hyprland starts so GUI children inherit the
# NVM-selected Node. Interactive non-login shells source the same file as a
# fallback. NVM_SYMLINK_CURRENT gives non-interactive descendants a stable
# ~/.nvm/current/bin path even when the concrete default Node version changes.
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
export NVM_SYMLINK_CURRENT=true

if [[ -s "$NVM_DIR/nvm.sh" ]]; then
    if ! typeset -f nvm >/dev/null 2>&1; then
        . "$NVM_DIR/nvm.sh" --no-use
    fi
    nvm use --silent default >/dev/null
fi
