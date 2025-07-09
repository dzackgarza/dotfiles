#!/usr/bin/env zsh

# Test script for fzf deep navigation functionality
# This script tests the _fzf_cd_subdir and _fzf_insert_subdir functions

# Source the functions
source "${0:a:h}/fzf-z-jump.zsh"

# Create a temporary test file with sample data
create_test_file() {
  cat << 'EOF' > /tmp/test_fzf_input.txt
995	/home
989	/home/dzack
983	/home/dzack/notes
981	/home/dzack/Dropbox
980	/home/dzack/dotfiles
975	/home/dzack/Downloads
970	/home/dzack/Documents
965	/home/dzack/Pictures
960	/home/dzack/Music
955	/home/dzack/Videos
EOF
  echo "Created test file with sample data"
  echo "---------------------------------"
  cat /tmp/test_fzf_input.txt | column -t -s $'\t'
  echo "---------------------------------"
}

# Mock the fzf command to select specific lines
mock_fzf() {
  local expected_selection="$1"
  shift  # Remove the first argument
  
  # Simulate fzf with the expected selection
  echo "$expected_selection"
}

# Test _fzf_cd_subdir with mock fzf
test_cd_subdir() {
  echo "\n🔹 Testing _fzf_cd_subdir"
  echo "----------------------"
  
  # Mock the fzf command
  alias fzf="mock_fzf '/home/dzack/dotfiles'"
  
  # Test the function
  echo "Expected selection: /home/dzack/dotfiles"
  _fzf_cd_subdir
  
  # Verify the current directory changed
  echo "Current directory: $(pwd)"
  
  # Clean up
  unalias fzf
}

# Test _fzf_insert_subdir with mock fdfind
test_insert_subdir() {
  echo "\n🔹 Testing _fzf_insert_subdir"
  echo "--------------------------"
  
  # Mock the fzf command
  alias fzf="mock_fzf '/home/dzack/notes'"
  
  # Test the function
  LBUFFER=""
  _fzf_insert_subdir
  
  # Verify the directory was inserted
  echo "LBUFFER after insertion: '$LBUFFER'"
  
  # Clean up
  unalias fzf
}

# Main test execution
main() {
  # Save the original fzf_input.txt path
  local original_fzf_input="$HOME/fzf_input.txt"
  
  # Create and use a test file
  create_test_file
  
  # Set up the test environment
  export FZF_DEFAULT_OPTS="--no-height --no-reverse"
  
  # Run the tests
  test_cd_subdir
  test_insert_subdir
  
  # Restore the original fzf_input.txt path
  echo "\n✅ Tests completed"
  echo "Note: These tests use mocked fzf output. For interactive testing:"
  echo "1. Press Ctrl+T to test directory navigation"
  echo "2. Press Ctrl+Shift+T to test directory insertion"
}

# Run the tests
main "$@"
