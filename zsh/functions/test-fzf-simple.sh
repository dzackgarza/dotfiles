#!/bin/zsh

# Simple test script for fzf filtering logic

test_filtering() {
  local test_name="$1"
  local current_dir="$2"
  local search_term="$3"
  
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

  # Print the test input for debugging
  echo "Test input:"
  cat /tmp/test_input.txt | sort -nr
  
  # Run the filter logic
  echo "\nFiltering results:"
  awk -v current="$current_dir" -v search="$search_term" '
    BEGIN {FS="\t"} 
    {
      # If we have a current directory, only show subdirectories
      if (current != "" && $2 !~ "^" current "/") next
      
      # Remove the current directory prefix if it exists
      if (current != "") sub("^" current "/*", "", $2)
      
      # If we have a search term, check for a match
      if (search != "" && tolower($2) !~ tolower(search)) next
      
      # Print: score and display path
      print "  " $1 " " $2
    }' /tmp/test_input.txt | sort -nr
}

# Test cases
echo "Starting fzf filtering tests..."

# Test 1: Show all entries
echo "\n📋 Test 1: Show all entries"
test_filtering "Show all entries" "" ""

# Test 2: Search for 'dis'
echo "\n📋 Test 2: Search for 'dis'"
test_filtering "Search for 'dis'" "" "dis"

# Test 3: Filter from documents
echo "\n📋 Test 3: Filter from 'documents'"
test_filtering "Filter from documents" "documents" ""

# Cleanup
rm -f /tmp/test_input.txt
echo "\n✅ Tests completed"
