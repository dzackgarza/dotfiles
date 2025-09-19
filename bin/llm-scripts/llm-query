#!/bin/bash

# Cleanup function
cleanup() {
    rm -f /tmp/prompts_array.sh
}
trap cleanup EXIT 
# Modern template injection with fzf preview
# Usage: script [theme_name]
# Available themes: catppuccin, dracula, nord, gruvbox, tokyo, onedark

PROMPTS_FILE="${HOME}/.config/prompts.md"
THEME="${1:-catppuccin}"  # Default to catppuccin if no theme specified

# Function to get theme colors for fzf
get_theme_colors() {
    case "$1" in
        catppuccin)
            echo "--color=bg:#1e1e2e,fg:#cdd6f4,header:#f38ba8,info:#cba6f7,pointer:#f5e0dc,marker:#f5e0dc,spinner:#f5e0dc,prompt:#cba6f7,hl:#f38ba8,hl+:#f38ba8,bg+:#313244,fg+:#cdd6f4,gutter:#1e1e2e,border:#6c7086"
            ;;
        dracula)
            echo "--color=bg:#282a36,fg:#f8f8f2,header:#ff79c6,info:#bd93f9,pointer:#ffb86c,marker:#50fa7b,spinner:#8be9fd,prompt:#bd93f9,hl:#ff79c6,hl+:#ff79c6,bg+:#44475a,fg+:#f8f8f2,gutter:#282a36,border:#6272a4"
            ;;
        nord)
            echo "--color=bg:#2e3440,fg:#d8dee9,header:#bf616a,info:#5e81ac,pointer:#d08770,marker:#a3be8c,spinner:#88c0d0,prompt:#5e81ac,hl:#bf616a,hl+:#bf616a,bg+:#3b4252,fg+:#d8dee9,gutter:#2e3440,border:#4c566a"
            ;;
        gruvbox)
            echo "--color=bg:#1d2021,fg:#ebdbb2,header:#fb4934,info:#fabd2f,pointer:#fe8019,marker:#b8bb26,spinner:#8ec07c,prompt:#fabd2f,hl:#fb4934,hl+:#fb4934,bg+:#3c3836,fg+:#ebdbb2,gutter:#1d2021,border:#504945"
            ;;
        tokyo)
            echo "--color=bg:#1a1b26,fg:#c0caf5,header:#f7768e,info:#bb9af7,pointer:#ff9e64,marker:#9ece6a,spinner:#7dcfff,prompt:#bb9af7,hl:#f7768e,hl+:#f7768e,bg+:#24283b,fg+:#c0caf5,gutter:#1a1b26,border:#565f89"
            ;;
        onedark)
            echo "--color=bg:#282c34,fg:#abb2bf,header:#e06c75,info:#c678dd,pointer:#d19a66,marker:#98c379,spinner:#56b6c2,prompt:#c678dd,hl:#e06c75,hl+:#e06c75,bg+:#3e4451,fg+:#abb2bf,gutter:#282c34,border:#4b5263"
            ;;
        *)
            echo "--color=bg:#1e1e2e,fg:#cdd6f4,header:#f38ba8,info:#cba6f7,pointer:#f5e0dc,marker:#f5e0dc,spinner:#f5e0dc,prompt:#cba6f7,hl:#f38ba8,hl+:#f38ba8,bg+:#313244,fg+:#cdd6f4,gutter:#1e1e2e,border:#6c7086"
            ;;
    esac
}

# Validate theme
valid_themes="catppuccin dracula nord gruvbox tokyo onedark"
if [[ ! " $valid_themes " =~ " $THEME " ]]; then
    echo "Error: Unknown theme '$THEME'"
    echo "Available themes: $valid_themes"
    exit 1
fi

# Check if prompts file exists
if [[ ! -f "$PROMPTS_FILE" ]]; then
    echo "Error: Prompts file not found at $PROMPTS_FILE"
    exit 1
fi

# Parse prompts
declare -A prompts
header=""
content=""
while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ $line =~ ^#[[:space:]]+(.+)$ ]]; then
        [[ -n "$header" && -n "$content" ]] && prompts["$header"]="$content"
        header="${BASH_REMATCH[1]}"
        content=""
    elif [[ -n "$header" && -n "${line// /}" ]]; then
        content="${content:+$content$'\n'}$line"
    fi
done < "$PROMPTS_FILE"
[[ -n "$header" && -n "$content" ]] && prompts["$header"]="$content"

# Check if we have any prompts
if [[ ${#prompts[@]} -eq 0 ]]; then
    echo "Error: No prompts found in $PROMPTS_FILE"
    exit 1
fi

# Get theme colors
theme_colors=$(get_theme_colors "$THEME")

# Create a simple preview function
preview_template() {
    echo "${prompts[$1]}"
}

# Export the function and prompts array for the preview
export -f preview_template
export prompts
declare -p prompts > /tmp/prompts_array.sh

# Select template with preview
template=$(printf '%s\n' "${!prompts[@]}" | sort | fzf \
    --prompt="❯ template: " \
    --height=80% \
    --border=rounded \
    --margin=2% \
    --padding=1% \
    --info=inline \
    --layout=reverse \
    --pointer='▶' \
    --marker='✓' \
    --bind='ctrl-c:abort' \
    --bind='esc:abort' \
    --cycle \
    --preview="source /tmp/prompts_array.sh && echo \"\${prompts[{}]}\"" \
    --preview-window=right:60%:wrap \
    $theme_colors)

[[ -z "$template" ]] && exit 0

# Get query input
query=$(echo "" | fzf \
    --prompt="❯ $template: " \
    --print-query \
    --height=40% \
    --border=rounded \
    --margin=2% \
    --padding=1% \
    --info=inline \
    --layout=reverse \
    --pointer='▶' \
    --marker='✓' \
    --bind='ctrl-c:abort' \
    --bind='esc:abort' \
    $theme_colors | tail -1)

[[ -z "$query" ]] && exit 0

# Process and copy
result="${prompts[$template]//\{\{QUERY\}\}/$query}"
echo "$result" | wl-copy

# Theme-appropriate notification
case $THEME in
    catppuccin) icon="🌸" ;;
    dracula) icon="🧛" ;;
    nord) icon="❄️" ;;
    gruvbox) icon="🍂" ;;
    tokyo) icon="🌃" ;;
    onedark) icon="🌑" ;;
    *) icon="✓" ;;
esac

notify-send -t 2000 "$icon Applied" "$template"
