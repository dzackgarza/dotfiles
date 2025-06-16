#!/usr/bin/env bash
# filter_zsh_history.sh
# Remove multiline commands from zsh history file, keep only single-line commands.

set -euo pipefail

# Input and output files can be passed as arguments, or default to ~/.zsh_history and ~/.zsh_history_clean
INPUT_FILE="${1:-$HOME/.zsh_history}"
OUTPUT_FILE="${2:-$HOME/.zsh_history_clean}"

awk '
  /^: / {
    if (block) {
      if (block_lines == 1) print block;
      block = $0; block_lines = 1;
    } else {
      block = $0; block_lines = 1;
    }
    next;
  }
  /^[ \t]+\\/ {
    block = block "\n" $0;
    block_lines++;
    next;
  }
  {
    block = block "\n" $0;
    block_lines++;
  }
  END {
    if (block_lines == 1) print block;
  }
' "$INPUT_FILE" > "$OUTPUT_FILE"

