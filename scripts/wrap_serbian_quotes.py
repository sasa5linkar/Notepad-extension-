# -*- coding: utf-8 -*-
"""
wrap_serbian_quotes.py
PythonScript skripta za Notepad++ koja obavija selektovani tekst u srpske navodnike.
"""

from Npp import editor

# Uzmi selektovani tekst
sel = editor.getSelText()

# Ako postoji selekcija, obavij je u srpske navodnike („ i “)
if sel:
    editor.replaceSel('„{0}“'.format(sel))
