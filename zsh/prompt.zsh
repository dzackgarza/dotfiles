 #autoload colors && colors
  #cheers, @ehrenmurdick
  #http://github.com/ehrenmurdick/config/blob/master/zsh/prompt.zsh

 #if (( $+commands[git] ))
 #then
   #git="$commands[git]"
 #else
   #git="/usr/bin/git"
 #fi

 #git_branch() {
   #echo $($git symbolic-ref HEAD 2>/dev/null | awk -F/ {'print $NF'})
 #}

 #git_dirty() {
   #if $(! $git status -s &> /dev/null)
   #then
     #echo ""
   #else
     #if [[ $($git status --porcelain) == "" ]]
     #then
       #echo "{%{$fg_bold[green]%}$(git_prompt_info)%{$reset_color%}}"
     #else
       #echo "{%{$fg_bold[red]%}$(git_prompt_info)%{$reset_color%}}"
     #fi
   #fi
 #}

 #git_prompt_info () {
  #ref=$($git symbolic-ref HEAD 2>/dev/null) || return
  #echo "(%{\e[0;33m%}${ref#refs/heads/}%{\e[0m%})"
  #echo "${ref#refs/heads/}"
 #}

 #unpushed () {
   #$git cherry -v @{upstream} 2>/dev/null
 #}

 #need_push () {
   #if [[ $(unpushed) == "" ]]
   #then
     #echo " "
   #else
     #echo " with %{$fg_bold[magenta]%}unpushed%{$reset_color%} "
   #fi
 #}

 #ruby_version() {
   #if (( $+commands[rbenv] ))
   #then
     #echo "$(rbenv version | awk '{print $1}')"
   #fi

   #if (( $+commands[rvm-prompt] ))
   #then
     #echo "$(rvm-prompt | awk '{print $1}')"
   #fi
 #}

 #rb_prompt() {
   #if ! [[ -z "$(ruby_version)" ]]
   #then
     #echo "%{$fg_bold[yellow]%}$(ruby_version)%{$reset_color%} "
   #else
     #echo ""
   #fi
 #}

 #directory_name() {
   #echo "%{$fg_bold[cyan]%}%1/%\/%{$reset_color%}"
 #}

 #export PROMPT=$'\n$hostname:$(rb_prompt)$(directory_name) $(git_dirty)$(need_push)\n› '

 #set_prompt () {
   #export RPROMPT="%{$fg_bold[cyan]%}%{$reset_color%}"
 #}

 #precmd() {
   #title "zsh" "%m" "%55<...<%~"
   #set_prompt
 #}

# Fix obnoxious syntax highlighting colros
# Must be loaded after some other stuff (?)
# Enable highlighters
ZSH_HIGHLIGHT_HIGHLIGHTERS=(main brackets pattern)

# Override highlighter colors
ZSH_HIGHLIGHT_STYLES[default]=none
ZSH_HIGHLIGHT_STYLES[unknown-token]=fg=009
ZSH_HIGHLIGHT_STYLES[reserved-word]=fg=009,standout
ZSH_HIGHLIGHT_STYLES[alias]=fg=white,bold
ZSH_HIGHLIGHT_STYLES[builtin]=fg=white,bold
ZSH_HIGHLIGHT_STYLES[function]=fg=white,bold
ZSH_HIGHLIGHT_STYLES[command]=fg=white,bold
ZSH_HIGHLIGHT_STYLES[precommand]=fg=white,underline
ZSH_HIGHLIGHT_STYLES[commandseparator]=none
ZSH_HIGHLIGHT_STYLES[hashed-command]=fg=009
ZSH_HIGHLIGHT_STYLES[path]=fg=214,underline
ZSH_HIGHLIGHT_STYLES[globbing]=fg=063
ZSH_HIGHLIGHT_STYLES[history-expansion]=fg=white,underline
ZSH_HIGHLIGHT_STYLES[single-hyphen-option]=none
ZSH_HIGHLIGHT_STYLES[double-hyphen-option]=none
ZSH_HIGHLIGHT_STYLES[back-quoted-argument]=none
ZSH_HIGHLIGHT_STYLES[single-quoted-argument]=fg=063
ZSH_HIGHLIGHT_STYLES[double-quoted-argument]=fg=063
ZSH_HIGHLIGHT_STYLES[dollar-double-quoted-argument]=fg=009
ZSH_HIGHLIGHT_STYLES[back-double-quoted-argument]=fg=009
ZSH_HIGHLIGHT_STYLES[assign]=none


