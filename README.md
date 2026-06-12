# 🤖 AutoMate

![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)
![Automation](https://img.shields.io/badge/Automation-FF6B6B?logo=robot&logoColor=white)
![PowerShell](https://img.shields.io/badge/PowerShell-5391FE?logo=powershell&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Google Apps Script](https://img.shields.io/badge/Google_Apps_Script-34A853?logo=google&logoColor=white)
![VBScript](https://img.shields.io/badge/VBScript-00599C?logo=windows&logoColor=white)
![n8n](https://img.shields.io/badge/n8n-EA4B71?logo=n8n&logoColor=white)
![Automation Anywhere](https://img.shields.io/badge/Automation_Anywhere-FF6600?logo=robot-framework&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/Status-Abgeschlossen-brightgreen)

---

## 📖 INHALTSVERZEICHNIS

- [📝 PROJEKTBESCHREIBUNG](#-projektbeschreibung)
- [✨ FEATURES](#-features)
- [🚀 TOOL](#-tool)
- [📁 STRUKTUR](#-struktur)
- [⚡ QUICK START](#-quick-start)
- [⚠️ WICHTIGE HINWEISE](#️-wichtige-hinweise)
- [📝 LIZENZ](#-lizenz)
- [👤 AUTOR](#-autor)
- [📊 REPOSITORY STATISTIK](#-repository-statistik)

---

## 📝 PROJEKTBESCHREIBUNG

**AutoMate** ist meine zentrale Sammlung von Automatisierungsskripten und RPA-Komponenten für wiederkehrende Aufgaben im Büro- und Systemumfeld.  
Die Skripte sind primär in **Python** geschrieben, werden aber durch **VBScript**, **PowerShell**, **Automation Anywhere** und **n8n**‑Workflows ergänzt.

Der Fokus liegt auf Robustheit, minimalen Abhängigkeiten und klarer Dokumentation. Jedes Werkzeug kommt mit einem eigenen `README.md`, das Zweck, Voraussetzungen und Ausführung erklärt.  
Das Repository wächst kontinuierlich – neue Automatisierungen werden laufend hinzugefügt.

---

## ✨ FEATURES

### 🤖 Enthaltene Projekte
| Projekt | Inhalte & Schwerpunkte | Status |
|---------------------|--------------|--------|
| 🔐 **CryptSheetSync** (AppsScript) | Google Sheets verschlüsselt synchronisieren | ✅ |
| 🔄 **CopySync** | 1:1-Festplattensynchronisation mit SHA-256-Hash | ✅ |
| 🔨 **FolderForge** | Ordner-Stapelerstellung aus Namensliste | ✅ |
| 🎬 **MediaTracker** | Video-Bibliotheksanalyse mit ffprobe & Multithreading | ✅ |
| 🔄 **MultiConverter** | Batch-Konvertierung von Medien mit ffmpeg (Python + Batch) | ✅ |
| 🔄 **NameShift** | Ordner & Dateien umbenennen + Dateiliste exportieren | ✅ |
| 🎬 **TTSFactory** (Automation Anywhere) | Text-to-Speech in großer Stückzahl | ✅ |
| 🌳 **TreeMapper** | Ordnerstruktur als JSON/CSV exportieren | ✅ |
| ⏱️ **WorkingTimeTracker** | Arbeitszeiterfassung aus Excel/CSV mit automatischer Archivierung | ✅ |
| 🎬 **YTBatch** | YouTube Batch-Downloader (MP3/MP4) mit dynamischem Terminal | ✅ |

*Jedes fertige Projekt besitzt ein eigenes `README.md` mit Quick-Start und Konfiguration.*

---

## 🚀 TOOL

| Kategorie | Werkzeuge & Technologien |
|-----------|--------------------------|
| Hauptsprache | Python 3.11+ (pandas, openpyxl, logging) |
| Betriebssystem | Windows (primär), Linux (n8n) |
| RPA-Plattformen | Automation Anywhere A360, n8n |
| Scripting | VBScript, PowerShell, Bash |
| Datenformate | Excel (.xlsx, .csv), JSON |
| Versionskontrolle | Git & GitHub |

---

## 📁 STRUKTUR

### 📂 Hauptverzeichnis
```text
🤖 AutoMate/
├── 📜 AppsScript/
│   └── 🔐 CryptSheetSync/
├── 🤖 AutomationAnywhere/
│   ├── 🎬 TTSFactory/
├── 🐍 Python/
│   ├── 🔄 CopySync/
│   ├── 🔨 FolderForge/
│   ├── 🎬 MediaTracker/
│   ├── 🔄 MultiConverter/
│   ├── 🔄 NameShift/
│   ├── 🌳 TreeMapper/
│   ├── ⏱️ WorkingTimeTracker/
│   └── 🎬 YTBatch/
└── 📄 README.md
```

### 📁 Struktur-Legende
```text
🤖 AutoMate/
├── 📜 AppsScript/          # Google Apps Script Projekte
├── 🤖 AutomationAnywhere/  # Automation Anywhere Bot-Ordner (inkl. Python)
├── 🐍 Python/              # Python Automatisierungen (alle Skripte)
└── 📄 README.md            # Projektbeschreibung (diese Datei)
```

---

## ⚡ QUICK START

### 📦 Git & GitHub
```bash
# 1. Repository klonen
git clone https://github.com/mucahid-emin-tomakin/AutoMate.git
cd AutoMate

# 2. In ein Projektverzeichnis wechseln
cd Python/WorkingTimeTracker
python WorkingTimeTracker.py

# 3. Ergebnis im Archive-Ordner prüfen
cd Archive/YYYY.MM.DD_HH.MM.SS/
cat Result.txt
```

---

## ⚠️ WICHTIGE HINWEISE

### 🔒 Sicherheit
- ⚠️ Keine Zugangsdaten, Passwörter oder API-Keys committen
- ⚠️ Große Dateien (>100 MB) gehören nicht ins Repository (.gitignore verwenden)
- ⚠️ Skripte vor dem ersten Einsatz in Testumgebung ausführen

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
| **Interessen** | System-Automation | ⚙️ |

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
- 🔄 Festplatten-Synchronisation & Backup
- 🎬 Medien-Bibliotheksanalyse
- ⚙️ System-Wartung & Automatisierung

---

## 📊 REPOSITORY STATISTIK

| Metrik | Wert | Trend |
|--------|------|-------|
| **Stars** | ![GitHub Stars](https://img.shields.io/github/stars/mucahid-emin-tomakin/AutoMate) | 📈 |
| **Forks** | ![GitHub Forks](https://img.shields.io/github/forks/mucahid-emin-tomakin/AutoMate) | 🔄 |
| **Issues** | ![GitHub Issues](https://img.shields.io/github/issues/mucahid-emin-tomakin/AutoMate) | ✅ |
| **Letztes Update** | ![GitHub Last Commit](https://img.shields.io/github/last-commit/mucahid-emin-tomakin/AutoMate) | 🕐 |

---

### 🔧 Made with ❤️ on AutoMate
