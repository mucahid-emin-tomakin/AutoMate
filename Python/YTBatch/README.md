# 🎬 YTBatch

![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![yt-dlp](https://img.shields.io/badge/yt--dlp-FF6B6B?logo=youtube&logoColor=white)
![ffmpeg](https://img.shields.io/badge/ffmpeg-007808?logo=ffmpeg&logoColor=white)
![Terminal](https://img.shields.io/badge/Terminal-4EAA25?logo=gnubash&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/Status-Aktiv-brightgreen)

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

**YTBatch** ist ein Python-basiertes Tool zum gleichzeitigen Herunterladen mehrerer YouTube-Videos oder Playlists als **MP3 (Audio)** oder **MP4 (Video)** in bester Qualität. Es unterstützt separate Listen für MP3 und MP4, löst Playlists automatisch in einzelne Video-URLs auf und zeigt eine **dynamische 4‑Zeilen‑Terminalanzeige** mit Fortschrittsbalken und aktuellem Titel.

**Warum dieses Tool?**
- Kein manuelles Eingeben jedes einzelnen Links – einfach alle URLs in eine Textdatei.
- Unterstützung für gemischte Listen: Playlists werden **komplett** heruntergeladen, einzelne Video-URLs einzeln.
- Fortschrittsanzeige, die immer an derselben Stelle bleibt – kein Scrollen.
- Automatische Konvertierung zu MP3 (beste Audio-Qualität) oder Zusammenführung zu MP4 (beste Video-Qualität).
- Keine externe Datenbank – die Ausgabeordner bleiben übersichtlich.

**Für wen ist das?**
- Für alle, die viele YouTube-Videos als MP3 offline hören oder als MP4 archivieren möchten.
- Für Musik-Sammler, die ganze Playlists herunterladen wollen.
- Für Windows‑Benutzer, die eine einfache Batch‑Lösung ohne komplizierte Skripte suchen.

---

## ✨ FEATURES

### 🎯 Download & Konvertierung
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 📂 Batch‑Download | Liste mit beliebig vielen URLs (eine pro Zeile) | ✅ |
| 🎵 MP3‑Download | Extrahiert nur Audio, beste Qualität (ca. 320 kbit/s) | ✅ |
| 🎬 MP4‑Download | Video + Audio, bestes verfügbares MP4‑Format | ✅ |
| 📁 Playlist‑Unterstützung | Playlist‑URLs werden vollständig aufgelöst | ✅ |
| 📄 Getrennte Listen | `ListMP3.txt` und `ListMP4.txt` für unterschiedliche Formate | ✅ |
| 🗂️ Getrennte Ausgabe | Automatische Ordner `MP3` und `MP4` | ✅ |
| 🍪 Cookie‑Unterstützung | Optionale `cookies.txt` für private/altersbeschränkte Videos | ✅ |

### 📺 Dynamische Terminalanzeige
| Element | Beschreibung |
|---------|-------------|
| 🔄 4‑Zeilen‑Layout | Bleibt immer an derselben Stelle, kein Scrollen |
| 📊 Fortschrittsbalken | 40 Zeichen, zeigt Download‑Fortschritt des aktuellen Videos |
| 🎵 Aktueller Titel | Wird live aus der Ausgabe von `yt-dlp` extrahiert |
| ⏱️ Echtzeit‑Update | Alle 200 ms aktualisiert |

### 🧩 Zusätzliche Features
| Feature | Beschreibung |
|---------|-------------|
| 🔁 Fortsetzen bei Unterbrechung | Bereits heruntergeladene Dateien werden übersprungen |
| 🛡️ Fehler‑Toleranz | Fehlerhafte URLs brechen den gesamten Prozess nicht ab |
| 📦 Keine externen Python‑Pakete | Nutzt nur `subprocess` und `pathlib` – yt‑dlp und ffmpeg müssen separat installiert sein |
| 🧹 Keine Log‑Dateien | Das Skript schreibt keine zusätzlichen Logs, nur die Ausgabe im Terminal (optional kann man Logging aktivieren) |

---

## 🚀 TOOL

| Sprache / Format | Zweck |
|------------------|-------|
| Python 3.7+ | Kernlogik & Ausführung |
| yt-dlp | Download und Konvertierung |
| ffmpeg | Konvertierung zu MP3 / Zusammenführung MP4 |
| deno (optional) | Für JavaScript‑Challenges (empfohlen, aber nicht zwingend) |

### 🐍 Verwendete Bibliotheken
| Bibliothek | Zweck |
|------------|-------|
| 🐍 **Python 3** | Hauptprogrammiersprache |
| 📦 **subprocess** | Aufruf von yt‑dlp |
| 🛤️ **pathlib** | Plattformunabhängige Pfadbehandlung |
| 📜 **re** | Reguläre Ausdrücke für Fortschrittserkennung |
| 🔧 **shutil / time / sys** | Hilfsfunktionen |

---

## ⚙️ KONFIGURATION

Alle Einstellungen sind **direkt im Python‑Skript** über Konstanten am Anfang definiert:
```python
# ==================================================
#  KONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).parent.absolute()
MP3_DIR = BASE_DIR / "MP3"                # Ausgabeordner für MP3
MP4_DIR = BASE_DIR / "MP4"                # Ausgabeordner für MP4
LIST_MP3 = BASE_DIR / "ListMP3.txt"       # Liste mit URLs für MP3
LIST_MP4 = BASE_DIR / "ListMP4.txt"       # Liste mit URLs für MP4
COOKIE_FILE = BASE_DIR / "cookies.txt"    # Optionale Cookie‑Datei
```
**Weitere Einstellungen (im Code änderbar):**
--concurrent-fragments 4 – Anzahl paralleler Fragment‑Downloads
--sleep-interval 5 – Pause zwischen einzelnen Downloads (Sekunden)
--limit-rate 1M – Maximale Download‑Rate (1 MB/s)
--js-runtimes deno – JavaScript‑Laufzeit für YouTube‑Challenges
> **Hinweis:** Die Format‑Optionen (bestaudio[ext=m4a]/bestaudio für MP3 bzw. bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best für MP4) sind bereits auf höchste Qualität voreingestellt.

### 📦 Voraussetzungen
1. **Python 3.7+** – [python.org](https://python.org)
2. **yt-dlp** – [github.com/yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)  
   *Einfach `yt-dlp.exe` in den Skriptordner legen oder per `pip install yt-dlp` installieren.*
3. **ffmpeg** – [ffmpeg.org](https://ffmpeg.org)  
   *Die `ffmpeg.exe` muss im `PATH` oder im Skriptordner liegen.*
4. **Optional: deno** – [deno.com](https://deno.com)  
   *Empfohlen, um JavaScript‑Challenges zu lösen (bessere Formatauswahl).*
   
### 💡 Einfache Installation von Abhängigkeiten (Windows)
```powershell
# yt-dlp und ffmpeg mit winget installieren (setzt Windows 10/11 voraus)
winget install yt-dlp.yt-dlp
winget install Gyan.FFmpeg

# Deno installieren (falls gewünscht)
winget install denoland.deno
```

### ✅ Überprüfung der Installation
Nach der Installation sollten folgende Befehle in einer **neuen** Eingabeaufforderung (CMD) oder PowerShell funktionieren:
```bash
yt-dlp --version
ffmpeg -version
deno --version
```

---

## 📁 STRUKTUR

### 📂 Hauptverzeichnis
```Text
🎬 YTBatch/
├── 🐍 YTBatch.py
├── 🐍 YTBatch - NoComment.py
├── 🐍 YTBatch - NoArchive.py
├── 🐍 YTBatch - NoLog.py
└── 📄 README.md
```

### 🐍 YTBatch  - Beispiel Run
```text
🎬 YTBatch/
├── 🐍 YTBatch.py
├── 📄 ListMP3.txt
├── 📄 ListMP4.txt
├── 📄 ArchiveMP3.txt
├── 📄 ArchiveMP4.txt
├── 📄 cookies.txt
├── 📁 MP3/
│   ├── 🎵 Song1.mp3
│   ├── 🎵 Song2.mp3
│   └── ...
└── 📁 MP4/
    ├── 🎬 Video1.mp4
    └── ...
```

### 📁 Struktur-Legende
```text
🎬 YTBatch/                 # Hauptverzeichnis
├── 🐍 .py                  # Python‑Skript (Hauptprogramm)
├── 📄 .txt                 # Konfigurations‑/Listendateien
├── 📁 MP3/                 # Heruntergeladene MP3‑Dateien
├── 📁 MP4/                 # Heruntergeladene MP4‑Dateien
└── 📄 README.md            # Projektdokumentation
```

---

## ⚡ QUICK START

### 📦 Git & GitHub
```bash
# 1. Repository klonen
git clone https://github.com/mucahid-emin-tomakin/AutoMate.git
cd AutoMate

# 2. In den ein Projektfodler wechseln
cd AutoMate/Python/YTBatch

# 3. Konfiguration anpassen (BASE_DIR, MP3_DIR)

# 4. Textdateien mit URLs erstellen
#    → ListMP3.txt für Audio-Downloads
#    → ListMP4.txt für Video-Downloads
#    (jeweils eine URL pro Zeile)

# 5. cookies.txt für eingeschränkte Videos

# 6. Tool ausführen
python YTBatch.py

# 7. Format wählen (1 = MP3, 2 = MP4) – der Download beginnt automatisch

# 8. Ergebnis prüfen
#    → MP3
#    → MP4
```

### 🐍 Python virtueller Umgebung
```bash
# Mit virtueller Umgebung
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
python YTBatch.py
```

---

## 🖼️ SCREENSHOTS

### Schritt 1 – Formatwahl
```text
=============================================
   YouTube Batch Downloader (MP3 oder MP4)
=============================================

Wähle das Format:
  1 - MP3 (nur Audio, beste Qualität)
  2 - MP4 (Video + Audio, beste Qualität)

Bitte 1 oder 2 eingeben:
```

### 📋 Schritt 2 – Auflösung von Playlists
```Text
📋 Sammle alle erwarteten Video-IDs aus den URLs (Playlists werden aufgelöst)...
  → 12 IDs extrahiert
  → 12 IDs extrahiert
  → 1 IDs extrahiert
...
✅ Insgesamt 136 Videos werden erwartet.
```

### 📋 Schritt 3 – Dynamische Download‑Anzeige
```Text
==============================================
= Download:  47% I====================I 100%
= Title:     Gladiator Ambience — Cinema ...
==============================================
```
(Die Anzeige bleibt stationär und aktualisiert sich live.)

### 📋 Schritt 4 – Abschlussmeldung
```Text
==============================================
= Download:  47% I====================I 100%
= Title:    Fertig!
==============================================

✅ Download abgeschlossen! Die Dateien wurden nach MP3 gespeichert.
```

---

## ⚠️ WICHTIGE HINWEISE

### 📌 Vor dem ersten Start
- ✅ Stelle sicher, dass `yt-dlp` und `ffmpeg` entweder im `PATH` oder als `.exe` im Skriptordner liegen.
- ✅ Die Dateien `ListMP3.txt` und/oder `ListMP4.txt` müssen vorhanden sein (auch leer erlaubt).
- ✅ Playlist‑URLs werden **vollständig** aufgelöst – das kann bei großen Playlists einige Sekunden dauern.
- ✅ Cookies werden nur verwendet, wenn die Datei `cookies.txt` im Skriptordner existiert (exportiert z. B. mit Browser‑Erweiterung "Get cookies.txt").

### 🔒 Rechtliches
- ⚠️ Nutze das Tool nur für Inhalte, zu denen du die entsprechenden Rechte besitzt oder die ausdrücklich für den Download freigegeben sind.
- ⚠️ Das Herunterladen urheberrechtlich geschützter Materialien ist in vielen Ländern illegal.

### 💡 Tipps für den Betrieb
- ✅ Bei großen Playlists: Die Vorab‑Auflösung (Sammeln der IDs) kann einige Minuten dauern – das ist normal.
- ✅ Verwende `--limit-rate 1M`, um eine Überlastung deiner Internetleitung zu vermeiden (der Wert kann im Skript geändert werden).
- ✅ Falls die dynamische Anzeige nicht richtig funktioniert (z. B. Titel bleibt leer), liegt das an der Ausgabe von `yt-dlp`. Das Skript erkennt `[download] Destination:` – aktuelle `yt-dlp`‑Versionen zeigen das weiterhin an.
- ✅ Bei Problemen mit JavaScript‑Challenges installiere **deno** und setze `--js-runtimes deno` (im Skript bereits enthalten).

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
🤖 AutoMate | 🔧 Automation Scripts | 🐍 Python | 🎬 YTBatch

## 📊 REPOSITORY STATISTIK

| Metrik | Wert | Trend |
|--------|------|-------|
| **Stars** | ![GitHub Stars](https://img.shields.io/github/stars/mucahid-emin-tomakin/AutoMate) | 📈 |
| **Forks** | ![GitHub Forks](https://img.shields.io/github/forks/mucahid-emin-tomakin/AutoMate) | 🔄 |
| **Issues** | ![GitHub Issues](https://img.shields.io/github/issues/mucahid-emin-tomakin/AutoMate) | ✅ |
| **Letztes Update** | ![GitHub Last Commit](https://img.shields.io/github/last-commit/mucahid-emin-tomakin/AutoMate) | 🕐 |

---

### 🔧 Made with ❤️ on Python
