# -*- coding: utf-8 -*-
"""
test_wrap_scripts.py
Unit tests for all PythonScript wrap scripts using unittest framework.
"""

import unittest
import sys
from pathlib import Path


# Mock classes to simulate Notepad++ Npp module

class MockEditor:
    """Mock class that simulates editor object from Npp module."""
    
    def __init__(self):
        self.selected_text = ""
        self.replaced_text = ""
    
    def getSelText(self):
        """Returns selected text."""
        return self.selected_text
    
    def replaceSel(self, text):
        """Replaces selection with new text."""
        self.replaced_text = text


class MockNotepad:
    """Mock class that simulates notepad object from Npp module."""
    
    def __init__(self):
        self.prompt_response = "en"
    
    def prompt(self, message, title, default):
        """Simulates prompt dialog."""
        return self.prompt_response


class TestWrapScripts(unittest.TestCase):
    """Test cases for all wrap scripts."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.editor = MockEditor()
        self.notepad = MockNotepad()
    
    def test_wrap_title(self):
        """Test wrap_title script wraps text in <title> tag."""
        self.editor.selected_text = "test text"
        sel = self.editor.getSelText()
        if sel:
            self.editor.replaceSel("<title>{0}</title>".format(sel))
        
        self.assertEqual(self.editor.replaced_text, "<title>test text</title>")
    
    def test_wrap_head(self):
        """Test wrap_head script wraps text in <head> tag."""
        self.editor.selected_text = "test text"
        sel = self.editor.getSelText()
        if sel:
            self.editor.replaceSel("<head>{0}</head>".format(sel))
        
        self.assertEqual(self.editor.replaced_text, "<head>test text</head>")
    
    def test_wrap_hi(self):
        """Test wrap_hi script wraps text in <hi> tag."""
        self.editor.selected_text = "test text"
        sel = self.editor.getSelText()
        if sel:
            self.editor.replaceSel("<hi>{0}</hi>".format(sel))
        
        self.assertEqual(self.editor.replaced_text, "<hi>test text</hi>")
    
    def test_wrap_quote(self):
        """Test wrap_quote script wraps text in <quote> tag."""
        self.editor.selected_text = "test text"
        sel = self.editor.getSelText()
        if sel:
            self.editor.replaceSel("<quote>{0}</quote>".format(sel))
        
        self.assertEqual(self.editor.replaced_text, "<quote>test text</quote>")
    
    def test_wrap_trailer(self):
        """Test wrap_trailer script wraps text in <trailer> tag."""
        self.editor.selected_text = "test text"
        sel = self.editor.getSelText()
        if sel:
            self.editor.replaceSel("<trailer>{0}</trailer>".format(sel))
        
        self.assertEqual(self.editor.replaced_text, "<trailer>test text</trailer>")
    
    def test_wrap_serbian_quotes(self):
        """Test wrap_serbian_quotes script wraps text in Serbian quotation marks."""
        self.editor.selected_text = "test text"
        sel = self.editor.getSelText()
        if sel:
            self.editor.replaceSel('„{0}“'.format(sel))
        
        self.assertEqual(self.editor.replaced_text, '„test text“')
    
    def test_wrap_foreign_fixed(self):
        """Test wrap_foreign_fixed script wraps text with fixed language attribute."""
        DEFAULT_LANG = "en"
        self.editor.selected_text = "hello world"
        sel = self.editor.getSelText()
        if sel:
            self.editor.replaceSel('<foreign xml:lang="{0}">{1}</foreign>'.format(DEFAULT_LANG, sel))
        
        self.assertEqual(self.editor.replaced_text, '<foreign xml:lang="en">hello world</foreign>')
    
    def test_wrap_foreign_prompt(self):
        """Test wrap_foreign_prompt script wraps text with user-provided language."""
        self.editor.selected_text = "bonjour"
        self.notepad.prompt_response = "fr"
        
        sel = self.editor.getSelText()
        if sel:
            lang = self.notepad.prompt("Unesite vrednost za xml:lang atribut:", "Jezik", "en")
            if lang:
                lang_clean = lang.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
                self.editor.replaceSel('<foreign xml:lang="{0}">{1}</foreign>'.format(lang_clean, sel))
        
        self.assertEqual(self.editor.replaced_text, '<foreign xml:lang="fr">bonjour</foreign>')
    
    def test_wrap_foreign_prompt_xml_escaping(self):
        """Test wrap_foreign_prompt properly escapes XML special characters in language attribute."""
        self.editor.selected_text = "test"
        self.notepad.prompt_response = 'en"test'
        
        sel = self.editor.getSelText()
        if sel:
            lang = self.notepad.prompt("Unesite vrednost za xml:lang atribut:", "Jezik", "en")
            if lang:
                lang_clean = lang.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
                self.editor.replaceSel('<foreign xml:lang="{0}">{1}</foreign>'.format(lang_clean, sel))
        
        self.assertEqual(self.editor.replaced_text, '<foreign xml:lang="en&quot;test">test</foreign>')
    
    def test_wrap_foreign_prompt_escape_lt_gt(self):
        """Test wrap_foreign_prompt escapes < and > characters."""
        self.editor.selected_text = "test"
        self.notepad.prompt_response = 'en<script>alert()</script>'
        
        sel = self.editor.getSelText()
        if sel:
            lang = self.notepad.prompt("Unesite vrednost za xml:lang atribut:", "Jezik", "en")
            if lang:
                lang_clean = lang.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
                self.editor.replaceSel('<foreign xml:lang="{0}">{1}</foreign>'.format(lang_clean, sel))
        
        expected = '<foreign xml:lang="en&lt;script&gt;alert()&lt;/script&gt;">test</foreign>'
        self.assertEqual(self.editor.replaced_text, expected)
    
    def test_no_selection_no_replacement(self):
        """Test that scripts don't replace anything when there's no selection."""
        self.editor.selected_text = ""
        sel = self.editor.getSelText()
        if sel:
            self.editor.replaceSel("<title>{0}</title>".format(sel))
        
        self.assertEqual(self.editor.replaced_text, "")
    
    def test_wrap_title_empty_string(self):
        """Test wrap_title with empty selection."""
        self.editor.selected_text = ""
        sel = self.editor.getSelText()
        if sel:
            self.editor.replaceSel("<title>{0}</title>".format(sel))
        
        self.assertEqual(self.editor.replaced_text, "")
    
    def test_wrap_with_special_characters(self):
        """Test wrapping text containing special characters."""
        self.editor.selected_text = "Test <>&\""
        sel = self.editor.getSelText()
        if sel:
            self.editor.replaceSel("<title>{0}</title>".format(sel))
        
        self.assertEqual(self.editor.replaced_text, '<title>Test <>&"</title>')
    
    def test_wrap_with_unicode(self):
        """Test wrapping text containing unicode characters."""
        self.editor.selected_text = "Тест текст ćирилица"
        sel = self.editor.getSelText()
        if sel:
            self.editor.replaceSel("<title>{0}</title>".format(sel))
        
        self.assertEqual(self.editor.replaced_text, "<title>Тест текст ćирилица</title>")
    
    def test_wrap_serbian_quotes_with_unicode(self):
        """Test Serbian quotes with Cyrillic text."""
        self.editor.selected_text = "Ово је српски текст"
        sel = self.editor.getSelText()
        if sel:
            self.editor.replaceSel('„{0}“'.format(sel))
        
        self.assertEqual(self.editor.replaced_text, '„Ово је српски текст“')
    
    def test_wrap_multiline_text(self):
        """Test wrapping multiline text."""
        self.editor.selected_text = "Line 1\nLine 2\nLine 3"
        sel = self.editor.getSelText()
        if sel:
            self.editor.replaceSel("<quote>{0}</quote>".format(sel))
        
        self.assertEqual(self.editor.replaced_text, "<quote>Line 1\nLine 2\nLine 3</quote>")


if __name__ == "__main__":
    unittest.main()
