# 🎙️ TTSFactory

![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)
![Automation Anywhere](https://img.shields.io/badge/Automation%20Anywhere-2D2D2D?logo=automationanywhere&logoColor=white)
![RPA](https://img.shields.io/badge/RPA-FF6B6B?logo=robot&logoColor=white)
![ChatGPT](https://img.shields.io/badge/ChatGPT-00A67E?logo=openai&logoColor=white)
![Tortoise TTS](https://img.shields.io/badge/Tortoise%20TTS-8A2BE2?logo=python&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/Status-Abgeschlossen-brightgreen)

---

## 📖 INHALTSVERZEICHNIS

- [📝 PROJEKTBESCHREIBUNG](#-projektbeschreibung)
  - [🤖 Die fünf Automation Anywhere Bots](#-die-fünf-automation-anywhere-bots)
  - [🐍 Das TortoiseTTS Python-Skript](#-das-tortoisetts-python-skript)
- [✨ FEATURES](#-features)
- [🚀 TOOL](#-tool)
  - [🤖 Automation Anywhere Bots](#-automation-anywhere-bots)
  - [🐍 Python (Tortoise TTS Wrapper)](#-python-tortoise-tts-wrapper)
  - [📜 Startkette (AA → VBS → BAT → Python)](#-startkette-aa--vbs--bat--python)
- [⚙️ KONFIGURATION](#️-konfiguration)
  - [FFmpeg](#ffmpeg)
  - [Miniconda](#miniconda)
  - [Tortoise TTS](#tortoisetts)
  - [TTSFactory Runtime Struktur](#ttsfactory-runtime-struktur)
  - [Conda-Umgebung einrichten](#conda-umgebung-einrichten)
  - [Automation Anywhere Bots importieren](#automation-anywhere-bots-importieren)
  - [Variablen anpassen](#variablen-anpassen)
- [📁 STRUKTUR](#-struktur)
  - [📂 Hauptverzeichnis](#-hauptverzeichnis)
  - [🎙️ TTSFactory - Beispiel Run](#️-ttsfactory---beispiel-run)
  - [📁 Struktur-Legende](#-struktur-legende)
- [⚡ QUICK START](#-quick-start)
  - [📦 Git & GitHub](#-git--github)
- [🖼️ SCREENSHOTS](#️-screenshots)
  - [🎬 DemoWorkflow.mp4](#-demoworkflowmp4)
- [⚠️ WICHTIGE HINWEISE](#️-wichtige-hinweise)
  - [📌 Vor der Verwendung](#-vor-der-verwendung)
  - [🔒 Sicherheit](#-sicherheit)
  - [💡 Tipps](#-tipps)
- [📝 LIZENZ](#-lizenz)
- [👤 AUTOR](#-autor)
- [📊 REPOSITORY STATISTIK](#-repository-statistik)

---

## 📝 PROJEKTBESCHREIBUNG

**TTSFactory** ist eine vollautomatische Pipeline, die aus einer einfachen Idee ein gesprochenes Motivationsvideo-Skript generiert – komplett orchestriert durch **Automation Anywhere (Community Edition)**.
#### Die Pipeline durchläuft fünf Phasen:
1. **PreConfiguration** – Definiert Pfade, Parameter und baut die ChatGPT‑Prompts
2. **PromptGenerator** – ChatGPT liefert 5 aktuelle Motivationsthemen
3. **TextGenerator** – ChatGPT schreibt ein vollständiges 90‑Sekunden‑Skript
4. **AudioGenerator** – Tortoise TTS (lokal auf NVIDIA GPU) wandelt das Skript in MP3 um
5. **Main** – Orchestriert alle Schritte und protokolliert alles in `Main.csv`
Alle Komponenten (FFmpeg, Miniconda, Tortoise TTS) sind in einer **portablen Runtime** zusammengefasst – kein manuelles Installieren von Abhängigkeiten nötig.

### 🤖 Die fünf Automation Anywhere Bots
#### 1. Main (Orchestrator)
**Aufgabe:** Startet die Sub‑Bots der Reihe nach, fängt Fehler ab, sammelt alle Log‑Informationen und schreibt sie in Main.csv.
**Besonderheiten:** Enthält runTask‑Aufrufe für jeden der vier anderen Bots, jeweils mit Input/Output‑Dictionary. Nach jedem Sub‑Bot wird booleanError geprüft – bei Fehler erfolgt Abbruch mit Fehler‑Log.
#### 2. PreConfiguration (Setup & Prompt‑Bau)
**Aufgabe:** Definiert alle Pfade, Parameter, erstellt die beiden ChatGPT‑Prompts und generiert die kompletten Steuerungsskripte (.vbs, .bat, .py) als Strings.
**Wichtige Variablen:**
- `stringDateTimeFormat` = dd.MM.yyyy_HH:mm:ss
- `stringWorkDirectory` (muss angepasst werden)
- `stringPromptGeneratorPrompt` (Themen‑Prompt)
- `stringTextGeneratorPrompt` (Skript‑Prompt, enthält den Platzhalter `>>>stringPromptGeneratorChatGPT<<<`)
- `listAudioGenerator` – eine Liste mit **31 Elementen**, die alle nötigen Pfade, Parameter und die generierten Skript‑Strings enthält.
**Generierte Skripte (als Strings in der Liste):**
- `AudioGeneratorText.txt` – der zu sprechende Text (wird später vom AudioGenerator‑Bot befüllt)
- `AudioGenerator.vbs` – startet die Batch‑Datei im gleichen Ordner
- `AudioGenerator.bat` – setzt PATH, aktiviert Conda, ruft Python mit allen Parametern auf
- `AudioGenerator.py` – der vollständige Tortoise‑TTS‑Wrapper (über 500 Zeilen)
#### 3. PromptGenerator (Themen von ChatGPT holen)
**Aufgabe:** Öffnet einen temporary chat von ChatGPT, fügt `stringPromptGeneratorPrompt` ein, wartet auf die Antwort, klickt den Copy‑Button und speichert den Inhalt in `stringPromptGeneratorChatGPT`.
**Technik:** Verwendet `capture` (UI‑Objekt) für das Textfeld und den Copy‑Button, `assignFromClipboard` und eine Loop mit Try/Catch, falls der Button noch nicht sichtbar ist. Am Ende wird der Tab geschlossen.
#### 4. TextGenerator (Skript generieren)
**Aufgabe:** Ersetzt im `stringTextGeneratorPrompt` den Platzhalter durch `stringPromptGeneratorChatGPT`. Sendet den Prompt an ChatGPT, kopiert die Antwort und extrahiert mit `beforeAfter()` die vier Abschnitte Topic, Description, Script, Quote.
**Besonderheiten:** Mehrere `replace`‑Aufrufe, um die störenden `[SHIFT DOWN]` / `[SHIFT UP]` Marker zu entfernen. Das extrahierte `stringScript` ist reiner Text – der einzige Teil, der später gesprochen wird.
#### 5. AudioGenerator (Tortoise TTS starten und MP3 erzeugen)
**Aufgabe:** Schreibt den Text (`stringScript`) in `AudioGeneratorText.txt`, erzeugt die drei Skriptdateien aus den Strings der `listAudioGenerator`, startet `wscript.exe` mit der `.vbs`, wartet auf das `Flag.txt` (max. 3333 Sekunden), parst die erzeugte Log‑Datei und speichert alles in einer Tabelle.
**Details:**
- Der Bot nutzt `logToFile` zum Schreiben der Dateien.
- `runApp` mit `wscript.exe` und Parameter `"AudioGenerator.vbs"` startet die Batch‑Kette.
- Eine While‑Loop prüft auf Existenz von `Flag.txt`.
- Mit `CsvTxt` werden die Log‑ und Flag‑Dateien wieder eingelesen und bereinigt (Entfernung von `{`, `}`, `},`).
- Die Ergebnisse (Text, Log, Flag) landen in `tableAudioGenerator`.

### 🐍 Das TortoiseTTS Python-Skript
Das Python‑Skript AudioGenerator.py wird dynamisch von AA generiert und anschließend ausgeführt. Es ist ein Wrapper für die offizielle Tortoise‑TTS‑Bibliothek.
#### Aufgaben im Überblick:
1. Umgebungsvariablen setzen (HF_HOME, MODELS_DIR) – für portable Modelle.
2. CLI‑Argumente parsen – alle Parameter werden aus der Batch‑Datei übergeben.
3. Logging einrichten – im Fehlerfall hilfreich.
4. Tortoise TTS initialisieren – LocalTextToSpeech (eigene Subklasse) mit Presets.
5. Text laden und splitten – unterstützt --text_split "80,200".
6. Sprachgenerierung – für jeden Satzteil (max. 200 Zeichen) wird tts_with_preset aufgerufen.
7. WAV‑Dateien zusammenführen, MP3 konvertieren (FFmpeg) und WAVs löschen.
8. Flag.txt schreiben – Signal an AA, dass die Generierung beendet ist.
#### Wichtige eigene Anpassungen
- LocalTextToSpeech – erbt von TextToSpeech, überschreibt aber settings und presets, um auch die Werte aus den CLI‑Argumenten zu übernehmen.
- get_ffmpeg_executable() – sucht zuerst relativ zum Skript (2 Ordner hoch) nach FFMPEG\bin\ffmpeg.exe, danach im System‑PATH.
- Fehlerbehandlung – bei --regenerate "None" wird der Parameter ignoriert, um den früheren 0.wav‑Fehler zu vermeiden.

---

## ✨ FEATURES

| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 🧠 **ChatGPT Integration** | Automatische Themen‑ & Skript‑Generierung via UI‑Automatisierung | ✅ |
| 🎤 **Lokales Tortoise TTS** | Hochwertige Sprachsynthese auf eigener NVIDIA GPU | ✅ |
| 🔄 **Vollautomatische Pipeline** | Von der Idee bis zur MP3 – kein manueller Eingriff | ✅ |
| 📁 **Portable Runtime** | FFmpeg, Miniconda, Modelle – alles in einem Ordner | ✅ |
| 📊 **Detailliertes CSV‑Logging** | Jeder Schritt wird in `Main.csv` festgehalten | ✅ |
| 🧩 **Modularer Bot‑Aufbau** | 5 eigenständige AA‑Bots, leicht wartbar | ✅ |

---

## 🚀 TOOL

### 🤖 Automation Anywhere Bots
| Bot | Aufgabe | Input | Output |
|-----|---------|-------|--------|
| **Main** | Orchestrator | Startzeit | `Main.csv` |
| **PreConfiguration** | Setup & Prompt‑Bau | System‑Datum | 4 Prompt‑Strings + 31‑teilige Liste |
| **PromptGenerator** | ChatGPT Themen holen | Themen‑Prompt | 5 Themen (CSV) |
| **TextGenerator** | ChatGPT Skript holen | Themen + Skript‑Prompt | Topic, Script, Quote |
| **AudioGenerator** | Tortoise TTS starten | Script‑String | MP3 + Logs + Flag |
| **OneForAll** | Beinhaltet alle Bots |

### 🐍 Python (Tortoise TTS Wrapper)
| Schritt | Aufgabe |
|---------|---------|
| 1 | Laden des Texts aus `AudioGeneratorText.txt` |
| 2 | Splitten in Satzteile (max. 200 Zeichen) |
| 3 | Aufruf von Tortoise TTS mit allen CLI‑Parametern |
| 4 | WAV‑Zusammenführung, MP3‑Konvertierung (FFmpeg) und Bereinigung |
| 5 | Schreiben von `Flag.txt` als Signal an AA |

### 📜 Startkette (AA → VBS → BAT → Python)
| Schritt | Komponente | Aufgabe |
|---------|------------|---------|
| 1 | **Automation Anywhere (AudioGenerator Bot)** | Ruft `C:\Windows\System32\wscript.exe` mit Parameter `AudioGenerator.vbs` auf |
| 2 | `AudioGenerator.vbs` | Ermittelt das eigene Verzeichnis, startet `AudioGenerator.bat` im gleichen Ordner und wartet auf Beendigung |
| 3 | `AudioGenerator.bat` | Setzt PATH, aktiviert die Conda‑Umgebung `AudioGenerator`, ruft `AudioGenerator.py` mit allen Parametern auf |
| 4 | `AudioGenerator.py` | Führt Tortoise TTS aus, generiert MP3, schreibt `Flag.txt` als Signal |

---

## ⚙️ KONFIGURATION

### FFmpeg
Lade `ffmpeg-git-full.7z` von [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) oder von [Release](https://github.com/mucahid-emin-tomakin/AutoMate/blob/main/AutomationAnywhere/TTSFactory/FFMPEG/Installer/ffmpeg-2026-05-11-git-17bc88e67f-full_build.7z) herunter und entpacke es unter `..\TTSFactory\FFMPEG\`.  
`ffmpeg.exe` sollte unter `..\TTSFactory\FFMPEG\bin` sein.

### Miniconda
Installer runterladen und unter `..\TTSFactory\MINICONDA` entpacken. Entweder von [release](https://github.com/mucahid-emin-tomakin/AutoMate/blob/main/AutomationAnywhere/TTSFactory/MINICONDA/Installer/Miniconda3-latest-Windows-x86_64.exe) oder mittels command-line interface.
#### [CMD](https://www.anaconda.com/docs/getting-started/miniconda/install/windows-cli-install#powershell)
```CMD
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe --output .\Miniconda3-latest-Windows-x86_64.exe
```
#### [PowerShell](https://www.anaconda.com/docs/getting-started/miniconda/install/windows-cli-install#powershell)
```PowerShell
Invoke-WebRequest -Uri "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe" -OutFile ".\Miniconda3-latest-Windows-x86_64.exe"
```
activate.bat sollte unter `..\TTSFactory\MINICONDA\Scripts` sein.

### TortoiseTTS
Lade TortoiseTTS von [release](https://github.com/mucahid-emin-tomakin/AutoMate/blob/main/AutomationAnywhere/TTSFactory/TortoiseTTS/Installer/tortoise-tts-main.zip) oder von der offiziellen [GitHub repository](https://github.com/neonbjb/tortoise-tts) runter.
```CMD
git clone https://github.com/neonbjb/tortoise-tts.git
```

### TTSFactory Runtime Struktur
```Text
..\TTSFactory\
├── FFMPEG\
│   └── bin\ffmpeg.exe        # Runter geladene FFmpag
├── MINICONDA\
│   └── Scripts\activate.bat  # Runter geladene conda
└── TortoiseTTS\
    ├── tortoise\             # geklonte Tortoise-Repos
    └── .cache\               # Modelle (optional im Repo, oder wird bei der ersten ausführung automatisch installiert)
```

### Conda-Umgebung einrichten
Öffne eine normale Eingabeaufforderung (CMD) – nicht die Anaconda Prompt, wechsle in den MINICONDA‑Ordner und aktiviere Conda (ohne PATH‑Eintrag) und führe aus:
```Python
cd ..\TTSFactory\MINICONDA
.\Scripts\activate.bat
conda create --name AudioGenerator python=3.9 -y
conda activate AudioGenerator
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117  # funktioniert zuverlässig mit NVIDIA GPU
pip install transformers==4.30.0 tokenizers==0.13.3
pip install librosa scipy inflect rotary_embedding_torch unidecode tqdm einops progressbar
cd ..\TortoiseTTS
pip install -e .
```
Hinweis: Die Modelle werden beim ersten Start von Tortoise automatisch heruntergeladen (ca. 4 GB). Du kannst sie auch manuell aus dem Release übernehmen.

### Automation Anywhere Bots importieren
- Voraussetzung: [Automation Anywhere Community Edition](https://community2.cloud-2.automationanywhere.digital/#/login?next=/index) & [AA360 Bot Assistant Extension](https://chromewebstore.google.com/detail/bdnogmeijaanbgpnmbhlhmkfcbaoejcp?utm_source=item-share-cb) für Google Chrome.
- Gehe in den AA Control Room, erstelle für jede der fünf .json‑Dateien im Ordner AA-Bots/ einen neuen Bot (Achte auch die Namengebung).
- Öffne die Extension → "Copy from Clipboard" → Inhalt der .json einfügen → "Patch Content".
- Wiederhole für alle fünf Bots.
![DemoAA](https://github.com/mucahid-emin-tomakin/AutoMate/blob/main/AutomationAnywhere/TTSFactory/DemoAA.gif)

### Variablen anpassen
Öffne den PreConfiguration‑Bot im AA‑Editor. Suche die Variable stringWorkDirectory und setze sie auf deinen Entpack‑Pfad (z. B. C:\Users\Public\TTSFactory\).
Passe gegebenenfalls auch stringAudioGeneratorVoice (Name der Tortoise‑Stimme) und die Restlichen Variablen an.

---

## 📁 STRUKTUR

### 📂 Hauptverzeichnis
```Text
🎙️ TTSFactory/
├── 📂 AA-Bots
│   ├── 🔧 Main.json
│   ├── 🔧 PreConfiguration.json
│   ├── 🔧 PromptGenerator.json
│   ├── 🔧 TextGenerator.json
│   └── 🔧 AudioGenerator.json
├── 📂 FFMPEG
│   └── 📂 Installer
│       └── 📦 ffmpeg-2026-05-11-git-17bc88e67f-full_build.7z
├── 📂 MINICONDA
│   └── 📂 Installer
│       └── 📦 Miniconda3-latest-Windows-x86_64.exe
├── 📂 TortoiseTTS
│   ├── 📂 Installer
│   │   └── 📦 tortoise-tts-main.zip
│   ├── 📂 tortoise
│   │   ├── 📂 voices
│   │   │   └── 📂 Madara Uchiha
│   │   │       └── 🎵 1.mp3
│   │   ├── ⚙️ AudioGenerator.bat
│   │   ├── 🐍 AudioGenerator.py
│   │   └── 📜 AudioGenerator.vbs
│   ├── 🎵 AudioGenerator.mp3
│   └── 📊 Main.csv
├── 📘 ArchitectureOverview.txt
├── 🎬 DemoAA.mp4
└── 🎬 DemoWorkflow.mp4
```

### 🎙️ TTSFactory - Beispiel Run
[ArchitectureOverview.txt](https://github.com/mucahid-emin-tomakin/AutoMate/blob/main/AutomationAnywhere/TTSFactory/ArchitectureOverview.txt)

### 📁 Struktur-Legende
```text
🎙️ TTSFactory/
├── 📂 Ordner
├── 🔧 Automation Anywhere Bot (JSON)
├── ⚙️ Batch-Datei (.bat)
├── 📜 VBScript (.vbs)
├── 🐍 Python‑Skript (.py)
├── 📘 Textdatei (.txt)
├── 📊 CSV‑Datei (.csv)
├── 🎵 Audio‑Datei (.mp3)
├── 🎬 Video‑Datei (.mp4)
└── 📦 Installer / Archiv (.7z, .exe, .zip)
```

---

## ⚡ QUICK START

### 📦 Git & GitHub
```bash
# 1. Repository klonen
git clone https://github.com/mucahid-emin-tomakin/AutoMate.git
cd AutoMate

# 2. In den ein Projektfodler wechseln
cd AutomationAnywhere/TTSFactory

# 3. JSON-Dateien in Automation Anywhere importieren

# 4. Main Bot starten

# 5. Ergebnisse prüfen
```

---

## 🖼️ SCREENSHOTS

### 🎬 DemoWorkflow.mp4
![DemoWorkflow](https://github.com/mucahid-emin-tomakin/AutoMate/blob/main/AutomationAnywhere/TTSFactory/DemoWorkflow.mp4)
> **Hinweis:** Das Video zeigt die Ausführung des Main‑Bots und das Ergebnis (MP3 + Main.csv).

---

## ⚠️ WICHTIGE HINWEISE

### 📌 Vor der Verwendung
- ✅ stringWorkDirectory im PreConfiguration‑Bot auf den Entpack‑Pfad setzen
- ✅ Conda‑Umgebung AudioGenerator mit den obigen Befehlen einmalig erstellen
- ✅ Tortoise‑Modelle werden beim ersten Start automatisch heruntergeladen (ca. 4 GB)
- ✅ Die Runtime (FFMPEG, MINICONDA, TortoiseTTS) nicht ins Git‑Repo, sondern über Releases bereitstellen

### 🔒 Sicherheit
- ⚠️ Keine API‑Keys oder Passwörter in den JSON‑Bots speichern
- ⚠️ Die Modelle sind ca. 4 GB groß – Stelle sicher, dass genug Speicherplatz vorhanden ist
- ⚠️ Tortoise TTS benötigt eine NVIDIA GPU – auf CPU ist es extrem langsam

### 💡 Tipps
- ✅ Für schnellere Generierung --preset "ultra_fast" verwenden (geringere Qualität)
- ✅ Für beste Qualität --preset "high_quality" verwenden (deutlich langsamer)
- ✅ Eigene Stimmen: .wav‑Datei in tortoise/voices/Stimmenname/ ablegen
- ✅ Bei Fehlern: Die Main.csv enthält detaillierte Logs aller Schritte

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
| **Interessen** | Automation Anywhere, System-Automation | ⚙️ |

**Teil der AutoMate Familie:**
🤖 AutoMate | 🔧 Automation Scripts | Automation Anywhere | 🎙️ TTSFactory

## 📊 REPOSITORY STATISTIK

| Metrik | Wert | Trend |
|--------|------|-------|
| **Stars** | ![GitHub Stars](https://img.shields.io/github/stars/mucahid-emin-tomakin/AutoMate) | 📈 |
| **Forks** | ![GitHub Forks](https://img.shields.io/github/forks/mucahid-emin-tomakin/AutoMate) | 🔄 |
| **Issues** | ![GitHub Issues](https://img.shields.io/github/issues/mucahid-emin-tomakin/AutoMate) | ✅ |
| **Letztes Update** | ![GitHub Last Commit](https://img.shields.io/github/last-commit/mucahid-emin-tomakin/AutoMate) | 🕐 |

---

### 🔧 Made with ❤️ on Automation Anywhere
