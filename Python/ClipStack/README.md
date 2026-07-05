# 🎬 ClipStack

![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-007808?logo=ffmpeg&logoColor=white)
![Video Processing](https://img.shields.io/badge/Video%20Processing-FF6B6B?logo=video&logoColor=white)
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

**ClipStack** ist ein Python-basiertes Tool, das mehrere Videodateien zu einem einzigen Video zusammenfügt – mit **automatischer Auflösungsanpassung** und **Kapitelmarken** als Inhaltsverzeichnis.

**Das Problem:**
- Du hast viele einzelne Videos (z. B. Vorlesungsaufzeichnungen, Tutorials, Kurzclips).
- Du möchtest sie zu einer einzigen Datei zusammenfügen.
- Die Videos haben unterschiedliche Auflösungen.
- Du möchtest ein Inhaltsverzeichnis mit Kapiteln, um direkt zu einem bestimmten Video springen zu können.

**Die Lösung:**
- **ClipStack** analysiert alle Videos im Ordner und ermittelt die **größte Auflösung**.
- Jedes Video wird entweder **1:1 kopiert** (falls bereits die Zielauflösung hat) oder **mit schwarzen Balken (Letterbox/Pillarbox)** auf die Zielauflösung skaliert.
- **Kein Strecken, kein Abschneiden** – das Seitenverhältnis bleibt immer erhalten.
- Die **Kapitelmarken** werden automatisch aus den Dateinamen generiert.
- Das Ergebnis ist eine einzige MP4-Datei mit einem **klickbaren Inhaltsverzeichnis**.

**Für wen ist das?**
- Für Studierende, die Vorlesungsvideos zusammenführen möchten.
- Für Content-Creator, die mehrere Clips zu einem Video verbinden.
- Für alle, die eine strukturierte Video-Sammlung in einer Datei haben möchten.

Das Tool ist Teil der **AutoMate**-Familie und wird dort zusammen mit weiteren Automatisierungslösungen weiterentwickelt.

---

## ✨ FEATURES

### 🎬 Video-Verarbeitung
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 📐 Automatische Auflösung | Ermittelt die größte Auflösung aus allen Videos | ✅ |
| 🖼️ Seitenverhältnis erhalten | Skaliert mit schwarzen Balken (kein Strecken/Schneiden) | ✅ |
| ⚡ Intelligentes Kopieren | Videos mit bereits passender Auflösung werden 1:1 kopiert | ✅ |
| 📑 Kapitelmarken | Automatisches Inhaltsverzeichnis aus Dateinamen | ✅ |
| 🔗 Verlustfreies Zusammenfügen | Nutzt `-c copy` für maximale Geschwindigkeit | ✅ |
| 🧹 Automatische Bereinigung | Temporäre Dateien werden nach Fertigstellung gelöscht | ✅ |

### 📁 Was es generiert
| Ergebnis | Beschreibung |
|----------|-------------|
| Gesamtvideo | Eine einzige MP4-Datei mit allen Clips |
| Kapitelstruktur | Jedes Video ist ein Kapitel mit dem Dateinamen als Titel |

---

## 🚀 TOOL

| Sprache / Format | Zweck |
|------------------|-------|
| Python 3.11+ | Kernlogik & Ausführung |
| FFmpeg / FFprobe | Videoanalyse, Skalierung & Zusammenfügung |

### 🐍 Verwendete Bibliotheken
| Bibliothek | Zweck |
|------------|-------|
| 🐍 **Python 3.11** | Hauptprogrammiersprache |
| 📁 **subprocess** | Ausführung von FFmpeg-Befehlen |
| 📄 **json** | Verarbeitung von FFprobe-Ausgaben |
| 📂 **pathlib** | Moderne Pfadbehandlung |
| 🗑️ **shutil** | Dateioperationen & temporäre Ordner |

---

## ⚙️ KONFIGURATION

Alle Einstellungen sind am Anfang der Datei oder als konstante Werte festgelegt:

### 📦 Voraussetzungen
1. **Python 3.7+** – [python.org](https://python.org)
2. **ffmpeg** – [ffmpeg.org](https://ffmpeg.org)  
   *Die `ffmpeg.exe` und `ffprobe.exe` müssen im System-`PATH` oder im Skriptordner liegen.*

### 💡 Einfache Installation von Abhängigkeiten (Windows)
```powershell
# ffmpeg mit winget installieren (setzt Windows 10/11 voraus)
winget install Gyan.FFmpeg
```

### ✅ Überprüfung der Installation
Nach der Installation sollten folgende Befehle in einer **neuen** Eingabeaufforderung (CMD) oder PowerShell funktionieren:
```bash
ffmpeg -version
ffprobe -version
```
> **Hinweis:** `ffprobe` wird für die Analyse der Video-Daten (Auflösung, Dauer) benötigt – es ist Teil der FFmpeg-Installation.

---

## 📁 STRUKTUR

### 📂 Hauptverzeichnis
```Text
🎬 ClipStack/
├── 🐍 ClipStack.py
├── 🐍 ClipStack - NoComment.py
└── 📄 README.md
```

### 🐍 ClipStack - Beispiel Run
```text
C:\Users\USER\Downloads\MGIPS/
├── 📁 temp_scaled/              # Temporärer Ordner (wird automatisch gelöscht)
│   ├── scaled_000.mp4
│   ├── scaled_001.mp4
│   ├── ...
│   └── concat_list.txt
├── 📹 aequivalenzrelationen.mp4
├── 📹 Aussagenlogik.mp4
├── 📹 Kettenregel.mp4
├── ...
└── 🎬 Gesamtvideo_mit_Kapiteln.mp4   # Fertiges zusammengefügtes Video
```

### 📁 Struktur-Legende
```text
🎬 ClipStack/
├── 🐍 .py                    # Python-Skripte (Hauptprogramm & Varianten)
├── 📄 README.md              # Projektbeschreibung (diese Datei)
├── 📹 .mp4                   # Originale Einzelvideos (bleiben unverändert)
└── 🎬 .mp4                   # Fertiges Gesamtvideo (neu erstellt)
```

---

## ⚡ QUICK START

### 📦 Git & GitHub
```bash
# 1. Repository klonen
git clone https://github.com/mucahid-emin-tomakin/AutoMate.git
cd AutoMate

# 2. In den Projektordner wechseln
cd AutoMate/Python/ClipStack

# 3. Skript in den Ordner mit den Videos kopieren (oder ClipStack.py dorthin legen)
#    → Alle .mp4-Dateien müssen im selben Ordner liegen wie das Skript

# 4. Tool ausführen (installiert fehlende Pakete automatisch – keine externen Abhängigkeiten)
python ClipStack.py

# 5. Fertiges Video: "Gesamtvideo_mit_Kapiteln.mp4" im selben Ordner
```

### 🐍 Python virtueller Umgebung
```bash
# Mit virtueller Umgebung
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
python ClipStack.py
```

---

## 🖼️ SCREENSHOTS

### Erfolgreiche Ausführung (alle Videos haben bereits die gleiche Auflösung)
```text
Arbeitsordner: C:\Users\tomak\Downloads\MGIPS
Analysiere 42 Videodateien...
  aequivalenzrelationen.mp4: 400x224, 739.72s
  Aussagenlogik.mp4: 400x224, 639.92s
  Kettenregel.mp4: 400x224, 571.28s
  ...
Zielauflösung (größte): 400x224
Bereite Videos vor...
  Kopiere (unverändert): aequivalenzrelationen.mp4
  Kopiere (unverändert): Aussagenlogik.mp4
  Kopiere (unverändert): Kettenregel.mp4
  ...
Füge zusammen zu: Gesamtvideo_mit_Kapiteln.mp4
✅ Fertig! Video erstellt: C:\Users\tomak\Downloads\MGIPS\Gesamtvideo_mit_Kapiteln.mp4
   Enthält 42 Kapitel zum Springen.
```

### 📋 Mit Skalierung (unterschiedliche Auflösungen)
```Text
Arbeitsordner: C:\Users\USER\Videos\Projekt
Analysiere 3 Videodateien...
  clip_720p.mp4: 1280x720, 120.00s
  clip_1080p.mp4: 1920x1080, 90.00s
  clip_480p.mp4: 640x480, 60.00s
Zielauflösung (größte): 1920x1080
Bereite Videos vor...
  Kopiere (unverändert): clip_1080p.mp4
  Skaliere + Balken: clip_720p.mp4
  Skaliere + Balken: clip_480p.mp4
Füge zusammen zu: Gesamtvideo_mit_Kapiteln.mp4
✅ Fertig! Video erstellt: C:\Users\USER\Videos\Projekt\Gesamtvideo_mit_Kapiteln.mp4
   Enthält 3 Kapitel zum Springen.
```

### 📋 Fehler (FFmpeg nicht installiert)
```Text
Arbeitsordner: C:\Users\USER\Videos\Projekt
Error: ffmpeg not found. Please install ffmpeg and add it to your PATH.
```

---

## ⚠️ WICHTIGE HINWEISE

### 📌 Vor der Verwendung
- ✅ **FFmpeg muss installiert und im System-Pfad verfügbar sein** (ffmpeg und ffprobe).
- ✅ Das Skript muss **im gleichen Ordner** wie die `.mp4`-Dateien liegen.
- ✅ Die Originalvideos werden **nie verändert** – es werden nur Kopien im Temp-Ordner erstellt.
- ✅ Das Skript funktioniert mit **beliebig vielen Videos** (getestet mit 42 Dateien).

### 🔒 Sicherheit
- ⚠️ Bereits existierende `Gesamtvideo_mit_Kapiteln.mp4` wird **überschrieben**.
- ⚠️ Der temporäre Ordner `temp_scaled` wird nach Fertigstellung gelöscht.
- ⚠️ Bei Fehlern bleibt der Temp-Ordner erhalten – du kannst ihn manuell löschen.

### 💡 Tipps
- ✅ Für **maximale Geschwindigkeit**: Alle Videos sollten bereits die gleiche Auflösung haben (dann wird nur kopiert, nicht neu codiert).
- ✅ Die Kapitelmarken funktionieren in **VLC**, **MPC-HC**, **QuickTime** und den meisten modernen Playern.
- ✅ In VLC: `Wiedergabe → Kapitel` oder die Tasten `Strg+N` (nächstes) / `Strg+P` (vorheriges).
- ✅ Das Skript kann auch mit **anderen Videoformaten** erweitert werden (einfach `*.mp4` durch `*.mkv` oder `*.avi` ersetzen).

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
| **Interessen** | Python, System-Automation, Video-Processing | ⚙️ |

**Teil der AutoMate Familie:**
🤖 AutoMate | 🔧 Automation Scripts | 🐍 Python | 🎬 ClipStack

## 📊 REPOSITORY STATISTIK

| Metrik | Wert | Trend |
|--------|------|-------|
| **Stars** | ![GitHub Stars](https://img.shields.io/github/stars/mucahid-emin-tomakin/AutoMate) | 📈 |
| **Forks** | ![GitHub Forks](https://img.shields.io/github/forks/mucahid-emin-tomakin/AutoMate) | 🔄 |
| **Issues** | ![GitHub Issues](https://img.shields.io/github/issues/mucahid-emin-tomakin/AutoMate) | ✅ |
| **Letztes Update** | ![GitHub Last Commit](https://img.shields.io/github/last-commit/mucahid-emin-tomakin/AutoMate) | 🕐 |

---

### 🔧 Made with ❤️ on Python
