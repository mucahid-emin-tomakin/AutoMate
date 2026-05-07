# ⏱️ WorkingTimeTracker

![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Excel](https://img.shields.io/badge/Excel-217346?logo=microsoft-excel&logoColor=white)
![CSV](https://img.shields.io/badge/CSV-4A90E2?logo=code&logoColor=white)
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

Der **WorkingTimeTracker** ist ein Python-basiertes Tool zur automatischen Berechnung von Arbeitszeiten aus Excel- oder CSV-Tabellen.  
Statt mühsam manuell Stunden zusammenzurechnen, genügt eine zweispaltige Tabelle (Start / Ende) pro Mitarbeiter – das Skript erledigt den Rest.

**Warum dieses Tool?**
- Es verarbeitet fast jedes erdenkliche Zeitformat – ob `13:20`, `1320`, `9` oder `1705.0` aus Excel – und erkennt Nachtschichten automatisch.
- Es unterstützt mehrere Mitarbeiter in einer einzigen Datei und fasst die Ergebnisse übersichtlich zusammen.
- Sämtliche Schritte werden protokolliert (`Log.txt`) und die Ergebnisse inklusive Originaldatei in einem Zeitstempel-Archiv abgelegt – ideal für Nachvollziehbarkeit und Revisionssicherheit.
- Fehlende Python-Pakete werden bei Bedarf selbstständig nachinstalliert.

**Für wen ist das?**
- Für mich selbst – als zuverlässiger Helfer im Arbeitsalltag.
- Für Kollegen oder Freelancer, die ihre Arbeitszeiten schnell und fehlerfrei auswerten wollen.
- Für jeden, der eine simple, aber robuste Lösung für Excel-basierte Zeiterfassung sucht.

Das Tool ist Teil der **AutoMate**-Familie und wird dort zusammen mit weiteren Automatisierungslösungen weiterentwickelt.

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

## 🚀 TOOL

### 🐍 VERWENDETE BIBLIOTHEKEN
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

## 🖼️ SCREENSHOTS

### WorkingTimeTracker - Beispielausgabe
```text
========================================================================================================================
📊 WORKING HOURS - SUMMARY
========================================================================================================================
Employee                         Total (h/m/s)    Total (h)    Total (m)    Total (s)     Days
------------------------------------------------------------------------------------------------------------------------
Employee1                           26h 21m 00s        26.35         1581        94860        7
Employee2                           56h 33m 36s        56.56         3394       203616        7
------------------------------------------------------------------------------------------------------------------------
ALL EMPLOYEES                      82h 54m 36s        82.91         4975       298476       14
========================================================================================================================
```

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

### 📊 Excel/CSV Struktur
| Employee1         | Employee2         | Employee3         |
|-------------------|-------------------|-------------------|
| Start     | Ende  | Start     | Ende  | Start     | Ende  |
| 09:00     | 17:00 | 08:30     | 16:30 | 13:20     | 17:05 |
| 14:20     | 18:05 | 10:00     | 18:05 | 14:20     | 18:05 |

### ⏱️ Unterstützte Zeitformate
| Format | Beispiel | Erkannt als |
|--------|----------|-------------|
| hh:mm:ss | 13:20:00 | 13:20 |
| hh:mm | 13:20 | 13:20 |
| hhmmss | 132000 | 13:20 |
| hhmm | 1320 | 13:20 |
| h / hh | 9 oder 17 | 09:00 oder 17:00 |
| Excel-Zahl | 11.0, 1705.0 | 11:00, 17:05 |

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
| **Automation** | Skript-Entwickler & Automatisierer | 🤖 |
| **Interessen** | Python, System-Automation | ⚙️ |

**Teil der AutoMate Familie:**
🤖 AutoMate | 🔧 Automation Scripts | 🐍 Python | ⏱️ WorkingTimeTracker

## 📊 REPOSITORY STATISTIK

| Metrik | Wert | Trend |
|--------|------|-------|
| **Stars** | ![GitHub Stars](https://img.shields.io/github/stars/mucahid-emin-tomakin/AutoMate) | 📈 |
| **Forks** | ![GitHub Forks](https://img.shields.io/github/forks/mucahid-emin-tomakin/AutoMate) | 🔄 |
| **Issues** | ![GitHub Issues](https://img.shields.io/github/issues/mucahid-emin-tomakin/AutoMate) | ✅ |
| **Letztes Update** | ![GitHub Last Commit](https://img.shields.io/github/last-commit/mucahid-emin-tomakin/AutoMate) | 🕐 |

---

### 🔧 Made with ❤️ on Python
