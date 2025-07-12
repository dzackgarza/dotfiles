#!/usr/bin/env python3
"""
Code Context Gatherer - Mimics human code review workflows
Gathers comprehensive contextual information for enhanced AI code reviews
"""

import os
import sys
import ast
import subprocess
from pathlib import Path
from datetime import datetime
import re
from typing import Dict, List, Optional, Tuple
import json


class CodeContextGatherer:
    """Gathers contextual information about code files for enhanced reviews"""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.file_name = file_path.name
        self.directory = file_path.parent
        self.is_git_repo = self._check_git_repo()
        
    def _check_git_repo(self) -> bool:
        """Check if file is in a git repository"""
        try:
            subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.directory,
                capture_output=True,
                check=True
            )
            return True
        except:
            return False

    def gather_all_context(self) -> Dict:
        """Gather all contextual information"""
        context = {
            "file_info": self._get_file_info(),
            "code_structure": self._analyze_code_structure(),
            "documentation": self._extract_documentation(),
            "dependencies": self._analyze_dependencies(),
            "related_files": self._find_related_files(),
            "recent_changes": self._get_recent_changes() if self.is_git_repo else None,
            "code_patterns": self._analyze_code_patterns(),
            "project_context": self._get_project_context(),
            "quality_indicators": self._analyze_quality_indicators()
        }
        return context

    def _get_file_info(self) -> Dict:
        """Get basic file information"""
        stat_info = self.file_path.stat()
        return {
            "name": self.file_name,
            "path": str(self.file_path),
            "size_bytes": stat_info.st_size,
            "lines_of_code": len(self.file_path.read_text().splitlines()),
            "last_modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
            "file_type": self.file_path.suffix
        }

    def _analyze_code_structure(self) -> Dict:
        """Analyze code structure using AST"""
        try:
            with open(self.file_path) as f:
                tree = ast.parse(f.read())
                
            structure = {
                "classes": [],
                "functions": [],
                "async_functions": [],
                "decorators": set(),
                "imports": []
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    bases = [self._get_name(base) for base in node.bases]
                    methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                    structure["classes"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "bases": bases,
                        "methods": methods,
                        "decorators": [self._get_name(d) for d in node.decorator_list]
                    })
                elif isinstance(node, ast.FunctionDef):
                    structure["functions"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "args": [arg.arg for arg in node.args.args],
                        "decorators": [self._get_name(d) for d in node.decorator_list],
                        "is_method": self._is_method(node),
                        "complexity": self._estimate_complexity(node)
                    })
                elif isinstance(node, ast.AsyncFunctionDef):
                    structure["async_functions"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "args": [arg.arg for arg in node.args.args],
                        "decorators": [self._get_name(d) for d in node.decorator_list]
                    })
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    structure["imports"].append(self._format_import(node))
                    
            structure["decorators"] = list(structure["decorators"])
            return structure
        except Exception as e:
            return {"error": f"Failed to parse: {str(e)}"}

    def _extract_documentation(self) -> Dict:
        """Extract docstrings and comments"""
        try:
            with open(self.file_path) as f:
                content = f.read()
                tree = ast.parse(content)
                
            docs = {
                "module_doc": ast.get_docstring(tree),
                "classes": {},
                "functions": {},
                "inline_comments": self._extract_inline_comments(content)
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    doc = ast.get_docstring(node)
                    if doc:
                        docs["classes"][node.name] = {
                            "docstring": doc,
                            "line": node.lineno
                        }
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    doc = ast.get_docstring(node)
                    if doc:
                        docs["functions"][node.name] = {
                            "docstring": doc,
                            "line": node.lineno,
                            "summary": doc.split('\n')[0] if doc else None
                        }
                        
            return docs
        except Exception as e:
            return {"error": f"Failed to extract docs: {str(e)}"}

    def _analyze_dependencies(self) -> Dict:
        """Analyze imports and dependencies"""
        try:
            with open(self.file_path) as f:
                tree = ast.parse(f.read())
                
            deps = {
                "stdlib": [],
                "third_party": [],
                "local": [],
                "type_imports": []
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._categorize_import(alias.name, deps)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self._categorize_import(node.module, deps, node.names)
                        
            return deps
        except Exception as e:
            return {"error": f"Failed to analyze deps: {str(e)}"}

    def _find_related_files(self) -> List[Dict]:
        """Find related files in the project"""
        related = []
        
        # Look for test files
        test_patterns = [
            f"test_{self.file_path.stem}.py",
            f"{self.file_path.stem}_test.py",
            f"test_{self.file_name}"
        ]
        
        for pattern in test_patterns:
            # Check in tests directory
            test_file = self.directory.parent / "tests" / pattern
            if test_file.exists():
                related.append({
                    "path": str(test_file),
                    "type": "test",
                    "exists": True
                })
                
        # Look for __init__.py in same directory
        init_file = self.directory / "__init__.py"
        if init_file.exists():
            related.append({
                "path": str(init_file),
                "type": "package_init",
                "exists": True
            })
            
        # Look for related modules (same prefix)
        prefix = self.file_path.stem.split('_')[0]
        for file in self.directory.glob(f"{prefix}*.py"):
            if file != self.file_path and file.name != "__init__.py":
                related.append({
                    "path": str(file),
                    "type": "related_module",
                    "exists": True
                })
                
        return related

    def _get_recent_changes(self) -> Dict:
        """Get recent git history"""
        try:
            # Get recent commits
            commits_output = subprocess.run(
                ["git", "log", "-n", "5", "--pretty=format:%h|%ad|%s|%an", "--date=short", "--", str(self.file_path)],
                cwd=self.directory,
                capture_output=True,
                text=True,
                check=True
            ).stdout
            
            commits = []
            for line in commits_output.strip().split('\n'):
                if line:
                    parts = line.split('|')
                    commits.append({
                        "hash": parts[0],
                        "date": parts[1],
                        "message": parts[2],
                        "author": parts[3]
                    })
                    
            # Get current diff
            diff_output = subprocess.run(
                ["git", "diff", str(self.file_path)],
                cwd=self.directory,
                capture_output=True,
                text=True
            ).stdout
            
            # Get blame info for complex areas
            blame_info = self._get_blame_summary()
            
            return {
                "recent_commits": commits,
                "has_uncommitted_changes": bool(diff_output),
                "lines_changed": len(diff_output.splitlines()) if diff_output else 0,
                "blame_summary": blame_info
            }
        except Exception as e:
            return {"error": f"Failed to get git info: {str(e)}"}

    def _analyze_code_patterns(self) -> Dict:
        """Analyze common code patterns and potential issues"""
        with open(self.file_path) as f:
            content = f.read()
            
        patterns = {
            "uses_type_hints": bool(re.search(r':\s*\w+\s*[=)]', content)),
            "has_error_handling": bool(re.search(r'\btry\s*:', content)),
            "uses_logging": bool(re.search(r'\blogging\.|logger\.', content)),
            "has_tests_reference": bool(re.search(r'test_|_test|pytest|unittest', content, re.I)),
            "uses_async": bool(re.search(r'\basync\s+def|\bawait\s+', content)),
            "has_todos": bool(re.search(r'TODO|FIXME|HACK|XXX', content)),
            "uses_dataclasses": bool(re.search(r'@dataclass|from dataclasses', content)),
            "has_main_block": bool(re.search(r'if\s+__name__\s*==\s*["\']__main__["\']', content)),
            "complexity_indicators": {
                "nested_loops": len(re.findall(r'for .* in .*:\s*\n\s*for', content)),
                "long_functions": self._count_long_functions(content),
                "deep_nesting": self._estimate_max_nesting(content)
            }
        }
        
        return patterns

    def _get_project_context(self) -> Dict:
        """Get broader project context"""
        context = {
            "framework": None,
            "project_type": None,
            "config_files": []
        }
        
        # Check for common project files
        project_root = self._find_project_root()
        if project_root:
            # Python project files
            for config_file in ["pyproject.toml", "setup.py", "requirements.txt", "pdm.lock", "poetry.lock"]:
                if (project_root / config_file).exists():
                    context["config_files"].append(config_file)
                    
            # Detect framework
            if (project_root / "manage.py").exists():
                context["framework"] = "Django"
            elif any((project_root / f).exists() for f in ["app.py", "wsgi.py"]):
                context["framework"] = "Flask/FastAPI"
                
            # Read pyproject.toml if exists
            pyproject = project_root / "pyproject.toml"
            if pyproject.exists():
                try:
                    import tomllib
                    with open(pyproject, 'rb') as f:
                        data = tomllib.load(f)
                        if "tool" in data and "poetry" in data["tool"]:
                            context["project_type"] = "Poetry project"
                        elif "project" in data:
                            context["project_type"] = "PEP 517 project"
                            context["project_name"] = data["project"].get("name")
                except:
                    pass
                    
        return context

    def _analyze_quality_indicators(self) -> Dict:
        """Analyze code quality indicators"""
        with open(self.file_path) as f:
            lines = f.readlines()
            content = ''.join(lines)
            
        quality = {
            "has_docstrings": self._check_docstring_coverage(content),
            "follows_pep8": self._check_basic_pep8(lines),
            "test_coverage_hints": self._check_test_hints(content),
            "security_concerns": self._check_security_patterns(content),
            "performance_hints": self._check_performance_patterns(content)
        }
        
        return quality

    # Helper methods
    def _get_name(self, node) -> str:
        """Get name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return str(node)

    def _is_method(self, node) -> bool:
        """Check if function is a method"""
        return any(parent for parent in ast.walk(node) if isinstance(parent, ast.ClassDef))

    def _estimate_complexity(self, node) -> int:
        """Estimate cyclomatic complexity"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
        return complexity

    def _format_import(self, node) -> str:
        """Format import statement"""
        if isinstance(node, ast.Import):
            return f"import {', '.join(alias.name for alias in node.names)}"
        else:
            names = ', '.join(alias.name for alias in node.names)
            return f"from {node.module or '.'} import {names}"

    def _extract_inline_comments(self, content: str) -> int:
        """Count inline comments"""
        return len(re.findall(r'#[^#\n]+', content))

    def _categorize_import(self, module: str, deps: Dict, names=None):
        """Categorize import as stdlib, third-party, or local"""
        stdlib_modules = {
            'os', 'sys', 'ast', 'json', 're', 'pathlib', 'datetime', 
            'subprocess', 'typing', 'collections', 'itertools', 'functools'
        }
        
        if module.startswith('.'):
            deps["local"].append(module)
        elif module.split('.')[0] in stdlib_modules:
            deps["stdlib"].append(module)
        elif module == "typing" or (names and any("TYPE_CHECKING" in str(n) for n in names)):
            deps["type_imports"].append(module)
        else:
            deps["third_party"].append(module)

    def _get_blame_summary(self) -> Dict:
        """Get summary of who last modified complex parts"""
        # Simplified - would need more complex implementation
        return {"available": False}

    def _count_long_functions(self, content: str) -> int:
        """Count functions over 50 lines"""
        # Simplified implementation
        functions = re.findall(r'def \w+.*?(?=\n(?:def|class|\Z))', content, re.DOTALL)
        return sum(1 for f in functions if len(f.splitlines()) > 50)

    def _estimate_max_nesting(self, content: str) -> int:
        """Estimate maximum nesting depth"""
        max_indent = 0
        for line in content.splitlines():
            if line.strip():
                indent = len(line) - len(line.lstrip())
                max_indent = max(max_indent, indent // 4)
        return max_indent

    def _find_project_root(self) -> Optional[Path]:
        """Find project root directory"""
        current = self.directory
        for _ in range(5):  # Max 5 levels up
            if any((current / f).exists() for f in ["pyproject.toml", "setup.py", ".git"]):
                return current
            current = current.parent
        return None

    def _check_docstring_coverage(self, content: str) -> Dict:
        """Check docstring coverage"""
        try:
            tree = ast.parse(content)
            total_defs = 0
            with_docs = 0
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    total_defs += 1
                    if ast.get_docstring(node):
                        with_docs += 1
                        
            return {
                "total_definitions": total_defs,
                "with_docstrings": with_docs,
                "coverage_percent": (with_docs / total_defs * 100) if total_defs > 0 else 0
            }
        except:
            return {"error": "Failed to analyze"}

    def _check_basic_pep8(self, lines: List[str]) -> Dict:
        """Check basic PEP8 compliance"""
        issues = {
            "long_lines": sum(1 for line in lines if len(line.rstrip()) > 88),
            "trailing_whitespace": sum(1 for line in lines if line.rstrip() != line),
            "mixed_indentation": bool(re.search(r'^\t', ''.join(lines))) and bool(re.search(r'^ {4}', ''.join(lines)))
        }
        return issues

    def _check_test_hints(self, content: str) -> List[str]:
        """Look for testing-related patterns"""
        hints = []
        if "assert" in content and "def test" not in content:
            hints.append("Uses assertions but no test functions found")
        if re.search(r'if __name__.*test', content, re.I):
            hints.append("Has test code in main block")
        return hints

    def _check_security_patterns(self, content: str) -> List[str]:
        """Check for potential security issues"""
        concerns = []
        patterns = {
            r'eval\s*\(': "Uses eval() - potential security risk",
            r'exec\s*\(': "Uses exec() - potential security risk",
            r'pickle\.loads': "Uses pickle.loads - potential security risk",
            r'subprocess.*shell\s*=\s*True': "Uses shell=True in subprocess",
            r'\.execute\s*\(.*%': "Possible SQL injection vulnerability"
        }
        
        for pattern, message in patterns.items():
            if re.search(pattern, content):
                concerns.append(message)
                
        return concerns

    def _check_performance_patterns(self, content: str) -> List[str]:
        """Check for performance anti-patterns"""
        hints = []
        patterns = {
            r'for.*in.*\.keys\(\)': "Iterating over .keys() unnecessarily",
            r'\+\s*=.*loop': "String concatenation in loop",
            r'sleep\s*\(': "Uses sleep() - consider async alternatives"
        }
        
        for pattern, message in patterns.items():
            if re.search(pattern, content, re.I):
                hints.append(message)
                
        return hints

    def format_context_summary(self) -> str:
        """Format context as human-readable summary"""
        context = self.gather_all_context()
        
        summary = f"""
=== Code Context Analysis: {self.file_name} ===

📄 File Info:
- Size: {context['file_info']['size_bytes']:,} bytes ({context['file_info']['lines_of_code']} lines)
- Last modified: {context['file_info']['last_modified']}

🏗️ Structure:
- Classes: {len(context['code_structure'].get('classes', []))}
- Functions: {len(context['code_structure'].get('functions', []))}
- Async Functions: {len(context['code_structure'].get('async_functions', []))}

📚 Documentation:
- Module docstring: {'Yes' if context['documentation'].get('module_doc') else 'No'}
- Documented classes: {len(context['documentation'].get('classes', {}))}
- Documented functions: {len(context['documentation'].get('functions', {}))}

🔗 Dependencies:
- Standard library: {len(context['dependencies'].get('stdlib', []))}
- Third-party: {len(context['dependencies'].get('third_party', []))}
- Local imports: {len(context['dependencies'].get('local', []))}

🎯 Code Patterns:
- Uses type hints: {context['code_patterns'].get('uses_type_hints', False)}
- Has error handling: {context['code_patterns'].get('has_error_handling', False)}
- Uses async/await: {context['code_patterns'].get('uses_async', False)}
- Has TODOs: {context['code_patterns'].get('has_todos', False)}

📊 Quality Indicators:
- Docstring coverage: {context['quality_indicators']['has_docstrings'].get('coverage_percent', 0):.1f}%
- Long lines (>88 chars): {context['quality_indicators']['follows_pep8'].get('long_lines', 0)}
- Security concerns: {len(context['quality_indicators'].get('security_concerns', []))}
- Performance hints: {len(context['quality_indicators'].get('performance_hints', []))}
"""
        
        if context.get('recent_changes'):
            summary += f"""
📝 Recent Changes:
- Recent commits: {len(context['recent_changes'].get('recent_commits', []))}
- Uncommitted changes: {'Yes' if context['recent_changes'].get('has_uncommitted_changes') else 'No'}
"""

        if context.get('project_context'):
            summary += f"""
🏢 Project Context:
- Framework: {context['project_context'].get('framework', 'None detected')}
- Project type: {context['project_context'].get('project_type', 'Unknown')}
- Config files: {', '.join(context['project_context'].get('config_files', []))}
"""
        
        return summary


def main():
    if len(sys.argv) < 2:
        print("Usage: gather-code-context.py <file>")
        sys.exit(1)
        
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
        
    gatherer = CodeContextGatherer(file_path)
    
    # Check for JSON output flag
    if "--json" in sys.argv:
        context = gatherer.gather_all_context()
        print(json.dumps(context, indent=2, default=str))
    else:
        print(gatherer.format_context_summary())
        
    # Optionally save to file
    if "--save" in sys.argv:
        context = gatherer.gather_all_context()
        output_file = file_path.with_suffix('.context.json')
        with open(output_file, 'w') as f:
            json.dump(context, f, indent=2, default=str)
        print(f"\nContext saved to: {output_file}")


if __name__ == "__main__":
    main()