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
                formatted += f"""
## Recent Development History
"""
                for commit in recent_commits[:3]:
                    formatted += f"- `{commit['hash']}` ({commit['date']}): {commit['message'][:60]}{'...' if len(commit['message']) > 60 else ''}\n"
                    
            if changes.get('has_uncommitted_changes'):
                formatted += "- **⚠️ Uncommitted changes detected**\n"
        
        # Related files
        related = context.get('related_files', [])
        if related:
            formatted += f"""
## Related Files
"""
            for rel in related[:5]:
                formatted += f"- {rel['type']}: `{Path(rel['path']).name}`\n"
        
        # Advanced analysis
        advanced = context.get('advanced_analysis', {})
        if advanced and not advanced.get('error'):
            formatted += f"""
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

Consider the provided contextual information about the project, codebase patterns, dependencies, and development history when making your recommendations.

Focus on:
- Architecture fit and consistency with project patterns
- Code quality improvements specific to this codebase
- Security and performance issues relevant to the detected framework/libraries
- Maintainability improvements that align with project conventions
- Integration concerns with detected dependencies
- Recommendations that respect the project's apparent development practices

Provide specific, actionable feedback with code examples where helpful."""

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
            return result["choices"][0]["message"]["content"]
            
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
        print(f"Enhanced Context-Aware Code Review")
        print(f"File: {args.file.name}")
        print(f"Model: {selected_model}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print(review)


if __name__ == "__main__":
    main()