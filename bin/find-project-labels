#!/bin/bash

set -euo pipefail

GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo ".")
WRITING_DIR="$GIT_ROOT/writing"

# Get current file from vim/coc context or current directory
CURRENT_FILE="${1:-$PWD}"
if [[ -f "$CURRENT_FILE" ]]; then
    CURRENT_DIR=$(dirname "$CURRENT_FILE")
else
    CURRENT_DIR="$CURRENT_FILE"
fi

# Function to process a batch of files and extract academic labels
process_batch() {
    if [[ $# -eq 0 ]]; then return; fi
    cat "$@" 2>/dev/null | pandoc -f markdown -t json 2>/dev/null | \
    jq -r --unbuffered '
        def extract_divs:
            if type == "object" then
                if .t == "Div" then
                    .c[0] as $attrs |
                    if ($attrs | length) >= 2 and $attrs[0] != "" and ($attrs[1] | length) > 0 then
                        "#" + $attrs[0]
                    else
                        empty
                    end
                else
                    .[] | if type == "object" or type == "array" then extract_divs else empty end
                end
            elif type == "array" then
                .[] | if type == "object" or type == "array" then extract_divs else empty end
            else
                empty
            end;
        
        extract_divs
    '
}

# Priority 1: Current file - most likely references
if [[ -f "$CURRENT_FILE" && "$CURRENT_FILE" == *.md ]]; then
    process_batch "$CURRENT_FILE"
fi

# Priority 2: Same directory - local chapter/section
if [[ -d "$CURRENT_DIR" ]]; then
    mapfile -t SAME_DIR < <(find "$CURRENT_DIR" -maxdepth 1 -name "*.md" -type f ! -path "$CURRENT_FILE" 2>/dev/null)
    if [[ ${#SAME_DIR[@]} -gt 0 ]]; then
        process_batch "${SAME_DIR[@]}"
    fi
fi

# Priority 3: Parent/sibling directories - related topics
PARENT_DIR=$(dirname "$CURRENT_DIR")
if [[ -d "$PARENT_DIR" && "$PARENT_DIR" != "$CURRENT_DIR" ]]; then
    mapfile -t NEARBY < <(find "$PARENT_DIR" -maxdepth 2 -name "*.md" -type f ! -path "$CURRENT_DIR/*" ! -path "$CURRENT_FILE" 2>/dev/null)
    if [[ ${#NEARBY[@]} -gt 0 ]]; then
        process_batch "${NEARBY[@]}"
    fi
fi

# Priority 4: Complete project corpus (background processing)
{
    if [[ -d "$WRITING_DIR" ]]; then
        mapfile -t ALL_FILES < <(find "$WRITING_DIR" -name "*.md" -type f 2>/dev/null)
        REMAINING=()
        
        for file in "${ALL_FILES[@]}"; do
            # Skip already processed files
            if [[ "$file" == "$CURRENT_FILE" ]]; then continue; fi
            if [[ "$file" == "$CURRENT_DIR"/* ]]; then continue; fi
            if [[ "$file" == "$PARENT_DIR"/* ]] && [[ $(dirname "$file") != "$CURRENT_DIR" ]]; then continue; fi
            REMAINING+=("$file")
        done
        
        if [[ ${#REMAINING[@]} -gt 0 ]]; then
            process_batch "${REMAINING[@]}"
        fi
    fi
} &
