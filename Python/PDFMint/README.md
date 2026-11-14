# 🍃 PDFMint

![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Marker](https://img.shields.io/badge/Marker-PDF%20Parsing-FF6B6B)
![Qwen](https://img.shields.io/badge/Qwen2.5--VL-Vision-8B5CF6)
![GLM](https://img.shields.io/badge/GLM--OCR-OCR-10B981)
![llama.cpp](https://img.shields.io/badge/llama.cpp-Local%20Inference-4B5563)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/Status-Aktiv-brightgreen)

---

## 🎬 DEMO

Zwei kurze Aufnahmen zeigen den kompletten Ablauf – einmal beim **ersten Start** (Setup mit automatischem Download der Modelle) und einmal bei einem **weiteren Lauf** (alle Modelle bereits im Cache, Pipeline startet sofort).

### 🚀 Erster Start – automatisches Setup

> Beim ersten Lauf erstellt PDFMint die venv, installiert alle Python-Pakete, lädt GLM-OCR (~1,4 GB) und das Qwen2.5-VL-Vision-Modell (~2 GB) automatisch herunter. Je nach Internetverbindung dauert das **10–30 Minuten**. Danach startet die Pipeline selbstständig.

![Setup beim ersten Start](setup.gif)

### ▶️ Nächster Lauf – Pipeline läuft sofort

> Beim zweiten und allen weiteren Läufen prüft PDFMint in Sekunden, ob venv, Pakete und Modelle vorhanden sind – und beginnt direkt mit der Verarbeitung. Die vier Phasen (Erkennung → Marker → Vision → GLM-OCR) laufen automatisch nacheinander.

![Pipeline-Ausführung nach Download](run.gif)

---

## 📖 INHALTSVERZEICHNIS

- [🎬 Demo](#-demo)
- [📝 Projektbeschreibung](#-projektbeschreibung)
- [✨ Features](#-features)
- [🚀 Tool](#-tool)
- [⚙️ Konfiguration](#️-konfiguration)
- [📁 Struktur](#-struktur)
- [⚡ Quick Start](#-quick-start)
- [⚠️ Wichtige Hinweise](#️-wichtige-hinweise)
- [📝 Lizenz](#-lizenz)
- [👤 Autor](#-autor)

---

## 📝 PROJEKTBESCHREIBUNG

**PDFMint** ist eine vollautomatische, lokal laufende **PDF-zu-Markdown-Pipeline** für KI-Modelle und Wissensdatenbanken. Es verwandelt hunderte Seiten Literatur, Studienhefte oder gescannte Dokumente in **strukturiertes, sauberes Markdown** – inklusive Text, Tabellen, Formeln, Code und **Bildbeschreibungen**.

**Das Problem:**
- PDFs sind für Text-LLMs (DeepSeek, Llama, Mistral) nur schwer lesbar.
- Bilder und Diagramme werden von reinen Text-Modellen ignoriert.
- Reine Textextraktion verliert Tabellen, Formeln und Layout.
- Klassische OCR-Tools halluzinieren oder scheitern an deutschen Umlauten.
- Cloud-APIs (Baidu, Google Vision) haben Limits und kosten Geld.

**Die Lösung:**
- **PDFMint** erkennt automatisch, ob eine PDF einen Textlayer hat (digital) oder ein Scan ist.
- **Digitale PDFs** laufen durch **Marker** (Surya-Layout-Modell) → Text, Tabellen, Formeln, Code in Markdown.
- **Scans** laufen durch **GLM-OCR** (0,9B, exzellent bei Code) → reiner Text aus Seitenbildern.
- **Bilder** werden durch **Qwen2.5-VL** beschrieben → Diagramme werden zu lesbarem Text.
- **Druckseitenzahlen** werden aus den Fußzeilen extrahiert und als Kommentar eingefügt.
- **Alles lokal**, ohne Cloud, ohne Docker, ohne API-Keys.

**Für wen ist das?**
- Für Studierende, die Skripte und Lehrbücher für NotebookLM oder andere LLMs aufbereiten möchten.
- Für Forschende, die Paper-Sammlungen als durchsuchbares Markdown-Archiv brauchen.
- Für alle, die aus PDFs eine **KI-freundliche Wissensdatenbank** bauen wollen.

Teil der **AutoMate**-Familie: 🤖 AutoMate | 🔧 Automation Scripts | 🐍 Python | 🎬 ClipStack | 🍃 PDFMint

---

## ✨ FEATURES

### 🎯 Intelligente Pipeline-Auswahl
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 🔍 Automatische PDF-Erkennung | Textlayer vs. Scan wird in 3 Stichproben erkannt | ✅ |
| 📄 Digital-Pipeline | **Marker** mit Surya-Layout-Modell für Text, Tabellen, Formeln | ✅ |
| 📷 Scan-Pipeline | **GLM-OCR** (0,9B) für gescannte Seiten mit exzellenter Code-Erkennung | ✅ |
| 🖼️ Vision-Pipeline | **Qwen2.5-VL** beschreibt Bilder (Diagramme, Grafiken, Achsen) | ✅ |

### 🧠 Modell-Management
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 💾 VRAM-Optimierung | Modelle werden nach jeder Phase entladen (kein Parallelbetrieb) | ✅ |
| 🔄 Server-Lifecycle | llama-server startet nur bei Bedarf, stoppt nach Gebrauch | ✅ |
| 📦 Auto-Download | Modelle werden beim ersten Lauf automatisch geladen | ✅ |
| 🗂️ Cache-Umleitung | Alle Caches im Projektordner (`.cache\`), temporäre Junctions | ✅ |
| 🛠️ Selbstheilend | Erkennt fehlende venv/Pakete/Modelle und installiert sie automatisch | ✅ |

### 📑 Output-Qualität
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 📝 Struktur-Erhalt | Überschriften, Listen, Tabellen als Markdown | ✅ |
| 🧮 LaTeX-Formeln | Mathematische Formeln als LaTeX-Code | ✅ |
| 💻 Code-Blöcke | Python-Code in syntax-highlighted Blöcken | ✅ |
| 🖼️ Bildbeschreibungen | Diagramme als Text-Blockquotes statt tote Bildpfade | ✅ |
| 🔢 Druckseitenzahlen | Gedruckte Seitenzahl als `<!-- PDF-Seite X \| Druckseite Y -->` | ✅ |

### 🛡️ Zuverlässigkeit
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| ♻️ Resume-Funktion | Bricht der Lauf ab, wird bei der letzten Seite fortgesetzt | ✅ |
| 🚨 Halluzinations-Filter | Chinesischer Text in deutschen PDFs wird verworfen | ✅ |
| 🔁 Wiederholungsschutz | Endlosschleifen werden erkannt und Seite übersprungen | ✅ |
| 🧹 Auto-Cleanup | Temporäre Bilder werden nach Verarbeitung gelöscht | ✅ |

---

## 🚀 TOOL

| Sprache / Format | Zweck |
|------------------|-------|
| Python 3.12 | Kernlogik & Orchestrierung |
| llama.cpp | Lokale Vision-/OCR-Inferenz (Qwen2.5-VL, GLM-OCR) |
| Marker (datalab-to) | PDF-Layout-Parsing mit Surya |

### 🐍 Verwendete Bibliotheken
| Bibliothek | Zweck |
|------------|-------|
| 🐍 **Python 3.12** | Hauptprogrammiersprache |
| 📄 **pymupdf (fitz)** | PDF-Rendering & Fußzeilen-Analyse |
| 🏗️ **marker-pdf** | PDF → Markdown mit Layout-Erhalt |
| 👁️ **surya-ocr** | Layout- und Tabellenerkennung (via Marker) |
| 🤖 **openai** | Client für llama-server (OpenAI-kompatibel) |
| 🤗 **huggingface_hub** | Modell-Downloads (GGUF) |
| 🗂️ **pathlib / shutil** | Pfad- und Dateiverwaltung |

### 🤖 Verwendete KI-Modelle
| Modell | Größe | Zweck |
|--------|-------|-------|
| **Marker (Surya)** | ~2–3 GB VRAM | Layout, Tabellen, Formeln (in-process) |
| **Qwen2.5-VL-3B** | ~2–3 GB VRAM | Bildbeschreibungen (Port 8081) |
| **GLM-OCR-Q8_0** | ~1,4 GB VRAM | OCR für Scans (Port 8080) |

---

## ⚙️ KONFIGURATION

### 📦 Voraussetzungen
1. **Python 3.12** – [python.org](https://python.org)
2. **llama.cpp** (`llama-server` im PATH) – Installation:
   ```powershell
   winget install ggml.llamacpp
   ```
3. **NVIDIA GPU** mit mind. 6 GB VRAM (getestet auf RTX 2060 Super)
4. **~15 GB freier Speicherplatz** (Modelle, Cache, venv)

### ✅ Überprüfung der Installation
Nach der Installation sollte dieser Befehl funktionieren:
```bash
llama-server --version
```

### 🎛️ Konfigurierbare Variablen (`scripts/PDFMint.py`)
| Variable | Standard | Beschreibung |
|----------|----------|--------------|
| `MARKER_MODE` | `"fast"` | `fast` (CPU/llama.cpp) oder `balanced` (GPU/Docker) |
| `OCR_DPI` | `96` | Rendering-Auflösung für Scans |
| `OCR_PROMPT` | `"OCR"` | Prompt für GLM-OCR |
| `OCR_MAX_TOKENS` | `2048` | Maximale Output-Länge pro Seite |
| `MIN_TEXT_CHARS_PER_PAGE` | `50` | Schwelle für „digital vs. Scan“ |
| `VISION_MODEL` | `Qwen2.5-VL-3B-Instruct-GGUF` | Bildbeschreibungs-Modell |
| `GGUF_MODEL` | `GLM-OCR-Q8_0.gguf` | OCR-Modell für Scans |

---

## 📁 STRUKTUR

### 📂 Hauptverzeichnis
```text
🍃 PDFMint/
├── 📂 scripts/
│   └── 🐍 PDFMint.py         # Hauptprogramm (Setup + Pipeline)
├── 📂 assets/
│   ├── 🎬 setup.gif          # Demo: Erster Start
│   └── 🎬 run.gif            # Demo: Pipeline-Lauf
├── 📂 input/                 # PDFs hier ablegen
├── 📂 output/                # Markdown-Ergebnisse pro PDF
├── 📂 models/                # GGUF-Modelle (auto-download)
├── 📂 .cache/                # HF / Datalab / llama.cpp Cache
├── 📂 .venv/                 # Python-Virtualenv
└── 📄 README.md
```

### 📂 Ergebnis-Struktur (nach dem Lauf)
```text
input/
├── buch1.pdf                 # Bleibt erhalten
├── buch2.pdf
└── scan1.pdf

output/
├── buch1/
│   └── buch1.md              # Markdown mit Bildbeschreibungen
├── buch2/
│   └── buch2.md
└── scan1/
    └── scan1.md              # Markdown aus OCR
```

---

## ⚡ QUICK START

### 📦 Installation (einmalig)

```powershell
# 1. Repository klonen
git clone https://github.com/mucahid-emin-tomakin/AutoMate.git
cd AutoMate/Python/PDFMint

# 2. PDFMint starten – Setup läuft automatisch
python scripts\PDFMint.py
```

**Beim ersten Start passiert alles automatisch:**
- ✅ venv wird erstellt (mit Python 3.12)
- ✅ Alle Python-Pakete werden installiert (`pymupdf`, `marker-pdf`, `openai`, …)
- ✅ GLM-OCR-Modelle werden heruntergeladen (~1,4 GB)
- ✅ Qwen2.5-VL-Vision-Modell wird heruntergeladen (~2 GB)
- ✅ Marker-Modelle werden heruntergeladen (~3–5 GB)

> ⏱️ **Erster Start:** 10–30 Minuten (je nach Internetverbindung).  
> 🚀 **Weitere Starts:** ~10 Sekunden (alles gecacht).

### ▶️ Pipeline starten (ab dem zweiten Lauf)

```powershell
# 1. PDFs in "input\" legen
# 2. PDFMint starten
python scripts\PDFMint.py
```

**Was automatisch passiert:**
1. **Phase 0 – Vorbereitung** – venv, Pakete, Modelle prüfen
2. **Phase 1 – PDF-Erkennung** – Textlayer vs. Scan (3 Stichproben)
3. **Phase 2 – Marker** – verarbeitet digitale PDFs (Layout, Tabellen, Formeln)
4. **Phase 3 – Qwen2.5-VL** – beschreibt alle extrahierten Bilder
5. **Phase 4 – GLM-OCR** – verarbeitet gescannte PDFs (falls vorhanden)

### 🐍 Manuell (mit aktivierter venv)

```powershell
.venv\Scripts\activate
python scripts\PDFMint.py
```

---

## 🖼️ SCREENSHOTS

### Beispiel-Output (Markdown)
```markdown
## 1.1 Gängige Programmiersprachen für die KI-Programmierung

Im Portal Kaggle tauscht sich eine große Online Community zu Data Science 
und maschinellem Lernen (ML) aus...

<!-- PDF-Seite 9 | Druckseite 3 -->

> **Bildbeschreibung:** Das Bild zeigt ein Balkendiagramm, das die 
> häufigsten Programmiersprachen nach Benutzergruppen (Anfänger, 
> Fortgeschrittene, Experten) darstellt. **Python** ist die häufigste 
> Programmiersprache für alle drei Gruppen, gefolgt von **SQL**, 
> **JavaScript** und **R**.

$$MSE = \frac{1}{m} \sum_{i=1}^m \left( h(\mathbf{x}^{(i)}) - \mathbf{y}^{(i)} \right)^2$$
```

---

## ⚠️ WICHTIGE HINWEISE

### 📌 Vor der Verwendung
- ✅ **`llama-server` muss im PATH sein** (aus `ggml.llamacpp`).
- ✅ **Alle PDFs** in `input/` legen – Unterordner werden nicht durchsucht.
- ✅ Die Original-PDFs werden **nie verändert** – sie bleiben in `input/`.
- ✅ Der Cache liegt **im Projektordner** (`.cache/`), nicht im Benutzerprofil.

### 🔒 Sicherheit & Datenschutz
- ✅ **100% lokal** – keine Cloud, keine API-Keys, keine Telemetrie.
- ✅ Modelle werden einmalig von Hugging Face geladen.
- ⚠️ Beim ersten Lauf werden **~9 GB** heruntergeladen (Modelle + venv + Cache).

### 🔧 Bekannte Einschränkungen
- ⚠️ **Marker** kann bei sehr komplexen Tabellen scheitern (eine von 20 Tabellen).
- ⚠️ **GLM-OCR** ist bei extrem kleinen Schriftgrößen (< 8 pt) weniger zuverlässig.
- ⚠️ **Qwen2.5-VL** halluziniert manchmal bei abstrakten Logos (interpretiert zu viel).
- ⚠️ **Druckseitenzahlen** werden nur erkannt, wenn sie in den unteren 15 % einer Seite stehen.

---

## 📝 LIZENZ

Dieses Projekt ist unter der **MIT License** lizenziert – frei für persönliche und kommerzielle Nutzung.

---

## 👤 AUTOR

**Mücahid Emin Tomakin (TomaKing)**

| Platform | Link | Icon |
|----------|------|------|
| **GitHub** | [@mucahid-emin-tomakin](https://github.com/mucahid-emin-tomakin) | 🐙 |
| **Automation** | Skript-Entwickler & Automatisierer | 🤖 |
| **Interessen** | Python, System-Automation, KI-Pipelines | ⚙️ |

**Teil der AutoMate Familie:**
🤖 AutoMate | 🔧 Automation Scripts | 🐍 Python | 🎬 ClipStack | 🍃 PDFMint

---

### 🍃 Made with ❤️ on Python — für saubere Markdown-Pipelines
