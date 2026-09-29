# Environment Variables and PATH
# --------------------------------

# Perl
PATH="/home/dzack/perl5/bin${PATH:+:${PATH}}"; export PATH;
PERL5LIB="/home/dzack/perl5/lib/perl5${PERL5LIB:+:${PERL5LIB}}"; export PERL5LIB;
PERL_LOCAL_LIB_ROOT="/home/dzack/perl5${PERL_LOCAL_LIB_ROOT:+:${PERL_LOCAL_LIB_ROOT}}"; export PERL_LOCAL_LIB_ROOT;
PERL_MB_OPT="--install_base "/home/dzack/perl5""; export PERL_MB_OPT;
PERL_MM_OPT="INSTALL_BASE=/home/dzack/perl5"; export PERL_MM_OPT;

# Git
export GIT_EDITOR='echo'
export GIT_MERGE_AUTOEDIT=no

# Editor
export EDITOR=nvim
export VISUAL=nvim

# FZF Configuration
export FZF_CTRL_T_COMMAND="find . -name .git -prune -o -name node_modules -prune -o -name __pycache__ -prune -o -name .pytest_cache -prune -o -name venv -prune -o -name .venv -prune -o -name env -prune -o -name .env -prune -o -name dist -prune -o -name build -prune -o -name .mypy_cache -prune -o -name .tox -prune -o -name .local -prune -o -name .cache -prune -o -name .cargo -prune -o -name .npm -prune -o -name .yarn -prune -o -name .composer -prune -o -name .gradle -prune -o -name .m2 -prune -o -name .nuget -prune -o -name target -prune -o -name vendor -prune -o -name .bundle -prune -o -type f -print -o -type d -print"

# Base16 Theme Integration (managed by tinty)
[[ -f ~/.config/zsh/base16-theme.zsh ]] && source ~/.config/zsh/base16-theme.zsh

# Load dircolors for themed LS colors
[[ -f ~/.config/dircolors ]] && eval "$(dircolors -b ~/.config/dircolors)"

# Wayland
# export WAYLAND_DISPLAY=wayland-1
# export MOZ_ENABLE_WAYLAND=1

# Ollama
export OLLAMA_NUM_GPU=999
export ZES_ENABLE_SYSMAN=1
export SYCL_CACHE_PERSISTENT=1
export OLLAMA_KEEP_ALIVE=30m
export OLLAMA_MAX_LOADED_MODELS=1

# NPM
export PATH=~/.npm-global/bin:$PATH

# Dotfiles bin directory
export PATH=~/dotfiles/bin:$PATH
export PATH=~/dotfiles/bin/llm-scripts:$PATH
export PATH=~/go/bin/:$PATH
export PATH=~/.cargo/bin/:$PATH
export XDG_DATA_DIRS=~/.local/share/:$XDG_DATA_DIRS
