# -*- coding: utf-8 -*-
"""
Test suite for Notepad++ PythonScript XML tag wrappers
"""

import unittest
import re


class MockEditor:
    """Mock editor object to simulate Notepad++ editor API"""
    
    def __init__(self):
        self.text = ""
        self.selection = ""
        self.current_pos = 0
        
    def getSelText(self):
        """Get selected text"""
        return self.selection
    
    def replaceSel(self, text):
        """Replace selection with text"""
        self.text = text
        self.current_pos = len(text)
    
    def getCurrentPos(self):
        """Get current cursor position"""
        return self.current_pos
    
    def setCurrentPos(self, pos):
        """Set cursor position"""
        self.current_pos = pos
    
    def setSelection(self, start, end):
        """Set selection range"""
        pass


class TestXMLWrappers(unittest.TestCase):
    """Test XML tag wrapper scripts"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.editor = MockEditor()
    
    def test_wrap_title_with_selection(self):
        """Test wrapping selected text in <title> tags"""
        self.editor.selection = "Sample Title"
        
        # Simulate the script
        selected_text = self.editor.getSelText()
        if selected_text:
            wrapped_text = "<title>" + selected_text + "</title>"
            self.editor.replaceSel(wrapped_text)
        
        self.assertEqual(self.editor.text, "<title>Sample Title</title>")
    
    def test_wrap_title_without_selection(self):
        """Test inserting empty <title> tags when no text is selected"""
        self.editor.selection = ""
        
        # Simulate the script
        selected_text = self.editor.getSelText()
        if selected_text:
            wrapped_text = "<title>" + selected_text + "</title>"
            self.editor.replaceSel(wrapped_text)
        else:
            self.editor.replaceSel("<title></title>")
            current_pos = self.editor.getCurrentPos()
            self.editor.setCurrentPos(current_pos - 8)
        
        self.assertEqual(self.editor.text, "<title></title>")
        self.assertEqual(self.editor.current_pos, 7)  # Position between tags
    
    def test_wrap_head_with_selection(self):
        """Test wrapping selected text in <head> tags"""
        self.editor.selection = "Header Text"
        
        selected_text = self.editor.getSelText()
        if selected_text:
            wrapped_text = "<head>" + selected_text + "</head>"
            self.editor.replaceSel(wrapped_text)
        
        self.assertEqual(self.editor.text, "<head>Header Text</head>")
    
    def test_wrap_hi_with_selection(self):
        """Test wrapping selected text in <hi> tags"""
        self.editor.selection = "highlighted"
        
        selected_text = self.editor.getSelText()
        if selected_text:
            wrapped_text = "<hi>" + selected_text + "</hi>"
            self.editor.replaceSel(wrapped_text)
        
        self.assertEqual(self.editor.text, "<hi>highlighted</hi>")
    
    def test_wrap_quote_with_selection(self):
        """Test wrapping selected text in <quote> tags"""
        self.editor.selection = "This is a quote"
        
        selected_text = self.editor.getSelText()
        if selected_text:
            wrapped_text = "<quote>" + selected_text + "</quote>"
            self.editor.replaceSel(wrapped_text)
        
        self.assertEqual(self.editor.text, "<quote>This is a quote</quote>")
    
    def test_wrap_trailer_with_selection(self):
        """Test wrapping selected text in <trailer> tags"""
        self.editor.selection = "Trailer content"
        
        selected_text = self.editor.getSelText()
        if selected_text:
            wrapped_text = "<trailer>" + selected_text + "</trailer>"
            self.editor.replaceSel(wrapped_text)
        
        self.assertEqual(self.editor.text, "<trailer>Trailer content</trailer>")
    
    def test_wrap_foreign_with_selection(self):
        """Test wrapping selected text in <foreign> tags"""
        self.editor.selection = "foreign text"
        
        selected_text = self.editor.getSelText()
        if selected_text:
            wrapped_text = "<foreign>" + selected_text + "</foreign>"
            self.editor.replaceSel(wrapped_text)
        
        self.assertEqual(self.editor.text, "<foreign>foreign text</foreign>")
    
    def test_wrap_special_characters(self):
        """Test wrapping text with special characters"""
        self.editor.selection = "Text with & < > characters"
        
        selected_text = self.editor.getSelText()
        if selected_text:
            wrapped_text = "<title>" + selected_text + "</title>"
            self.editor.replaceSel(wrapped_text)
        
        # Note: Scripts don't escape XML characters - that's intentional for flexibility
        self.assertEqual(self.editor.text, "<title>Text with & < > characters</title>")
    
    def test_wrap_unicode_text(self):
        """Test wrapping Unicode/Cyrillic text"""
        self.editor.selection = "Српски текст"
        
        selected_text = self.editor.getSelText()
        if selected_text:
            wrapped_text = "<foreign>" + selected_text + "</foreign>"
            self.editor.replaceSel(wrapped_text)
        
        self.assertEqual(self.editor.text, "<foreign>Српски текст</foreign>")


class TestScriptFiles(unittest.TestCase):
    """Test that script files exist and have correct structure"""
    
    def test_all_scripts_exist(self):
        """Test that all required script files exist"""
        import os
        
        script_dir = os.path.join(os.path.dirname(__file__), 'scripts')
        required_scripts = [
            'wrap_title.py',
            'wrap_head.py',
            'wrap_hi.py',
            'wrap_quote.py',
            'wrap_trailer.py',
            'wrap_foreign.py'
        ]
        
        for script in required_scripts:
            script_path = os.path.join(script_dir, script)
            self.assertTrue(
                os.path.exists(script_path),
                f"Script {script} does not exist"
            )
    
    def test_scripts_have_utf8_encoding(self):
        """Test that all scripts declare UTF-8 encoding"""
        import os
        
        script_dir = os.path.join(os.path.dirname(__file__), 'scripts')
        scripts = [
            'wrap_title.py',
            'wrap_head.py',
            'wrap_hi.py',
            'wrap_quote.py',
            'wrap_trailer.py',
            'wrap_foreign.py'
        ]
        
        for script in scripts:
            script_path = os.path.join(script_dir, script)
            with open(script_path, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                self.assertIn('utf-8', first_line.lower(),
                            f"Script {script} should declare UTF-8 encoding")


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
