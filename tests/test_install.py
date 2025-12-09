# -*- coding: utf-8 -*-
"""
test_install.py
Unit tests for install.py script.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import xml.etree.ElementTree as ET
import sys
import os

# Add parent directory to path to import install module
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import install
except (ImportError, ModuleNotFoundError):
    # On non-Windows systems, install.py might fail to import due to missing winreg module
    install = None


class TestInstallHelperFunctions(unittest.TestCase):
    """Test helper functions from install.py."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Skip tests on non-Windows systems
        if install is None or sys.platform != 'win32':
            self.skipTest("install.py requires Windows")
    
    def test_create_empty_shortcuts_xml(self):
        """Test creation of empty shortcuts.xml structure."""
        root = install.create_empty_shortcuts_xml()
        
        # Check root element
        self.assertEqual(root.tag, 'NotepadPlus')
        
        # Check child elements exist
        children_tags = [child.tag for child in root]
        self.assertIn('InternalCommands', children_tags)
        self.assertIn('Macros', children_tags)
        self.assertIn('UserDefinedCommands', children_tags)
        self.assertIn('PluginCommands', children_tags)
        self.assertIn('ScintillaCommands', children_tags)
    
    def test_indent_xml(self):
        """Test XML indentation function."""
        root = ET.Element('root')
        child1 = ET.SubElement(root, 'child1')
        child2 = ET.SubElement(root, 'child2')
        
        install.indent_xml(root)
        
        # Check that text and tail are set (indicating indentation)
        self.assertIsNotNone(root.text)
        self.assertIn('\n', root.text)
    
    def test_copy_scripts_error_if_source_not_exists(self):
        """Test that copy_scripts raises error if source directory doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            target_dir = Path(tmpdir) / 'target'
            target_dir.mkdir()
            
            with self.assertRaises(RuntimeError) as context:
                install.copy_scripts('/nonexistent/path', target_dir)
            
            self.assertIn('Source directory not found', str(context.exception))
    
    def test_copy_scripts_error_if_target_not_exists(self):
        """Test that copy_scripts raises error if target directory doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source_dir = Path(tmpdir) / 'source'
            source_dir.mkdir()
            
            with self.assertRaises(RuntimeError) as context:
                install.copy_scripts(source_dir, '/nonexistent/target')
            
            self.assertIn('PythonScript scripts directory not found', str(context.exception))
    
    def test_copy_scripts_success(self):
        """Test successful script copying."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create source directory with test scripts
            source_dir = Path(tmpdir) / 'source'
            source_dir.mkdir()
            
            # Create test .py files
            (source_dir / 'wrap_title.py').write_text('# test script')
            (source_dir / 'wrap_head.py').write_text('# test script')
            (source_dir / 'test_scripts.py').write_text('# test file - should be filtered')
            
            # Create target directory
            target_dir = Path(tmpdir) / 'target'
            target_dir.mkdir()
            
            # Copy scripts
            copied = install.copy_scripts(source_dir, target_dir)
            
            # Verify scripts were copied (excluding test_scripts.py)
            self.assertEqual(len(copied), 2)
            self.assertIn('wrap_title.py', copied)
            self.assertIn('wrap_head.py', copied)
            self.assertNotIn('test_scripts.py', copied)
            
            # Verify files exist in target
            self.assertTrue((target_dir / 'wrap_title.py').exists())
            self.assertTrue((target_dir / 'wrap_head.py').exists())
            self.assertFalse((target_dir / 'test_scripts.py').exists())


class TestShortcutConfiguration(unittest.TestCase):
    """Test shortcut configuration constants."""
    
    def test_script_shortcuts_defined(self):
        """Test that script shortcuts are properly defined."""
        if install is None:
            self.skipTest("install.py requires Windows")
        
        # Check that SCRIPT_SHORTCUTS exists and has expected entries
        self.assertIsInstance(install.SCRIPT_SHORTCUTS, dict)
        
        # Check specific scripts
        expected_scripts = [
            'wrap_title.py',
            'wrap_head.py',
            'wrap_hi.py',
            'wrap_quote.py',
            'wrap_trailer.py',
            'wrap_foreign_prompt.py',
            'wrap_foreign_fixed.py'
        ]
        
        for script in expected_scripts:
            self.assertIn(script, install.SCRIPT_SHORTCUTS)
            shortcut = install.SCRIPT_SHORTCUTS[script]
            self.assertIn('key', shortcut)
            self.assertIn('ctrl', shortcut)
            self.assertIn('alt', shortcut)
            self.assertIn('shift', shortcut)
    
    def test_shortcuts_have_valid_keys(self):
        """Test that shortcuts have valid key codes."""
        if install is None:
            self.skipTest("install.py requires Windows")
        
        for script_name, shortcut in install.SCRIPT_SHORTCUTS.items():
            # Key should be a string representing a number
            self.assertIsInstance(shortcut['key'], str)
            self.assertTrue(shortcut['key'].isdigit())
            
            # Modifiers should be 'yes' or 'no'
            self.assertIn(shortcut['ctrl'], ['yes', 'no'])
            self.assertIn(shortcut['alt'], ['yes', 'no'])
            self.assertIn(shortcut['shift'], ['yes', 'no'])


class TestGetPaths(unittest.TestCase):
    """Test path detection functions."""
    
    def test_get_appdata_notepad_dir(self):
        """Test getting Notepad++ AppData directory."""
        if install is None or sys.platform != 'win32':
            self.skipTest("install.py requires Windows")
        
        # This will use actual APPDATA environment variable
        appdata_path = install.get_appdata_notepad_dir()
        
        # Should be a Path object
        self.assertIsInstance(appdata_path, Path)
        
        # Should end with Notepad++
        self.assertEqual(appdata_path.name, 'Notepad++')
    
    def test_get_pythonscript_dir(self):
        """Test getting PythonScript directory."""
        if install is None or sys.platform != 'win32':
            self.skipTest("install.py requires Windows")
        
        ps_dir = install.get_pythonscript_dir()
        
        # Should be a Path object
        self.assertIsInstance(ps_dir, Path)
        
        # Should end with scripts
        self.assertEqual(ps_dir.name, 'scripts')


if __name__ == "__main__":
    unittest.main()
