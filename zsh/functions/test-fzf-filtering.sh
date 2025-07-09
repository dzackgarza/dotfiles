#!/bin/zsh

# Simple test script for fzf filtering logic

test_filtering() {
  local test_name="$1"
  local current_dir="$2"
  local search_term="$3"
  local expected_count="$4"
  
  echo "\n🔹 Testing $test_name"
  echo "Current dir: $current_dir"
  echo "Search term: $search_term"
  
  # Create a test input file with paths relative to home
  cat > /tmp/test_input.txt << 'EOF'
1000	dotfiles/config
999	dotfiles/zsh
998	dotfiles/vim
997	documents/work
996	documents/personal
995	dissertation.pdf
994	diss/chapter1
993	diss/chapter2
992	downloads/archives
991	downloads/temp
EOF

  # Run the filter logic
  local output
  output=$(cat /tmp/test_input.txt | \
    awk -v current="$current_dir" -v search="$search_term" '
      BEGIN {FS="\t"; found=0} 
      {
        # If we have a current path, only show subdirectories
        if (current != "" && $2 !~ "^" current "") next
        
        # Remove the current directory prefix if it exists
        if (current != "") {
          sub("^" current "/*", "", $2)
          # Skip if we're not at the right level
          if (current != "" && $2 ~ "/") next
        }
        
        # If we have a search term, check for a match
        if (search != "") {
          if (tolower($2) !~ tolower(search)) next
        }
        # Otherwise, only show paths with subdirectories
        else if ($2 !~ "/") next
        
        # Print: score and display path
        print $1 " " $2
        found=1
      }
      END {exit !found}'
  )
  
  local exit_status=$?
  
  if [ $exit_status -ne 0 ]; then
    echo "❌ No results found"
    return 1
  fi
  
  echo "📋 Filtered results:"
  echo "$output"
  
  # Verify expected count if provided
  if [ -n "$expected_count" ]; then
    local result_count=$(echo "$output" | wc -l)
    if [ "$result_count" -ne "$expected_count" ]; then
      echo "❌ Unexpected number of results"
      echo "   Expected: $expected_count"
      echo "   Got: $result_count"
      return 1
    fi
    echo "✅ Found expected number of results ($result_count)"
  fi
  
  return 0
}

# Test cases
echo "Starting tests..."

# Test 1: Basic filtering from home - should show all entries with subdirectories
# (dotfiles/*, documents/*, diss/*, downloads/*, and dissertation.pdf)
test_filtering "Basic filtering from home" "" "" 9 || exit 1

# Test 2: Search for 'diss' - should match 'diss' entries and 'dissertation.pdf'
test_filtering "Search for 'diss'" "" "diss" 3 || exit 1

# Test 3: Filter from documents - should show work and personal directories
test_filtering "Filter from documents" "documents" "" 2 || exit 1

# Test 4: Filter from dotfiles - should show config, zsh, vim
test_filtering "Filter from dotfiles" "dotfiles" "" 3 || exit 1

echo "\n🎉 All tests passed!"
rm -f /tmp/test_input.txt
