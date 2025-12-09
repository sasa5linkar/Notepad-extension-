# -*- coding: utf-8 -*-
"""
wrap_quote.py
PythonScript skripta za Notepad++ koja obavija selektovani tekst u <quote> tag.
"""

from Npp import editor

# Uzmi selektovani tekst
sel = editor.getSelText()

# Ako postoji selekcija, obavij je u <quote> tag
if sel:
    editor.replaceSel(f"<quote>{sel}</quote>")
