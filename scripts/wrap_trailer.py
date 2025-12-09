# -*- coding: utf-8 -*-
"""
wrap_trailer.py
PythonScript skripta za Notepad++ koja obavija selektovani tekst u <trailer> tag.
"""

from Npp import editor

# Uzmi selektovani tekst
sel = editor.getSelText()

# Ako postoji selekcija, obavij je u <trailer> tag
if sel:
    editor.replaceSel(f"<trailer>{sel}</trailer>")
