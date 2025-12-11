# -*- coding: utf-8 -*-
"""
test_python27_compliance.py
Unit tests to verify that all scripts in /scripts/ are Python 2.7 compatible.
This test ensures that Notepad++ PythonScript scripts will work with Python 2.7.
"""

import ast
import os
import sys
import unittest
from pathlib import Path


class Python27ComplianceTest(unittest.TestCase):
    """Test suite to verify Python 2.7 compliance of Notepad++ scripts."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class by finding all scripts to check."""
        cls.scripts_dir = Path(__file__).parent.parent / "scripts"
        cls.script_files = list(cls.scripts_dir.glob("*.py"))
        # Exclude test_scripts.py from compliance checks as it's a test harness
        cls.script_files = [
            f for f in cls.script_files 
            if f.name != "test_scripts.py"
        ]
    
    def test_scripts_directory_exists(self):
        """Verify that the scripts directory exists."""
        self.assertTrue(self.scripts_dir.exists(), 
                       f"Scripts directory not found: {self.scripts_dir}")
    
    def test_scripts_found(self):
        """Verify that script files are found."""
        self.assertGreater(len(self.script_files), 0, 
                          "No Python scripts found in scripts/ directory")
    
    def test_no_fstrings(self):
        """Verify that scripts don't use f-strings (Python 3.6+ feature)."""
        errors = []
        
        for script_file in self.script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                tree = ast.parse(content, filename=str(script_file))
                
                # Check for JoinedStr nodes which represent f-strings
                for node in ast.walk(tree):
                    if sys.version_info >= (3, 6) and isinstance(node, ast.JoinedStr):
                        errors.append(
                            f"{script_file.name}:{node.lineno}: "
                            f"f-string detected (not compatible with Python 2.7)"
                        )
            except SyntaxError as e:
                errors.append(f"{script_file.name}: Syntax error - {e}")
        
        self.assertEqual(len(errors), 0, 
                        f"F-strings found:\n" + "\n".join(errors))
    
    def test_no_type_hints(self):
        """Verify that scripts don't use type hints (Python 3.5+ feature)."""
        errors = []
        
        for script_file in self.script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                tree = ast.parse(content, filename=str(script_file))
                
                # Check for function annotations (type hints)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        # Check return annotation
                        if node.returns is not None:
                            errors.append(
                                f"{script_file.name}:{node.lineno}: "
                                f"Function '{node.name}' has return type hint "
                                f"(not compatible with Python 2.7)"
                            )
                        
                        # Check argument annotations
                        if hasattr(node.args, 'args'):
                            for arg in node.args.args:
                                if hasattr(arg, 'annotation') and arg.annotation is not None:
                                    errors.append(
                                        f"{script_file.name}:{node.lineno}: "
                                        f"Function '{node.name}' has argument type hints "
                                        f"(not compatible with Python 2.7)"
                                    )
                    
                    # Check for AnnAssign (annotated assignments like x: int = 5)
                    if sys.version_info >= (3, 6) and isinstance(node, ast.AnnAssign):
                        errors.append(
                            f"{script_file.name}:{node.lineno}: "
                            f"Annotated assignment detected "
                            f"(not compatible with Python 2.7)"
                        )
            
            except SyntaxError as e:
                errors.append(f"{script_file.name}: Syntax error - {e}")
        
        self.assertEqual(len(errors), 0, 
                        f"Type hints found:\n" + "\n".join(errors))
    
    def test_no_walrus_operator(self):
        """Verify that scripts don't use walrus operator := (Python 3.8+ feature)."""
        errors = []
        
        for script_file in self.script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                tree = ast.parse(content, filename=str(script_file))
                
                # Check for NamedExpr nodes which represent walrus operator
                for node in ast.walk(tree):
                    if sys.version_info >= (3, 8) and isinstance(node, ast.NamedExpr):
                        errors.append(
                            f"{script_file.name}:{node.lineno}: "
                            f"Walrus operator ':=' detected "
                            f"(not compatible with Python 2.7)"
                        )
            except SyntaxError as e:
                errors.append(f"{script_file.name}: Syntax error - {e}")
        
        self.assertEqual(len(errors), 0, 
                        f"Walrus operators found:\n" + "\n".join(errors))
    
    def test_no_async_await(self):
        """Verify that scripts don't use async/await (Python 3.5+ feature)."""
        errors = []
        
        for script_file in self.script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                tree = ast.parse(content, filename=str(script_file))
                
                # Check for async function definitions
                for node in ast.walk(tree):
                    if isinstance(node, ast.AsyncFunctionDef):
                        errors.append(
                            f"{script_file.name}:{node.lineno}: "
                            f"Async function '{node.name}' detected "
                            f"(not compatible with Python 2.7)"
                        )
                    elif isinstance(node, (ast.Await, ast.AsyncFor, ast.AsyncWith)):
                        errors.append(
                            f"{script_file.name}:{node.lineno}: "
                            f"Async/await syntax detected "
                            f"(not compatible with Python 2.7)"
                        )
            except SyntaxError as e:
                errors.append(f"{script_file.name}: Syntax error - {e}")
        
        self.assertEqual(len(errors), 0, 
                        f"Async/await found:\n" + "\n".join(errors))
    
    def test_uses_format_method(self):
        """Verify that scripts use .format() for string formatting."""
        warnings = []
        
        for script_file in self.script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Simple pattern check for potential string formatting
            # This is informational, not a hard failure
            has_format = '.format(' in content
            has_percent = any('%s' in line or '%d' in line for line in lines 
                            if not line.strip().startswith('#'))
            
            if not has_format and has_percent:
                warnings.append(
                    f"{script_file.name}: Uses %-formatting instead of .format() "
                    f"(consider using .format() for consistency)"
                )
        
        # This is just a warning, not a failure
        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"  {warning}")
    
    def test_no_nonlocal_keyword(self):
        """Verify that scripts don't use 'nonlocal' keyword (Python 3+ feature)."""
        errors = []
        
        for script_file in self.script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                tree = ast.parse(content, filename=str(script_file))
                
                # Check for Nonlocal nodes
                for node in ast.walk(tree):
                    if isinstance(node, ast.Nonlocal):
                        errors.append(
                            f"{script_file.name}:{node.lineno}: "
                            f"'nonlocal' keyword detected "
                            f"(not compatible with Python 2.7)"
                        )
            except SyntaxError as e:
                errors.append(f"{script_file.name}: Syntax error - {e}")
        
        self.assertEqual(len(errors), 0, 
                        f"'nonlocal' keyword found:\n" + "\n".join(errors))
    
    def test_no_yield_from(self):
        """Verify that scripts don't use 'yield from' (Python 3.3+ feature)."""
        errors = []
        
        for script_file in self.script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                tree = ast.parse(content, filename=str(script_file))
                
                # Check for YieldFrom nodes
                for node in ast.walk(tree):
                    if isinstance(node, ast.YieldFrom):
                        errors.append(
                            f"{script_file.name}:{node.lineno}: "
                            f"'yield from' detected "
                            f"(not compatible with Python 2.7)"
                        )
            except SyntaxError as e:
                errors.append(f"{script_file.name}: Syntax error - {e}")
        
        self.assertEqual(len(errors), 0, 
                        f"'yield from' found:\n" + "\n".join(errors))
    
    def test_has_utf8_encoding_declaration(self):
        """Verify that scripts have UTF-8 encoding declaration."""
        missing_encoding = []
        
        for script_file in self.script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                second_line = f.readline()
            
            # Check if either first or second line has encoding declaration
            has_encoding = (
                'coding:' in first_line or 'coding=' in first_line or
                'coding:' in second_line or 'coding=' in second_line
            )
            
            if not has_encoding:
                missing_encoding.append(script_file.name)
        
        self.assertEqual(len(missing_encoding), 0,
                        f"Scripts missing UTF-8 encoding declaration: "
                        f"{', '.join(missing_encoding)}")
    
    def test_imports_only_from_npp_or_stdlib(self):
        """Verify that scripts only import from Npp module or standard library."""
        problematic_imports = []
        
        # Common third-party packages that shouldn't be imported
        third_party_modules = {
            'numpy', 'pandas', 'requests', 'flask', 'django', 
            'tensorflow', 'torch', 'scipy', 'matplotlib',
            'pytest', 'nose', 'mock'
        }
        
        for script_file in self.script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                tree = ast.parse(content, filename=str(script_file))
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            module_name = alias.name.split('.')[0]
                            if module_name in third_party_modules:
                                problematic_imports.append(
                                    f"{script_file.name}:{node.lineno}: "
                                    f"Third-party import '{alias.name}' "
                                    f"(only Npp and stdlib allowed)"
                                )
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            module_name = node.module.split('.')[0]
                            if module_name in third_party_modules:
                                problematic_imports.append(
                                    f"{script_file.name}:{node.lineno}: "
                                    f"Third-party import from '{node.module}' "
                                    f"(only Npp and stdlib allowed)"
                                )
            except SyntaxError as e:
                # Already caught by other tests
                pass
        
        self.assertEqual(len(problematic_imports), 0,
                        f"Problematic imports found:\n" + 
                        "\n".join(problematic_imports))
    
    def test_scripts_can_be_parsed(self):
        """Verify that all scripts can be successfully parsed by Python AST."""
        parsing_errors = []
        
        for script_file in self.script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                ast.parse(content, filename=str(script_file))
            except SyntaxError as e:
                parsing_errors.append(
                    f"{script_file.name}:{e.lineno}: {e.msg}"
                )
        
        self.assertEqual(len(parsing_errors), 0,
                        f"Syntax errors found:\n" + "\n".join(parsing_errors))


if __name__ == '__main__':
    unittest.main()
