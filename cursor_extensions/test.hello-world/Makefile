# Makefile for Hello World Cursor Extension

# Build all TypeScript files to JS
.PHONY: build
build:
	npx tsc --strict --esModuleInterop --outDir out

# Setup (alias for build)
.PHONY: setup
setup: build

# Run the standalone Pandoc test (depends on build)
.PHONY: test
test: build
	node out/test_pandoc.js

# Package the extension and install it in Cursor
# Always remove the old extension from ~/.cursor/extensions before installing to avoid caching issues
.PHONY: deploy
deploy:
	rm -rf ~/.cursor/extensions/test.hello-world-0.0.1
	npx --yes vsce package
	cursor --install-extension hello-world-0.0.1.vsix

# Remove build artifacts and logs
.PHONY: clean
clean:
	rm -f hello-world-0.0.1.vsix out/pandoc_debug.log

# Usage:
#   make build  # Compile all TypeScript files
#   make setup  # Alias for build
#   make test   # Build and run Pandoc test
#   make deploy # Remove old extension, package, and install in Cursor
#   make clean  # Remove build artifacts and logs 