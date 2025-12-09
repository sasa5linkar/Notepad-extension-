# -*- coding: utf-8 -*-
"""
wrap_head.py
PythonScript skripta za Notepad++ koja obavija selektovani tekst u <head> tag.
"""

from Npp import editor

# Uzmi selektovani tekst
sel = editor.getSelText()

# Ako postoji selekcija, obavij je u <head> tag
if sel:
    editor.replaceSel(f"<head>{sel}</head>")
