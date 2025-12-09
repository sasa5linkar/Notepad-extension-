# -*- coding: utf-8 -*-
"""
wrap_hi.py
PythonScript skripta za Notepad++ koja obavija selektovani tekst u <hi> tag.
"""

from Npp import editor

# Uzmi selektovani tekst
sel = editor.getSelText()

# Ako postoji selekcija, obavij je u <hi> tag
if sel:
    editor.replaceSel(f"<hi>{sel}</hi>")
