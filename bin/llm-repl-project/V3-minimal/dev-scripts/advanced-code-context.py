#!/usr/bin/env python3
"""
Advanced Code Context Analyzer
Implements comprehensive contextual analysis for enhanced code reviews
"""

import ast
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any, Union
from collections import defaultdict, Counter
import re
from dataclasses import dataclass


@dataclass
class FunctionInfo:
    name: str
    line: int
    args: List[str]
    returns: Optional[str]
    calls: Set[str]
    variables_used: Set[str]
    variables_modified: Set[str]
    complexity: int
    length: int
    decorators: List[str]
    exceptions_handled: List[str]
    exceptions_raised: List[str]


@dataclass
class ClassInfo:
    name: str
    line: int
    bases: List[str]
    methods: List[str]
    attributes: Set[str]
    decorators: List[str]


class AdvancedCodeAnalyzer:
    """Advanced AST-based code analysis"""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        with open(file_path) as f:
            self.content = f.read()
        try:
            self.tree = ast.parse(self.content)
        except SyntaxError as e:
            self.tree = None
            self.syntax_error = str(e)
        self.functions: Dict[str, FunctionInfo] = {}
        self.classes: Dict[str, ClassInfo] = {}
        self.global_variables: Set[str] = set()
        self.imports: Dict[str, List[str]] = defaultdict(list)
        
    def analyze_all(self) -> Dict[str, Any]:
        """Run all analysis methods"""
        if not self.tree:
            return {"error": f"Syntax error: {getattr(self, 'syntax_error', 'Unknown')}"}
            
        results = {
            "ast_analysis": self._analyze_ast(),
            "function_call_graph": self._build_call_graph(),
            "variable_analysis": self._analyze_variables(),
            "complexity_metrics": self._calculate_complexity_metrics(),
            "control_flow": self._analyze_control_flow(),
            "data_flow": self._analyze_data_flow(),
            "pattern_detection": self._detect_patterns(),
            "type_analysis": self._analyze_types(),
            "error_handling": self._analyze_error_handling(),
            "dependency_details": self._analyze_dependencies_detailed(),
            "code_metrics": self._calculate_code_metrics()
        }
        
        # Add external tool analysis if available
        results.update(self._run_external_tools())
        
        return results
    
    def _analyze_ast(self) -> Dict[str, Any]:
        """Comprehensive AST analysis"""
        visitor = ASTVisitor()
        visitor.visit(self.tree)
        
        return {
            "functions": {name: {
                "line": func.line,
                "args": func.args,
                "returns": func.returns,
                "complexity": func.complexity,
                "length": func.length,
                "decorators": func.decorators,
                "calls_made": list(func.calls),
                "variables_used": list(func.variables_used),
                "variables_modified": list(func.variables_modified),
                "exceptions_handled": func.exceptions_handled,
                "exceptions_raised": func.exceptions_raised
            } for name, func in visitor.functions.items()},
            "classes": {name: {
                "line": cls.line,
                "bases": cls.bases,
                "methods": cls.methods,
                "attributes": list(cls.attributes),
                "decorators": cls.decorators
            } for name, cls in visitor.classes.items()},
            "global_variables": list(visitor.global_variables),
            "imports": dict(visitor.imports),
            "entry_points": visitor.entry_points,
            "decorators_used": list(visitor.all_decorators),
            "async_usage": {
                "async_functions": visitor.async_functions,
                "await_calls": visitor.await_calls,
                "async_generators": visitor.async_generators
            }
        }
    
    def _build_call_graph(self) -> Dict[str, Any]:
        """Build function call graph"""
        visitor = CallGraphVisitor()
        visitor.visit(self.tree)
        
        # Find cycles in call graph
        cycles = self._find_cycles(visitor.call_graph)
        
        # Calculate call depth
        call_depths = self._calculate_call_depths(visitor.call_graph)
        
        return {
            "call_graph": dict(visitor.call_graph),
            "reverse_calls": dict(visitor.reverse_calls),
            "external_calls": list(visitor.external_calls),
            "recursive_functions": list(visitor.recursive_functions),
            "call_cycles": cycles,
            "max_call_depth": max(call_depths.values()) if call_depths else 0,
            "call_depths": call_depths,
            "most_called_functions": visitor.get_most_called(5),
            "leaf_functions": visitor.get_leaf_functions()
        }
    
    def _analyze_variables(self) -> Dict[str, Any]:
        """Analyze variable usage patterns"""
        visitor = VariableAnalyzer()
        visitor.visit(self.tree)
        
        return {
            "variable_scopes": dict(visitor.scopes),
            "variable_assignments": dict(visitor.assignments),
            "variable_reads": dict(visitor.reads),
            "unused_variables": list(visitor.get_unused_variables()),
            "global_modifications": list(visitor.global_modifications),
            "nonlocal_usage": list(visitor.nonlocal_usage),
            "variable_shadowing": list(visitor.find_shadowing()),
            "mutable_defaults": list(visitor.mutable_defaults)
        }
    
    def _calculate_complexity_metrics(self) -> Dict[str, Any]:
        """Calculate various complexity metrics"""
        visitor = ComplexityAnalyzer()
        visitor.visit(self.tree)
        
        return {
            "cyclomatic_complexity": visitor.complexity_by_function,
            "nesting_depth": visitor.max_nesting_by_function,
            "function_lengths": visitor.function_lengths,
            "parameter_counts": visitor.parameter_counts,
            "total_complexity": sum(visitor.complexity_by_function.values()),
            "average_complexity": (
                sum(visitor.complexity_by_function.values()) / len(visitor.complexity_by_function)
                if visitor.complexity_by_function else 0
            ),
            "complex_functions": [
                name for name, complexity in visitor.complexity_by_function.items()
                if complexity > 10
            ],
            "long_functions": [
                name for name, length in visitor.function_lengths.items()
                if length > 50
            ],
            "many_parameters": [
                name for name, count in visitor.parameter_counts.items()
                if count > 5
            ]
        }
    
    def _analyze_control_flow(self) -> Dict[str, Any]:
        """Analyze control flow patterns"""
        visitor = ControlFlowAnalyzer()
        visitor.visit(self.tree)
        
        return {
            "conditional_complexity": visitor.conditional_complexity,
            "loop_patterns": visitor.loop_patterns,
            "early_returns": visitor.early_returns,
            "nested_loops": visitor.nested_loops,
            "break_continue_usage": visitor.break_continue,
            "exception_flow": visitor.exception_flow,
            "generator_usage": visitor.generators
        }
    
    def _analyze_data_flow(self) -> Dict[str, Any]:
        """Analyze data flow patterns"""
        visitor = DataFlowAnalyzer()
        visitor.visit(self.tree)
        
        return {
            "return_patterns": visitor.return_patterns,
            "side_effects": visitor.side_effects,
            "state_modifications": visitor.state_modifications,
            "closure_variables": visitor.closure_variables,
            "global_state_access": visitor.global_access
        }
    
    def _detect_patterns(self) -> Dict[str, Any]:
        """Detect common patterns and anti-patterns"""
        detector = PatternDetector(self.content, self.tree)
        return detector.detect_all()
    
    def _analyze_types(self) -> Dict[str, Any]:
        """Analyze type usage and consistency"""
        visitor = TypeAnalyzer()
        visitor.visit(self.tree)
        
        return {
            "type_hints_coverage": visitor.calculate_type_coverage(),
            "type_annotations": visitor.type_annotations,
            "return_type_consistency": visitor.check_return_consistency(),
            "generic_usage": visitor.generic_usage,
            "union_types": visitor.union_types,
            "optional_types": visitor.optional_types
        }
    
    def _analyze_error_handling(self) -> Dict[str, Any]:
        """Analyze error handling patterns"""
        visitor = ErrorHandlingAnalyzer()
        visitor.visit(self.tree)
        
        return {
            "exception_handlers": visitor.exception_handlers,
            "bare_except": visitor.bare_except,
            "exception_types": list(visitor.exception_types),
            "finally_blocks": visitor.finally_blocks,
            "resource_management": visitor.resource_management,
            "error_propagation": visitor.error_propagation
        }
    
    def _analyze_dependencies_detailed(self) -> Dict[str, Any]:
        """Detailed dependency analysis"""
        visitor = DependencyAnalyzer()
        visitor.visit(self.tree)
        
        # Enhanced categorization
        stdlib_modules = self._get_stdlib_modules()
        categorized = {
            "standard_library": [],
            "third_party": [],
            "local": [],
            "dynamic": visitor.dynamic_imports,
            "conditional": visitor.conditional_imports
        }
        
        for module in visitor.all_imports:
            if module.startswith('.'):
                categorized["local"].append(module)
            elif module.split('.')[0] in stdlib_modules:
                categorized["standard_library"].append(module)
            else:
                categorized["third_party"].append(module)
        
        return {
            "categorized_imports": categorized,
            "import_cycles": visitor.potential_cycles,
            "unused_imports": visitor.unused_imports,
            "wildcard_imports": visitor.wildcard_imports,
            "relative_imports": visitor.relative_imports
        }
    
    def _calculate_code_metrics(self) -> Dict[str, Any]:
        """Calculate various code metrics"""
        lines = self.content.splitlines()
        
        return {
            "total_lines": len(lines),
            "code_lines": len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
            "comment_lines": len([l for l in lines if l.strip().startswith('#')]),
            "blank_lines": len([l for l in lines if not l.strip()]),
            "docstring_lines": self._count_docstring_lines(),
            "avg_line_length": sum(len(l) for l in lines) / len(lines) if lines else 0,
            "max_line_length": max(len(l) for l in lines) if lines else 0,
            "indentation_levels": self._analyze_indentation(lines)
        }
    
    def _run_external_tools(self) -> Dict[str, Any]:
        """Run external analysis tools if available"""
        results = {}
        
        # Try radon for complexity metrics
        try:
            radon_result = subprocess.run(
                ["radon", "cc", "-j", str(self.file_path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            if radon_result.returncode == 0:
                results["radon_complexity"] = json.loads(radon_result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            pass
        
        # Try pylint for additional analysis
        try:
            pylint_result = subprocess.run(
                ["pylint", "--output-format=json", str(self.file_path)],
                capture_output=True,
                text=True,
                timeout=15
            )
            if pylint_result.returncode in [0, 4, 8, 16]:  # Various pylint exit codes
                try:
                    pylint_data = json.loads(pylint_result.stdout)
                    results["pylint_analysis"] = self._process_pylint_output(pylint_data)
                except json.JSONDecodeError:
                    pass
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return results
    
    # Helper methods
    def _find_cycles(self, call_graph: Dict[str, Set[str]]) -> List[List[str]]:
        """Find cycles in call graph using DFS"""
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node: str, path: List[str]) -> None:
            if node in rec_stack:
                # Found a cycle
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return
            
            if node in visited:
                return
                
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in call_graph.get(node, set()):
                dfs(neighbor, path + [neighbor])
            
            rec_stack.remove(node)
        
        for node in call_graph:
            if node not in visited:
                dfs(node, [node])
        
        return cycles
    
    def _calculate_call_depths(self, call_graph: Dict[str, Set[str]]) -> Dict[str, int]:
        """Calculate maximum call depth for each function"""
        depths = {}
        
        def get_depth(func: str, visited: Set[str]) -> int:
            if func in visited:  # Cycle detected
                return 0
            if func in depths:
                return depths[func]
            
            visited.add(func)
            max_depth = 0
            
            for called_func in call_graph.get(func, set()):
                depth = get_depth(called_func, visited.copy())
                max_depth = max(max_depth, depth + 1)
            
            depths[func] = max_depth
            return max_depth
        
        for func in call_graph:
            get_depth(func, set())
        
        return depths
    
    def _count_docstring_lines(self) -> int:
        """Count lines in docstrings"""
        count = 0
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                docstring = ast.get_docstring(node)
                if docstring:
                    count += len(docstring.splitlines())
        return count
    
    def _analyze_indentation(self, lines: List[str]) -> Dict[str, int]:
        """Analyze indentation patterns"""
        indents = []
        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                indents.append(indent)
        
        return {
            "max_indentation": max(indents) if indents else 0,
            "avg_indentation": sum(indents) / len(indents) if indents else 0,
            "indentation_levels": len(set(indents))
        }
    
    def _get_stdlib_modules(self) -> Set[str]:
        """Get standard library module names"""
        return {
            'os', 'sys', 'ast', 'json', 're', 'pathlib', 'datetime', 'subprocess',
            'typing', 'collections', 'itertools', 'functools', 'math', 'random',
            'time', 'io', 'logging', 'unittest', 'asyncio', 'threading', 'multiprocessing',
            'urllib', 'http', 'email', 'html', 'xml', 'sqlite3', 'csv', 'configparser',
            'argparse', 'shutil', 'tempfile', 'glob', 'fnmatch', 'pickle', 'copy',
            'gc', 'weakref', 'abc', 'contextlib', 'dataclasses', 'enum', 'operator'
        }
    
    def _process_pylint_output(self, pylint_data: List[Dict]) -> Dict[str, Any]:
        """Process pylint output into useful metrics"""
        issues_by_type = defaultdict(int)
        issues_by_category = defaultdict(int)
        
        for issue in pylint_data:
            issues_by_type[issue.get('type', 'unknown')] += 1
            issues_by_category[issue.get('category', 'unknown')] += 1
        
        return {
            "total_issues": len(pylint_data),
            "issues_by_type": dict(issues_by_type),
            "issues_by_category": dict(issues_by_category),
            "critical_issues": [
                issue for issue in pylint_data 
                if issue.get('type') in ['error', 'fatal']
            ]
        }


# AST Visitor Classes
class ASTVisitor(ast.NodeVisitor):
    """Comprehensive AST visitor for code analysis"""
    
    def __init__(self):
        self.functions: Dict[str, FunctionInfo] = {}
        self.classes: Dict[str, ClassInfo] = {}
        self.global_variables: Set[str] = set()
        self.imports: Dict[str, List[str]] = defaultdict(list)
        self.entry_points: List[str] = []
        self.all_decorators: Set[str] = set()
        self.async_functions: List[str] = []
        self.await_calls: List[str] = []
        self.async_generators: List[str] = []
        self.current_function = None
        self.current_class = None
    
    def visit_FunctionDef(self, node):
        self._visit_function(node, is_async=False)
    
    def visit_AsyncFunctionDef(self, node):
        self._visit_function(node, is_async=True)
        self.async_functions.append(node.name)
    
    def _visit_function(self, node, is_async=False):
        old_function = self.current_function
        self.current_function = node.name
        
        # Analyze function
        args = [arg.arg for arg in node.args.args]
        returns = self._get_annotation(node.returns) if node.returns else None
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]
        
        # Track decorators
        self.all_decorators.update(decorators)
        
        # Create function info
        func_info = FunctionInfo(
            name=node.name,
            line=node.lineno,
            args=args,
            returns=returns,
            calls=set(),
            variables_used=set(),
            variables_modified=set(),
            complexity=self._calculate_complexity(node),
            length=self._calculate_function_length(node),
            decorators=decorators,
            exceptions_handled=[],
            exceptions_raised=[]
        )
        
        self.functions[node.name] = func_info
        
        # Visit function body
        self.generic_visit(node)
        
        self.current_function = old_function
    
    def visit_ClassDef(self, node):
        old_class = self.current_class
        self.current_class = node.name
        
        bases = [self._get_name(base) for base in node.bases]
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]
        methods = []
        attributes = set()
        
        # Find methods and attributes
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(item.name)
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attributes.add(target.id)
        
        self.classes[node.name] = ClassInfo(
            name=node.name,
            line=node.lineno,
            bases=bases,
            methods=methods,
            attributes=attributes,
            decorators=decorators
        )
        
        self.generic_visit(node)
        self.current_class = old_class
    
    def visit_Call(self, node):
        if self.current_function:
            func_name = self._get_call_name(node)
            if func_name:
                self.functions[self.current_function].calls.add(func_name)
        self.generic_visit(node)
    
    def visit_Await(self, node):
        if self.current_function:
            self.await_calls.append(self.current_function)
        self.generic_visit(node)
    
    def visit_If(self, node):
        if node.lineno == 1 and isinstance(node.test, ast.Compare):
            # Check for if __name__ == "__main__"
            if (isinstance(node.test.left, ast.Name) and 
                node.test.left.id == "__name__"):
                self.entry_points.append("__main__")
        self.generic_visit(node)
    
    # Helper methods
    def _get_annotation(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            return str(node.value)
        return "Unknown"
    
    def _get_decorator_name(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return "Unknown"
    
    def _get_name(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return "Unknown"
    
    def _get_call_name(self, node) -> Optional[str]:
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return f"{self._get_name(node.func.value)}.{node.func.attr}"
        return None
    
    def _calculate_complexity(self, node) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity
    
    def _calculate_function_length(self, node) -> int:
        """Calculate function length in lines"""
        if hasattr(node, 'end_lineno') and node.end_lineno:
            return node.end_lineno - node.lineno + 1
        # Fallback: count nodes
        return len(list(ast.walk(node)))


class CallGraphVisitor(ast.NodeVisitor):
    """Build function call graph"""
    
    def __init__(self):
        self.call_graph: Dict[str, Set[str]] = defaultdict(set)
        self.reverse_calls: Dict[str, Set[str]] = defaultdict(set)
        self.external_calls: Set[str] = set()
        self.recursive_functions: Set[str] = set()
        self.current_function = None
        self.defined_functions: Set[str] = set()
    
    def visit_FunctionDef(self, node):
        self.defined_functions.add(node.name)
        old_function = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = old_function
    
    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)
    
    def visit_Call(self, node):
        if self.current_function:
            called_func = self._get_call_name(node)
            if called_func:
                self.call_graph[self.current_function].add(called_func)
                self.reverse_calls[called_func].add(self.current_function)
                
                # Check for recursion
                if called_func == self.current_function:
                    self.recursive_functions.add(called_func)
                
                # Check if external call
                if called_func not in self.defined_functions:
                    self.external_calls.add(called_func)
        
        self.generic_visit(node)
    
    def _get_call_name(self, node) -> Optional[str]:
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr  # Just the method name
        return None
    
    def get_most_called(self, n: int) -> List[Tuple[str, int]]:
        """Get most called functions"""
        call_counts = Counter()
        for calls in self.reverse_calls.values():
            for caller in calls:
                call_counts[caller] += 1
        return call_counts.most_common(n)
    
    def get_leaf_functions(self) -> List[str]:
        """Get functions that don't call others"""
        return [func for func, calls in self.call_graph.items() if not calls]


class VariableAnalyzer(ast.NodeVisitor):
    """Analyze variable usage patterns"""
    
    def __init__(self):
        self.scopes: Dict[str, Set[str]] = defaultdict(set)
        self.assignments: Dict[str, List[int]] = defaultdict(list)
        self.reads: Dict[str, List[int]] = defaultdict(list)
        self.global_modifications: Set[str] = set()
        self.nonlocal_usage: Set[str] = set()
        self.mutable_defaults: List[str] = []
        self.current_scope = "global"
        self.scope_stack = ["global"]
    
    def visit_FunctionDef(self, node):
        # Check for mutable default arguments
        for default in node.args.defaults:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self.mutable_defaults.append(node.name)
        
        self._enter_scope(node.name)
        self.generic_visit(node)
        self._exit_scope()
    
    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)
    
    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.assignments[target.id].append(node.lineno)
                self.scopes[self.current_scope].add(target.id)
        self.generic_visit(node)
    
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.reads[node.id].append(node.lineno)
    
    def visit_Global(self, node):
        for name in node.names:
            self.global_modifications.add(name)
    
    def visit_Nonlocal(self, node):
        for name in node.names:
            self.nonlocal_usage.add(name)
    
    def _enter_scope(self, name: str):
        self.scope_stack.append(name)
        self.current_scope = name
    
    def _exit_scope(self):
        self.scope_stack.pop()
        self.current_scope = self.scope_stack[-1] if self.scope_stack else "global"
    
    def get_unused_variables(self) -> Set[str]:
        """Find variables that are assigned but never read"""
        unused = set()
        for var, assignments in self.assignments.items():
            if var not in self.reads or not self.reads[var]:
                unused.add(var)
        return unused
    
    def find_shadowing(self) -> List[str]:
        """Find variables that shadow outer scope variables"""
        shadowing = []
        # Simplified implementation
        global_vars = self.scopes.get("global", set())
        for scope, variables in self.scopes.items():
            if scope != "global":
                for var in variables:
                    if var in global_vars:
                        shadowing.append(f"{var} in {scope}")
        return shadowing


class ComplexityAnalyzer(ast.NodeVisitor):
    """Calculate complexity metrics"""
    
    def __init__(self):
        self.complexity_by_function: Dict[str, int] = {}
        self.max_nesting_by_function: Dict[str, int] = {}
        self.function_lengths: Dict[str, int] = {}
        self.parameter_counts: Dict[str, int] = {}
        self.current_function = None
        self.nesting_level = 0
        self.max_nesting = 0
    
    def visit_FunctionDef(self, node):
        old_function = self.current_function
        old_nesting = self.nesting_level
        old_max = self.max_nesting
        
        self.current_function = node.name
        self.nesting_level = 0
        self.max_nesting = 0
        
        # Calculate metrics
        self.complexity_by_function[node.name] = self._calculate_complexity(node)
        self.parameter_counts[node.name] = len(node.args.args)
        self.function_lengths[node.name] = self._calculate_length(node)
        
        self.generic_visit(node)
        
        self.max_nesting_by_function[node.name] = self.max_nesting
        
        self.current_function = old_function
        self.nesting_level = old_nesting
        self.max_nesting = old_max
    
    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)
    
    def visit_If(self, node):
        self._enter_nesting()
        self.generic_visit(node)
        self._exit_nesting()
    
    def visit_For(self, node):
        self._enter_nesting()
        self.generic_visit(node)
        self._exit_nesting()
    
    def visit_While(self, node):
        self._enter_nesting()
        self.generic_visit(node)
        self._exit_nesting()
    
    def visit_With(self, node):
        self._enter_nesting()
        self.generic_visit(node)
        self._exit_nesting()
    
    def visit_Try(self, node):
        self._enter_nesting()
        self.generic_visit(node)
        self._exit_nesting()
    
    def _enter_nesting(self):
        self.nesting_level += 1
        self.max_nesting = max(self.max_nesting, self.nesting_level)
    
    def _exit_nesting(self):
        self.nesting_level -= 1
    
    def _calculate_complexity(self, node) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1
        return complexity
    
    def _calculate_length(self, node) -> int:
        """Calculate function length"""
        if hasattr(node, 'end_lineno') and node.end_lineno:
            return node.end_lineno - node.lineno + 1
        return len([n for n in ast.walk(node) if hasattr(n, 'lineno')])


class ControlFlowAnalyzer(ast.NodeVisitor):
    """Analyze control flow patterns"""
    
    def __init__(self):
        self.conditional_complexity: Dict[str, int] = defaultdict(int)
        self.loop_patterns: Dict[str, List[str]] = defaultdict(list)
        self.early_returns: Dict[str, int] = defaultdict(int)
        self.nested_loops: Dict[str, int] = defaultdict(int)
        self.break_continue: Dict[str, Dict[str, int]] = defaultdict(lambda: {"break": 0, "continue": 0})
        self.exception_flow: Dict[str, List[str]] = defaultdict(list)
        self.generators: List[str] = []
        self.current_function = None
        self.loop_depth = 0
    
    def visit_FunctionDef(self, node):
        old_function = self.current_function
        self.current_function = node.name
        
        # Check if it's a generator
        for child in ast.walk(node):
            if isinstance(child, ast.Yield):
                self.generators.append(node.name)
                break
        
        self.generic_visit(node)
        self.current_function = old_function
    
    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)
    
    def visit_If(self, node):
        if self.current_function:
            self.conditional_complexity[self.current_function] += 1
        self.generic_visit(node)
    
    def visit_For(self, node):
        if self.current_function:
            self.loop_patterns[self.current_function].append("for")
            if self.loop_depth > 0:
                self.nested_loops[self.current_function] += 1
        
        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1
    
    def visit_While(self, node):
        if self.current_function:
            self.loop_patterns[self.current_function].append("while")
            if self.loop_depth > 0:
                self.nested_loops[self.current_function] += 1
        
        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1
    
    def visit_Return(self, node):
        if self.current_function:
            self.early_returns[self.current_function] += 1
        self.generic_visit(node)
    
    def visit_Break(self, node):
        if self.current_function:
            self.break_continue[self.current_function]["break"] += 1
    
    def visit_Continue(self, node):
        if self.current_function:
            self.break_continue[self.current_function]["continue"] += 1
    
    def visit_Try(self, node):
        if self.current_function:
            for handler in node.handlers:
                if handler.type:
                    exc_type = self._get_exception_name(handler.type)
                    self.exception_flow[self.current_function].append(exc_type)
                else:
                    self.exception_flow[self.current_function].append("bare_except")
        self.generic_visit(node)
    
    def _get_exception_name(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return "Unknown"
    
    def _get_name(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return "Unknown"


class DataFlowAnalyzer(ast.NodeVisitor):
    """Analyze data flow patterns"""
    
    def __init__(self):
        self.return_patterns: Dict[str, List[str]] = defaultdict(list)
        self.side_effects: Dict[str, List[str]] = defaultdict(list)
        self.state_modifications: Dict[str, List[str]] = defaultdict(list)
        self.closure_variables: Dict[str, Set[str]] = defaultdict(set)
        self.global_access: Dict[str, Set[str]] = defaultdict(set)
        self.current_function = None
    
    def visit_FunctionDef(self, node):
        old_function = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = old_function
    
    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)
    
    def visit_Return(self, node):
        if self.current_function and node.value:
            return_type = type(node.value).__name__
            self.return_patterns[self.current_function].append(return_type)
        self.generic_visit(node)
    
    def visit_Global(self, node):
        if self.current_function:
            for name in node.names:
                self.global_access[self.current_function].add(name)
    
    def visit_Call(self, node):
        if self.current_function:
            # Check for potential side effects
            func_name = self._get_call_name(node)
            if func_name and self._has_side_effects(func_name):
                self.side_effects[self.current_function].append(func_name)
        self.generic_visit(node)
    
    def _get_call_name(self, node) -> Optional[str]:
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return None
    
    def _has_side_effects(self, func_name: str) -> bool:
        """Check if function likely has side effects"""
        side_effect_patterns = {
            'print', 'write', 'append', 'insert', 'remove', 'pop', 'clear',
            'update', 'setattr', 'delattr', 'exec', 'eval'
        }
        return func_name in side_effect_patterns


class PatternDetector:
    """Detect common patterns and anti-patterns"""
    
    def __init__(self, content: str, tree: ast.AST):
        self.content = content
        self.tree = tree
    
    def detect_all(self) -> Dict[str, Any]:
        """Detect all patterns"""
        return {
            "design_patterns": self._detect_design_patterns(),
            "anti_patterns": self._detect_anti_patterns(),
            "code_smells": self._detect_code_smells(),
            "best_practices": self._check_best_practices()
        }
    
    def _detect_design_patterns(self) -> List[str]:
        """Detect common design patterns"""
        patterns = []
        
        # Singleton pattern
        if re.search(r'class.*:\s*\n.*_instance.*=.*None', self.content):
            patterns.append("Singleton")
        
        # Factory pattern
        if re.search(r'def create_.*\(', self.content):
            patterns.append("Factory")
        
        # Observer pattern
        if re.search(r'def (add|remove)_(observer|listener)', self.content):
            patterns.append("Observer")
        
        # Decorator pattern
        if re.search(r'@\w+', self.content):
            patterns.append("Decorator")
        
        return patterns
    
    def _detect_anti_patterns(self) -> List[str]:
        """Detect anti-patterns"""
        anti_patterns = []
        
        # God class (many methods)
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                if len(methods) > 20:
                    anti_patterns.append(f"God class: {node.name}")
        
        # Long parameter lists
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.args.args) > 7:
                    anti_patterns.append(f"Long parameter list: {node.name}")
        
        # Nested loops
        if re.search(r'for.*:\s*\n.*for.*:', self.content):
            anti_patterns.append("Nested loops detected")
        
        # Magic numbers
        magic_numbers = re.findall(r'\b(?<!\.)\d{2,}\b(?!\s*[,\]])', self.content)
        if len(magic_numbers) > 5:
            anti_patterns.append("Magic numbers detected")
        
        return anti_patterns
    
    def _detect_code_smells(self) -> List[str]:
        """Detect code smells"""
        smells = []
        
        # Duplicate code (simplified)
        lines = self.content.splitlines()
        line_counts = Counter(line.strip() for line in lines if line.strip())
        duplicates = [line for line, count in line_counts.items() if count > 2 and len(line) > 20]
        if duplicates:
            smells.append(f"Duplicate code: {len(duplicates)} repeated lines")
        
        # Dead code (unreachable after return)
        if re.search(r'return.*\n.*\w+', self.content):
            smells.append("Potential dead code after return")
        
        # Comments as deodorant
        comment_ratio = len(re.findall(r'#.*', self.content)) / len(lines) if lines else 0
        if comment_ratio > 0.3:
            smells.append("High comment ratio - possible complex code")
        
        return smells
    
    def _check_best_practices(self) -> Dict[str, bool]:
        """Check adherence to best practices"""
        return {
            "has_docstrings": bool(re.search(r'""".*?"""', self.content, re.DOTALL)),
            "uses_type_hints": bool(re.search(r':\s*\w+\s*[=)]', self.content)),
            "follows_naming": bool(re.search(r'def [a-z_][a-z0-9_]*\(', self.content)),
            "has_main_guard": '__name__' in self.content and '__main__' in self.content,
            "imports_at_top": self._check_imports_at_top(),
            "no_global_vars": not bool(re.search(r'^[A-Z_]{2,} = ', self.content, re.MULTILINE))
        }
    
    def _check_imports_at_top(self) -> bool:
        """Check if imports are at the top of the file"""
        lines = self.content.splitlines()
        first_non_comment = None
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and not stripped.startswith('"""'):
                first_non_comment = i
                break
        
        if first_non_comment is None:
            return True
        
        # Check if imports come before other code
        import_lines = [i for i, line in enumerate(lines) if line.strip().startswith(('import ', 'from '))]
        if not import_lines:
            return True
        
        return max(import_lines) < first_non_comment + 10  # Allow some flexibility


class TypeAnalyzer(ast.NodeVisitor):
    """Analyze type usage and consistency"""
    
    def __init__(self):
        self.type_annotations: Dict[str, List[str]] = defaultdict(list)
        self.return_annotations: Dict[str, str] = {}
        self.generic_usage: List[str] = []
        self.union_types: List[str] = []
        self.optional_types: List[str] = []
        self.total_functions = 0
        self.typed_functions = 0
    
    def visit_FunctionDef(self, node):
        self.total_functions += 1
        
        # Check return type annotation
        if node.returns:
            self.typed_functions += 1
            return_type = self._get_annotation_string(node.returns)
            self.return_annotations[node.name] = return_type
            
            if 'Union' in return_type:
                self.union_types.append(node.name)
            if 'Optional' in return_type:
                self.optional_types.append(node.name)
            if any(generic in return_type for generic in ['List', 'Dict', 'Set', 'Tuple']):
                self.generic_usage.append(node.name)
        
        # Check parameter annotations
        for arg in node.args.args:
            if arg.annotation:
                annotation = self._get_annotation_string(arg.annotation)
                self.type_annotations[node.name].append(f"{arg.arg}: {annotation}")
        
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)
    
    def _get_annotation_string(self, node) -> str:
        """Convert annotation node to string"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Attribute):
            return f"{self._get_annotation_string(node.value)}.{node.attr}"
        elif isinstance(node, ast.Subscript):
            value = self._get_annotation_string(node.value)
            slice_val = self._get_annotation_string(node.slice)
            return f"{value}[{slice_val}]"
        return "Unknown"
    
    def calculate_type_coverage(self) -> Dict[str, float]:
        """Calculate type annotation coverage"""
        return {
            "function_coverage": (self.typed_functions / self.total_functions * 100) if self.total_functions > 0 else 0,
            "total_functions": self.total_functions,
            "typed_functions": self.typed_functions
        }
    
    def check_return_consistency(self) -> List[str]:
        """Check for consistent return types"""
        # Simplified implementation
        inconsistent = []
        for func, return_type in self.return_annotations.items():
            if 'Union' in return_type and 'None' not in return_type:
                inconsistent.append(f"{func}: Union type without None may indicate inconsistent returns")
        return inconsistent


class ErrorHandlingAnalyzer(ast.NodeVisitor):
    """Analyze error handling patterns"""
    
    def __init__(self):
        self.exception_handlers: Dict[str, List[str]] = defaultdict(list)
        self.bare_except: List[str] = []
        self.exception_types: Set[str] = set()
        self.finally_blocks: List[str] = []
        self.resource_management: List[str] = []
        self.error_propagation: List[str] = []
        self.current_function = None
    
    def visit_FunctionDef(self, node):
        old_function = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = old_function
    
    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)
    
    def visit_Try(self, node):
        if self.current_function:
            for handler in node.handlers:
                if handler.type:
                    exc_type = self._get_exception_name(handler.type)
                    self.exception_handlers[self.current_function].append(exc_type)
                    self.exception_types.add(exc_type)
                else:
                    self.bare_except.append(self.current_function)
            
            if node.finalbody:
                self.finally_blocks.append(self.current_function)
        
        self.generic_visit(node)
    
    def visit_With(self, node):
        if self.current_function:
            self.resource_management.append(self.current_function)
        self.generic_visit(node)
    
    def visit_Raise(self, node):
        if self.current_function:
            self.error_propagation.append(self.current_function)
        self.generic_visit(node)
    
    def _get_exception_name(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return "Unknown"
    
    def _get_name(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return "Unknown"


class DependencyAnalyzer(ast.NodeVisitor):
    """Detailed dependency analysis"""
    
    def __init__(self):
        self.all_imports: Set[str] = set()
        self.dynamic_imports: List[str] = []
        self.conditional_imports: List[str] = []
        self.unused_imports: List[str] = []
        self.wildcard_imports: List[str] = []
        self.relative_imports: List[str] = []
        self.potential_cycles: List[str] = []
        self.import_depth = 0
    
    def visit_Import(self, node):
        for alias in node.names:
            self.all_imports.add(alias.name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        if node.module:
            self.all_imports.add(node.module)
            if node.module.startswith('.'):
                self.relative_imports.append(node.module)
        
        for alias in node.names:
            if alias.name == '*':
                self.wildcard_imports.append(node.module or 'unknown')
        
        self.generic_visit(node)
    
    def visit_If(self, node):
        # Check for conditional imports
        old_depth = self.import_depth
        self.import_depth += 1
        
        for child in ast.walk(node):
            if isinstance(child, (ast.Import, ast.ImportFrom)):
                self.conditional_imports.append("conditional_import")
        
        self.generic_visit(node)
        self.import_depth = old_depth
    
    def visit_Call(self, node):
        # Check for dynamic imports
        if (isinstance(node.func, ast.Name) and 
            node.func.id == '__import__'):
            self.dynamic_imports.append("__import__")
        elif (isinstance(node.func, ast.Attribute) and
              node.func.attr == 'import_module'):
            self.dynamic_imports.append("importlib.import_module")
        
        self.generic_visit(node)


def main():
    if len(sys.argv) < 2:
        print("Usage: advanced-code-context.py <file> [--json]")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    analyzer = AdvancedCodeAnalyzer(file_path)
    results = analyzer.analyze_all()
    
    if "--json" in sys.argv:
        print(json.dumps(results, indent=2, default=str))
    else:
        # Pretty print results
        print(f"=== Advanced Analysis: {file_path.name} ===\n")
        
        # Function complexity
        complexity = results.get("complexity_metrics", {})
        if complexity:
            print("🔢 Complexity Metrics:")
            total_complexity = complexity.get("total_complexity", 0)
            avg_complexity = complexity.get("average_complexity", 0)
            print(f"  Total complexity: {total_complexity}")
            print(f"  Average complexity: {avg_complexity:.1f}")
            
            complex_funcs = complexity.get("complex_functions", [])
            if complex_funcs:
                print(f"  Complex functions (>10): {', '.join(complex_funcs)}")
            print()
        
        # Call graph
        call_graph = results.get("function_call_graph", {})
        if call_graph:
            print("📞 Call Graph:")
            recursive = call_graph.get("recursive_functions", [])
            if recursive:
                print(f"  Recursive functions: {', '.join(recursive)}")
            
            cycles = call_graph.get("call_cycles", [])
            if cycles:
                print(f"  Call cycles detected: {len(cycles)}")
            
            max_depth = call_graph.get("max_call_depth", 0)
            print(f"  Maximum call depth: {max_depth}")
            print()
        
        # Patterns
        patterns = results.get("pattern_detection", {})
        if patterns:
            print("🎯 Pattern Detection:")
            design_patterns = patterns.get("design_patterns", [])
            if design_patterns:
                print(f"  Design patterns: {', '.join(design_patterns)}")
            
            anti_patterns = patterns.get("anti_patterns", [])
            if anti_patterns:
                print(f"  Anti-patterns: {', '.join(anti_patterns)}")
            
            smells = patterns.get("code_smells", [])
            if smells:
                print(f"  Code smells: {', '.join(smells)}")
            print()


if __name__ == "__main__":
    main()