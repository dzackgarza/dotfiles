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
test: clean build
	@echo "\033[1;34m[TEST] Showing first 500 chars of input file:\033[0m"
	@if [ ! -f $(shell yq '.pandoc.test_inputs.test_custom_pandoc' pandoc_global.yaml) ]; then \
	  echo "\033[1;31m[ERROR] Input file $(shell yq '.pandoc.test_inputs.test_custom_pandoc' pandoc_global.yaml) does not exist!\033[0m"; exit 1; \
	fi
	@head -c 500 $(shell yq '.pandoc.test_inputs.test_custom_pandoc' pandoc_global.yaml)
	@echo "\n\033[1;34m[TEST] Running stripmacros and showing first 500 chars of output:\033[0m"
	@/home/dzack/.pandoc/bin/pandoc_stripmacros.sh < $(shell yq '.pandoc.test_inputs.test_custom_pandoc' pandoc_global.yaml) > $(shell yq '.pandoc.test_outputs.stripmacros_test_output' pandoc_global.yaml) || { echo "\033[1;31m[ERROR] stripmacros command failed!\033[0m"; exit 1; }
	@if [ ! -f $(shell yq '.pandoc.test_outputs.stripmacros_test_output' pandoc_global.yaml) ]; then \
	  echo "\033[1;31m[ERROR] Output file $(shell yq '.pandoc.test_outputs.stripmacros_test_output' pandoc_global.yaml) does not exist!\033[0m"; exit 1; \
	fi
	@head -c 500 $(shell yq '.pandoc.test_outputs.stripmacros_test_output' pandoc_global.yaml)
	@echo "\033[1;32m[TEST] stripmacros test completed successfully.\033[0m"

# Run the test that saves the webview HTML output
.PHONY: test-webview-html
test-webview-html: build
	npx ts-node test/test_pandoc.ts
	@for f in test/outputs/*.html; do \
	  if [ -f "$$f" ]; then \
	    echo "Opening $$f"; \
	    xdg-open "$$f"; \
	  fi; \
	done

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
	rm -f ../webview_test_output.final.html
	rm -f ../test_pandoc_direct.html
	rm -f webview_test_output.final.html
	rm -f test_pandoc.js test_pandoc.js.map test_pandoc_error_isolation.js test_pandoc_error_isolation.js.map pandocUtil.js pandocUtil.js.map conversionPipeline.js conversionPipeline.js.map minimal_pandoc_test.js minimal_pandoc_test.js.map test_stripmacros.js test_stripmacros.js.map extension.js extension.js.map
	rm -f ../test_custom_pandoc.js ../test_custom_pandoc.js.map ../test.hello-world/*.js ../test.hello-world/*.js.map
	rm -f test/outputs/*

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

.PHONY: test-macros
# Test macro stripping and Pandoc conversion
# 1. Print first 500 chars of input
# 2. Run stripmacros
# 3. Print first 500 non-blank chars of output
# 4. Lint stripped markdown
# 5. Run Pandoc to HTML
# 6. Print first 500 chars of HTML
# 7. Fail loudly on error

test-macros:
	@echo "\033[1;34m[TEST] Showing first 500 chars of test_custom_pandoc.md:\033[0m"
	@if [ ! -f $(shell yq '.pandoc.test_inputs.test_custom_pandoc' pandoc_global.yaml) ]; then \
	  echo "\033[1;31m[ERROR] Input file $(shell yq '.pandoc.test_inputs.test_custom_pandoc' pandoc_global.yaml) does not exist!\033[0m"; exit 1; \
	fi
	@head -c 500 $(shell yq '.pandoc.test_inputs.test_custom_pandoc' pandoc_global.yaml)
	@echo "\n\033[1;34m[TEST] Running stripmacros...\033[0m"
	@cat $(shell yq '.pandoc.test_inputs.test_custom_pandoc' pandoc_global.yaml) | /home/dzack/.pandoc/bin/pandoc_stripmacros.sh > $(shell yq '.pandoc.test_inputs.test_custom_pandoc_stripped' pandoc_global.yaml) || { echo "\033[1;31m[ERROR] stripmacros command failed!\033[0m"; exit 1; }
	@if [ ! -f $(shell yq '.pandoc.test_inputs.test_custom_pandoc_stripped' pandoc_global.yaml) ]; then \
	  echo "\033[1;31m[ERROR] Output file $(shell yq '.pandoc.test_inputs.test_custom_pandoc_stripped' pandoc_global.yaml) does not exist!\033[0m"; exit 1; \
	fi
	@echo "\033[1;34m[TEST] Showing first 500 non-blank chars of stripped markdown:\033[0m"
	@awk 'NF' $(shell yq '.pandoc.test_inputs.test_custom_pandoc_stripped' pandoc_global.yaml) | head -c 500
	@echo "\n\033[1;34m[TEST] Linting stripped markdown...\033[0m"
	@echo "[LINT] Checking stripped markdown for validity..."
	markdownlint -c .markdownlint.json $(shell yq '.pandoc.test_inputs.test_custom_pandoc_stripped' pandoc_global.yaml) || (echo "\033[1;31m[ERROR] Markdown linter failed!\033[0m" && exit 1)
	@echo "\033[1;32m[TEST] Markdown linter passed.\033[0m"
	@echo "\n\033[1;34m[TEST] Running Pandoc to HTML...\033[0m"
	@$(PANDOC_PATH) --from=$(PANDOC_FROM) --to=$(PANDOC_TO) --template=$(PANDOC_TEMPLATE) $(PANDOC_ARGS) < $(shell yq '.pandoc.test_inputs.test_custom_pandoc_stripped' pandoc_global.yaml) > $(shell yq '.pandoc.test_outputs.test_custom_pandoc_html' pandoc_global.yaml) || { echo "\033[1;31m[ERROR] Pandoc command failed!\033[0m"; exit 1; }
	@if [ ! -f $(shell yq '.pandoc.test_outputs.test_custom_pandoc_html' pandoc_global.yaml) ]; then \
	  echo "\033[1;31m[ERROR] Output file $(shell yq '.pandoc.test_outputs.test_custom_pandoc_html' pandoc_global.yaml) does not exist!\033[0m"; exit 1; \
	fi
	@echo "\033[1;34m[TEST] Showing first 500 chars of output HTML:\033[0m"
	@head -c 500 $(shell yq '.pandoc.test_outputs.test_custom_pandoc_html' pandoc_global.yaml)
	@echo "\033[1;32m[TEST] Macro + Pandoc test completed successfully.\033[0m" 

.PHONY: help
help:
	@echo "Available make targets:" && \
	awk -F: '/^[a-zA-Z0-9][^$#\t=]*:/ {print "  - " $$1}' Makefile | sort | uniq

.PHONY: all
all: clean build test test-webview-html

.DEFAULT_GOAL := all

# Helper to extract Pandoc command from YAML
PANDOC_PATH := $(shell yq '.pandoc.path' pandoc_global.yaml)
PANDOC_FROM := $(shell yq '.pandoc.from' pandoc_global.yaml)
PANDOC_TO := $(shell yq '.pandoc.to' pandoc_global.yaml)
PANDOC_ARGS := $(shell yq '.pandoc.args[]' pandoc_global.yaml)
PANDOC_TEMPLATE := $(shell yq '.pandoc.template' pandoc_global.yaml) 