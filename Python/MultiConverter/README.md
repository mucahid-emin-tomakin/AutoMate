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

### FFmpeg‑Parameter (im Code)
| Medientyp | ffmpeg‑Aufruf / Parameter | Beschreibung |
|-----------|---------------------------|--------------|
| **Bilder** | `ffmpeg -i infile -y outfile` | Einfache Konvertierung ohne weitere Optionen |
| **Videos (erster Versuch)** | `-c copy` | Kopiert alle Streams (schnell, verlustfrei) |
| **Videos (Fallback)** | `-i infile -y outfile` | Vollständige Neukodierung (langsamer, aber kompatibler) |
| **MP3 (Audio)** | `-vn -acodec libmp3lame` | Entfernt Video‑Spur, nutzt LAME‑MP3‑Encoder |
| **Andere Audioformate** | `-vn` | Nur Audio extrahieren, ohne speziellen Codec |
> **Hinweis:** Die ffmpeg‑Aufrufe sind für beste Qualität voreingestellt (keine Qualitätseinschränkung).

### 📦 Voraussetzungen
1. **Python 3.7+** – [python.org](https://python.org)
2. **ffmpeg** – [ffmpeg.org](https://ffmpeg.org)  
   Die `ffmpeg.exe` muss im `PATH` **oder** im Skriptordner liegen.
3. **Keine weiteren Python‑Pakete!** – Nur die Standardbibliothek wird verwendet.

### 💡 Einfache Installation von ffmpeg (Windows)
```powershell
# ffmpeg mit winget installieren (setzt Windows 10/11 voraus)
winget install Gyan.FFmpeg

# Oder manuell:
# 1. ZIP von https://gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip herunterladen
# 2. Nach C:\ffmpeg entpacken
# 3. C:\ffmpeg\bin zum PATH hinzufügen
```

### ✅ Überprüfung der Installation
Nach der Installation sollte in einer neuen Eingabeaufforderung (CMD) oder PowerShell folgender Befehl funktionieren:
```bash
ffmpeg -version
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

# 2. In den Projektfodler wechseln
cd Python/MultiConverter

# 3. ffmpeg installieren (siehe oben)

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

### Schritt 1 – Ordnerauswahl & Dateiliste
```text
============================================================================
                         MultiConverter (ffmpeg)
============================================================================
Aktueller Ordner: C:\Users\Benutzer\Downloads
---------------------------------------------------------------
Mochtest du einen anderen Ordner? (J/N): n
============================================================================
                          Dateien auswahlen
============================================================================
Auswahlmoglichkeiten: [A]lle  [1]  [1,3]  [1-3]  oder [1-3,5,7-9]
-----------------------------------------------------------------
  [1] bild.png
  [2] video.mp4
  [3] song.flac
-----------------------------------------------------------------
Deine Auswahl: 1,3
--------------------------------
Ausgewahlte Dateien:
  - bild.png
  - song.flac
```

### 📋 Schritt 2 – Zielformat wählen
```Text
============================================================================
                        Zielformat auswahlen
============================================================================
  Bild-Formate:    [1] png     [2] jpg     [3] jpeg    [4] gif
                   [5] bmp     [6] tiff    [7] webp    [8] heic
  Video-Formate:   [9] mp4     [10] webm   [11] avi    [12] mkv
                   [13] mov    [14] flv
  Audio-Formate:   [15] mp3    [16] wav    [17] ogg    [18] flac
                   [19] aac    [20] m4a
---------------------------------------------------------------
Format-Nummer (1-20): 15
------------------------
Gewahltes Format: mp3
```

### 📋 Schritt 3 – Konvertierung
```Text
============================================================================
                         Konvertierung lauft...
============================================================================
[>>] bild.png --> bild.mp3
  [OK] bild.mp3
[>>] song.flac --> song.mp3
  [OK] song.mp3
============================================================================
                       Konvertierung abgeschlossen!
============================================================================
Erfolgreich: 2
Fehlgeschlagen: 0
------------------------
Drücke Enter zum Beenden...
```

---

## ⚠️ WICHTIGE HINWEISE

### 📌 Vor dem ersten Start
- ✅ Stelle sicher, dass **ffmpeg** entweder im `PATH` oder als `ffmpeg.exe` im Skriptordner liegt.
- ✅ Das Skript arbeitet **nur mit Dateien** im aktuellen Ordner (Unterordner werden ignoriert).
- ✅ Die konvertierten Dateien landen **immer im gleichen Ordner** wie die Originale.
- ✅ Bei Videos wird zuerst `-c copy` versucht (schnell, verlustfrei). Falls das fehlschlägt, wird automatisch neu codiert.
- ✅ Bei MP3 wird `libmp3lame` verwendet – das liefert beste Qualität.

### 🔒 Rechtliches (keine Einschränkung)
- ⚠️ Die Konvertierung von Medien, die du besitzt oder für die du eine Lizenz hast, ist völlig legal.
- ⚠️ Das Tool enthält keine Umgehung von Kopierschutzmechanismen.

### 💡 Tipps für den Betrieb
- ✅ Für große Batch‑Konvertierungen: Lege alle zu konvertierenden Dateien in einen eigenen Ordner, starte das Skript dort und wähle `A` (alle Dateien).
- ✅ Nutze die Bereichsauswahl, um nur bestimmte Dateien zu konvertieren – z. B. `1-5,7,9-12`.
- ✅ Die Batch‑Version (`MultiConverter.bat`) funktioniert ebenfalls, ist aber weniger robust bei der Bereichsauswahl. Die Python‑Version ist **immer vorzuziehen**.
- ✅ Falls ffmpeg nicht gefunden wird, zeigt das Skript eine klare Fehlermeldung mit Link zur Installation.

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
| **Interessen** | Python, System‑Automation, ffmpeg | ⚙️ |

**Teil der AutoMate Familie:**
🤖 AutoMate | 🔧 Automation Scripts | 🐍 Python | 🔄 MultiConverter

## 📊 REPOSITORY STATISTIK

| Metrik | Wert | Trend |
|--------|------|-------|
| **Stars** | ![GitHub Stars](https://img.shields.io/github/stars/mucahid-emin-tomakin/AutoMate) | 📈 |
| **Forks** | ![GitHub Forks](https://img.shields.io/github/forks/mucahid-emin-tomakin/AutoMate) | 🔄 |
| **Issues** | ![GitHub Issues](https://img.shields.io/github/issues/mucahid-emin-tomakin/AutoMate) | ✅ |
| **Letztes Update** | ![GitHub Last Commit](https://img.shields.io/github/last-commit/mucahid-emin-tomakin/AutoMate) | 🕐 |

---

### 🔧 Made with ❤️ on Python
