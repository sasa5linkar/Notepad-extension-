# PythonScript Makroi za Notepad++ — XML Obeležavanje

## Šta je ovo?

Ovo je kolekcija gotovih **PythonScript makroa** za Notepad++ editor, osmišljena da olakša rad sa XML obeležavanjem tekstualnih datoteka. Skripte omogućavaju jednostavno i brzo obavijanje označenog (selektovanog) teksta u specifične XML tagove poput `<title>`, `<quote>`, `<trailer>`, `<hi>`, `<head>` i `<foreign>` — sve pomoću jednog klika ili prečice na tastaturi.

Sve skripte su napisane u Python programskom jeziku i spremne su za direktno korišćenje sa **PythonScript pluginom** u Notepad++. Ne zahtevaju nikakve dodatne biblioteke ili instalacije — samo kopirajte fajlove u odgovarajući folder i počnite da ih koristite.

## Koje skripte postoje?

Repozitorijum sadrži sledeće skripte u `scripts/` folderu:

- **wrap_trailer.py** — Obavija selektovani tekst u `<trailer>` tag
- **wrap_title.py** — Obavija selektovani tekst u `<title>` tag
- **wrap_quote.py** — Obavija selektovani tekst u `<quote>` tag
- **wrap_hi.py** — Obavija selektovani tekst u `<hi>` tag
- **wrap_head.py** — Obavija selektovani tekst u `<head>` tag
- **wrap_foreign_fixed.py** — Obavija selektovani tekst u `<foreign xml:lang="en">` sa fiksnim jezikom (en)
- **wrap_foreign_prompt.py** — Obavija selektovani tekst u `<foreign>` tag i pita korisnika da unese vrednost za `xml:lang` atribut kroz dijalog
- **test_scripts.py** — Mock okruženje za testiranje svih skripti van Notepad++

## Kako instalirati PythonScript plugin?

Da biste koristili ove skripte, prvo morate instalirati PythonScript plugin u Notepad++:

1. Otvorite Notepad++
2. Idite na meni **Plugins → Plugins Admin**
3. U listi dostupnih pluginova pronađite i označite **PythonScript**
4. Kliknite na dugme **Install**
5. Nakon instalacije, **restartujte Notepad++**

**Napomena:** PythonScript plugin je dostupan samo za Windows verziju Notepad++.

## Kako pronaći Scripts folder?

Nakon što instalirate PythonScript, potrebno je da pronađete lokaciju gde se čuvaju skripte:

1. U Notepad++ meniju idite na **Plugins → PythonScript → Scripts**
2. Izaberite opciju **Open Script Folder** (ili **Show Console**)
3. Otvoriće se folder gde možete da dodate svoje skripte

Tipična putanja je:
```
C:\Users\[VašeKorisničkoIme]\AppData\Roaming\Notepad++\plugins\config\PythonScript\scripts\
```

## Kako kopirati skripte iz repozitorijuma?

1. Preuzmite sve `.py` fajlove iz `scripts/` foldera ovog GitHub repozitorijuma
2. Kopirajte ih u Scripts folder koji ste pronašli u prethodnom koraku
3. Skripte će odmah biti dostupne u Notepad++

## Kako pokrenuti skripte?

Postoje dva načina da pokrenete skriptu:

### Način 1: Ručno iz menija
1. Selektujte (označite) tekst koji želite da obavijete u tag
2. Idite na **Plugins → PythonScript → Scripts**
3. Kliknite na naziv skripte (npr. `wrap_title`)
4. Selektovani tekst će biti automatski obavijen u odgovarajući XML tag

### Način 2: Pomoću tastaturnih prečica
Za brži rad, preporučuje se dodela tastaturnih prečica:

1. Idite na **Settings → Shortcut Mapper**
2. Izaberite tab **Plugin commands**
3. Pronađite vašu skriptu u listi (npr. `wrap_title`)
4. Dvoklikom otvorite dijalog i dodelite željenu kombinaciju tastera (npr. `Ctrl+Alt+T`)
5. Kliknite **OK** i zatvorite Shortcut Mapper
6. Od sada možete koristiti prečicu za brzo pokretanje skripte

## Bezbednost i Undo funkcija

Sve skripte su potpuno bezbedne za upotrebu:

- **Undo funkcija radi normalno** — Ako napravite grešku ili želite da poništite izmenu, jednostavno pritisnite `Ctrl+Z`
- Skripte ne menjaju fajlove na disku automatski — izmene su samo u editoru dok ne sačuvate fajl
- Ne postoji rizik od gubitka podataka jer Notepad++ čuva istoriju izmena

## Kako proširiti skripte?

Možete lako kreirati sopstvene skripte koristeći postojeće kao šablon:

1. Otvorite bilo koju od postojećih skripti (npr. `wrap_title.py`)
2. Kopirajte sadržaj i izmenite naziv taga prema vašim potrebama
3. Sačuvajte novu skriptu sa opisnim nazivom (npr. `wrap_author.py`)
4. Nova skripta će automatski biti dostupna u PythonScript meniju

Primer izmene:
```python
from Npp import editor

sel = editor.getSelText()
if sel:
    editor.replaceSel(f"<author>{sel}</author>")
```

## Testiranje skripti

Repozitorijum sadrži `test_scripts.py` koji služi kao mock okruženje za testiranje skripti van Notepad++:

- Pokreće se standardnom Python komandom: `python test_scripts.py`
- Simulira `editor` i `notepad` objekte iz Npp modula
- Testira sve skripte i prikazuje rezultate
- Koristan za razvoj novih skripti ili proveru da li skripte rade ispravno

## Licenca

MIT License

Copyright (c) 2025

Dozvoljeno je slobodno korišćenje, kopiranje, modifikacija i distribucija ovog softvera.