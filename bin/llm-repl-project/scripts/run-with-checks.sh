#!/bin/bash
# /home/dzack/dotfiles/bin/llm-repl-project/scripts/run-with-checks.sh

# This script acts as a gatekeeper, running pre-flight checks
# before executing the main command.

# Run the acceptance test hook first.
/home/dzack/dotfiles/bin/llm-repl-project/scripts/acceptance-test-hook.sh
ACCEPTANCE_STATUS=$?

if [ $ACCEPTANCE_STATUS -ne 0 ]; then
  # The acceptance test hook will have already printed an error.
  # We exit with its status code to halt execution.
  exit $ACCEPTANCE_STATUS
fi

# If the checks pass, execute the command that was passed to this script.
exec "$@"
