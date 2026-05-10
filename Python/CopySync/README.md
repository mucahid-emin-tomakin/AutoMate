# 🔄 CopySync

![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![SHA-256](https://img.shields.io/badge/SHA--256-FF6B6B?logo=hash&logoColor=white)
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

**CopySync** ist ein Python-basiertes Tool zur vollständigen 1:1-Synchronisation zweier Festplatten oder Verzeichnisse.  
Es vergleicht Quelle und Ziel, identifiziert fehlende oder fehlerhafte Elemente und kopiert diese automatisch – inklusive abschließender Integritätsprüfung.

**Warum dieses Tool?**
- Exakte Spiegelung ganzer Laufwerke ohne manuelles Durchsuchen und Kopieren.
- Intelligenter Vergleich: Größen-Check und optionaler SHA-256-Hash für absolute Sicherheit.
- Vier-Schritt-Prozess: Scannen → Kopieren → Prüfen → Report – alles automatisch.
- Fortschrittsanzeige mit Geschwindigkeit, hochgerechneter Zeit und GB-Statistik.
- Alles wird geloggt und als CSV + Text-Report gespeichert – ideal für Nachvollziehbarkeit.

**Für wen ist das?**
- Für Backup-Verantwortliche, die Festplatten exakt synchron halten müssen.
- Für alle, die eine verlässliche, automatisierte Kopierlösung suchen.
- Für Anwender, die vor dem Austausch einer Platte den Bestand prüfen wollen.

Das Tool ist Teil der **AutoMate**-Familie und wird dort zusammen mit weiteren Automatisierungslösungen weiterentwickelt.

---

## ✨ FEATURES

### 🔄 Synchronisation & Vergleich
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 📂 Vollständiger Abgleich | Rekursiver Vergleich aller Dateien & Ordner | ✅ |
| 📏 Größenvergleich | Erkennt abweichende Dateigrößen | ✅ |
| 🔐 Hash-Vergleich | Optionaler SHA-256-Inhaltsvergleich | ✅ |
| 📁 Ordner-Erstellung | Fehlende Verzeichnisse werden automatisch erstellt | ✅ |
| 📋 Datei-Kopie | Fehlende/fehlerhafte Dateien werden kopiert | ✅ |
| 🔄 Abschluss-Check | Finaler Vergleich nach dem Kopieren | ✅ |
| 📊 Report | CSV-Detail + TXT-Zusammenfassung | ✅ |
| 📝 Logging | Vollständiges Ausführungslog mit Zeitstempel | ✅ |

### 📁 Was es generiert
| Datei | Beschreibung |
|-------|-------------|
| `CheckComplete.csv` | Detaillierte Liste aller gefundenen Probleme |
| `Backup_Summary.txt` | Zusammenfassung mit Statistik |
| `BackupAutomationLog.txt` | Vollständiges Ausführungslog |
| `remaining_issues.txt` | Noch fehlende Elemente (nur bei Problemen) |
| `*.bak` | Backup der alten Logdatei |

---

## 🚀 TOOL

| Sprache / Format | Zweck |
|------------------|-------|
| Python 3.11+ | Kernlogik & Ausführung |
| SHA-256 | Optionaler Hash-Vergleich |
| CSV / TXT | Ausgabeformate |
| pathlib | Plattformunabhängige Pfadbehandlung |

### 🐍 Verwendete Bibliotheken
| Bibliothek | Zweck |
|------------|-------|
| 🐍 **Python 3.11** | Hauptprogrammiersprache |
| 🔐 **hashlib** | SHA-256 Hash-Berechnung |
| 📁 **os / shutil** | Dateisystem-Operationen & Kopieren |
| 🛤️ **pathlib** | Moderne Pfadbehandlung |
| 📝 **csv** | CSV-Report-Erstellung |
| 📅 **time** | Zeitmessung & Zeitstempel |
| 🔧 **sys** | System-Integration |

---

## ⚙️ KONFIGURATION

Alle Einstellungen sind am Anfang der Datei:

```python
# ============================== CONFIGURATION ==============================

SOURCE_DRIVE = r"F:\\"                          # Quelllaufwerk
TARGET_DRIVE = r"E:\\"                          # Ziellaufwerk
CHECK_CSV = "CheckComplete.csv"                 # CSV-Detail-Report
LOG_FILE = "BackupAutomationLog.txt"            # Logdatei
SUMMARY_FILE = "Backup_Summary.txt"             # Zusammenfassung
REMAINING_ISSUES_FILE = "remaining_issues.txt"  # Verbleibende Probleme

USE_HASH_COMPARISON = False                     # SHA-256-Vergleich (True = gründlich, False = schnell)
EXCLUDE_ITEMS = [                               # Ignorierte Elemente
    '$RECYCLE.BIN',
    'System Volume Information',
    '.Trash',
    '.Trashes',
    'Thumbs.db',
    'desktop.ini'
]

HASH_BUFFER_SIZE = 65536                        # Puffergröße für Hash-Berechnung
PROGRESS_INTERVAL_SCAN = 1000                   # Fortschritt alle N gescannten Elemente
PROGRESS_INTERVAL_COPY = 10                     # Fortschritt alle N kopierten Dateien
MAX_DISPLAY_MISSING = 20                        # Maximal angezeigte fehlende Elemente
LOG_BACKUP_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"   # Zeitstempel-Format
SUMMARY_LINE_WIDTH = 70                         # Breite der Haupt-Trennlinien
SUB_LINE_WIDTH = 40                             # Breite der Neben-Trennlinien
FILE_ENCODING = "utf-8"                         # Zeichenkodierung
```

---

## 📁 STRUKTUR

### 📂 Hauptverzeichnis
```Text
🔄 CopySync/
├── 🐍 CopySync.py
├── 🐍 CopySync - NoComment.py
├── 🐍 CopySync - Original.py
└── 📄 README.md

```

### 🐍 CopySync - Beispiel Run
```text
🔄 CopySync/
├── 🐍 CopySync.py
├── 📊 CheckComplete.csv
├── 📘 Backup_Summary.txt
├── 📘 BackupAutomationLog.txt
├── 📘 BackupAutomationLog.20260221_005208.bak
└── 📘 remaining_issues.txt      (nur bei Problemen)
```

### 📁 Struktur-Legende
```text
🔄 CopySync/
├── 🐍 .py                    # Python-Skripte (Hauptprogramm & Varianten)
├── 📄 README.md              # Projektbeschreibung (diese Datei)
├── 📊 .csv                   # CSV-Detail-Report
├── 📘 .txt                   # Log- & Summary-Dateien
└── 📘 .bak                   # Backups alter Logdateien
```

---

## ⚡ QUICK START

### 📦 Git & GitHub
```bash
# 1. Repository klonen
git clone https://github.com/mucahid-emin-tomakin/AutoMate.git
cd AutoMate

# 2. In den ein Projektfodler wechseln
cd AutoMate/Python/CopySync

# 3. Konfiguration anpassen (SOURCE_DRIVE, TARGET_DRIVE)

# 4. Tool ausführen (installiert fehlende Pakete automatisch)
python CopySync.py

# 5. Ergebnis prüfen
#    → Backup_Summary.txt für Zusammenfassung
#    → BackupAutomationLog.txt für Details
```

### 🐍 Python virtueller Umgebung
```bash
# Mit virtueller Umgebung
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
python CopySync.py
```

---

## 🖼️ SCREENSHOTS

### Schritt 1 – Vergleich
```text
======================================================================
 STEP 1: COMPARE ALL FILES AND FOLDERS
======================================================================
Scanning source directory...
Scanned: 5000 | Missing: 12 | Time: 00:00:23

Comparison complete!
Elements scanned: 5234
Missing/faulty elements: 12
Time elapsed: 00:00:25
```

### 📋 Schritt 2 – Kopieren
```Text
======================================================================
 STEP 2: COPY MISSING ELEMENTS
======================================================================
Creating missing directories...
Directories: 3/3

Copying 9 missing files...
Files: 9/9 (100.0%) | 4.52 GB | 112.3 MB/s

======================================================================
 COPY STATISTICS
======================================================================
Time elapsed:            00:00:41
Directories created:     3
Files copied:            9
Files skipped:           0
Total data copied:       4.52 GB
Average speed:           112.3 MB/s
Errors:                  0
```

### 📋 Schritt 3 – Abschluss-Check
```Text
======================================================================
 STEP 3: FINAL COMPLETE CHECK
======================================================================
Checking if all elements are present...
Checked: 5234 | Still missing: 0

✅ CONGRATULATIONS!
✅ All 5234 elements were successfully copied!
✅ Backup is complete and consistent!
✅ Check time: 00:00:12
```

### 📋 Schritt 4 – Report
```Text
======================================================================
 STEP 4: CREATE REPORT
======================================================================
✓ Detailed list saved as: CheckComplete.csv
✓ Summary saved as: Backup_Summary.txt
✓ Log file: BackupAutomationLog.txt
```

### 📋 Backup_Summary.txt
```Text
======================================================================
BACKUP AUTOMATION - SUMMARY
======================================================================

Timestamp:               2026-02-21 00:55:42
Source:                  F:\
Target:                  E:\
Hash comparison:         NO

RESULTS:
----------------------------------------
Problems found:           12
  • Missing directories:  3
  • Missing/faulty files: 9

✅ All missing elements were successfully copied!
✅ Final check passed!

FILES:
----------------------------------------
Detailed CSV list:        CheckComplete.csv
Log file:                 BackupAutomationLog.txt
Summary:                  Backup_Summary.txt
```

---

## ⚠️ WICHTIGE HINWEISE

### 📌 Vor der Verwendung
- ✅ SOURCE_DRIVE und TARGET_DRIVE korrekt setzen (z. B. r"F:\\")
- ✅ Zielpfad muss existieren – wird nicht automatisch erstellt
- ✅ Bei Hash-Vergleich: USE_HASH_COMPARISON = True (dauert länger, aber 100% sicher)
- ✅ Keine externen Python-Pakete nötig – nur Standard-Bibliothek

### 🔒 Sicherheit
- ⚠️ Vorhandene Logdatei wird automatisch als .bak gesichert
- ⚠️ Dateien werden kopiert, nicht verschoben – Quelle bleibt unverändert
- ⚠️ Bei großen Datenmengen: Skript kann je nach Größe mehrere Stunden dauern
- ⚠️ shutil.copy2 erhält Metadaten (Zeitstempel) der Originaldateien

### 💡 Tipps
- ✅ Bei Fehlern: BackupAutomationLog.txt prüfen
- ✅ EXCLUDE_ITEMS um systemspezifische Ordner erweitern
- ✅ Bei Netzwerklaufwerken: ausreichend Zeit einplanen
- ✅ PROGRESS_INTERVAL_SCAN anpassen für häufigere/seltenere Updates
- ✅ Für reine Backups reicht USE_HASH_COMPARISON = False (Größenvergleich)

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
🤖 AutoMate | 🔧 Automation Scripts | 🐍 Python | 🔄 CopySync

## 📊 REPOSITORY STATISTIK

| Metrik | Wert | Trend |
|--------|------|-------|
| **Stars** | ![GitHub Stars](https://img.shields.io/github/stars/mucahid-emin-tomakin/AutoMate) | 📈 |
| **Forks** | ![GitHub Forks](https://img.shields.io/github/forks/mucahid-emin-tomakin/AutoMate) | 🔄 |
| **Issues** | ![GitHub Issues](https://img.shields.io/github/issues/mucahid-emin-tomakin/AutoMate) | ✅ |
| **Letztes Update** | ![GitHub Last Commit](https://img.shields.io/github/last-commit/mucahid-emin-tomakin/AutoMate) | 🕐 |

---

### 🔧 Made with ❤️ on Python
