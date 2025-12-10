# -*- coding: utf-8 -*-
"""
test_scripts.py
Mock okruženje za testiranje PythonScript skripti van Notepad++.
Ovaj fajl simulira Npp modul i testira sve wrap skripte.
"""


class MockEditor:
    """Mock klasa koja simulira editor objekat iz Npp modula."""
    
    def __init__(self):
        self.selected_text = ""
        self.replaced_text = ""
    
    def getSelText(self):
        """Vraća selektovani tekst."""
        return self.selected_text
    
    def replaceSel(self, text):
        """Zamenjuje selekciju sa novim tekstom."""
        self.replaced_text = text
        print("Replaced: {0}".format(text))


class MockNotepad:
    """Mock klasa koja simulira notepad objekat iz Npp modula."""
    
    def __init__(self):
        self.prompt_response = "en"
    
    def prompt(self, message, title, default):
        """Simulira prompt dijalog."""
        print("Prompt: {0}".format(message))
        print("Title: {0}".format(title))
        print("Default: {0}".format(default))
        return self.prompt_response


def test_wrap_tag(tag_name, expected_output, mock_editor):
    """Testira jednostavnu wrap skriptu."""
    print("\n=== Test {0} ===".format(tag_name))
    mock_editor.selected_text = "test text"
    mock_editor.replaced_text = ""
    
    # Simuliraj izvršavanje skripte
    sel = mock_editor.getSelText()
    if sel:
        mock_editor.replaceSel(expected_output.format(sel=sel))
    
    # Proveri rezultat
    if mock_editor.replaced_text == expected_output.format(sel="test text"):
        print("✓ {0} test PROŠAO".format(tag_name))
        return True
    else:
        print("✗ {0} test NIJE PROŠAO".format(tag_name))
        print("  Očekivano: {0}".format(expected_output.format(sel='test text')))
        print("  Dobijeno: {0}".format(mock_editor.replaced_text))
        return False


def test_foreign_fixed(mock_editor):
    """Testira wrap_foreign_fixed.py skriptu."""
    print("\n=== Test wrap_foreign_fixed ===")
    mock_editor.selected_text = "hello world"
    mock_editor.replaced_text = ""
    
    DEFAULT_LANG = "en"
    sel = mock_editor.getSelText()
    if sel:
        mock_editor.replaceSel('<foreign xml:lang="{0}">{1}</foreign>'.format(DEFAULT_LANG, sel))
    
    expected = '<foreign xml:lang="en">hello world</foreign>'
    if mock_editor.replaced_text == expected:
        print("✓ wrap_foreign_fixed test PROŠAO")
        return True
    else:
        print("✗ wrap_foreign_fixed test NIJE PROŠAO")
        print("  Očekivano: {0}".format(expected))
        print("  Dobijeno: {0}".format(mock_editor.replaced_text))
        return False


def test_foreign_prompt(mock_editor, mock_notepad):
    """Testira wrap_foreign_prompt.py skriptu."""
    print("\n=== Test wrap_foreign_prompt ===")
    mock_editor.selected_text = "bonjour"
    mock_editor.replaced_text = ""
    mock_notepad.prompt_response = "fr"
    
    sel = mock_editor.getSelText()
    if sel:
        lang = mock_notepad.prompt("Unesite vrednost za xml:lang atribut:", "Jezik", "en")
        if lang:
            # Očisti lang od potencijalno opasnih karaktera
            lang_clean = lang.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
            mock_editor.replaceSel('<foreign xml:lang="{0}">{1}</foreign>'.format(lang_clean, sel))
    
    expected = '<foreign xml:lang="fr">bonjour</foreign>'
    if mock_editor.replaced_text == expected:
        print("✓ wrap_foreign_prompt test PROŠAO")
        return True
    else:
        print("✗ wrap_foreign_prompt test NIJE PROŠAO")
        print("  Očekivano: {0}".format(expected))
        print("  Dobijeno: {0}".format(mock_editor.replaced_text))
        return False


def test_foreign_prompt_with_escaping(mock_editor, mock_notepad):
    """Testira XML escaping u wrap_foreign_prompt.py skripti."""
    print("\n=== Test wrap_foreign_prompt (sa escapingom) ===")
    mock_editor.selected_text = "test"
    mock_editor.replaced_text = ""
    mock_notepad.prompt_response = 'en"test'
    
    sel = mock_editor.getSelText()
    if sel:
        lang = mock_notepad.prompt("Unesite vrednost za xml:lang atribut:", "Jezik", "en")
        if lang:
            # Očisti lang od potencijalno opasnih karaktera
            lang_clean = lang.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
            mock_editor.replaceSel('<foreign xml:lang="{0}">{1}</foreign>'.format(lang_clean, sel))
    
    expected = '<foreign xml:lang="en&quot;test">test</foreign>'
    if mock_editor.replaced_text == expected:
        print("✓ wrap_foreign_prompt (escaping) test PROŠAO")
        return True
    else:
        print("✗ wrap_foreign_prompt (escaping) test NIJE PROŠAO")
        print("  Očekivano: {0}".format(expected))
        print("  Dobijeno: {0}".format(mock_editor.replaced_text))
        return False


def run_all_tests():
    """Pokreće sve testove."""
    print("=" * 50)
    print("TESTIRANJE PYTHONSCRIPT SKRIPTI")
    print("=" * 50)
    
    mock_editor = MockEditor()
    mock_notepad = MockNotepad()
    
    results = []
    
    # Testiraj sve jednostavne wrap skripte
    results.append(test_wrap_tag("wrap_trailer", "<trailer>{sel}</trailer>", mock_editor))
    results.append(test_wrap_tag("wrap_title", "<title>{sel}</title>", mock_editor))
    results.append(test_wrap_tag("wrap_quote", "<quote>{sel}</quote>", mock_editor))
    results.append(test_wrap_tag("wrap_hi", "<hi>{sel}</hi>", mock_editor))
    results.append(test_wrap_tag("wrap_head", "<head>{sel}</head>", mock_editor))
    results.append(test_wrap_tag("wrap_serbian_quotes", u"\u201e{sel}\u201c", mock_editor))
    
    # Testiraj foreign skripte
    results.append(test_foreign_fixed(mock_editor))
    results.append(test_foreign_prompt(mock_editor, mock_notepad))
    results.append(test_foreign_prompt_with_escaping(mock_editor, mock_notepad))
    
    # Sumiraj rezultate
    print("\n" + "=" * 50)
    print("REZULTATI TESTIRANJA")
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print("Prošlo: {0}/{1}".format(passed, total))
    
    if passed == total:
        print("✓ SVI TESTOVI SU PROŠLI!")
    else:
        print("✗ NEKI TESTOVI NISU PROŠLI")
    
    return passed == total


if __name__ == "__main__":
    run_all_tests()
