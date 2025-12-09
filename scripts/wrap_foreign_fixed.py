# -*- coding: utf-8 -*-
"""
wrap_foreign_fixed.py
PythonScript skripta za Notepad++ koja obavija selektovani tekst 
u <foreign> tag sa fiksnim xml:lang="en" atributom.
"""

from Npp import editor

# Podrazumevani jezik
DEFAULT_LANG = "en"

# Uzmi selektovani tekst
sel = editor.getSelText()

# Ako postoji selekcija, obavij je u <foreign> tag sa xml:lang atributom
if sel:
    editor.replaceSel('<foreign xml:lang="{0}">{1}</foreign>'.format(DEFAULT_LANG, sel))
