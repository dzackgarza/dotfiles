#!/usr/bin/python3
"""
Enhanced Groq Code Review Tool
Context-aware AI code reviews using gathered contextual information
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv
from datetime import datetime
import tiktoken


class EnhancedGroqCodeReviewer:
    """Enhanced code reviewer with contextual awareness"""

    BASE_URL = "https://api.groq.com/openai/v1"

    # Updated model preferences for July 2025
    PREFERRED_MODELS = [
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "mixtral-8x7b-32768",
        "llama-3.1-8b-instant",
        "llama3-70b-8192",
        "gemma2-9b-it",
    ]

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        # Initialize tokenizer for token counting
        try:
            self.tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")  # Close approximation for most models
        except (KeyError, ValueError) as e:
            print(f"Warning: Could not load model-specific tokenizer ({e}), using fallback")
            self.tokenizer = tiktoken.get_encoding("cl100k_base")  # Fallback
        except Exception as e:
            print(f"Error: Failed to initialize tokenizer ({e}), token counting may be inaccurate")
            self.tokenizer = tiktoken.get_encoding("cl100k_base")  # Fallback

    def get_available_models(self) -> List[Dict]:
        """Fetch list of available models from Groq API"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/models",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json().get("data", [])
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []

    def select_best_model(self, available_models: List[Dict]) -> Optional[str]:
        """Select the best model based on availability and preferences"""
        available_ids = {model["id"] for model in available_models}

        for preferred in self.PREFERRED_MODELS:
            if preferred in available_ids:
                return preferred

        # Fallback
        for model in available_models:
            model_id = model["id"].lower()
            if "llama" in model_id or "mixtral" in model_id:
                return model["id"]

        return available_models[0]["id"] if available_models else None

    def count_tokens(self, text: str) -> int:
        """Count tokens in text using tiktoken"""
        try:
            return len(self.tokenizer.encode(text))
        except (UnicodeDecodeError, UnicodeEncodeError) as e:
            print(f"Warning: Text encoding issue during token counting ({e}), using fallback")
            # Fallback: rough estimate of 4 chars per token
            return len(text) // 4
        except Exception as e:
            print(f"Error: Tokenizer failed ({e}), using fallback estimate")
            # Fallback: rough estimate of 4 chars per token
            return len(text) // 4

    def gather_context(self, file_path: Path) -> Dict:
        """Gather contextual information about the file"""
        try:
            # Use our context gatherer script (in same directory as this script)
            script_dir = Path(__file__).parent
            script_path = script_dir / "gather-code-context.py"
            result = subprocess.run(
                [sys.executable, str(script_path), str(file_path), "--json"],
                capture_output=True,
                text=True,
                check=True
            )
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Warning: Could not gather context: {e}")
            return {}

    def format_context_for_ai(self, context: Dict, file_content: str, file_path: Path) -> str:
        """Format context information for AI consumption"""
        if not context:
            return f"File: {file_path.name}\n```{file_path.suffix[1:] if file_path.suffix else 'text'}\n{file_content}\n```"

        formatted = f"""# Context-Aware Code Review Request

## File Information
- **File**: {file_path.name}
- **Path**: {context.get('file_info', {}).get('path', 'Unknown')}
- **Size**: {context.get('file_info', {}).get('lines_of_code', 0)} lines
- **Last Modified**: {context.get('file_info', {}).get('last_modified', 'Unknown')}

## Project Context
"""

        # Project context
        proj_ctx = context.get('project_context', {})
        if proj_ctx:
            framework = proj_ctx.get('framework')
            if framework:
                formatted += f"- **Framework**: {framework}\n"
            proj_type = proj_ctx.get('project_type')
            if proj_type:
                formatted += f"- **Project Type**: {proj_type}\n"
            config_files = proj_ctx.get('config_files', [])
            if config_files:
                formatted += f"- **Config Files**: {', '.join(config_files)}\n"

        # Code structure
        structure = context.get('code_structure', {})
        if structure and not structure.get('error'):
            formatted += f"""
## Code Structure
- **Classes**: {len(structure.get('classes', []))}
- **Functions**: {len(structure.get('functions', []))}
- **Async Functions**: {len(structure.get('async_functions', []))}

### Key Components:
"""

            # List main classes
            for cls in structure.get('classes', [])[:3]:  # Limit to first 3
                bases = cls.get('bases', [])
                base_info = f" (inherits from {', '.join(bases)})" if bases else ""
                formatted += f"- **Class `{cls['name']}`{base_info}**: {len(cls.get('methods', []))} methods\n"

            # List main functions
            for func in structure.get('functions', [])[:5]:  # Limit to first 5
                complexity = func.get('complexity', 0)
                complexity_note = f" (complexity: {complexity})" if complexity > 5 else ""
                formatted += f"- **Function `{func['name']}`{complexity_note}**: line {func.get('line', '?')}\n"

        # Dependencies
        deps = context.get('dependencies', {})
        if deps and not deps.get('error'):
            formatted += f"""
## Dependencies
- **Standard Library**: {', '.join(deps.get('stdlib', [])[:5])}{"..." if len(deps.get('stdlib', [])) > 5 else ""}
- **Third-Party**: {', '.join(deps.get('third_party', []))}
- **Local Imports**: {', '.join(deps.get('local', []))}
"""

        # Code patterns and quality
        patterns = context.get('code_patterns', {})
        if patterns:
            formatted += f"""
## Code Patterns Detected
- Type hints: {'✓' if patterns.get('uses_type_hints') else '✗'}
- Error handling: {'✓' if patterns.get('has_error_handling') else '✗'}
- Async/await: {'✓' if patterns.get('uses_async') else '✗'}
- Logging: {'✓' if patterns.get('uses_logging') else '✗'}
- TODOs/FIXMEs: {'⚠️ Yes' if patterns.get('has_todos') else '✓ None'}
"""

            complexity = patterns.get('complexity_indicators', {})
            if complexity:
                if complexity.get('long_functions', 0) > 0:
                    formatted += f"- **Long functions detected**: {complexity['long_functions']}\n"
                if complexity.get('deep_nesting', 0) > 4:
                    formatted += f"- **Deep nesting detected**: {complexity['deep_nesting']} levels\n"

        # Documentation
        docs = context.get('documentation', {})
        if docs and not docs.get('error'):
            if docs.get('module_doc'):
                formatted += f"""
## Module Documentation
{docs['module_doc'][:200]}{'...' if len(docs.get('module_doc', '')) > 200 else ''}
"""

        # Quality indicators
        quality = context.get('quality_indicators', {})
        if quality:
            doc_coverage = quality.get('has_docstrings', {})
            if doc_coverage:
                formatted += f"""
## Quality Indicators
- **Docstring Coverage**: {doc_coverage.get('coverage_percent', 0):.1f}%
"""

            pep8_issues = quality.get('follows_pep8', {})
            if pep8_issues:
                issues = []
                if pep8_issues.get('long_lines', 0) > 0:
                    issues.append(f"{pep8_issues['long_lines']} long lines")
                if pep8_issues.get('trailing_whitespace', 0) > 0:
                    issues.append("trailing whitespace")
                if pep8_issues.get('mixed_indentation'):
                    issues.append("mixed indentation")
                if issues:
                    formatted += f"- **Style Issues**: {', '.join(issues)}\n"

            security = quality.get('security_concerns', [])
            if security:
                formatted += f"- **Security Concerns**: {len(security)} potential issues detected\n"

            performance = quality.get('performance_hints', [])
            if performance:
                formatted += f"- **Performance Hints**: {len(performance)} optimization opportunities\n"

        # Recent changes
        changes = context.get('recent_changes')
        if changes and not changes.get('error'):
            recent_commits = changes.get('recent_commits', [])
            if recent_commits:
                formatted += """
## Recent Development History
"""
                for commit in recent_commits[:3]:
                    formatted += f"- `{commit['hash']}` ({commit['date']}): {commit['message'][:60]}{'...' if len(commit['message']) > 60 else ''}\n"

            if changes.get('has_uncommitted_changes'):
                formatted += "- **⚠️ Uncommitted changes detected**\n"

        # Related files
        related = context.get('related_files', [])
        if related:
            formatted += """
## Related Files
"""
            for rel in related[:5]:
                formatted += f"- {rel['type']}: `{Path(rel['path']).name}`\n"

        # Advanced analysis
        advanced = context.get('advanced_analysis', {})
        if advanced and not advanced.get('error'):
            formatted += """
## Advanced Code Analysis
"""

            # Complexity metrics
            complexity = advanced.get('complexity_metrics', {})
            if complexity:
                total_complexity = complexity.get('total_complexity', 0)
                avg_complexity = complexity.get('average_complexity', 0)
                complex_funcs = complexity.get('complex_functions', [])
                long_funcs = complexity.get('long_functions', [])
                many_params = complexity.get('many_parameters', [])

                formatted += f"- **Total Cyclomatic Complexity**: {total_complexity} (average: {avg_complexity:.1f})\n"
                if complex_funcs:
                    formatted += f"- **Complex Functions** (>10): {', '.join(complex_funcs)}\n"
                if long_funcs:
                    formatted += f"- **Long Functions** (>50 lines): {', '.join(long_funcs)}\n"
                if many_params:
                    formatted += f"- **Functions with Many Parameters** (>5): {', '.join(many_params)}\n"

            # Call graph analysis
            call_graph = advanced.get('function_call_graph', {})
            if call_graph:
                recursive = call_graph.get('recursive_functions', [])
                max_depth = call_graph.get('max_call_depth', 0)
                cycles = call_graph.get('call_cycles', [])

                formatted += f"- **Maximum Call Depth**: {max_depth}\n"
                if recursive:
                    formatted += f"- **Recursive Functions**: {', '.join(recursive)}\n"
                if cycles:
                    formatted += f"- **Call Cycles Detected**: {len(cycles)} cycles found\n"

            # Pattern detection
            patterns = advanced.get('pattern_detection', {})
            if patterns:
                design_patterns = patterns.get('design_patterns', [])
                anti_patterns = patterns.get('anti_patterns', [])
                code_smells = patterns.get('code_smells', [])

                if design_patterns:
                    formatted += f"- **Design Patterns Detected**: {', '.join(design_patterns)}\n"
                if anti_patterns:
                    formatted += f"- **⚠️ Anti-Patterns**: {', '.join(anti_patterns)}\n"
                if code_smells:
                    formatted += f"- **🔍 Code Smells**: {', '.join(code_smells)}\n"

            # Error handling analysis
            error_handling = advanced.get('error_handling', {})
            if error_handling:
                bare_except = error_handling.get('bare_except', [])
                exception_types = error_handling.get('exception_types', [])
                resource_mgmt = error_handling.get('resource_management', [])

                if bare_except:
                    formatted += f"- **⚠️ Bare Except Blocks**: Found in {', '.join(bare_except)}\n"
                if exception_types:
                    formatted += f"- **Exception Types Used**: {', '.join(list(exception_types)[:5])}\n"
                if resource_mgmt:
                    formatted += f"- **Resource Management**: Context managers used in {', '.join(resource_mgmt)}\n"

            # Variable analysis
            var_analysis = advanced.get('variable_analysis', {})
            if var_analysis:
                unused_vars = var_analysis.get('unused_variables', [])
                shadowing = var_analysis.get('variable_shadowing', [])
                mutable_defaults = var_analysis.get('mutable_defaults', [])

                if unused_vars:
                    formatted += f"- **⚠️ Unused Variables**: {', '.join(unused_vars[:5])}\n"
                if shadowing:
                    formatted += f"- **Variable Shadowing**: {', '.join(shadowing[:3])}\n"
                if mutable_defaults:
                    formatted += f"- **⚠️ Mutable Default Arguments**: {', '.join(mutable_defaults)}\n"

        # Test Coverage Analysis
        test_coverage = context.get('test_coverage', {})
        if test_coverage:
            formatted += """
## Test Coverage Analysis
"""
            if test_coverage.get('is_test_file'):
                formatted += f"- **Test File**: Yes ({test_coverage.get('test_functions', 0)} test functions)\n"
                formatted += f"- **Assertions**: {test_coverage.get('assertion_count', 0)} assertions\n"
                formatted += f"- **Async Tests**: {test_coverage.get('async_tests', 0)}\n"
                formatted += f"- **Fixtures Used**: {test_coverage.get('fixtures_used', 0)}\n"
                formatted += f"- **Parametrized Tests**: {test_coverage.get('parametrized_tests', 0)}\n"
                if test_coverage.get('mock_usage'):
                    formatted += "- **Mocking**: Used\n"
            else:
                has_test = test_coverage.get('has_test_file', False)
                formatted += f"- **Has Test File**: {'Yes' if has_test else 'No'}\n"

        # Enhanced Performance Analysis
        perf_hints = context.get('performance_hints', [])
        if perf_hints:
            formatted += """
## Performance Analysis
"""
            for hint in perf_hints[:5]:  # Limit to top 5
                formatted += f"- ⚠️ {hint}\n"

        # Security Analysis
        security = context.get('security_analysis', {})
        if security:
            formatted += """
## Security Analysis
"""
            if security.get('high_risk'):
                formatted += "**🚨 High Risk Issues:**\n"
                for issue in security['high_risk']:
                    formatted += f"- {issue}\n"

            if security.get('medium_risk'):
                formatted += "**⚠️ Medium Risk Issues:**\n"
                for issue in security['medium_risk']:
                    formatted += f"- {issue}\n"

            if security.get('good_practices'):
                formatted += "**✅ Security Good Practices:**\n"
                for practice in security['good_practices']:
                    formatted += f"- {practice}\n"

        # Refactoring Opportunities
        refactoring = context.get('refactoring_opportunities', {})
        if refactoring:
            formatted += """
## Refactoring Opportunities
"""
            if refactoring.get('duplicate_code'):
                formatted += f"- **Duplicate Code**: {len(refactoring['duplicate_code'])} instances found\n"

            if refactoring.get('magic_numbers'):
                numbers = refactoring['magic_numbers'][:5]  # Limit display
                formatted += f"- **Magic Numbers**: {', '.join(numbers)}\n"

            if refactoring.get('complex_conditions'):
                formatted += f"- **Complex Conditions**: {len(refactoring['complex_conditions'])} found\n"

            if refactoring.get('naming_improvements'):
                names = refactoring['naming_improvements'][:3]
                formatted += f"- **Poor Variable Names**: {', '.join(names)}\n"

        # Error Handling Analysis
        error_patterns = context.get('error_patterns', {})
        if error_patterns and not error_patterns.get('error'):
            formatted += """
## Error Handling Analysis
"""
            exc_handling = error_patterns.get('exception_handling', {})
            if exc_handling:
                formatted += f"- **Try Blocks**: {exc_handling.get('try_blocks', 0)}\n"
                if exc_handling.get('bare_except', 0) > 0:
                    formatted += f"- **⚠️ Bare Except Blocks**: {exc_handling['bare_except']}\n"
                if exc_handling.get('specific_exceptions'):
                    exceptions = list(set(exc_handling['specific_exceptions']))[:5]
                    formatted += f"- **Exception Types**: {', '.join(exceptions)}\n"

            defensive = error_patterns.get('defensive_programming', {})
            if defensive:
                formatted += f"- **Assertions**: {defensive.get('assertions', 0)}\n"
                formatted += f"- **Type Checks**: {defensive.get('type_checks', 0)}\n"

        # Dependency Health
        dep_health = context.get('dependency_health', {})
        if dep_health and not dep_health.get('error'):
            formatted += """
## Dependency Health
"""
            import_analysis = dep_health.get('import_analysis', {})
            if import_analysis:
                formatted += f"- **Total Imports**: {import_analysis.get('total_imports', 0)}\n"
                formatted += f"- **Unique Modules**: {import_analysis.get('unique_modules', 0)}\n"

            if dep_health.get('deprecated_usage'):
                formatted += "**⚠️ Deprecated Usage:**\n"
                for dep in dep_health['deprecated_usage']:
                    formatted += f"- {dep}\n"

        # Python-Specific Deep Analysis
        python_analysis = context.get('python_specific')
        if python_analysis and not python_analysis.get('error'):
            formatted += """
## Python-Specific Analysis
"""

            # Type Hints Analysis
            type_hints = python_analysis.get('type_hints_analysis', {})
            if type_hints.get('coverage_stats'):
                stats = type_hints['coverage_stats']
                formatted += "### Type Hints Coverage\n"
                formatted += f"- **Function Returns**: {stats.get('function_return_coverage', 0):.1f}% ({stats.get('annotated_functions', 0)}/{stats.get('total_functions', 0)})\n"
                formatted += f"- **Parameters**: {stats.get('parameter_coverage', 0):.1f}% ({stats.get('annotated_parameters', 0)}/{stats.get('total_parameters', 0)})\n"

                if type_hints.get('generic_usage'):
                    formatted += f"- **Generic Types Used**: {len(type_hints['generic_usage'])} instances\n"

            # Call Hierarchy
            call_hierarchy = python_analysis.get('call_hierarchy', {})
            if call_hierarchy:
                if call_hierarchy.get('recursive_calls'):
                    formatted += "### Call Hierarchy\n"
                    formatted += f"- **Recursive Functions**: {', '.join(call_hierarchy['recursive_calls'])}\n"

                if call_hierarchy.get('external_calls'):
                    external_count = len(call_hierarchy['external_calls'])
                    formatted += f"- **External Function Calls**: {external_count} different functions\n"

            # Class Hierarchy
            class_hierarchy = python_analysis.get('class_hierarchy', {})
            if class_hierarchy:
                formatted += "### Class Structure\n"
                for class_name, class_info in class_hierarchy.items():
                    if class_info.get('bases'):
                        formatted += f"- **{class_name}** inherits from: {', '.join(class_info['bases'])}\n"

                    method_count = len(class_info.get('methods', []))
                    property_count = len(class_info.get('properties', []))
                    if method_count > 0 or property_count > 0:
                        formatted += f"  - Methods: {method_count}, Properties: {property_count}\n"

            # Exception Patterns
            exceptions = python_analysis.get('exception_patterns', {})
            if exceptions:
                formatted += "### Exception Handling\n"
                try_count = len(exceptions.get('try_blocks', []))
                if try_count > 0:
                    formatted += f"- **Try Blocks**: {try_count}\n"

                if exceptions.get('bare_except_locations'):
                    locations = exceptions['bare_except_locations']
                    formatted += f"- **⚠️ Bare Except Blocks**: Lines {', '.join(map(str, locations))}\n"

                if exceptions.get('exception_types'):
                    exc_types = exceptions['exception_types']
                    # Handle both Counter and dict objects
                    if hasattr(exc_types, 'most_common'):
                        common_exceptions = list(exc_types.most_common(3))
                    else:
                        common_exceptions = list(exc_types.items())[:3]
                    formatted += f"- **Common Exception Types**: {', '.join([f'{exc}({count})' for exc, count in common_exceptions])}\n"

            # Complexity Hotspots
            hotspots = python_analysis.get('complexity_hotspots', [])
            if hotspots:
                formatted += "### Complexity Hotspots\n"
                for hotspot in hotspots[:3]:  # Top 3
                    formatted += f"- **{hotspot['function']}()**: Complexity {hotspot['complexity']} (line {hotspot['line']})\n"

            # Decorator Usage
            decorators = python_analysis.get('decorator_usage', {})
            if decorators:
                builtin_count = len(decorators.get('builtin_decorators', []))
                custom_count = len(decorators.get('custom_decorators', []))
                if builtin_count > 0 or custom_count > 0:
                    formatted += "### Decorator Usage\n"
                    formatted += f"- **Built-in Decorators**: {builtin_count}\n"
                    formatted += f"- **Custom Decorators**: {custom_count}\n"

            # Docstring Analysis
            docstrings = python_analysis.get('docstring_analysis', {})
            if docstrings:
                styles = docstrings.get('docstring_styles', {})
                if styles:
                    formatted += "### Documentation Style\n"
                    # Handle both Counter and dict objects
                    style_items = styles.most_common() if hasattr(styles, 'most_common') else styles.items()
                    for style, count in style_items:
                        formatted += f"- **{style} Style**: {count} docstrings\n"

                missing = docstrings.get('missing_docstrings', [])
                if missing:
                    formatted += f"- **Missing Docstrings**: {len(missing)} items\n"

        # Multi-Tool Analysis Integration
        multi_tool = context.get('multi_tool_analysis')
        if multi_tool and not multi_tool.get('error'):
            formatted += """
## Professional Tool Analysis
"""

            # Summary
            summary = multi_tool.get('summary', {})
            if summary:
                successful = summary.get('successful_tools', 0)
                total = summary.get('total_tools', 0)
                execution_time = summary.get('execution_time', 0)
                formatted += "### Analysis Coverage\n"
                formatted += f"- **Tools Successfully Run**: {successful}/{total}\n"
                formatted += f"- **Total Analysis Time**: {execution_time:.2f}s\n"

            # Tool Results
            tools = multi_tool.get('tools', {})

            # Static Analysis Results
            static_tools = tools.get('static_analysis', {})
            if static_tools:
                formatted += "### Static Analysis\n"
                pylint_data = static_tools.get('pylint', {})
                if pylint_data.get('success') and pylint_data.get('data'):
                    issues = pylint_data['data'].get('issues', [])
                    if issues:
                        error_count = len([i for i in issues if i.get('type') == 'error'])
                        warning_count = len([i for i in issues if i.get('type') == 'warning'])
                        formatted += f"- **Pylint Issues**: {len(issues)} total ({error_count} errors, {warning_count} warnings)\n"

                        # Show top issues
                        for issue in issues[:3]:
                            formatted += f"  - Line {issue.get('line')}: {issue.get('message')} ({issue.get('symbol')})\n"

            # Security Analysis Results
            security_tools = tools.get('security', {})
            if security_tools:
                formatted += "### Security Analysis\n"
                bandit_data = security_tools.get('bandit', {})
                if bandit_data.get('success') and bandit_data.get('data'):
                    bandit_results = bandit_data['data']
                    if bandit_results.get('results'):
                        issues = bandit_results['results']
                        formatted += f"- **Security Issues Found**: {len(issues)}\n"
                        for issue in issues[:3]:  # Top 3
                            formatted += f"  - {issue.get('issue_text', 'Security issue')} (Line {issue.get('line_number')})\n"
                    else:
                        formatted += "- **Security Scan**: No issues found ✅\n"

            # Complexity Metrics
            metrics_tools = tools.get('metrics', {})
            if metrics_tools:
                radon_data = metrics_tools.get('radon', {})
                if radon_data.get('success') and radon_data.get('data'):
                    radon_results = radon_data['data']
                    if radon_results.get('complexity'):
                        formatted += "### Complexity Metrics (Radon)\n"
                        for radon_file_path, file_data in radon_results['complexity'].items():
                            for item in file_data[:3]:  # Top 3 most complex
                                complexity = item.get('complexity', 0)
                                if complexity > 5:  # Only show notable complexity
                                    formatted += f"- **{item.get('name', 'Function')}**: Complexity {complexity} (Line {item.get('lineno')})\n"

            # Dependencies
            deps_tools = tools.get('dependencies', {})
            if deps_tools:
                pipdeptree_data = deps_tools.get('pipdeptree', {})
                if pipdeptree_data.get('success') and pipdeptree_data.get('data'):
                    deps = pipdeptree_data['data'].get('dependencies', [])
                    formatted += "### Dependency Analysis\n"
                    formatted += f"- **Total Dependencies**: {len(deps)}\n"

                    # Show main dependencies
                    for dep in deps[:5]:  # Top 5
                        if isinstance(dep, dict):
                            package_name = dep.get('package_name', 'Unknown')
                            installed_version = dep.get('installed_version', 'Unknown')
                            formatted += f"  - {package_name} ({installed_version})\n"

            # Recommendations from tool analysis
            recommendations = multi_tool.get('recommendations', [])
            if recommendations:
                formatted += "### Tool Recommendations\n"
                for rec in recommendations[:5]:  # Top 5
                    formatted += f"- {rec}\n"

        # The actual code
        formatted += f"""
## Code to Review

```{file_path.suffix[1:] if file_path.suffix else 'text'}
{file_content}
```

---

Please provide a comprehensive, context-aware code review considering:
1. How this code fits within the detected project architecture
2. Adherence to the project's apparent patterns and conventions  
3. Integration with detected dependencies and frameworks
4. Quality improvements based on the project's current standards
5. Security and performance considerations specific to this codebase
6. Recommendations that align with the project's development history and practices
"""

        return formatted

    def review_code_with_context(self, file_path: Path, model: str) -> str:
        """Send code with context to Groq for review"""
        try:
            # Gather context
            print("🔍 Gathering contextual information...")
            context = self.gather_context(file_path)

            # Read file
            code_content = file_path.read_text()

            # Format for AI
            prompt = self.format_context_for_ai(context, code_content, file_path)

            # Create enhanced system prompt
            system_prompt = """You are a senior software engineer conducting a thorough, context-aware code review. 

CRITICAL GUIDELINES:
1. **Respect Framework Patterns**: Don't suggest changes to well-established framework patterns unless there's a clear bug or security issue. Mixed sync/async in tests, framework-specific testing utilities, and standard conventions should be preserved.

2. **Context-Specific Advice**: Avoid generic recommendations. Every suggestion must be directly relevant to the detected project type, framework, and specific code context. For example, don't suggest "add caching" unless you see clear performance bottlenecks.

3. **Framework Expertise**: If the code uses specific frameworks (Textual, pytest, Django, etc.), demonstrate understanding of their conventions. Don't flag framework-standard practices as issues.

4. **Testing Context Awareness**: For test files, understand testing patterns. Don't suggest making sync test methods async unless required. Recognize testing utilities vs. production anti-patterns.

5. **Actionable Over Comprehensive**: Prioritize 2-3 high-impact, specific improvements over exhaustive lists of minor issues. Focus on what will meaningfully improve the code.

Consider the provided contextual information about the project, codebase patterns, dependencies, and development history when making your recommendations.

Focus on:
- Architecture fit and consistency with project patterns
- Code quality improvements specific to this codebase  
- Security and performance issues relevant to the detected framework/libraries
- Maintainability improvements that align with project conventions
- Integration concerns with detected dependencies
- Recommendations that respect the project's apparent development practices

Provide specific, actionable feedback with code examples where helpful. Avoid suggesting changes to code that already follows appropriate patterns for its context."""

            # Count tokens for analysis
            system_tokens = self.count_tokens(system_prompt)
            user_tokens = self.count_tokens(prompt)
            total_input_tokens = system_tokens + user_tokens

            print("📊 Token Analysis:")
            print(f"   System prompt: {system_tokens:,} tokens")
            print(f"   Context + code: {user_tokens:,} tokens")
            print(f"   Total input: {total_input_tokens:,} tokens")

            print("🤖 Generating context-aware review...")
            response = requests.post(
                f"{self.BASE_URL}/chat/completions",
                headers=self.headers,
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 4096
                }
            )
            response.raise_for_status()

            result = response.json()
            response_content = result["choices"][0]["message"]["content"]

            # Count output tokens
            output_tokens = self.count_tokens(response_content)
            print(f"   Response: {output_tokens:,} tokens")
            print(f"   Total tokens: {total_input_tokens + output_tokens:,}")

            # Check if we're approaching context limits
            if total_input_tokens > 20000:
                print("⚠️  Warning: High token count - consider reducing context")

            return response_content

        except Exception as e:
            return f"Error during enhanced code review: {e}"


def load_api_key() -> Optional[str]:
    """Load Groq API key from ~/.env file"""
    env_path = Path.home() / ".env"

    if not env_path.exists():
        print("Error: ~/.env file not found")
        return None

    load_dotenv(env_path)
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("Error: GROQ_API_KEY not found in ~/.env")
        return None

    return api_key


def main():
    parser = argparse.ArgumentParser(
        description="Get context-aware AI code review using Groq API"
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Path to the file to review"
    )
    parser.add_argument(
        "--model",
        help="Specific model to use (otherwise auto-selects best available)"
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List all available models and exit"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Save review to file instead of printing"
    )
    parser.add_argument(
        "--context-only",
        action="store_true",
        help="Only show gathered context, don't run review"
    )

    args = parser.parse_args()

    # Load API key
    api_key = load_api_key()
    if not api_key:
        sys.exit(1)

    reviewer = EnhancedGroqCodeReviewer(api_key)

    # Get available models
    print("🔍 Fetching available Groq models...")
    models = reviewer.get_available_models()

    if not models:
        print("Error: No models available")
        sys.exit(1)

    # List models if requested
    if args.list_models:
        print("\n📋 Available Groq Models:")
        for model in models:
            print(f"  - {model['id']}")
        sys.exit(0)

    # Check file exists
    if not args.file.exists():
        print(f"Error: File not found: {args.file}")
        sys.exit(1)

    # Context-only mode
    if args.context_only:
        print("🔍 Gathering context information...")
        try:
            script_dir = Path(__file__).parent
            script_path = script_dir / "gather-code-context.py"
            subprocess.run([sys.executable, str(script_path), str(args.file)])
        except Exception as e:
            print(f"Error gathering context: {e}")
        sys.exit(0)

    # Select model
    if args.model:
        selected_model = args.model
        available_ids = {m["id"] for m in models}
        if selected_model not in available_ids:
            print(f"Error: Model '{selected_model}' not available")
            print("Use --list-models to see available options")
            sys.exit(1)
    else:
        selected_model = reviewer.select_best_model(models)
        if not selected_model:
            print("Error: Could not select a suitable model")
            sys.exit(1)

    print(f"✨ Using model: {selected_model}")
    print(f"📄 Reviewing: {args.file}")

    # Get enhanced review
    review = reviewer.review_code_with_context(args.file, selected_model)

    # Output results
    if args.output:
        args.output.write_text(review)
        print(f"✅ Enhanced review saved to: {args.output}")
    else:
        print("=" * 80)
        print("Enhanced Context-Aware Code Review")
        print(f"File: {args.file.name}")
        print(f"Model: {selected_model}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print(review)


if __name__ == "__main__":
    main()
