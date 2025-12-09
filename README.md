# Notepad++ PythonScript Ekstenzije za XML Tagove

Kolekcija PythonScript skripti za Notepad++ koje automatski obavijaju selektovani tekst u XML tagove.

## 📋 Sadržaj

- [Opis](#opis)
- [Dostupni XML Tagovi](#dostupni-xml-tagovi)
- [Instalacija](#instalacija)
- [Korišćenje](#korišćenje)
- [Testiranje](#testiranje)
- [Primeri](#primeri)

## Opis

Ova repozitorijum sadrži set Python skripti za Notepad++ koje omogućavaju brzo obavijanje selektovanog teksta u najčešće korišćene XML tagove. Skripta automatski prepoznaje da li je tekst selektovan ili ne, i na osnovu toga ili obavija postojeći tekst ili kreira prazne tagove sa kursorom pozicioniranim između njih.

## Dostupni XML Tagovi

Repozitorijum sadrži sledeće skripte u `/scripts` folderu:

- **wrap_title.py** - Obavija tekst u `<title>` tagove
- **wrap_head.py** - Obavija tekst u `<head>` tagove
- **wrap_hi.py** - Obavija tekst u `<hi>` tagove (highlight)
- **wrap_quote.py** - Obavija tekst u `<quote>` tagove
- **wrap_trailer.py** - Obavija tekst u `<trailer>` tagove
- **wrap_foreign.py** - Obavija tekst u `<foreign>` tagove

## Instalacija

### Korak 1: Instalacija PythonScript Plugina

1. Otvorite Notepad++
2. Idite na **Plugins** → **Plugins Admin**
3. U pretrazi ukucajte "PythonScript"
4. Označite checkbox pored **PythonScript** i kliknite **Install**
5. Restartujte Notepad++ kada vas to program zatraži

### Korak 2: Instalacija Skripti

#### Metod 1: Manuelno kopiranje

1. Preuzmite ili klonirajte ovaj repozitorijum:
   ```bash
   git clone https://github.com/sasa5linkar/Notepad-extension-.git
   ```

2. Pronađite PythonScript folder u Notepad++ instalaciji:
   - Obično se nalazi na: `%APPDATA%\Notepad++\plugins\config\PythonScript\scripts`
   - Ili koristite **Plugins** → **PythonScript** → **Show Console** i ukucajte:
     ```python
     import os
     print(os.path.dirname(__file__))
     ```

3. Kopirajte sve `.py` fajlove iz `scripts` foldera ovog repozitorijuma u PythonScript `scripts` folder

#### Metod 2: Korišćenje simboličkog linka (preporučeno za developere)

```bash
# Windows (pokrenite kao Administrator)
mklink /D "%APPDATA%\Notepad++\plugins\config\PythonScript\scripts\xml_wrappers" "C:\path\to\Notepad-extension-\scripts"

# Linux/Mac
ln -s /path/to/Notepad-extension-/scripts ~/.config/notepad++/plugins/config/PythonScript/scripts/xml_wrappers
```

### Korak 3: Kreiranje Prečica (Opciono ali Preporučeno)

Za brži pristup skriptama, možete kreirati tastaturne prečice:

1. Idite na **Plugins** → **PythonScript** → **Configuration**
2. U "User Scripts" sekciji, dodajte skripte koje želite
3. Kliknite **Add** da dodate svaku skriptu
4. Zatvorite dijalog i idite na **Settings** → **Shortcut Mapper**
5. Kliknite na **Plugin commands** tab
6. Pronađite vaše PythonScript skripte i dodelite im tastaturne prečice (npr. Ctrl+Alt+T za title)

## Korišćenje

### Osnovna Upotreba

1. **Sa selektovanim tekstom:**
   - Selektujte tekst koji želite da obavijete u XML tag
   - Idite na **Plugins** → **PythonScript** → **Scripts** → izaberite odgovarajuću skriptu
   - Tekst će biti automatski obavijen u odabrani XML tag

2. **Bez selektovanog teksta:**
   - Postavite kursor na mesto gde želite da ubacite tagove
   - Pokrenite skriptu
   - Prazni tagovi će biti ubačeni, a kursor će biti pozicioniran između njih

### Primeri Korišćenja

#### Primer 1: Obavijanje naslova
**Pre:**
```
Uvod u XML
```

**Selektujte tekst i pokrenite `wrap_title.py`:**
```xml
<title>Uvod u XML</title>
```

#### Primer 2: Kreiranje praznih tagova
**Pokrenite `wrap_quote.py` bez selekcije:**
```xml
<quote>|</quote>
```
(| predstavlja poziciju kursora)

#### Primer 3: Obavijanje stranog teksta
**Pre:**
```
Hello World
```

**Selektujte tekst i pokrenite `wrap_foreign.py`:**
```xml
<foreign>Hello World</foreign>
```

#### Primer 4: Rad sa cirillicom
**Pre:**
```
Важан текст
```

**Selektujte tekst i pokrenite `wrap_hi.py`:**
```xml
<hi>Важан текст</hi>
```

## Testiranje

Repozitorijum uključuje `test_scripts.py` koji testira funkcionalnost svih skripti.

### Pokretanje Testova

```bash
# Navigirajte do foldera projekta
cd Notepad-extension-

# Pokrenite testove
python test_scripts.py
```

### Testovi Pokrivaju

- Obavijanje selektovanog teksta u sve podržane XML tagove
- Kreiranje praznih tagova kada nema selekcije
- Pozicioniranje kursora između praznih tagova
- Podršku za specijalne karaktere
- Podršku za Unicode/Ćirilični tekst
- Proveru postojanja svih script fajlova
- Proveru UTF-8 enkodiranja

## Napomene

- Sve skripte koriste UTF-8 enkodiranje i podržavaju Unicode karaktere (uključujući ćirilicu)
- Skripte **ne vrše** automatsko escape-ovanje specijalnih XML karaktera (& < > itd.) - to vam daje fleksibilnost da sami kontrolišete encoding
- Svaka skripta je samostalna i može se koristiti nezavisno od drugih

## Tehnički Detalji

### Struktura Projekta

```
Notepad-extension-/
├── scripts/
│   ├── wrap_title.py      # <title> tag wrapper
│   ├── wrap_head.py       # <head> tag wrapper
│   ├── wrap_hi.py         # <hi> tag wrapper
│   ├── wrap_quote.py      # <quote> tag wrapper
│   ├── wrap_trailer.py    # <trailer> tag wrapper
│   └── wrap_foreign.py    # <foreign> tag wrapper
├── test_scripts.py        # Unit testovi
├── README.md              # Ova dokumentacija
└── LICENSE                # Licenca
```

### Zavisnosti

- **Notepad++** (testirano na verziji 8.x)
- **PythonScript plugin** za Notepad++ (testirano na verziji 3.x)
- **Python 3.x** (samo za pokretanje testova)

## Doprinos

Doprinosi su dobrodošli! Ako želite da dodate nove tagove ili poboljšate postojeće skripte:

1. Forkujte repozitorijum
2. Kreirajte feature branch (`git checkout -b feature/novi-tag`)
3. Komitujte promene (`git commit -am 'Dodaj novi tag wrapper'`)
4. Pushujte na branch (`git push origin feature/novi-tag`)
5. Otvorite Pull Request

## Licenca

Pogledajte [LICENSE](LICENSE) fajl za detalje.

## Autor

**sasa5linkar**

## Podrška

Ako imate pitanja ili probleme, molimo vas da otvorite issue na GitHub-u.