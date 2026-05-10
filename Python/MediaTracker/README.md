# 🎬 MediaTracker

![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![ffprobe](https://img.shields.io/badge/ffprobe-0078D6?logo=ffmpeg&logoColor=white)
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

Der **MediaTracker** ist ein Python-basiertes Tool zur automatischen Indizierung und Analyse einer lokalen Videosammlung.  
Statt manuell die Gesamtspielzeit und Dateigrößen einer Serien-/Anime-Bibliothek zu berechnen, durchsucht das Skript rekursiv das angegebene Verzeichnis, ermittelt Videolängen via `ffprobe` und erstellt eine übersichtliche Textdatei mit allen relevanten Statistiken.

**Warum dieses Tool?**
- Es verschafft einen schnellen, exakten Überblick über die gesamte Videosammlung – sortiert nach Serien und Staffeln.
- Parallele Verarbeitung mit mehreren Threads beschleunigt die Analyse erheblich.
- Fehlerhafte oder unvollständige Dateien werden protokolliert, ohne den Gesamtprozess abzubrechen.
- Automatisches Backup der vorherigen Ausgabedatei sorgt für Datensicherheit.

**Für wen ist das?**
- Für Sammler großer Medienbibliotheken, die eine schnelle Inventur benötigen.
- Für alle, die Serie/Staffel-Übersichten automatisch generieren wollen.
- Für Anwender, die einen klaren Report über Speicherplatz und Laufzeit brauchen.

---

## ✨ FEATURES

### 🎬 Video-Analyse & Indizierung
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 📂 Rekursive Suche | Durchsucht alle Unterordner | ✅ |
| 🎞️ Multi-Format | .mp4, .mkv, .avi (konfigurierbar) | ✅ |
| ⏱️ Laufzeit-Ermittlung | Exakte Dauer via ffprobe | ✅ |
| 📊 Dateigröße | Größe jeder Videodatei | ✅ |
| 🔢 Natürliche Sortierung | Folgen werden numerisch sortiert | ✅ |
| 🧵 Multithreading | Parallele Analyse (8 Threads) | ✅ |
| 🗄️ Backup | Automatische Sicherung der letzten Ausgabe | ✅ |
| 📝 Fehlerprotokoll | Separate Log-Datei für Problemfälle | ✅ |

### 📁 Was es generiert
| Datei | Beschreibung |
|-------|-------------|
| `NAME.txt` | Gesamtstatistik + Serien/Staffeln-Liste |
| `error_log.txt` | Fehlerprotokoll (nur bei Problemen) |
| `backup/` | Ordner mit timestamp-Backups |

---

## 🚀 TOOL

| Sprache / Format | Zweck |
|------------------|-------|
| Python 3.11+ | Kernlogik & Ausführung |
| ffprobe (FFmpeg) | Externe Abhängigkeit für Videodauer |
| TXT | Ausgabe & Fehlerprotokoll |
| Multi-Threading | Parallele Beschleunigung |

### 🐍 Verwendete Bibliotheken
| Bibliothek | Zweck |
|------------|-------|
| 🐍 **Python 3.11** | Hauptprogrammiersprache |
| 🎬 **subprocess** | Aufruf von ffprobe |
| 🧵 **threading** | Parallele Verarbeitung |
| 📊 **queue** | Thread-sichere Aufgabenverteilung |
| 📝 **re** | Nummernextraktion aus Dateinamen |
| 🗄️ **shutil** | Backup der Ausgabedatei |
| 📅 **datetime** | Zeitstempel für Backups |

---

## ⚙️ KONFIGURATION

Alle Einstellungen sind am Anfang der Datei:

```python
# ============================== CONFIGURATION ==============================

root_folder = r"C:\Users\USER\Downloads"                # Zu durchsuchendes Verzeichnis
output_file = os.path.join(root_folder, "NAME.txt")     # Ausgabedatei
error_log = os.path.join(root_folder, "error_log.txt")  # Fehlerprotokoll
backup_folder = os.path.join(root_folder, "backup")     # Backup-Ordner

VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi"]      # Unterstützte Videoformate
NUM_THREADS = 8                                  # Parallele Threads
FFPROBE_PATH = "ffprobe"                         # Pfad zur ffprobe-Exe
FFPROBE_TIMEOUT = 11                             # Timeout in Sekunden
NUMBER_PATTERN = r'\d+'                          # Regex für Episodennummer
BACKUP_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"        # Zeitstempel-Format
```

---

## 📁 STRUKTUR

### 📂 Hauptverzeichnis
```Text
🎬 MediaTracker/
├── 🐍 MediaTracker.py
├── 🐍 MediaTracker - NoComment.py
└── 📄 README.md

```

### 🐍 MediaTracker - Beispiel Run
```text
🎬 C:\Users\USER\Downloads/
├── 🐍 MediaTracker.py
├── 📘 NAME.txt
├── 📘 error_log.txt          (nur bei Fehlern)
├── 🗂️ backup/
│   └── 📘 NAME_backup_20260221_005208.txt
├── 📁 Serie A/
│   ├── 📁 Staffel 1/
│   │   ├── 🎬 Folge - 01.mp4
│   │   └── 🎬 Folge - 02.mp4
│   └── 📁 Staffel 2/
│       └── 🎬 Folge - 01.mkv
└── 📁 Serie B/
    └── 🎬 Film.avi
```

### 📁 Struktur-Legende
```text
🎬 MediaTracker/
├── 🐍 .py                    # Python-Skript
├── 📄 README.md              # Projektbeschreibung
├── 📘 .txt                   # Ausgabe- & Log-Dateien
├── 🎬 .mp4 / .mkv / .avi     # Videodateien
└── 🗂️ backup/                # Backups (automatisch erstellt)
```

---

## ⚡ QUICK START

### 📦 Git & GitHub
```bash
# 1. Repository klonen
git clone https://github.com/mucahid-emin-tomakin/AutoMate.git
cd AutoMate

# 2. In den ein Projektfodler wechseln
cd AutoMate/Python/MediaTracker

# 3. Konfiguration anpassen (root_folder, BACKUP_TIMESTAMP_FORMAT)

# 4. Tool ausführen (installiert fehlende Pakete automatisch)
python MediaTracker.py

# 5. Ergebnis prüfen
#    → NAME.txt öffnet sich im konfigurierten Ordner
#    → error_log.txt nur bei Problemen
```

### 🐍 Python virtueller Umgebung
```bash
# Mit virtueller Umgebung
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

---

## 🖼️ SCREENSHOTS

### NAME.txt
```text
[Information]
Anime anzahl : 3
Gesamtanzahl der Folgen: 48
Ungefähre Laufzeit: 1200 Minuten -> 20.00 Stunden -> 0.83 Tage
Gesamtgröße der Videos: 45.32 GB

[Serie A\Staffel 1]
Folge - 01.mp4
Folge - 02.mp4
Folge - 03.mp4

[Serie A\Staffel 2]
Folge - 01.mp4
Folge - 02.mp4

[Serie B\Staffel 1]
Folge - 01.mkv
Folge - 02.mkv
```

### 📋 error_log.txt
```Text
Timeout bei ffprobe für Datei C:\...\broken_video.mp4
Fehler bei Datei C:\...\corrupted.mkv: [Errno 2] No such file or directory
```

---

## ⚠️ WICHTIGE HINWEISE

### 📌 Vor der Verwendung
- ✅ ffprobe muss installiert und im System-PATH sein (oder FFPROBE_PATH auf absoluten Pfad setzen)
- ✅ root_folder auf das gewünschte Verzeichnis anpassen
- ✅ Keine Standard-Python-Bibliotheken außerhalb der Built-ins nötig
- ✅ Dateinamen sollten Episodennummern enthalten (z. B. 01, Ep 12) für die Sortierung

### 🔒 Sicherheit
- ⚠️ Vorhandene NAME.txt wird automatisch ins Backup kopiert
- ⚠️ Keine sensiblen Pfade committen – root_folder vor Veröffentlichung anpassen
- ⚠️ Bei großen Sammlungen: Skript kann je nach Anzahl und Größe der Dateien etwas dauern

### 💡 Tipps
- ✅ Bei Fehlern: error_log.txt prüfen
- ✅ NUM_THREADS an eigene CPU anpassen (Standard: 8)
- ✅ Bei Netzwerklaufwerken: FFPROBE_TIMEOUT eventuell erhöhen
- ✅ NUMBER_PATTERN anpassen, wenn Dateinamen spezielle Nummerierung haben

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
🤖 AutoMate | 🔧 Automation Scripts | 🐍 Python | 🎬 MediaTracker

## 📊 REPOSITORY STATISTIK

| Metrik | Wert | Trend |
|--------|------|-------|
| **Stars** | ![GitHub Stars](https://img.shields.io/github/stars/mucahid-emin-tomakin/AutoMate) | 📈 |
| **Forks** | ![GitHub Forks](https://img.shields.io/github/forks/mucahid-emin-tomakin/AutoMate) | 🔄 |
| **Issues** | ![GitHub Issues](https://img.shields.io/github/issues/mucahid-emin-tomakin/AutoMate) | ✅ |
| **Letztes Update** | ![GitHub Last Commit](https://img.shields.io/github/last-commit/mucahid-emin-tomakin/AutoMate) | 🕐 |

---

### 🔧 Made with ❤️ on Python
