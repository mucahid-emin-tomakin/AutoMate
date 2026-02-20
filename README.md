# 🤖 AutoMate

![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)
![Automation](https://img.shields.io/badge/Automation-FF6B6B?logo=robot&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Scripts](https://img.shields.io/badge/Scripts-4A90E2?logo=code&logoColor=white)
![Excel](https://img.shields.io/badge/Excel-217346?logo=microsoft-excel&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)

---

## 📖 Inhaltsverzeichnis

- [✨ FEATURES](#-features)
- [🖼️ SCREENSHOTS](#️-screenshots)
- [⚡ QUICK START](#-quick-start)
- [📁 STRUKTUR](#-struktur)
- [🚀 TOOL](#-tool)
- [⚙️ KONFIGURATION](#️-konfiguration)
- [⚠️ WICHTIGE HINWEISE](#️-wichtige-hinweise)
- [📝 LIZENZ](#-lizenz)
- [👤 AUTOR](#-autor)
- [📊 REPOSITORY STATISTIK](#-repository-statistik)

---

## ✨ FEATURES

### 🤖 Automatisierung & Skripte

| Feature | Beschreibung | Status |
|---------|-------------|--------|
| ⏱️ Arbeitszeiterfassung | Excel/CSV Zeitberechnung | ✅ |
| 📊 Excel Automatisierung | Datenverarbeitung & Analyse | 🚧 |
| 📁 Dateiorganisation | Automatische Sortierung | 🚧 |
| 🔄 Backup-Skripte | Automatische Datensicherung | 🚧 |
| ⚙️ Task-Automation | Wiederkehrende Aufgaben | 🚧 |

### 💻 Technologien & Sprachen

| Technologie | Verwendung |
|------------|-----------|
| Python 🐍 | Hauptsprache für Automatisierungen |
| VBScript 📜 | Windows-spezifische Skripte |
| PowerShell ⚡ | System-Administration |
| Batch 📦 | Einfache Windows-Automation |
| Excel VBA 📊 | Excel-Makros & Automatisierung |

### 📋 Skript-Typen

| Typ | Beispiele | Status |
|-----|----------|--------|
| ⏱️ Zeit-Tracker | WorkingTimeTracker | ✅ |
| 📊 Excel-Tools | Datenverarbeitung | 🚧 |
| 📁 File-Manager | Dateiorganisation | 🚧 |
| 🔧 System-Tools | Wartung & Backup | 🚧 |
| 🤖 Allgemein | Verschiedene Aufgaben | 🚧 |

---

## 🖼️ SCREENSHOTS

### WorkingTimeTracker - Beispielausgabe
```text
========================================================================================================================
📊 WORKING HOURS - SUMMARY
========================================================================================================================
Employee                         Total (h/m/s)    Total (h)    Total (m)    Total (s)     Days
------------------------------------------------------------------------------------------------------------------------
Mücahid                             26h 21m 0s        26.35         1581        94860        7
Bahaddin                           56h 33m 36s        56.56         3394       203616        7
------------------------------------------------------------------------------------------------------------------------
ALL EMPLOYEES                      82h 54m 36s        82.91         4975       298476       14
========================================================================================================================
```

---

## ⚡ QUICK START
```bash
# 1. Repository klonen
git clone https://github.com/mucahid-emin-tomakin/AutoMate.git

# 2. In ein Projektverzeichnis wechseln
cd AutoMate/Python/WorkingTimeTracker

# 3. Skript ausführen (installiert Pakete automatisch)
python WorkingTimeTracker.py

# 4. Ergebnis im Archive-Ordner prüfen
cd Archive/2026.02.20_23.30.45/
cat result_2026.02.20_23.30.45.txt
```

---

## 📁 STRUKTUR

### 📂 Hauptverzeichnis
```text
AutoMate/
├── 📁 Python/          # Python Automatisierungen
└── 📄 README.md
```

### 🐍 Python Automatisierungen
```text
Python/
└── 📁 WorkingTimeTracker/
```

### 🐍 WorkingTimeTracker
```text
WorkingTimeTracker/
├── 📄 WorkingTimeTracker.py
├── 📊 WorkingTimeTracker.xlsx
└── 📄 README.md
└── 📁 Archive/           # Automatisch erstellt
    └── 📁 YYYY.MM.DD_HH.MM.SS/
        ├── 📘 Result.txt
        ├── 📘 Log.txt
        └── 📊 WorkingTimeTracker.xlsx
```

---

## 🚀 TOOL

### 🐍 Python

#### 📦 **WorkingTimeTracker** ⏱️
- 🐍 **Python 3.11** - Hauptprogrammiersprache
- 📊 **pandas** - Für das Einlesen und Verarbeiten von Excel/CSV-Dateien
- 📗 **openpyxl** - Für Excel-Datei Unterstützung (.xlsx)
- 📘 **xlrd** - Für ältere Excel-Dateien (.xls)
- 🗄️ **shutil** - Für das Archivieren der Originaldateien
- 📝 **datetime** - Für Zeitberechnungen und Zeitstempel
- 🔧 **subprocess** - Für Auto-Installation fehlender Pakete
- 📋 **logging** - Für detaillierte Fehleranalyse und Nachvollziehbarkeit

---

## ⚙️ KONFIGURATION

### 🔧 Git Workflow
```bash
# Neues Projekt hinzufügen
git add Python/NeuesProjekt/
git commit -m "[Python] Add: NeuesProjekt - Beschreibung"
git push

# Strukturierte Commit-Nachrichten
git commit -m "[Python] Add: WorkingTimeTracker - Arbeitszeiten berechnen"
git commit -m "[Python] Update: ExcelMerger - Bessere Fehlerbehandlung"
git commit -m "[Fix] WorkingTimeTracker - Zeiterkennung korrigiert"
git commit -m "[Doc] README - Dokumentation erweitert"
```

### 📁 Struktur-Legende

| Icon | Bedeutung |
|------|-----------|
| 📁 | Ordner |
| 📄 | Python-Skript / Textdatei |
| 🐍 | Python-Datei |
| 📜 | VBScript-Datei |
| 🌐 | Anywhere-Skript |
| 📊 | Excel-Datei |
| 📝 | Log-Datei |
| 📘 | Ergebnis-Datei |
| 🗂️ | Archiv-Ordner |

---

## ⚠️ WICHTIGE HINWEISE

### 🔒 Sicherheit
- ⚠️ Keine sensiblen Daten (Passwörter, API-Keys) committen
- ⚠️ Große Dateien (>100MB) nicht ins Repository
- ⚠️ Immer input("Press Enter...") am Ende für GUI-Nutzer

### 💡 Empfehlungen
- ✅ Testen - Skripte vor dem Commit testen
- ✅ Backup - Wichtige Daten vorher sichern
- ✅ Dokumentation - Jedes Projekt mit README.md dokumentieren
- ✅ Versionierung - Klare Commit-Nachrichten verwenden
- ✅ Pfade - Relative Pfade verwenden, keine absoluten
- ✅ Fehlerbehandlung - Immer try/except verwenden
- ✅ Auto-Installation für Abhängigkeiten einbauen
- ✅ Logging für Fehleranalyse implementieren

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

**Über dieses Repository:**
- 🎯 Ziel: Zentrale Sammlung aller Automatisierungsskripte
- 🔧 Werkzeuge: Python, VBScript, Batch, PowerShell
- 🏗️ Struktur: Klare Organisation nach Sprache & Zweck
- 🚀 Zukunft: Ständig wachsende Skript-Sammlung
- 🤝 Beitrag: Jeder kann Vorschläge einreichen

**Spezialgebiete:**
- ⏱️ Zeiterfassung & Reporting
- 📊 Excel/CSV Datenverarbeitung
- 📁 Datei- & Ordner-Automatisierung
- 🔄 Wiederkehrende Tasks automatisieren
- ⚙️ System-Wartung & Backup

---

## 📊 REPOSITORY STATISTIK

| Metrik | Wert | Trend |
|--------|------|-------|
| **Stars** | ![GitHub Stars](https://img.shields.io/github/stars/mucahid-emin-tomakin/AutoMate) | 📈 |
| **Forks** | ![GitHub Forks](https://img.shields.io/github/forks/mucahid-emin-tomakin/AutoMate) | 🔄 |
| **Issues** | ![GitHub Issues](https://img.shields.io/github/issues/mucahid-emin-tomakin/AutoMate) | ✅ |
| **Letztes Update** | ![GitHub Last Commit](https://img.shields.io/github/last-commit/mucahid-emin-tomakin/AutoMate) | 🕐 |

---

### 🔧 Made with ❤️ on Automation
