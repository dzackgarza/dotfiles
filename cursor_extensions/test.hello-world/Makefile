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
test: clean build test-stripmacros
	# Run all tests (currently only Pandoc HTML/CSS test)
	npx ts-node test_pandoc.ts

# Run the test that saves the webview HTML output
.PHONY: test-webview-html
test-webview-html: build
	npx ts-node test_pandoc.ts

# Package the extension and install it in Cursor
# Always remove the old extension from ~/.cursor/extensions before installing to avoid caching issues
.PHONY: deploy
deploy: clean build
	rm -rf ~/.cursor/extensions/test.hello-world-0.0.1
	npx --yes vsce package
	cursor --install-extension hello-world-0.0.1.vsix

# Remove build artifacts and logs
.PHONY: clean
clean:
	rm -f hello-world-0.0.1.vsix out/pandoc_debug.log
	rm -rf out/
	rm -f *.log
	rm -f *.testoutput
	rm -f ../webview_test_output.*
	rm -f ../test_pandoc_direct.html
	rm -f *.html

# Remove all build artifacts, logs, and test outputs
.PHONY: clean-all
clean-all:
	rm -f hello-world-0.0.1.vsix out/pandoc_debug.log
	rm -rf out/
	rm -f *.log
	rm -f *.testoutput
	rm -f ../webview_test_output.*
	rm -f ../test_custom_pandoc.html
	rm -f ../test_custom_pandoc.js
	rm -f ../test_custom_pandoc.js.map
	rm -f ../test.hello-world/*.js ../test.hello-world/*.js.map

# Usage:
#   make build  # Compile all TypeScript files
#   make setup  # Alias for build
#   make test   # Build and run Pandoc test
#   make test-webview-html # Build, run test, and save webview HTML output
#   make deploy # Remove old extension, package, and install in Cursor
#   make clean  # Remove build artifacts and logs 
#   make clean-all  # Remove all build artifacts, logs, and test outputs 

.PHONY: test-stripmacros
test-stripmacros: build
	npx ts-node test_stripmacros.ts 