#!/usr/bin/env python3
"""
Code Context Gatherer - Mimics human code review workflows
Gathers comprehensive contextual information for enhanced AI code reviews
"""

import sys
import ast
import subprocess
from pathlib import Path
from datetime import datetime
import re
from typing import Dict, List, Optional
from collections import Counter
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
        except subprocess.CalledProcessError:
            # Not a git repository
            return False
        except FileNotFoundError:
            print("Warning: git command not found, skipping git-based analysis")
            return False
        except Exception as e:
            print(f"Warning: Git repository check failed ({e}), skipping git-based analysis")
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
            "quality_indicators": self._analyze_quality_indicators(),
            "advanced_analysis": self._get_advanced_analysis(),
            "test_coverage": self._analyze_test_coverage(),
            "performance_hints": self._analyze_performance_patterns(),
            "security_analysis": self._analyze_security_patterns(),
            "refactoring_opportunities": self._identify_refactoring_opportunities(),
            "error_patterns": self._analyze_error_patterns(),
            "dependency_health": self._check_dependency_health(),
            "python_specific": self._analyze_python_specific() if self.file_path.suffix == '.py' else None,
            "multi_tool_analysis": self._run_multi_tool_analysis()
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
                except (toml.TomlDecodeError, KeyError) as e:
                    print(f"Warning: Could not parse {file} ({e})")
                except Exception as e:
                    print(f"Warning: Error reading {file} ({e})")

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
        except (SyntaxError, UnicodeDecodeError) as e:
            print(f"Warning: Could not parse file for docstring analysis ({e})")
            return {"error": f"Parse error: {e}"}
        except Exception as e:
            print(f"Warning: Docstring analysis failed ({e})")
            return {"error": f"Analysis failed: {e}"}

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

    def _analyze_test_coverage(self) -> Dict:
        """Analyze test coverage and test patterns"""
        with open(self.file_path) as f:
            content = f.read()

        is_test_file = self.file_path.name.startswith('test_') or 'test' in self.file_path.name

        coverage = {
            "is_test_file": is_test_file,
            "test_functions": len(re.findall(r'def test_\w+', content)),
            "assertion_count": len(re.findall(r'\bassert\b', content)),
            "mock_usage": bool(re.search(r'mock|Mock|patch', content)),
            "async_tests": len(re.findall(r'async def test_', content)),
            "fixtures_used": len(re.findall(r'@pytest\.fixture', content)),
            "parametrized_tests": len(re.findall(r'@pytest\.mark\.parametrize', content))
        }

        if not is_test_file:
            # Look for corresponding test files
            test_patterns = [
                f"test_{self.file_path.stem}.py",
                f"{self.file_path.stem}_test.py"
            ]
            coverage["has_test_file"] = any(
                (self.directory.parent / "tests" / pattern).exists()
                for pattern in test_patterns
            )

        return coverage

    def _analyze_performance_patterns(self) -> List[str]:
        """Enhanced performance pattern analysis"""
        with open(self.file_path) as f:
            content = f.read()

        patterns = []

        # Performance anti-patterns
        if re.search(r'for.*in.*range\(len\(', content):
            patterns.append("Using range(len()) instead of enumerate or direct iteration")

        if re.search(r'\.append\(.*\)\s*\n.*for.*in', content, re.MULTILINE):
            patterns.append("List comprehension opportunity detected")

        if re.search(r'global\s+\w+', content):
            patterns.append("Global variable usage may impact performance")

        if re.search(r'time\.sleep\(', content):
            patterns.append("Blocking sleep calls - consider async alternatives")

        if re.search(r'subprocess\.(call|run).*shell=True', content):
            patterns.append("Shell=True in subprocess - security and performance concern")

        # Memory patterns
        if re.search(r'\.copy\(\)', content):
            patterns.append("Data copying detected - verify if necessary")

        if re.search(r'pickle\.(dump|load)', content):
            patterns.append("Pickle usage - consider faster serialization alternatives")

        return patterns

    def _analyze_security_patterns(self) -> Dict:
        """Enhanced security pattern analysis"""
        with open(self.file_path) as f:
            content = f.read()

        security = {
            "high_risk": [],
            "medium_risk": [],
            "low_risk": [],
            "good_practices": []
        }

        # High risk patterns
        if re.search(r'eval\s*\(', content):
            security["high_risk"].append("eval() usage - arbitrary code execution risk")

        if re.search(r'exec\s*\(', content):
            security["high_risk"].append("exec() usage - arbitrary code execution risk")

        if re.search(r'pickle\.loads?\s*\(', content):
            security["high_risk"].append("pickle.load() - arbitrary code execution risk")

        # Medium risk patterns
        if re.search(r'subprocess.*shell=True', content):
            security["medium_risk"].append("shell=True in subprocess - command injection risk")

        if re.search(r'input\s*\(.*\)', content):
            security["medium_risk"].append("input() usage - validate user input")

        if re.search(r'open\s*\(.*[\'"]w[\'"]', content):
            security["medium_risk"].append("File writing - ensure path validation")

        # Low risk patterns
        if re.search(r'random\.random\(\)', content):
            security["low_risk"].append("random.random() - not cryptographically secure")

        # Good practices
        if re.search(r'with\s+open\s*\(', content):
            security["good_practices"].append("Using context managers for file operations")

        if re.search(r'try:\s*.*except.*:', content, re.DOTALL):
            security["good_practices"].append("Exception handling implemented")

        return security

    def _identify_refactoring_opportunities(self) -> Dict:
        """Identify code refactoring opportunities"""
        with open(self.file_path) as f:
            content = f.read()
            lines = content.splitlines()

        opportunities = {
            "duplicate_code": [],
            "long_functions": [],
            "complex_conditions": [],
            "magic_numbers": [],
            "naming_improvements": []
        }

        # Find potential duplicate code blocks
        line_groups = {}
        for i, line in enumerate(lines):
            clean_line = line.strip()
            if len(clean_line) > 20 and not clean_line.startswith('#'):
                if clean_line in line_groups:
                    line_groups[clean_line].append(i + 1)
                else:
                    line_groups[clean_line] = [i + 1]

        for line, occurrences in line_groups.items():
            if len(occurrences) > 1:
                opportunities["duplicate_code"].append({
                    "line": line[:50] + "..." if len(line) > 50 else line,
                    "occurrences": occurrences
                })

        # Find magic numbers
        magic_numbers = re.findall(r'\b(?<!\.)\d{2,}\b(?!\s*[),])', content)
        if magic_numbers:
            opportunities["magic_numbers"] = list(set(magic_numbers))

        # Find complex boolean conditions
        complex_conditions = re.findall(r'if\s+.*(?:and|or).*(?:and|or)', content)
        if complex_conditions:
            opportunities["complex_conditions"] = [cond.strip() for cond in complex_conditions[:3]]

        # Find single-letter variable names (except common ones)
        single_letter_vars = re.findall(r'\b([a-z])\s*=', content)
        bad_names = [var for var in single_letter_vars if var not in ['i', 'j', 'k', 'x', 'y', 'z']]
        if bad_names:
            opportunities["naming_improvements"] = list(set(bad_names))

        return opportunities

    def _analyze_error_patterns(self) -> Dict:
        """Analyze error handling patterns"""
        with open(self.file_path) as f:
            content = f.read()

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            print(f"Warning: Syntax error in file ({e})")
            return {"error": f"Syntax error: {e}"}
        except Exception as e:
            print(f"Warning: Could not parse file ({e})")
            return {"error": f"Parse error: {e}"}

        patterns = {
            "exception_handling": {
                "try_blocks": 0,
                "bare_except": 0,
                "specific_exceptions": [],
                "finally_blocks": 0,
                "reraise_patterns": 0
            },
            "error_logging": {
                "has_logging": bool(re.search(r'logging\.|logger\.', content)),
                "print_debugging": len(re.findall(r'print\s*\(.*debug|error|exception', content, re.I)),
                "error_messages": len(re.findall(r'raise\s+\w+\s*\(', content))
            },
            "defensive_programming": {
                "assertions": len(re.findall(r'\bassert\b', content)),
                "type_checks": len(re.findall(r'isinstance\s*\(', content)),
                "none_checks": len(re.findall(r'if.*is None|if.*is not None', content))
            }
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                patterns["exception_handling"]["try_blocks"] += 1
                if node.finalbody:
                    patterns["exception_handling"]["finally_blocks"] += 1

                for handler in node.handlers:
                    if handler.type is None:
                        patterns["exception_handling"]["bare_except"] += 1
                    else:
                        if hasattr(handler.type, 'id'):
                            patterns["exception_handling"]["specific_exceptions"].append(handler.type.id)

            elif isinstance(node, ast.Raise):
                if node.exc is None:  # bare raise
                    patterns["exception_handling"]["reraise_patterns"] += 1

        return patterns

    def _check_dependency_health(self) -> Dict:
        """Check dependency health and update opportunities"""
        health = {
            "import_analysis": {},
            "circular_imports": [],
            "unused_imports": [],
            "deprecated_usage": []
        }

        try:
            with open(self.file_path) as f:
                content = f.read()
                tree = ast.parse(content)
        except (SyntaxError, UnicodeDecodeError) as e:
            print(f"Warning: Could not parse file for dependency analysis ({e})")
            return {"error": f"Parse error: {e}"}
        except Exception as e:
            print(f"Warning: Dependency health check failed ({e})")
            return {"error": f"Analysis failed: {e}"}

        # Collect all imports
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for alias in node.names:
                        imports.append(f"{node.module}.{alias.name}")

        # Check for deprecated patterns
        deprecated_patterns = [
            (r'imp\s+import', "imp module is deprecated, use importlib"),
            (r'from __future__ import print_function', "print_function future import not needed in Python 3"),
            (r'collections\.Mapping', "collections.Mapping deprecated, use collections.abc.Mapping"),
            (r'datetime\.datetime\.utcnow', "utcnow() deprecated, use datetime.now(timezone.utc)")
        ]

        for pattern, message in deprecated_patterns:
            if re.search(pattern, content):
                health["deprecated_usage"].append(message)

        health["import_analysis"]["total_imports"] = len(imports)
        health["import_analysis"]["unique_modules"] = len(set(imp.split('.')[0] for imp in imports))

        return health

    def _analyze_python_specific(self) -> Dict:
        """Python-specific deep analysis"""
        try:
            with open(self.file_path) as f:
                content = f.read()
                tree = ast.parse(content)
        except (SyntaxError, UnicodeDecodeError) as e:
            print(f"Warning: Could not parse file for Python-specific analysis ({e})")
            return {"error": f"Parse error: {e}"}
        except Exception as e:
            print(f"Warning: Python-specific analysis failed ({e})")
            return {"error": f"Analysis failed: {e}"}

        analysis = {
            "import_analysis": self._detailed_import_analysis(tree),
            "call_hierarchy": self._analyze_call_hierarchy(tree),
            "class_hierarchy": self._analyze_class_hierarchy(tree),
            "exception_patterns": self._detailed_exception_analysis(tree),
            "type_hints_analysis": self._analyze_type_hints(tree, content),
            "docstring_analysis": self._detailed_docstring_analysis(tree),
            "dependency_origins": self._analyze_dependency_origins(tree),
            "complexity_hotspots": self._identify_complexity_hotspots(tree),
            "method_overrides": self._find_method_overrides(tree),
            "decorator_usage": self._analyze_decorator_usage(tree)
        }

        return analysis

    def _run_multi_tool_analysis(self) -> Dict:
        """Run comprehensive multi-tool analysis"""
        try:
            script_dir = Path(__file__).parent
            tool_matrix_script = script_dir / "tool-integration-matrix.py"

            if not tool_matrix_script.exists():
                return {"error": "Tool integration matrix not found"}

            result = subprocess.run([
                sys.executable, str(tool_matrix_script), str(self.file_path), "--json"
            ], capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {"error": f"Tool matrix failed: {result.stderr}"}

        except subprocess.TimeoutExpired:
            return {"error": "Multi-tool analysis timed out"}
        except Exception as e:
            return {"error": f"Multi-tool analysis error: {str(e)}"}

    def _detailed_import_analysis(self, tree: ast.AST) -> Dict:
        """Detailed import analysis with line numbers and types"""
        imports = {
            "standard_library": [],
            "third_party": [],
            "local": [],
            "from_imports": [],
            "star_imports": [],
            "conditional_imports": []
        }

        # Known standard library modules (subset)
        stdlib_modules = {
            'os', 'sys', 'ast', 'json', 're', 'pathlib', 'datetime', 'time',
            'subprocess', 'typing', 'collections', 'itertools', 'functools',
            'asyncio', 'threading', 'multiprocessing', 'logging', 'unittest',
            'argparse', 'configparser', 'tempfile', 'shutil', 'glob', 'math',
            'random', 'string', 'io', 'csv', 'xml', 'http', 'urllib', 'socket'
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name.split('.')[0]
                    import_info = {
                        "module": alias.name,
                        "alias": alias.asname,
                        "line": node.lineno
                    }

                    if module_name in stdlib_modules:
                        imports["standard_library"].append(import_info)
                    elif module_name.startswith('.'):
                        imports["local"].append(import_info)
                    else:
                        imports["third_party"].append(import_info)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module_name = node.module.split('.')[0]
                    for alias in node.names:
                        if alias.name == '*':
                            imports["star_imports"].append({
                                "module": node.module,
                                "line": node.lineno
                            })
                        else:
                            import_info = {
                                "module": node.module,
                                "name": alias.name,
                                "alias": alias.asname,
                                "line": node.lineno
                            }
                            imports["from_imports"].append(import_info)

        return imports

    def _analyze_call_hierarchy(self, tree: ast.AST) -> Dict:
        """Analyze function call relationships"""
        call_graph = {
            "functions": {},
            "method_calls": {},
            "external_calls": set(),
            "recursive_calls": []
        }

        # First pass: collect all function definitions
        defined_functions = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                defined_functions.add(node.name)

        # Second pass: analyze calls within each function
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                calls_made = set()
                method_calls = set()

                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if hasattr(child.func, 'id'):  # Simple function call
                            func_name = child.func.id
                            calls_made.add(func_name)

                            # Check for recursion
                            if func_name == node.name:
                                call_graph["recursive_calls"].append(node.name)

                        elif hasattr(child.func, 'attr'):  # Method call
                            method_name = child.func.attr
                            method_calls.add(method_name)

                            # Check if it's a call on self
                            if (hasattr(child.func, 'value') and
                                hasattr(child.func.value, 'id') and
                                child.func.value.id == 'self'):
                                calls_made.add(method_name)

                call_graph["functions"][node.name] = {
                    "calls": list(calls_made),
                    "method_calls": list(method_calls),
                    "line": node.lineno
                }

                # Identify external calls (not defined in this file)
                for call in calls_made:
                    if call not in defined_functions:
                        call_graph["external_calls"].add(call)

        call_graph["external_calls"] = list(call_graph["external_calls"])
        return call_graph

    def _analyze_class_hierarchy(self, tree: ast.AST) -> Dict:
        """Analyze class inheritance and structure"""
        classes = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Get base classes
                bases = []
                for base in node.bases:
                    if hasattr(base, 'id'):
                        bases.append(base.id)
                    elif hasattr(base, 'attr'):
                        bases.append(f"{base.value.id}.{base.attr}" if hasattr(base.value, 'id') else base.attr)

                # Get methods and properties
                methods = []
                properties = []
                class_variables = []

                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_info = {
                            "name": item.name,
                            "line": item.lineno,
                            "is_private": item.name.startswith('_'),
                            "is_dunder": item.name.startswith('__') and item.name.endswith('__'),
                            "decorators": [d.id for d in item.decorator_list if hasattr(d, 'id')]
                        }

                        # Check for property decorator
                        if any(d == 'property' for d in method_info["decorators"]):
                            properties.append(method_info)
                        else:
                            methods.append(method_info)

                    elif isinstance(item, ast.AnnAssign) and hasattr(item.target, 'id'):
                        class_variables.append({
                            "name": item.target.id,
                            "type": ast.unparse(item.annotation) if item.annotation else None,
                            "line": item.lineno
                        })

                classes[node.name] = {
                    "line": node.lineno,
                    "bases": bases,
                    "methods": methods,
                    "properties": properties,
                    "class_variables": class_variables,
                    "decorators": [d.id for d in node.decorator_list if hasattr(d, 'id')]
                }

        return classes

    def _detailed_exception_analysis(self, tree: ast.AST) -> Dict:
        """Detailed exception handling analysis"""
        exceptions = {
            "try_blocks": [],
            "exception_types": Counter(),
            "bare_except_locations": [],
            "finally_blocks": [],
            "raise_statements": [],
            "exception_chaining": []
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                try_info = {
                    "line": node.lineno,
                    "handlers": [],
                    "has_finally": bool(node.finalbody),
                    "has_else": bool(node.orelse)
                }

                for handler in node.handlers:
                    handler_info = {"line": handler.lineno}

                    if handler.type is None:
                        exceptions["bare_except_locations"].append(handler.lineno)
                        handler_info["type"] = "bare_except"
                    else:
                        if hasattr(handler.type, 'id'):
                            exc_type = handler.type.id
                        elif hasattr(handler.type, 'elts'):  # Multiple exceptions
                            exc_type = [e.id for e in handler.type.elts if hasattr(e, 'id')]
                        else:
                            exc_type = ast.unparse(handler.type)

                        handler_info["type"] = exc_type
                        exceptions["exception_types"][str(exc_type)] += 1

                    if handler.name:
                        handler_info["name"] = handler.name.id if hasattr(handler.name, 'id') else str(handler.name)

                    try_info["handlers"].append(handler_info)

                exceptions["try_blocks"].append(try_info)

                if node.finalbody:
                    exceptions["finally_blocks"].append(node.lineno)

            elif isinstance(node, ast.Raise):
                raise_info = {"line": node.lineno}

                if node.exc:
                    if hasattr(node.exc, 'func') and hasattr(node.exc.func, 'id'):
                        raise_info["exception"] = node.exc.func.id
                    else:
                        raise_info["exception"] = ast.unparse(node.exc)
                else:
                    raise_info["exception"] = "re-raise"

                if node.cause:  # Exception chaining (raise ... from ...)
                    exceptions["exception_chaining"].append({
                        "line": node.lineno,
                        "cause": ast.unparse(node.cause)
                    })

                exceptions["raise_statements"].append(raise_info)

        return exceptions

    def _analyze_type_hints(self, tree: ast.AST, content: str) -> Dict:
        """Analyze type hint usage"""
        type_hints = {
            "function_annotations": [],
            "variable_annotations": [],
            "return_annotations": [],
            "type_imports": [],
            "generic_usage": [],
            "coverage_stats": {}
        }

        # Check for typing imports
        typing_imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == 'typing':
                for alias in node.names:
                    typing_imports.add(alias.name)
                    type_hints["type_imports"].append(alias.name)

        # Analyze function annotations
        total_functions = 0
        annotated_functions = 0
        total_params = 0
        annotated_params = 0

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                total_functions += 1

                # Check return annotation
                if node.returns:
                    annotated_functions += 1
                    type_hints["return_annotations"].append({
                        "function": node.name,
                        "return_type": ast.unparse(node.returns),
                        "line": node.lineno
                    })

                # Check parameter annotations
                for arg in node.args.args:
                    total_params += 1
                    if arg.annotation:
                        annotated_params += 1
                        type_hints["function_annotations"].append({
                            "function": node.name,
                            "parameter": arg.arg,
                            "type": ast.unparse(arg.annotation),
                            "line": node.lineno
                        })

                        # Check for generic usage
                        type_str = ast.unparse(arg.annotation)
                        if any(generic in type_str for generic in ['List', 'Dict', 'Optional', 'Union', 'Tuple']):
                            type_hints["generic_usage"].append({
                                "location": f"{node.name}.{arg.arg}",
                                "type": type_str
                            })

            elif isinstance(node, ast.AnnAssign):
                # Variable annotations
                if hasattr(node.target, 'id'):
                    type_hints["variable_annotations"].append({
                        "variable": node.target.id,
                        "type": ast.unparse(node.annotation),
                        "line": node.lineno
                    })

        # Calculate coverage statistics
        type_hints["coverage_stats"] = {
            "function_return_coverage": (annotated_functions / total_functions * 100) if total_functions > 0 else 0,
            "parameter_coverage": (annotated_params / total_params * 100) if total_params > 0 else 0,
            "total_functions": total_functions,
            "annotated_functions": annotated_functions,
            "total_parameters": total_params,
            "annotated_parameters": annotated_params
        }

        return type_hints

    def _detailed_docstring_analysis(self, tree: ast.AST) -> Dict:
        """Detailed docstring analysis"""
        docstrings = {
            "module_docstring": None,
            "class_docstrings": [],
            "function_docstrings": [],
            "missing_docstrings": [],
            "docstring_styles": Counter()
        }

        # Module docstring
        if (tree.body and isinstance(tree.body[0], ast.Expr) and
            isinstance(tree.body[0].value, ast.Constant) and
            isinstance(tree.body[0].value.value, str)):
            docstrings["module_docstring"] = {
                "content": tree.body[0].value.value.split('\n')[0],  # First line only
                "length": len(tree.body[0].value.value),
                "line": tree.body[0].lineno
            }

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                docstring = ast.get_docstring(node)
                if docstring:
                    docstrings["class_docstrings"].append({
                        "class": node.name,
                        "summary": docstring.split('\n')[0],
                        "length": len(docstring),
                        "line": node.lineno,
                        "style": self._detect_docstring_style(docstring)
                    })
                    docstrings["docstring_styles"][self._detect_docstring_style(docstring)] += 1
                else:
                    docstrings["missing_docstrings"].append(f"class {node.name}")

            elif isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node)
                if docstring:
                    docstrings["function_docstrings"].append({
                        "function": node.name,
                        "summary": docstring.split('\n')[0],
                        "length": len(docstring),
                        "line": node.lineno,
                        "style": self._detect_docstring_style(docstring)
                    })
                    docstrings["docstring_styles"][self._detect_docstring_style(docstring)] += 1
                else:
                    # Skip private and dunder methods for missing docstring reporting
                    if not node.name.startswith('_'):
                        docstrings["missing_docstrings"].append(f"function {node.name}")

        return docstrings

    def _detect_docstring_style(self, docstring: str) -> str:
        """Detect docstring style (Google, NumPy, Sphinx, etc.)"""
        if 'Args:' in docstring or 'Arguments:' in docstring:
            return 'Google'
        elif 'Parameters' in docstring and '----------' in docstring:
            return 'NumPy'
        elif ':param' in docstring or ':return' in docstring:
            return 'Sphinx'
        else:
            return 'Plain'

    def _analyze_dependency_origins(self, tree: ast.AST) -> Dict:
        """Analyze where dependencies come from"""
        import importlib.util

        dependencies = {
            "builtin_modules": [],
            "standard_library": [],
            "third_party": [],
            "local_modules": [],
            "unresolved": []
        }

        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split('.')[0])

        for module_name in imports:
            try:
                spec = importlib.util.find_spec(module_name)
                if spec is None:
                    dependencies["unresolved"].append(module_name)
                elif spec.origin is None:  # Builtin module
                    dependencies["builtin_modules"].append(module_name)
                elif 'site-packages' in str(spec.origin):
                    dependencies["third_party"].append(module_name)
                elif str(spec.origin).startswith('/usr') or 'python' in str(spec.origin):
                    dependencies["standard_library"].append(module_name)
                else:
                    dependencies["local_modules"].append(module_name)
            except (ImportError, ValueError, ModuleNotFoundError):
                dependencies["unresolved"].append(module_name)

        return dependencies

    def _identify_complexity_hotspots(self, tree: ast.AST) -> List[Dict]:
        """Identify complexity hotspots in the code"""
        hotspots = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_cyclomatic_complexity(node)

                # Consider functions with complexity > 10 as hotspots
                if complexity > 10:
                    hotspots.append({
                        "function": node.name,
                        "complexity": complexity,
                        "line": node.lineno,
                        "length": len(node.body)
                    })

        return sorted(hotspots, key=lambda x: x["complexity"], reverse=True)

    def _calculate_cyclomatic_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity for a function"""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, ast.comprehension):
                complexity += 1
                for if_clause in child.ifs:
                    complexity += 1

        return complexity

    def _find_method_overrides(self, tree: ast.AST) -> Dict:
        """Find method overrides in classes"""
        overrides = {}

        # Common methods that are often overridden
        common_overrides = {
            '__init__', '__str__', '__repr__', '__eq__', '__hash__',
            '__len__', '__iter__', '__getitem__', '__setitem__',
            '__enter__', '__exit__', '__call__'
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_methods = set()
                override_methods = []

                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        class_methods.add(item.name)

                        if item.name in common_overrides:
                            override_methods.append({
                                "method": item.name,
                                "line": item.lineno
                            })

                if override_methods:
                    overrides[node.name] = override_methods

        return overrides

    def _analyze_decorator_usage(self, tree: ast.AST) -> Dict:
        """Analyze decorator usage patterns"""
        decorators = {
            "function_decorators": Counter(),
            "class_decorators": Counter(),
            "custom_decorators": [],
            "builtin_decorators": []
        }

        builtin_decorator_names = {
            'property', 'staticmethod', 'classmethod', 'abstractmethod',
            'cached_property', 'lru_cache', 'wraps', 'dataclass'
        }

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                for decorator in node.decorator_list:
                    if hasattr(decorator, 'id'):
                        dec_name = decorator.id
                    elif hasattr(decorator, 'attr'):
                        dec_name = decorator.attr
                    else:
                        dec_name = ast.unparse(decorator)

                    if isinstance(node, ast.FunctionDef):
                        decorators["function_decorators"][dec_name] += 1
                    else:
                        decorators["class_decorators"][dec_name] += 1

                    if dec_name in builtin_decorator_names:
                        decorators["builtin_decorators"].append({
                            "name": dec_name,
                            "target": node.name,
                            "line": node.lineno
                        })
                    else:
                        decorators["custom_decorators"].append({
                            "name": dec_name,
                            "target": node.name,
                            "line": node.lineno
                        })

        return decorators

    def _get_advanced_analysis(self) -> Dict:
        """Get advanced AST-based analysis"""
        try:
            script_dir = Path(__file__).parent
            advanced_script = script_dir / "advanced-code-context.py"

            if not advanced_script.exists():
                return {"error": "Advanced analysis script not found"}

            result = subprocess.run(
                [sys.executable, str(advanced_script), str(self.file_path), "--json"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {"error": f"Advanced analysis failed: {result.stderr}"}

        except subprocess.TimeoutExpired:
            return {"error": "Advanced analysis timed out"}
        except Exception as e:
            return {"error": f"Advanced analysis error: {str(e)}"}

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

        # Advanced analysis
        advanced = context.get('advanced_analysis', {})
        if advanced and not advanced.get('error'):
            summary += """
🔬 Advanced Analysis:"""

            complexity = advanced.get('complexity_metrics', {})
            if complexity:
                total_complexity = complexity.get('total_complexity', 0)
                avg_complexity = complexity.get('average_complexity', 0)
                complex_funcs = complexity.get('complex_functions', [])
                summary += f"""
- Total complexity: {total_complexity} (avg: {avg_complexity:.1f})"""
                if complex_funcs:
                    summary += f"""
- Complex functions: {', '.join(complex_funcs)}"""

            call_graph = advanced.get('function_call_graph', {})
            if call_graph:
                recursive = call_graph.get('recursive_functions', [])
                max_depth = call_graph.get('max_call_depth', 0)
                summary += f"""
- Call depth: {max_depth}"""
                if recursive:
                    summary += f"""
- Recursive functions: {', '.join(recursive)}"""

            patterns = advanced.get('pattern_detection', {})
            if patterns:
                design_patterns = patterns.get('design_patterns', [])
                anti_patterns = patterns.get('anti_patterns', [])
                if design_patterns:
                    summary += f"""
- Design patterns: {', '.join(design_patterns)}"""
                if anti_patterns:
                    summary += f"""
- Anti-patterns: {', '.join(anti_patterns)}"""

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
