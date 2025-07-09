#!/usr/bin/env zsh

# Static test for fzf deep navigation
# This test verifies the filtering and display logic without requiring ZLE

# Create a test environment
setup_test_environment() {
  # Create a temporary directory for testing
  TEST_DIR="$(mktemp -d)"
  
  # Create sample directory structure
  mkdir -p "$TEST_DIR/home/dzack/{dotfiles,diss,documents,downloads}"
  touch "$TEST_DIR/home/dzack/dissertation.pdf"
  
  # Create test files in dotfiles directory
  mkdir -p "$TEST_DIR/home/dzack/dotfiles"
  touch "$TEST_DIR/home/dzack/dotfiles/"{config,zsh,vim}
  
  # Create a test fzf_input.txt with scores
  # Using relative paths from the test home directory
  cat > "$TEST_DIR/fzf_input.txt" << 'EOF'
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

  # Create expected output for testing
  cat > "$TEST_DIR/expected_home.txt" << 'EOF'
1000 dotfiles/config
999 dotfiles/zsh
998 dotfiles/vim
997 documents/work
996 documents/personal
995 dissertation.pdf
994 diss/chapter1
993 diss/chapter2
992 downloads/archives
991 downloads/temp
EOF

  echo "Test environment created at: $TEST_DIR"
}

# Test the filtering logic
test_filtering() {
  local current_dir="$1"
  local test_name="$2"
  local expected_count=$3
  local search_term="$4"
  
  echo "\n🔹 Testing $test_name"
  # Get the relative path from home
  local rel_path="${current_dir#$HOME/}"
  
  # Run the filter logic
  local output
  output=$(cat "$TEST_DIR/fzf_input.txt" | \
    awk -v current="$rel_path" -v search="$search_term" '
      BEGIN {FS="\t"; found=0} 
      {
        # If we have a current path, only show subdirectories
        if (current != "" && $2 !~ "^" current "/") next
        
        # Remove the current directory prefix if it exists
        if (current != "") sub("^" current "/?", "", $2)
        
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
    echo "❌ No results found for search term: $search_term"
    return 1
  fi
  
  echo "📋 Filtered results:"
  echo "$output" | sort -nr | head -n 5
  
  # Verify the search results when a search term is provided
  if [ -n "$search_term" ]; then
    local matched=0
    local first_result=$(echo "$output" | sort -nr | head -n 1 | cut -d' ' -f2-)
    
    # Check if any result contains the search term
    while IFS= read -r line; do
      local path_part=$(echo "$line" | cut -d' ' -f2-)
      if [[ "${path_part:0:${#search_term}}" == "$search_term" ]]; then
        matched=1
        first_result="$path_part"
        break
      fi
    done <<< "$output"
    
    if [ $matched -eq 0 ]; then
      echo "❌ No results found matching search term: $search_term"
      return 1
    fi
    
    echo "✅ Found matching result: $first_result"
  fi
  
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

# Main test execution
main() {
  # Set up test environment
  setup_test_environment
  
  # Set the HOME directory to our test directory
  local OLD_HOME="$HOME"
  export HOME="$TEST_DIR/home/dzack"
  
  # Change to the test home directory
  mkdir -p "$HOME"
  cd "$HOME" || { echo "Failed to change to test directory"; return 1 }
  
  # Test cases
  echo "\n🔍 Running tests..."
  
  # Test 1: Basic filtering from home directory - expect 5 results (only directories with subdirectories)
  test_filtering "$HOME" "Basic filtering from home" 5 "" || return 1
  
  # Test 2: Search for 'dis' should match 'diss' entries
  test_filtering "$HOME" "Search for 'dis'" "" "diss" || return 1
  
  # Test 3: Search for 'doc' should match 'documents' entries
  test_filtering "$HOME" "Search for 'doc'" "" "docu" || return 1
  
  # Test 4: Filter from dotfiles directory - expect 0 results (no subdirectories in our test data)
  test_filtering "$HOME/dotfiles" "Filter from dotfiles" 0 "" || return 1
  
  # Test 5: Search for 'zsh' in dotfiles
  test_filtering "$HOME/dotfiles" "Search for 'zsh'" "" "zsh" || return 1
  
  # Restore HOME
  export HOME="$OLD_HOME"
  
  echo "\n🎉 All tests passed!"
  echo "Test directory: $TEST_DIR"
  echo "You can inspect the test files there."
}

# Run the tests
main "$@"
