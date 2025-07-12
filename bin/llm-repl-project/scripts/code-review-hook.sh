#!/bin/bash
# Code Review Hook for Claude Code
# Provides automated code analysis and review feedback for modified files

# Get modified files from environment variable set by Claude Code
FILES="${CLAUDE_FILE_PATHS:-}"

if [ -z "$FILES" ]; then
    echo "No files to review"
    exit 0
fi

# Project root detection
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🔍 Running automated code review..."

# Track if any significant issues found
ISSUES_FOUND=false
REVIEW_OUTPUT=""

# Review each file
for file in $FILES; do
    # Skip if file doesn't exist
    if [ ! -f "$file" ]; then
        continue
    fi
    
    echo "📄 Reviewing: $(basename "$file")"
    
    # Determine file type and run appropriate analysis
    case "$file" in
        *.py)
            # Python file analysis
            echo "  🐍 Python analysis..."
            
            # Use our comprehensive tool matrix for Python files
            PYTHON_REVIEW=$("$PROJECT_ROOT/V3-minimal/dev-scripts/tool-integration-matrix.py" "$file" --json 2>/dev/null)
            
            if [ $? -eq 0 ] && [ -n "$PYTHON_REVIEW" ]; then
                # Parse results and check for issues
                ERROR_COUNT=$(echo "$PYTHON_REVIEW" | jq -r '.tools.static_analysis.pylint.data.issues // [] | map(select(.type == "error")) | length' 2>/dev/null || echo "0")
                WARNING_COUNT=$(echo "$PYTHON_REVIEW" | jq -r '.tools.static_analysis.pylint.data.issues // [] | map(select(.type == "warning")) | length' 2>/dev/null || echo "0")
                COMPLEXITY=$(echo "$PYTHON_REVIEW" | jq -r '.tools.metrics.radon.data.complexity // {} | to_entries | map(select(.value[0].complexity > 10)) | length' 2>/dev/null || echo "0")
                SECURITY_ISSUES=$(echo "$PYTHON_REVIEW" | jq -r '.tools.security.bandit.data.results // [] | length' 2>/dev/null || echo "0")
                
                if [ "$ERROR_COUNT" -gt 0 ] || [ "$WARNING_COUNT" -gt 5 ] || [ "$COMPLEXITY" -gt 0 ] || [ "$SECURITY_ISSUES" -gt 0 ]; then
                    ISSUES_FOUND=true
                    REVIEW_OUTPUT+="\n⚠️  $(basename "$file"): $ERROR_COUNT errors, $WARNING_COUNT warnings"
                    if [ "$COMPLEXITY" -gt 0 ]; then
                        REVIEW_OUTPUT+=", high complexity detected"
                    fi
                    if [ "$SECURITY_ISSUES" -gt 0 ]; then
                        REVIEW_OUTPUT+=", $SECURITY_ISSUES security issues"
                    fi
                else
                    REVIEW_OUTPUT+="\n✅ $(basename "$file"): Clean (no significant issues)"
                fi
            else
                REVIEW_OUTPUT+="\n🔧 $(basename "$file"): Analysis failed, manual review recommended"
            fi
            ;;
            
        *.css|*.tcss)
            # CSS/TCSS file analysis
            echo "  🎨 CSS/TCSS analysis..."
            
            # Use our custom CSS analysis tool
            CSS_REVIEW=$("$PROJECT_ROOT/V3-minimal/dev-scripts/css-analysis-tool.py" "$file" --json --severity warning 2>/dev/null)
            
            if [ $? -eq 0 ] && [ -n "$CSS_REVIEW" ]; then
                # Parse CSS analysis results
                ISSUE_COUNT=$(echo "$CSS_REVIEW" | jq -r '.[0].summary.total_issues // 0' 2>/dev/null || echo "0")
                ERROR_COUNT=$(echo "$CSS_REVIEW" | jq -r '.[0].summary.error_count // 0' 2>/dev/null || echo "0")
                COMPLEXITY_SCORE=$(echo "$CSS_REVIEW" | jq -r '.[0].summary.complexity_score // 0' 2>/dev/null || echo "0")
                
                if [ "$ERROR_COUNT" -gt 0 ] || [ "$ISSUE_COUNT" -gt 3 ] || [ "$COMPLEXITY_SCORE" -gt 100 ]; then
                    ISSUES_FOUND=true
                    REVIEW_OUTPUT+="\n⚠️  $(basename "$file"): $ISSUE_COUNT issues ($ERROR_COUNT errors)"
                    if [ "$COMPLEXITY_SCORE" -gt 100 ]; then
                        REVIEW_OUTPUT+=", complexity: $COMPLEXITY_SCORE"
                    fi
                else
                    REVIEW_OUTPUT+="\n✅ $(basename "$file"): Clean CSS/TCSS"
                fi
            else
                REVIEW_OUTPUT+="\n🔧 $(basename "$file"): CSS analysis failed, manual review recommended"
            fi
            ;;
            
        *.js|*.ts)
            # JavaScript/TypeScript (basic check)
            echo "  📜 JavaScript/TypeScript analysis..."
            
            # Basic syntax check
            if command -v node >/dev/null 2>&1; then
                if node -c "$file" 2>/dev/null; then
                    REVIEW_OUTPUT+="\n✅ $(basename "$file"): Syntax valid"
                else
                    ISSUES_FOUND=true
                    REVIEW_OUTPUT+="\n❌ $(basename "$file"): Syntax errors detected"
                fi
            else
                REVIEW_OUTPUT+="\n🔧 $(basename "$file"): Node.js not available for syntax check"
            fi
            ;;
            
        *.json)
            # JSON validation
            echo "  📋 JSON validation..."
            
            if python -m json.tool "$file" >/dev/null 2>&1; then
                REVIEW_OUTPUT+="\n✅ $(basename "$file"): Valid JSON"
            else
                ISSUES_FOUND=true
                REVIEW_OUTPUT+="\n❌ $(basename "$file"): Invalid JSON format"
            fi
            ;;
            
        *.yml|*.yaml)
            # YAML validation
            echo "  📋 YAML validation..."
            
            if python -c "import yaml; yaml.safe_load(open('$file'))" 2>/dev/null; then
                REVIEW_OUTPUT+="\n✅ $(basename "$file"): Valid YAML"
            else
                ISSUES_FOUND=true
                REVIEW_OUTPUT+="\n❌ $(basename "$file"): Invalid YAML format"
            fi
            ;;
            
        *.md)
            # Markdown basic check
            echo "  📝 Markdown analysis..."
            
            # Check for common markdown issues
            if grep -q "^\s*#\{7,\}" "$file"; then
                ISSUES_FOUND=true
                REVIEW_OUTPUT+="\n⚠️  $(basename "$file"): Headers deeper than H6 detected"
            elif grep -q "\[.*\](" "$file" && ! grep -q "\[.*\](http" "$file"; then
                REVIEW_OUTPUT+="\n✅ $(basename "$file"): Well-formed markdown"
            else
                REVIEW_OUTPUT+="\n✅ $(basename "$file"): Markdown format OK"
            fi
            ;;
            
        *)
            # Unknown file type
            echo "  📄 File type not recognized for automated review"
            REVIEW_OUTPUT+="\n📄 $(basename "$file"): Manual review recommended (unknown type)"
            ;;
    esac
done

# Output summary
echo ""
echo "📊 Code Review Summary:"
echo -e "$REVIEW_OUTPUT"

# Check if we should recommend enhanced review
if [ "$ISSUES_FOUND" = true ]; then
    echo ""
    echo "🔍 Issues detected. Consider running enhanced analysis:"
    echo "   Python files: pdm run python dev-scripts/groq-code-review-enhanced.py <file>"
    echo "   CSS files: pdm run python dev-scripts/css-analysis-tool.py <file>"
    echo "   Run 'just test' for comprehensive validation"
fi

echo ""
echo "✅ Automated code review complete"

# Exit with a warning code if issues were found
if [ "$ISSUES_FOUND" = true ]; then
    exit 1
else
    exit 0
fi