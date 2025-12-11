#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_python27_compliance.py
Standalone script to check Python 2.7 compliance of Notepad++ scripts.

This script validates that all Python scripts in the /scripts/ directory
are compatible with Python 2.7, which is required by the PythonScript plugin
for Notepad++.

Usage:
    python check_python27_compliance.py
    
The script will check for:
- No f-strings (Python 3.6+)
- No type hints (Python 3.5+)
- No walrus operator := (Python 3.8+)
- No async/await (Python 3.5+)
- No 'nonlocal' keyword (Python 3+)
- No 'yield from' (Python 3.3+)
- UTF-8 encoding declaration present
- Only Npp module and standard library imports
"""

import ast
import sys
from pathlib import Path


class ComplianceChecker:
    """Checker for Python 2.7 compliance."""
    
    def __init__(self, scripts_dir):
        """Initialize the checker with the scripts directory."""
        self.scripts_dir = Path(scripts_dir)
        self.errors = []
        self.warnings = []
        self.passed_checks = 0
        self.total_checks = 0
    
    def check_all(self):
        """Run all compliance checks."""
        print("=" * 70)
        print("Python 2.7 Compliance Checker for Notepad++ Scripts")
        print("=" * 70)
        print()
        
        # Get all script files
        script_files = list(self.scripts_dir.glob("*.py"))
        script_files = [f for f in script_files if f.name != "test_scripts.py"]
        
        if not script_files:
            print("❌ No Python scripts found in scripts/ directory")
            return False
        
        print(f"Found {len(script_files)} script(s) to check:")
        for script_file in script_files:
            print(f"  • {script_file.name}")
        print()
        
        # Run all checks
        self._check_fstrings(script_files)
        self._check_type_hints(script_files)
        self._check_walrus_operator(script_files)
        self._check_async_await(script_files)
        self._check_nonlocal(script_files)
        self._check_yield_from(script_files)
        self._check_encoding(script_files)
        self._check_imports(script_files)
        self._check_syntax(script_files)
        
        # Print results
        print()
        print("=" * 70)
        print("RESULTS")
        print("=" * 70)
        
        if self.errors:
            print(f"\n❌ Found {len(self.errors)} error(s):\n")
            for error in self.errors:
                print(f"  {error}")
        
        if self.warnings:
            print(f"\n⚠️  Found {len(self.warnings)} warning(s):\n")
            for warning in self.warnings:
                print(f"  {warning}")
        
        print()
        if not self.errors:
            print("✅ All scripts are Python 2.7 compatible!")
            return True
        else:
            print(f"❌ Compliance check failed with {len(self.errors)} error(s)")
            return False
    
    def _check_fstrings(self, script_files):
        """Check for f-strings (Python 3.6+ feature)."""
        print("Checking for f-strings... ", end="", flush=True)
        found_errors = False
        
        for script_file in script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                tree = ast.parse(content, filename=str(script_file))
                
                for node in ast.walk(tree):
                    if sys.version_info >= (3, 6) and isinstance(node, ast.JoinedStr):
                        self.errors.append(
                            f"{script_file.name}:{node.lineno}: "
                            f"f-string detected (use .format() instead)"
                        )
                        found_errors = True
            except SyntaxError:
                pass  # Will be caught by syntax check
        
        if not found_errors:
            print("✅ PASS")
        else:
            print("❌ FAIL")
    
    def _check_type_hints(self, script_files):
        """Check for type hints (Python 3.5+ feature)."""
        print("Checking for type hints... ", end="", flush=True)
        found_errors = False
        
        for script_file in script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                tree = ast.parse(content, filename=str(script_file))
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        if node.returns is not None:
                            self.errors.append(
                                f"{script_file.name}:{node.lineno}: "
                                f"Type hints detected in function '{node.name}'"
                            )
                            found_errors = True
                    
                    if sys.version_info >= (3, 6) and isinstance(node, ast.AnnAssign):
                        self.errors.append(
                            f"{script_file.name}:{node.lineno}: "
                            f"Annotated assignment detected"
                        )
                        found_errors = True
            except SyntaxError:
                pass
        
        if not found_errors:
            print("✅ PASS")
        else:
            print("❌ FAIL")
    
    def _check_walrus_operator(self, script_files):
        """Check for walrus operator := (Python 3.8+ feature)."""
        print("Checking for walrus operator... ", end="", flush=True)
        found_errors = False
        
        for script_file in script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                tree = ast.parse(content, filename=str(script_file))
                
                for node in ast.walk(tree):
                    if sys.version_info >= (3, 8) and isinstance(node, ast.NamedExpr):
                        self.errors.append(
                            f"{script_file.name}:{node.lineno}: "
                            f"Walrus operator ':=' detected"
                        )
                        found_errors = True
            except SyntaxError:
                pass
        
        if not found_errors:
            print("✅ PASS")
        else:
            print("❌ FAIL")
    
    def _check_async_await(self, script_files):
        """Check for async/await (Python 3.5+ feature)."""
        print("Checking for async/await... ", end="", flush=True)
        found_errors = False
        
        for script_file in script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                tree = ast.parse(content, filename=str(script_file))
                
                for node in ast.walk(tree):
                    if isinstance(node, (ast.AsyncFunctionDef, ast.Await, 
                                       ast.AsyncFor, ast.AsyncWith)):
                        self.errors.append(
                            f"{script_file.name}:{node.lineno}: "
                            f"Async/await syntax detected"
                        )
                        found_errors = True
            except SyntaxError:
                pass
        
        if not found_errors:
            print("✅ PASS")
        else:
            print("❌ FAIL")
    
    def _check_nonlocal(self, script_files):
        """Check for 'nonlocal' keyword (Python 3+ feature)."""
        print("Checking for 'nonlocal' keyword... ", end="", flush=True)
        found_errors = False
        
        for script_file in script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                tree = ast.parse(content, filename=str(script_file))
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Nonlocal):
                        self.errors.append(
                            f"{script_file.name}:{node.lineno}: "
                            f"'nonlocal' keyword detected"
                        )
                        found_errors = True
            except SyntaxError:
                pass
        
        if not found_errors:
            print("✅ PASS")
        else:
            print("❌ FAIL")
    
    def _check_yield_from(self, script_files):
        """Check for 'yield from' (Python 3.3+ feature)."""
        print("Checking for 'yield from'... ", end="", flush=True)
        found_errors = False
        
        for script_file in script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                tree = ast.parse(content, filename=str(script_file))
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.YieldFrom):
                        self.errors.append(
                            f"{script_file.name}:{node.lineno}: "
                            f"'yield from' detected"
                        )
                        found_errors = True
            except SyntaxError:
                pass
        
        if not found_errors:
            print("✅ PASS")
        else:
            print("❌ FAIL")
    
    def _check_encoding(self, script_files):
        """Check for UTF-8 encoding declaration."""
        print("Checking UTF-8 encoding declaration... ", end="", flush=True)
        found_errors = False
        
        for script_file in script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                second_line = f.readline()
            
            has_encoding = (
                'coding:' in first_line or 'coding=' in first_line or
                'coding:' in second_line or 'coding=' in second_line
            )
            
            if not has_encoding:
                self.errors.append(
                    f"{script_file.name}: Missing UTF-8 encoding declaration"
                )
                found_errors = True
        
        if not found_errors:
            print("✅ PASS")
        else:
            print("❌ FAIL")
    
    def _check_imports(self, script_files):
        """Check for problematic imports."""
        print("Checking imports... ", end="", flush=True)
        found_errors = False
        
        third_party_modules = {
            'numpy', 'pandas', 'requests', 'flask', 'django',
            'tensorflow', 'torch', 'scipy', 'matplotlib',
            'pytest', 'nose', 'mock'
        }
        
        for script_file in script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                tree = ast.parse(content, filename=str(script_file))
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            module_name = alias.name.split('.')[0]
                            if module_name in third_party_modules:
                                self.errors.append(
                                    f"{script_file.name}:{node.lineno}: "
                                    f"Third-party import '{alias.name}' "
                                    f"(only Npp and stdlib allowed)"
                                )
                                found_errors = True
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            module_name = node.module.split('.')[0]
                            if module_name in third_party_modules:
                                self.errors.append(
                                    f"{script_file.name}:{node.lineno}: "
                                    f"Third-party import from '{node.module}'"
                                )
                                found_errors = True
            except SyntaxError:
                pass
        
        if not found_errors:
            print("✅ PASS")
        else:
            print("❌ FAIL")
    
    def _check_syntax(self, script_files):
        """Check for syntax errors."""
        print("Checking syntax... ", end="", flush=True)
        found_errors = False
        
        for script_file in script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                ast.parse(content, filename=str(script_file))
            except SyntaxError as e:
                self.errors.append(
                    f"{script_file.name}:{e.lineno}: Syntax error - {e.msg}"
                )
                found_errors = True
        
        if not found_errors:
            print("✅ PASS")
        else:
            print("❌ FAIL")


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent / "scripts"
    
    checker = ComplianceChecker(script_dir)
    success = checker.check_all()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
