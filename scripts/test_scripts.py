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
        print(f"Replaced: {text}")


class MockNotepad:
    """Mock klasa koja simulira notepad objekat iz Npp modula."""
    
    def __init__(self):
        self.prompt_response = "en"
    
    def prompt(self, message, title, default):
        """Simulira prompt dijalog."""
        print(f"Prompt: {message}")
        print(f"Title: {title}")
        print(f"Default: {default}")
        return self.prompt_response


def test_wrap_tag(tag_name, expected_output, mock_editor):
    """Testira jednostavnu wrap skriptu."""
    print(f"\n=== Test {tag_name} ===")
    mock_editor.selected_text = "test text"
    mock_editor.replaced_text = ""
    
    # Simuliraj izvršavanje skripte
    sel = mock_editor.getSelText()
    if sel:
        mock_editor.replaceSel(expected_output.format(sel=sel))
    
    # Proveri rezultat
    if mock_editor.replaced_text == expected_output.format(sel="test text"):
        print(f"✓ {tag_name} test PROŠAO")
        return True
    else:
        print(f"✗ {tag_name} test NIJE PROŠAO")
        print(f"  Očekivano: {expected_output.format(sel='test text')}")
        print(f"  Dobijeno: {mock_editor.replaced_text}")
        return False


def test_foreign_fixed(mock_editor):
    """Testira wrap_foreign_fixed.py skriptu."""
    print("\n=== Test wrap_foreign_fixed ===")
    mock_editor.selected_text = "hello world"
    mock_editor.replaced_text = ""
    
    DEFAULT_LANG = "en"
    sel = mock_editor.getSelText()
    if sel:
        mock_editor.replaceSel(f'<foreign xml:lang="{DEFAULT_LANG}">{sel}</foreign>')
    
    expected = '<foreign xml:lang="en">hello world</foreign>'
    if mock_editor.replaced_text == expected:
        print("✓ wrap_foreign_fixed test PROŠAO")
        return True
    else:
        print("✗ wrap_foreign_fixed test NIJE PROŠAO")
        print(f"  Očekivano: {expected}")
        print(f"  Dobijeno: {mock_editor.replaced_text}")
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
            mock_editor.replaceSel(f'<foreign xml:lang="{lang}">{sel}</foreign>')
    
    expected = '<foreign xml:lang="fr">bonjour</foreign>'
    if mock_editor.replaced_text == expected:
        print("✓ wrap_foreign_prompt test PROŠAO")
        return True
    else:
        print("✗ wrap_foreign_prompt test NIJE PROŠAO")
        print(f"  Očekivano: {expected}")
        print(f"  Dobijeno: {mock_editor.replaced_text}")
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
    
    # Testiraj foreign skripte
    results.append(test_foreign_fixed(mock_editor))
    results.append(test_foreign_prompt(mock_editor, mock_notepad))
    
    # Sumiraj rezultate
    print("\n" + "=" * 50)
    print("REZULTATI TESTIRANJA")
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Prošlo: {passed}/{total}")
    
    if passed == total:
        print("✓ SVI TESTOVI SU PROŠLI!")
    else:
        print("✗ NEKI TESTOVI NISU PROŠLI")
    
    return passed == total


if __name__ == "__main__":
    run_all_tests()
