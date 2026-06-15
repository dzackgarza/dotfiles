# dotfiles repository tasks
#
# `test` is invoked by the global pre-commit / pre-push hook
# (core.hooksPath -> ~/.config/git/hooks -> ai-review-ci/global-hooks),
# which runs `just test` for every repo. It must exit 0 for a healthy repo.

# Validate repository integrity: all declared submodules must be initialized.
test:
    #!/usr/bin/env bash
    set -euo pipefail
    cd "{{justfile_directory()}}"
    if git submodule status --recursive 2>/dev/null | grep -q '^-'; then
        echo "Error: uninitialized submodule(s) — run 'git submodule update --init --recursive':" >&2
        git submodule status --recursive | grep '^-' >&2
        exit 1
    fi
    echo "dotfiles: submodules OK"
