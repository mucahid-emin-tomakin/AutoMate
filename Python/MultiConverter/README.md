# 🔄 MultiConverter

![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![ffmpeg](https://img.shields.io/badge/ffmpeg-007808?logo=ffmpeg&logoColor=white)
![Batch](https://img.shields.io/badge/Batch-4EAA25?logo=windows&logoColor=white)
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

**MultiConverter** ist ein Python‑/Batch‑basiertes Tool zum **konvertieren von beliebigen Bild‑, Video‑ und Audiodateien** in ein anderes Format – mit **demselben Look & Feel** wie klassische Batch‑Skripte. Es unterstützt 20 verschiedene Zielformate, eine **intelligente Bereichsauswahl** (`1,3,5-9,11`) und eine **robuste Fehlerbehandlung**.

**Warum dieses Tool?**
- Keine komplizierten ffmpeg‑Parameter – einfache Menüführung.
- Unterstützt **alle gängigen Medienformate** (PNG, MP4, MP3, WEBM, …).
- **Batch‑ und Python‑Version** – wählbar, je nach Umgebung.
- **Auswahl per Nummer, Bereich oder `A`** (alle Dateien) – genau wie im Original‑Batch.
- **Fallback‑Mechanismus** für Video/Audio: zuerst schnelles Stream‑Kopieren, bei Fehler vollständige Neukodierung.

**Für wen ist das?**
- Für alle, die regelmäßig Medien konvertieren müssen (z. B. PNG → JPG, MP4 → MKV, FLAC → MP3).
- Für Windows‑Power‑User, die eine **konsistente Kommandozeilen‑Oberfläche** schätzen.
- Für alle, die ein **zuverlässiges, erweiterbares Skript** suchen, das ohne zusätzliche Bibliotheken auskommt.

---

## ✨ FEATURES

### 🎯 Konvertierungs‑Features
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 📂 Batch‑Konvertierung | Mehrere Dateien gleichzeitig auswählen | ✅ |
| 🖼️ Bild‑Formate | PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP, HEIC | ✅ |
| 🎬 Video‑Formate | MP4, WEBM, AVI, MKV, MOV, FLV | ✅ |
| 🎵 Audio‑Formate | MP3, WAV, OGG, FLAC, AAC, M4A | ✅ |
| 🔢 Intelligente Auswahl | `A` (alle), `1,3,5`, `1-3` oder `1-3,5,7-9` | ✅ |
| 📁 Ordnerauswahl | Vor dem Start kann ein beliebiger Ordner gewählt werden | ✅ |
| 💾 Originalnamen bleiben erhalten | Nur die Dateiendung wird geändert | ✅ |
| 🧹 Fehler‑Toleranz | Fehlerhafte Dateien brechen nicht den gesamten Durchlauf ab | ✅ |

### 🖥️ Terminal‑Ausgabe (exakt wie Batch)
| Element | Beschreibung |
|---------|-------------|
| 📏 76 Zeichen breite Trennlinien (`=` und `-`) | Originalgetreue Optik |
| 🔢 Nummerierte Dateiliste | `[1] datei.jpg` |
| 🗂️ Format‑Menü | Kategorisiert (Bild/Video/Audio) mit Zahlen 1‑20 |
| 📊 Erfolgs‑/Fehlerzähler | Am Ende wird angezeigt, wie viele Dateien erfolgreich waren |
| ⏸️ Pause am Ende | Fenster bleibt offen (wie bei Batch mit `pause`) |

### 🧩 Zusätzliche Features
| Feature | Beschreibung |
|---------|-------------|
| 🐍 Python‑Version | Einfach per Doppelklick oder `python converter.py` ausführbar |
| 📜 Batch‑Version | Original‑Batch‑Skript für Rechner ohne Python (nicht mehr empfohlen) |
| 🔁 Stream‑Copy für Videos | Erster Versuch mit `-c copy` – extrem schnell, verlustfrei |
| 🎚️ MP3‑Optimierung | Nutzt `libmp3lame` für beste Audio‑Qualität |
| 🛡️ Keine externen Python‑Pakete | Nur `os`, `subprocess`, `sys`, `shutil`, `pathlib` – Standardbibliothek |
| 🔧 FFmpeg‑Prüfung | Skript checkt, ob `ffmpeg` im PATH ist |

---

## 🚀 TOOL

| Sprache / Format | Zweck |
|------------------|-------|
| Python 3.7+ | Haupt‑Version (empfohlen) |
| Batch (cmd) | Ursprungsversion (für reine Windows‑Umgebungen) |
| ffmpeg | Konvertierungs‑Engine |

### 🐍 Verwendete Bibliotheken (Python‑Version)
| Bibliothek | Zweck |
|------------|-------|
| 🐍 **Python 3** | Hauptprogrammiersprache |
| 📦 **os / pathlib** | Pfad‑ und Dateiverwaltung |
| 🔧 **subprocess** | Aufruf von ffmpeg |
| 🖨️ **sys** | Exit‑Codes |
| 🔍 **shutil** | Prüfung auf `ffmpeg` im PATH |

---

## ⚙️ KONFIGURATION

Alle Einstellungen sind **direkt im Python‑Skript** über Konstanten am Anfang definiert (wenn gewünscht, können Sie angepasst werden).  
Standardmäßig ist **keine Konfiguration nötig** – das Skript arbeitet im aktuellen Ordner.

```python
# ==================================================
#  KONFIGURATION (optional, direkt im Code änderbar)
# ==================================================

# Der Arbeitsordner wird interaktiv abgefragt oder ist %cd%
# Ausgabedateien landen im gleichen Ordner wie die Quelldateien
# Format‑Mapping ist in format_map definiert (siehe Code)
```

---

## 📁 STRUKTUR

### 📂 Hauptverzeichnis
```Text
🔄 MultiConverter/
├── 🐍 MultiConverter.py
├── 🐍 MultiConverter - NoComment.py
└── 📄 README.md
```

### 🐍 MultiConverter  - Beispiel Run
```text
🔄 MultiConverter/
├── 🐍 MultiConverter.py
├── 📁 Bilder/
│   ├── 🖼️ Foto1.png
│   ├── 🖼️ Foto2.png
│   └── ...
├── 📁 Videos/
│   ├── 🎬 Clip1.mp4
│   └── ...
└── 📁 Ausgabe/
    ├── 🖼️ Foto1.jpg      # nach Konvertierung
    ├── 🖼️ Foto2.jpg
    ├── 🎬 Clip1.mkv
    └── ...
```

### 📁 Struktur-Legende
```text
🔄 MultiConverter/         # Hauptverzeichnis
├── 🐍 .py                 # Python‑Skript (Hauptprogramm)
├── 🎬 .mp4                # Video-Datei
├── 🖼️ .jpg                # Foto-Datei
└── 📄 README.md           # Projektdokumentation
```

---

## ⚡ QUICK START

### 📦 Git & GitHub
```bash
# 1. Repository klonen
git clone https://github.com/mucahid-emin-tomakin/AutoMate.git
cd AutoMate

# 2. In den ein Projektfodler wechseln
cd AutoMate/Python/MultiConverter

# 3. (Optional) ffmpeg installieren (siehe oben)

# 4. Konfiguration anpassen (wenn gewollt)

# 5. Das Skript ausführen
python MultiConverter.py
# Oder per Doppelklick auf MultiConverter.py (falls Python mit .py verknüpft ist)

# 6. Interaktiv:
#    - Ordner auswählen (oder aktuellen behalten)
#    - Dateien auswählen (z. B. A, 1, 1,3, 1-3, 1-3,5,7-9)
#    - Formatnummer eingeben (1‑20)
#    - Fertig – die konvertierten Dateien liegen im selben Ordner
```

### 🐍 Python virtueller Umgebung
```bash
# Mit virtueller Umgebung
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
python MultiConverter.py
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


