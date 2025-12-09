# -*- coding: utf-8 -*-
"""
wrap_foreign_prompt.py
PythonScript skripta za Notepad++ koja obavija selektovani tekst 
u <foreign> tag sa xml:lang atributom koji korisnik unosi kroz dijalog.
"""

from Npp import editor, notepad

# Uzmi selektovani tekst
sel = editor.getSelText()

# Ako postoji selekcija
if sel:
    # Pitaj korisnika za vrednost xml:lang atributa
    lang = notepad.prompt("Unesite vrednost za xml:lang atribut:", "Jezik", "en")
    
    # Ako je korisnik uneo jezik (nije pritisnuo Cancel)
    if lang:
        # Očisti lang od potencijalno opasnih karaktera
        lang_clean = lang.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
        editor.replaceSel('<foreign xml:lang="{0}">{1}</foreign>'.format(lang_clean, sel))
