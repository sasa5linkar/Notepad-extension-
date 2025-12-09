# -*- coding: utf-8 -*-
"""
wrap_title.py
PythonScript skripta za Notepad++ koja obavija selektovani tekst u <title> tag.
"""

from Npp import editor

# Uzmi selektovani tekst
sel = editor.getSelText()

# Ako postoji selekcija, obavij je u <title> tag
if sel:
    editor.replaceSel("<title>{0}</title>".format(sel))
