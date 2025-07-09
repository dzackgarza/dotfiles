#!/usr/bin/env zsh

# fzf navigation widgets
# This script provides interactive directory navigation tools using fzf

# Check if running in zsh (but don't exit if not, to allow for testing)
if [ -z "$ZSH_VERSION" ]; then
  echo "Warning: This script is optimized for zsh" >&2
fi

# fzf + zsh-z interactive directory jump (Ctrl+G)
# Uses zsh-z's frecency (frequency + recency) scoring
_fzf_z_widget() {
  local dir
  # z -l: List all directories with their scores
  # fzf +s --tac: Use fzf in non-sort mode with reversed input (newest first)
  # awk '{print $2}': Extract just the directory path
  dir=$(z -l | fzf +s --tac | awk '{print $2}') && cd "$dir"
  zle reset-prompt
}

# Enhanced directory navigation with hybrid matching
# Combines hardcoded shortcuts with dynamic path resolution

# Configuration
local -A NAV_SHORTCUTS=(
  [d]="$HOME/diss"
  [dd]="$HOME/diss/200-dev"
  [dp]="$HOME/diss/200-dev/projects"
  [dm]="$HOME/diss/200-dev/projects/mcp-servers"
  [dj]="$HOME/diss/200-dev/projects/mcp-servers/servers/jupyter-mcp"
)

# Main navigation function
_fzf_enhanced_nav() {
  local query="$*"
  
  # Check for exact shortcut match
  if [[ -n "${NAV_SHORTCUTS[$query]}" ]]; then
    echo "${NAV_SHORTCUTS[$query]}"
    return 0
  fi
  
  # Handle exact directory name matches first
  local exact_match=$(command find ~ -type d -name "$query" -not -path '*/.*' 2>/dev/null | head -n 1)
  if [[ -n "$exact_match" ]]; then
    echo "$exact_match"
    return 0
  fi
  
  # Then try basic path resolution (e.g., "diss")
  if [[ -d "$HOME/$query" ]]; then
    echo "$HOME/$query"
    return 0
  fi
  
  # Handle multi-part paths (e.g., "diss/200-dev")
  if [[ $query == */* ]]; then
    local -a parts=(${(s:/:)query})
    local current_path="$HOME"
    
    for part in "${parts[@]}"; do
      local found=""
      
      # Try exact match first
      if [[ -d "$current_path/$part" ]]; then
        found="$part"
      else
        # Try case-insensitive match
        found=$(command find "$current_path" -maxdepth 1 -type d -iname "${part}*" -not -path '*/.*' -print -quit 2>/dev/null)
        found="${found##*/}"  # Get just the directory name
      fi
      
      if [[ -n "$found" && -d "$current_path/$found" ]]; then
        current_path+="/$found"
      else
        # Fall back to fzf if no match found
        current_path+="/$part"
        break
      fi
    done
    
    if [[ -d "$current_path" ]]; then
      echo "$current_path"
      return 0
    fi
  fi
  
  # Fall back to fzf with enhanced scoring
  local selected
  
  # Custom scoring function for fzf
  export FZF_DEFAULT_OPTS="--height 40% --layout=reverse --border"
  
  # Use a custom scoring function to prioritize matches
  selected=$(command find ~ -type d -not -path '*/.*' 2>/dev/null | \
    while read -r dir; do
      local score=0
      local dirname="${dir##*/}"
      local lc_dirname="${(L)dirname}"  # Lowercase for case-insensitive comparison
      local lc_query="${(L)query}"      # Lowercase for case-insensitive comparison
      
      # 1. Exact match of directory name (highest priority)
      if [[ "$lc_dirname" == "$lc_query" ]]; then
        score=$((score + 1000))
      # 2. Query is a prefix of directory name (very high priority)
      elif [[ "$lc_dirname" == "$lc_query"* ]]; then
        # The closer the match is to the full name, the higher the score
        local remaining=${lc_dirname:${#lc_query}}
        score=$((score + 800 + (${#lc_query} * 10) - ${#remaining}))
      # 3. Directory name is a prefix of query (high priority)
      elif [[ "$lc_query" == "$lc_dirname"* ]]; then
        score=$((score + 600 + ${#lc_dirname}))
      # 4. Match at directory boundary
      elif [[ "$dir" == *"/$lc_query"* ]]; then
        score=$((score + 400))
      # 5. Match anywhere in path
      else
        # Check if all characters of query appear in order in the path
        local i=0
        local j=0
        local matched_chars=0
        local path_lc="${(L)dir}"
        
        while [[ $i -lt ${#lc_query} && $j -lt ${#path_lc} ]]; do
          if [[ "${lc_query[$i+1]}" == "${path_lc[$j+1]}" ]]; then
            ((i++))
            ((matched_chars++))
          fi
          ((j++))
        done
        
        if [[ $i -eq ${#lc_query} ]]; then
          score=$((score + 200 + (matched_chars * 10)))
        else
          score=$((score + 100))
        fi
      fi
      
      # Penalize longer paths (prefer shorter, more specific paths)
      local depth=$(tr -dc '/' <<< "$dir" | wc -c)
      score=$((score - (depth * 2)))
      
      # Bonus for matching multiple directory components in space-separated query
      if [[ "$lc_query" == *" "* ]]; then
        local -a query_parts=(${=lc_query})
        local -a dir_parts=(${(s:/:)dir})
        local part_matches=0
        
        for q in "${query_parts[@]}"; do
          for d in "${dir_parts[@]}"; do
            if [[ "${(L)d}" == "$q"* ]]; then
              ((part_matches++))
              break
            fi
          done
        done
        
        score=$((score + (part_matches * 50)))
      fi
      
      # Print score and path for sorting (higher scores first)
      printf "%d %s\n" "$score" "$dir"
    done | sort -nr | cut -d' ' -f2- | \
    fzf --query="$query" --preview='ls -F {}')
  
  if [[ -n "$selected" ]]; then
    echo "$selected"
    return 0
  fi
  
  return 1
}

# Zsh widget for changing directory
_fzf_cd_subdir() {
  local dir
  dir=$(_fzf_enhanced_nav "$BUFFER")
  
  if [[ -n "$dir" ]]; then
    cd "$dir"
    zle reset-prompt
  fi
}

# Zsh widget for inserting path
_fzf_insert_subdir() {
  local dir
  dir=$(_fzf_enhanced_nav "$BUFFER")
  
  if [[ -n "$dir" ]]; then
    # Convert to ~ if in home directory
    if [[ "$dir" == "$HOME"/* ]]; then
      dir="~${dir#$HOME}"
    fi
    LBUFFER+="${(q)dir}"
  fi
  
  zle reset-prompt
}

# Bind widgets
zle -N _fzf_cd_subdir
zle -N _fzf_insert_subdir

# Bind keys (can be customized in .zshrc)
bindkey '^T' _fzf_cd_subdir
bindkey '^[T' _fzf_insert_subdir

# Only define the widgets if running interactively and not in a script
if [[ $- == *i* ]] && [[ -z "$ZSH_FZF_JUMP_NO_WIDGET" ]]; then
  # Register widgets
  zle -N _fzf_z_widget
  zle -N _fzf_cd_subdir
  zle -N _fzf_insert_subdir
  
  # Set up key bindings if not already set
  if ! bindkey | grep -q _fzf_z_widget; then
    bindkey '^G' _fzf_z_widget        # Ctrl+G - Jump to frequent directory
    bindkey '^T' _fzf_cd_subdir      # Ctrl+T - Change to deep subdirectory
    bindkey '^[^T' _fzf_insert_subdir # Ctrl+Shift+T - Insert directory path
    # No console output during initialization for Powerlevel10k compatibility
  fi
fi

# vim: ft=zsh ts=2 sw=2 et
