# Makefile for Hello World Cursor Extension

# Run the standalone Pandoc test
.PHONY: test
test:
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
#   make test   # Run Pandoc test
#   make deploy # Remove old extension, package, and install in Cursor
#   make clean  # Remove build artifacts and logs 