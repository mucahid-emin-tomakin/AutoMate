# ⏱️ WorkingTimeTracker

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Excel](https://img.shields.io/badge/Excel-217346?logo=microsoft-excel&logoColor=white)
![CSV](https://img.shields.io/badge/CSV-4A90E2?logo=code&logoColor=white)
![Automation](https://img.shields.io/badge/Automation-FF6B6B?logo=robot&logoColor=white)
![Status](https://img.shields.io/badge/Status-Finished-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)

---

## 📖 Inhaltsverzeichnis

- [✨ FEATURES](#-features)
- [⚡ QUICK START](#-quick-start)
- [📁 STRUKTUR](#-struktur)
- [📋 EINGABEFORMAT](#-eingabeformat)
- [📊 BEISPIEL-AUSGABE](#-beispiel-ausgabe)
- [⚙️ KONFIGURATION](#️-konfiguration)
- [🐍 VERWENDETE BIBLIOTHEKEN](#-verwendete-bibliotheken)
- [⚠️ WICHTIGE HINWEISE](#️-wichtige-hinweise)
- [📝 LIZENZ](#-lizenz)
- [👤 AUTOR](#-autor)

---

## ✨ FEATURES

### ⏱️ Zeiterfassung & Berechnung

| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 📂 Datei-Unterstützung | Excel (.xlsx) & CSV Dateien | ✅ |
| 👥 Mehrere Mitarbeiter | Spalten A-B, C-D, usw. | ✅ |
| ⏰ Format-Erkennung | 13:20, 1320, 9, 11.0, 1705.0 | ✅ |
| 🌙 Nachtschicht | Automatische Erkennung | ✅ |
| 📊 Ergebnis-Datei | TXT mit h/m/s, Minuten, Sekunden | ✅ |
| 🗄️ Archivierung | Automatisch mit Zeitstempel | ✅ |
| 📝 Logging | Vollständiges Log für Fehlersuche | ✅ |
| 🔧 Auto-Installation | Fehlende Pakete werden installiert | ✅ |

### 📁 Was es generiert

| Datei | Beschreibung |
|-------|-------------|
| `Result.txt` | Zusammenfassung + Tagesdetails |
| `Log.txt` | Vollständiges Ausführungslog |
| `Archive/` | Ordner mit allen generierten Dateien |

---

## ⚡ QUICK START

```bash
# 1. Repository klonen (falls nicht vorhanden)
git clone https://github.com/mucahid-emin-tomakin/AutoMate.git
cd AutoMate/Python/WorkingTimeTracker

# 2. Excel/CSV-Datei mit "WorkingTimeTracker" im Namen bereitlegen
#    Beispiel: WorkingTimeTracker.xlsx oder WorkingTimeTracker.csv

# 3. Tool ausführen (installiert fehlende Pakete automatisch)
python WorkingTimeTracker.py

# 4. Ergebnis im Archive-Ordner prüfen
cd Archive/2026.02.20_23.30.45/
cat Result.txt
```

---

## 📁 STRUKTUR

### 📂 Hauptverzeichnis
```Text
WorkingTimeTracker/
├── 📄 WorkingTimeTracker.py
├── 📄 README.md
└── 📁 Archive/
└── 📁 YYYY.MM.DD_HH.MM.SS/
├── 📄 Result.txt
├── 📄 Log.txt
└── 📄 WorkingTimeTracker*.xlsx (Original)
```

### 🗂️ Archiv-Ordner (Beispiel)
```Text
Archive/
└── 📁 2026.02.20_23.30.45/
├── 📄 Result.txt
├── 📄 Log.txt
└── 📄 WorkingTimeTracker.xlsx
```

---

## 📋 EINGABEFORMAT

### 📊 Excel/CSV Struktur
| Employee1         | Employee2         | Employee3         |
|-------------------|-------------------|-------------------|
| Start     | Ende  | Start     | Ende  | Start     | Ende  |
| 09:00     | 17:00 | 08:30     | 16:30 | 13:20     | 17:05 |
| 14:20     | 18:05 | 10:00     | 18:05 | 14:20     | 18:05 |

### ⏱️ Unterstützte Zeitformate
| Format    | Beispiel  | Erkannt als  |
| hh:mm:ss  | 13:20:00  | 13:20 |
| hh:mm     | 13:20     | 13:20 |
| hhmmss    | 132000    | 13:20 |
| hhmm      | 1320      | 13:20 |
| h / hh    | 9 oder 17 | 09:00 oder 17:00  |
| Excel-Zahl| 11.0, 1705.0 | 11:00, 17:05   |

---

## 📊 BEISPIEL-AUSGABE

### 📋 Result.txt
```Text
===========================================================================================================================
================================================= 📊 WORKING HOURS - SUMMARY ==================================================
===========================================================================================================================

Employee                         Total (h/m/s)    Total (h)    Total (m)    Total (s)     Days
------------------------------------------------------------------------------------------------------------------------
Employee1                         26h 21m 00s        26.35         1581        94860        7
Employee2                         56h 33m 36s        56.56         3394       203616        7
Employee3                         36h 22m 48s        36.38         2183       130968        7
Employee4                         26h 21m 00s        26.35         1581        94860        7
------------------------------------------------------------------------------------------------------------------------
ALL EMPLOYEES                     145h 38m 24s       145.64         8738       524304       28
========================================================================================================================

===========================================================================================================================
================================================= 📋 DETAILS BY EMPLOYEE ==================================================
===========================================================================================================================

👤 Employee1:
  Day 1: 13:20:00 - 17:05:00 = 3h45m00s   3.75h   225m   13500s
  Day 2: 14:20:00 - 18:05:00 = 3h45m00s   3.75h   225m   13500s
  ...
  📊 Total: 26h 21m 0s in 7 days (3h45m36s/day) (3.76h/day) (226m/day) (13536s/day)
---------------------------------------------------------------------------------------------------------------------------
👤 Employee2:
  ...

===========================================================================================================================
==================================================== Completed =====================================================
===========================================================================================================================

📁 Original file: WorkingTimeTracker.xlsx
📅 Calculated on: 21.02.2026 00:52:08
📋 Log file: Log.txt

===========================================================================================================================
```

---

## ⚙️ KONFIGURATION

Alle Einstellungen sind am Anfang der Datei:
```Python
# ========== CONFIGURATION VARIABLES ==========
# Edit these variables as needed

FILE_PATTERNS = ["WorkingTimeTracker*.csv", "WorkingTimeTracker*.xlsx"]  # Dateimuster
ARCHIVE_FOLDER_NAME = "Archive"                 # Archiv-Ordner
MAX_HOURS_PER_DAY = 24                          # Maximale Stunden pro Tag
MIN_HOURS_PER_DAY = 0                           # Minimale Stunden pro Tag
LOG_FILE_PREFIX = "Log"                         # Log-Präfix
RESULT_FILE_PREFIX = "Result"                   # Ergebnis-Präfix
```

---

## 🐍 VERWENDETE BIBLIOTHEKEN
- 🐍 **Python 3.11** - Hauptprogrammiersprache
- 📊 **pandas** - Einlesen und Verarbeiten von Excel/CSV
- 📗 **openpyxl** - Excel-Datei Unterstützung (.xlsx)
- 📘 **xlrd** - Ältere Excel-Dateien (.xls)
- 🗄️ **shutil** - Archivieren der Originaldateien
- 📝 **datetime** - Zeitberechnungen und Zeitstempel
- 🔧 **subprocess** - Auto-Installation fehlender Pakete
- 🔧 **glob** - Dateisuche mit Platzhaltern
- 📋 **logging** - Für detaillierte Fehleranalyse und Nachvollziehbarkeit

---

## ⚠️ WICHTIGE HINWEISE

### 📌 Vor der Verwendung
- ✅ Excel/CSV-Datei muss mit "Zaman" beginnen (Groß-/Kleinschreibung beachten!)
- ✅ Datei muss im gleichen Ordner wie das Skript liegen
- ✅ Erste Zeile = Mitarbeiternamen (jeder Name 2 Spalten)
- ✅ Zweite Zeile = "Start", "Ende" Markierungen

### 🔒 Sicherheit
- ⚠️ Keine sensiblen Daten committen
- ⚠️ Originaldateien werden kopiert, nicht verschoben (ab jetzt)
- ⚠️ Bei Absturz: Log-Datei prüfen!

### 💡 Tipps
- ✅ Bei Problemen: log*.txt im Archive-Ordner prüfen
- ✅ Bei Nachtschichten: Automatische Erkennung
- ✅ Bei Formatfehlern: DEBUG-Ausgaben im Log

---

## 📝 LIZENZ
  Dieses Projekt ist unter der **MIT License** lizenziert - frei für persönliche und kommerzielle Nutzung.

---

## 👤 AUTOR

**Mücahid Emin Tomakin (TomaKing)**

| Platform | Link | Icon |
|----------|------|------|
| **GitHub** | [@mucahid-emin-tomakin](https://github.com/mucahid-emin-tomakin) | 🐙 |

**Teil der AutoMate Familie:**
🤖 AutoMate | 🔧 Automation Scripts | 🐍 Python | ⏱️ WorkingTimeTracker

---

### 🔧 Made with ❤️ on Python
