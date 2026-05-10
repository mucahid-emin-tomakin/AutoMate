# 🔄 NameShift

![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Automation](https://img.shields.io/badge/Automation-FF6B6B?logo=robot&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/Status-Abgeschlossen-brightgreen)

---

## 📖 INHALTSVERZEICHNIS

- [📝 PROJEKTBESCHREIBUNG](#-projektbeschreibung)
- [✨ FEATURES](#-features)
- [🚀 TOOL](#-tool)
- [⚙️ KONFIGURATION](#️-konfiguration)
- [📁 STRUKTUR](#-struktur)
- [🖼️ SCREENSHOTS](#️-screenshots)
- [⚡ QUICK START](#-quick-start)
- [⚠️ WICHTIGE HINWEISE](#️-wichtige-hinweise)
- [📝 LIZENZ](#-lizenz)
- [👤 AUTOR](#-autor)

---

## 📝 PROJEKTBESCHREIBUNG

**NameShift** ist ein Python-basiertes Tool zur automatischen Umbenennung von Ordnern und Dateien sowie zur Erstellung einer vollständigen Dateiliste.  
Es reorganisiert Datumsangaben in Ordnernamen, entfernt störende Zeichen aus Dateinamen und protokolliert alle Änderungen sauber in einer CSV-Datei.

**Warum dieses Tool?**
- Ordnernamen mit Datumsangaben wie `Projekt-01.02.2026-Rest` werden automatisch zu `Projekt-2026.02.01-Rest` umformatiert.
- Die Reihenfolge der Datumsbestandteile ist frei konfigurierbar – egal ob Tag.Monat.Jahr oder Monat.Tag.Jahr.
- Störende Zeichen wie `(` oder `)` werden aus Dateinamen entfernt.
- Alle Ordner- und Dateinamen können in eine übersichtliche Textdatei exportiert werden.
- Jede Umbenennung wird in einer CSV-Datei protokolliert – vollständig nachvollziehbar.

**Für wen ist das?**
- Für alle, die eine einheitliche Datumsstruktur in Projektordnern brauchen.
- Für Anwender, die Dateinamen für Web-Uploads bereinigen müssen.
- Für jeden, der einen schnellen Überblick über seine Ordnerinhalte als Liste benötigt.

Das Tool ist Teil der **AutoMate**-Familie und wird dort zusammen mit weiteren Automatisierungslösungen weiterentwickelt.

---

## ✨ FEATURES

### 🔄 Umbenennung & Export
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 📁 Ordner umbenennen | Datum im Ordnernamen neu anordnen | ✅ |
| 📄 Dateien umbenennen | Störende Zeichen entfernen | ✅ |
| 📋 Namens-Export | Alle Ordner- und Dateinamen als TXT | ✅ |
| 📝 Umbenennungs-Log | CSV mit Alt → Neu | ✅ |
| 🎯 Erweiterungs-Filter | Nur bestimmte Dateitypen umbenennen | ✅ |
| 🔧 Freie Datums-Reihenfolge | Tag.Monat.Jahr beliebig konfigurierbar | ✅ |

### 📁 Was es generiert
| Datei | Beschreibung |
|-------|-------------|
| `folder_file_list.txt` | Liste aller Ordner- und Dateinamen |
| `rename_log.csv` | CSV-Protokoll aller Umbenennungen |

---

## 🚀 TOOL

| Sprache / Format | Zweck |
|------------------|-------|
| Python 3.11+ | Kernlogik & Ausführung |
| CSV | Umbenennungs-Protokoll |
| TXT | Ordner-/Dateilisten-Export |
| os.walk | Rekursive Verzeichnisdurchsuche |

### 🐍 Verwendete Bibliotheken
| Bibliothek | Zweck |
|------------|-------|
| 🐍 **Python 3.11** | Hauptprogrammiersprache |
| 📁 **os** | Dateisystem-Operationen & Umbenennung |
| 📝 **re** | Reguläre Ausdrücke (vorbereitet) |
| 📅 **datetime** | Datumsmanipulation |

---

## ⚙️ KONFIGURATION

Alle Einstellungen sind am Anfang der Datei:

```python
# ============================== CONFIGURATION ==============================

FOLDER_PATH = r"C:\Users\USER\Documents\Projekte"      # Zielverzeichnis
LOG_FILE = r"C:\Users\USER\Downloads\folder_file_list.txt"  # Namens-Export
RENAME_LOG_FILE = r"C:\Users\USER\Downloads\rename_log.csv" # Umbenennungs-Log

RENAME_FOLDERS = True           # Ordner umbenennen aktivieren
LOG_FOLDER_FILE_NAMES = True    # Namens-Export aktivieren
RENAME_FILES = True             # Dateien umbenennen aktivieren

RENAME_FILE_EXTENSIONS = [".html"]   # Nur diese Dateitypen umbenennen
REMOVE_CHARS = ["(", ")"]            # Zu entfernende Zeichen
FILE_ENCODING = "utf-8"              # Zeichenkodierung für Logs
CSV_SEPARATOR = ";"                  # Trennzeichen für CSV

DATE_INPUT_ORDER = ["day", "month", "year"]      # Aktuelles Datumsformat
DATE_OUTPUT_ORDER = ["year", "month", "day"]     # Gewünschtes Datumsformat
DATE_SEPARATOR = "."                              # Trennzeichen im Datum
MIN_LENGTH_FOR_DATE = 18                          # Minimale Namenslänge für Datumsprüfung
```

---

## 📁 STRUKTUR

### 📂 Hauptverzeichnis
```Text
🔄 NameShift/
├── 🐍 NameShift.py
├── 🐍 NameShift - NoComment.py
└── 📄 README.md
```

### 🐍 NameShift - Beispiel Run
```text
🔄 NameShift/
├── 🐍 NameShift.py
├── 📘 folder_file_list.txt
├── 📊 rename_log.csv
└── 📄 README.md
```

### 🐍 NameShift - Beispieldaten vorher/nachher
```text
📁 Projekte/
├── 📁 Meeting-01.02.2026-Notizen     → 📁 Meeting-2026.02.01-Notizen
├── 📁 Bericht-15.03.2026             → 📁 Bericht-2026.03.15
├── 📄 index(1).html                  → 📄 index 1.html
└── 📄 about(2).html                  → 📄 about 2.html
```

### 📁 Struktur-Legende
```text
🔄 NameShift/
├── 🐍 .py                    # Python-Skripte (Hauptprogramm & Varianten)
├── 📄 README.md              # Projektbeschreibung (diese Datei)
├── 📘 .txt                   # Ordner-/Dateinamen-Export
└── 📊 .csv                   # Umbenennungs-Protokoll
```

---

## ⚡ QUICK START

### 📦 Git & GitHub
```bash
# 1. Repository klonen
git clone https://github.com/mucahid-emin-tomakin/AutoMate.git
cd AutoMate

# 2. In den ein Projektfodler wechseln
cd AutoMate/Python/NameShift

# 3. Konfiguration anpassen (FOLDER_PATH)

# 4. Tool ausführen (installiert fehlende Pakete automatisch)
python NameShift.py

# 5. Ergebnisse prüfen
#    → folder_file_list.txt für Namens-Export
#    → rename_log.csv für Umbenennungs-Protokoll
```

### 🐍 Python virtueller Umgebung
```bash
# Mit virtueller Umgebung
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
python NameShift.py
```

---

## 🖼️ SCREENSHOTS

### Schritt 1 – Ordner umbenennen
```text
==================================================
 STEP: RENAME FOLDERS
==================================================
✓ Renamed: Meeting-01.02.2026-Notizen  →  Meeting-2026.02.01-Notizen
✓ Renamed: Bericht-15.03.2026  →  Bericht-2026.03.15

Folders renamed: 2
```

### 📋 Schritt 2 – Namen exportieren
```Text
==================================================
 STEP: LOG FOLDER & FILE NAMES
==================================================
✓ Folders logged: 5
✓ Files logged: 12
✓ Log saved to: C:\Users\USER\Downloads\folder_file_list.txt
```

### 📋 Schritt 3 – Dateien umbenennen
```Text
==================================================
 STEP: RENAME FILES
==================================================
✓ Renamed: index(1).html  →  index 1.html
✓ Renamed: about(2).html  →  about 2.html

Files renamed: 2
```

### 📋 folder_file_list.txt
```Text
Meeting-2026.02.01-Notizen
Bericht-2026.03.15
index 1.html
about 2.html
```

### 📋 rename_log.csv
```Text
Meeting-01.02.2026-Notizen;Meeting-2026.02.01-Notizen
Bericht-15.03.2026;Bericht-2026.03.15
index(1).html;index 1.html
about(2).html;about 2.html
```

---

## ⚠️ WICHTIGE HINWEISE

### 📌 Vor der Verwendung
- ✅ FOLDER_PATH auf das gewünschte Verzeichnis setzen
- ✅ DATE_INPUT_ORDER und DATE_OUTPUT_ORDER ans aktuelle Format anpassen
- ✅ RENAME_FILE_EXTENSIONS definiert, welche Dateien umbenannt werden
- ✅ Keine externen Python-Pakete nötig – nur Standard-Bibliothek

### 🔒 Sicherheit
- ⚠️ Vor dem ersten Lauf: Test mit einer Kopie der Ordnerstruktur
- ⚠️ Umbenennungen werden in rename_log.csv protokolliert – zur Rückverfolgung
- ⚠️ Bei Namenskonflikten wird ein Zähler angehängt (index 1.html)
- ⚠️ Ordner unter MIN_LENGTH_FOR_DATE werden nicht umbenannt (Schutz vor Fehlern)

### 💡 Tipps
- ✅ RENAME_FOLDERS = False setzen, wenn nur Dateien umbenannt werden sollen
- ✅ LOG_FOLDER_FILE_NAMES = True für eine vollständige Inventarliste
- ✅ REMOVE_CHARS um weitere Zeichen erweitern (z. B. "[", "]")
- ✅ DATE_SEPARATOR anpassen, wenn Bindestriche statt Punkte verwendet werden

---

## 📝 LIZENZ
  Dieses Projekt ist unter der **MIT License** lizenziert - frei für persönliche und kommerzielle Nutzung.

---

## 👤 AUTOR

**Mücahid Emin Tomakin (TomaKing)**

| Platform | Link | Icon |
|----------|------|------|
| **GitHub** | [@mucahid-emin-tomakin](https://github.com/mucahid-emin-tomakin) | 🐙 |
| **Automation** | Skript-Entwickler & Automatisierer | 🤖 |
| **Interessen** | Python, System-Automation | ⚙️ |

**Teil der AutoMate Familie:**
🤖 AutoMate | 🔧 Automation Scripts | 🐍 Python | 🔄 NameShift

## 📊 REPOSITORY STATISTIK

| Metrik | Wert | Trend |
|--------|------|-------|
| **Stars** | ![GitHub Stars](https://img.shields.io/github/stars/mucahid-emin-tomakin/AutoMate) | 📈 |
| **Forks** | ![GitHub Forks](https://img.shields.io/github/forks/mucahid-emin-tomakin/AutoMate) | 🔄 |
| **Issues** | ![GitHub Issues](https://img.shields.io/github/issues/mucahid-emin-tomakin/AutoMate) | ✅ |
| **Letztes Update** | ![GitHub Last Commit](https://img.shields.io/github/last-commit/mucahid-emin-tomakin/AutoMate) | 🕐 |

---

### 🔧 Made with ❤️ on Python
