# PythonScript Makroi za Notepad++ — XML Obeležavanje

![Test Scripts](https://github.com/sasa5linkar/Notepad-extension-/actions/workflows/test.yml/badge.svg)

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

**Kompatibilnost:** Ove skripte su napisane da budu kompatibilne sa PythonScript pluginom verzije 2.x koja koristi Python 2.7 (standardna verzija dostupna kroz Plugins Admin). Skripte koriste `.format()` sintaksu umesto f-string sintakse, tako da će raditi sa svim verzijama PythonScript plugina (Python 2.7 i Python 3.x).

## Kako pronaći Scripts folder?

Nakon što instalirate PythonScript, potrebno je da pronađete lokaciju gde se čuvaju skripte:

1. U Notepad++ meniju idite na **Plugins → PythonScript → Scripts**
2. Izaberite opciju **Open Script Folder** (ili **Show Console**)
3. Otvoriće se folder gde možete da dodate svoje skripte

Tipična putanja je:
```
C:\Users\[VašeKorisničkoIme]\AppData\Roaming\Notepad++\plugins\config\PythonScript\scripts\
```

## Kako instalirati skripte?

### Automatska instalacija (preporučeno) 🚀

Najbrži i najlakši način je korišćenje automatskog instalera:

1. Preuzmite ceo repozitorijum (kliknite na zeleno dugme "Code" → "Download ZIP")
2. Raspakujte ZIP arhivu na bilo koju lokaciju
3. **Važno**: Uverite se da imate instaliran **PythonScript plugin** u Notepad++ (vidi odeljak iznad)
4. Dvoklikom pokrenite `install.bat`
5. Installer će automatski:
   - Pronaći Notepad++ instalaciju
   - Kopirati sve skripte u odgovarajući folder
   - Dodati tastaturne prečice za svaku skriptu
   - Prikazati poruke o uspehu ili grešci

**Tastaturne prečice koje installer dodaje:**
- `wrap_title.py` → **Ctrl+Alt+1**
- `wrap_head.py` → **Ctrl+Alt+2**
- `wrap_hi.py` → **Ctrl+Alt+3**
- `wrap_quote.py` → **Ctrl+Alt+4**
- `wrap_trailer.py` → **Ctrl+Alt+5**
- `wrap_foreign_prompt.py` → **Ctrl+Alt+6**

**Nakon instalacije:**
- Restartujte Notepad++ da bi se aktivirale tastaturne prečice
- Skripte su odmah dostupne kroz **Plugins → PythonScript → Scripts**
- Tastaturne prečice će automatski raditi

**Napomene:**
- Installer zahteva Python 3 (proverite sa `python --version`)
- Installer automatski detektuje Notepad++ instalaciju kroz Windows Registry
- PythonScript plugin **mora** biti instaliran pre pokretanja installer-a
- Postojeće tastaturne prečice u Notepad++ će biti sačuvane

### Ručna instalacija (alternativa)

Ako preferirate ručnu instalaciju ili imate problema sa automatskim installerom:

1. Preuzmite sve `.py` fajlove iz `scripts/` foldera ovog GitHub repozitorijuma
2. Kopirajte ih u Scripts folder koji ste pronašli u prethodnom koraku
3. Skripte će odmah biti dostupne u Notepad++
4. Tastaturne prečice ćete morati ručno da dodelite (vidi sledeći odeljak)

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
    editor.replaceSel("<author>{0}</author>".format(sel))
```

## Testiranje skripti

Repozitorijum sadrži nekoliko testova koji osiguravaju ispravan rad skripti:

### Postojeći test skripta

Repozitorijum sadrži `scripts/test_scripts.py` koji služi kao mock okruženje za testiranje skripti van Notepad++:

- Pokreće se standardnom Python komandom: `python scripts/test_scripts.py`
- Simulira `editor` i `notepad` objekte iz Npp modula
- Testira sve skripte i prikazuje rezultate
- Koristan za razvoj novih skripti ili proveru da li skripte rade ispravno

### Unit testovi

U `tests/` folderu se nalaze sveobuhvatni unit testovi:

- **test_wrap_scripts.py** — 14 testova za sve wrap skripte
  - Testira osnovnu funkcionalnost svakog taga
  - Testira XML escaping u wrap_foreign_prompt.py
  - Testira edge case-ove (prazna selekcija, specijalni karakteri, Unicode, multiline tekst)
- **test_install.py** — 9 testova za install.py
  - Testira helper funkcije
  - Testira konfiguraciju tastaturnih prečica
  - Testira detekciju putanja (samo na Windows sistemima)

Pokretanje unit testova:

```bash
# Svi testovi
python -m unittest discover -s tests -v

# Samo testovi wrap skripti
python -m unittest tests.test_wrap_scripts -v

# Samo testovi installer-a
python -m unittest tests.test_install -v
```

### CI/CD — Automatsko testiranje

Projekat koristi **GitHub Actions** za automatsko testiranje pri svakom push-u i pull request-u:

- **Workflow**: `.github/workflows/test.yml`
- **Multi-OS testiranje**: Ubuntu i Windows
- **Multi-verzija Python-a**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Automatske provere**:
  - Pokreće sve unit testove
  - Pokreće test_scripts.py
  - Proverava sintaksu svih .py fajlova
  - Verifikuje da svi potrebni fajlovi postoje

Status testova možete videti u GitHub Actions tabu repozitorijuma.

## Doprinos i razvoj

### Za razvojne inženjere i AI asistente

Ako planirate da doprinесete projektu ili koristite AI asistente (GitHub Copilot, ChatGPT, Claude, itd.) za modifikaciju koda, **obavezno pročitajte**:

📖 **[`.github/CONTRIBUTING_AI.md`](.github/CONTRIBUTING_AI.md)** — Smernice za AI agente i asistente

Ovaj dokument sadrži **kritične informacije** o:
- Python 2.7 kompatibilnosti za Notepad++ skripte
- Obaveznoj upotrebi samo standardnih biblioteka
- Razlikama između `/scripts/` (Python 2.7) i `/tests/`, `/install.py` (Python 3.8+)
- Pravilima kodiranja i sintakse (`.format()` vs f-strings)

**Bitno:** Skripte u `/scripts/` folderu moraju biti kompatibilne sa **Python 2.7** jer PythonScript plugin u Notepad++ koristi tu verziju. Sve buduće skripte moraju poštovati ova ograničenja.

## Licenca

MIT License

Copyright (c) 2025

Dozvoljeno je slobodno korišćenje, kopiranje, modifikacija i distribucija ovog softvera.