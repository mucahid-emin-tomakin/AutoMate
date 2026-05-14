# 🌳 TreeMapper

![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Automation](https://img.shields.io/badge/Automation-FF6B6B?logo=robot&logoColor=white)
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

**TreeMapper** ist ein Python-basiertes Tool, das eine übersichtliche Verzeichnisbaumstruktur mit **Emojis** und typischen Baumzeichen (`├──`, `└──`, `│`) in eine Textdatei exportiert.  
Es durchläuft rekursiv einen Ordner, sortiert Inhalte (Ordner zuerst, dann Dateien) und fügt individuelle Emojis für bestimmte Namen hinzu.

**Warum dieses Tool?**
- Visuelle Darstellung von Ordnerhierarchien in Klartext.
- Individuelle Emojis für bestimmte Ordner/Dateien (z. B. 🤖 für `AutoMate`, 🐍 für `Python`).
- Perfekt für Dokumentationen, READMEs oder Inventarlisten.
- Volle Kontrolle über die Ausgabe – exakt wie der Linux `tree`-Befehl, aber mit Emojis.

**Für wen ist das?**
- Entwickler, die ihre Projektstruktur in Textform festhalten möchten.
- Administratoren, die eine schnelle Übersicht über Dateisysteme brauchen.
- Jeder, der eine ansprechende Ordnerstruktur für GitHub-Repositories erstellen will.

Das Tool ist Teil der **AutoMate**-Familie und wird dort zusammen mit weiteren Automatisierungslösungen weiterentwickelt.

---

## ✨ FEATURES

### 📁 Baum-Export
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 🌳 Rekursive Baumdarstellung | Zeigt alle Unterordner und Dateien | ✅ |
| 🎨 Individuelle Emojis | Mapping von Namen auf Emojis (z. B. `"Python": "🐍"`) | ✅ |
| 📏 Baumzeichen | `├──`, `└──`, `│` für echte Baumstruktur | ✅ |
| 📄 Export nach `.txt` | Lesbare Textdatei mit UTF-8-Kodierung | ✅ |
| 🔍 Sortierung | Ordner zuerst, dann Dateien (alphabetisch) | ✅ |
| 🛡️ Fehlertoleranz | Überspringt nicht erreichbare Ordner | ✅ |

### 🎯 Konfigurationsmöglichkeiten
| Einstellung | Beschreibung |
|-------------|---------------|
| `FOLDER_PATH` | Startverzeichnis für den Baum |
| `emoji_mapping` | Diktat für benutzerdefinierte Emojis |
| `DEFAULT_FOLDER_EMOJI` | Fallback für Ordner ohne Emoji |
| `DEFAULT_FILE_EMOJI` | Fallback für Dateien ohne Emoji |

---

## 🚀 TOOL

| Sprache / Format | Zweck |
|------------------|-------|
| Python 3.11+ | Kernlogik & Ausführung |
| TXT | Exportierte Baumstruktur |
| pathlib | Moderne Dateipfad-Handhabung |

### 🐍 Verwendete Bibliotheken
| Bibliothek | Zweck |
|------------|-------|
| 🐍 **Python 3.11** | Hauptprogrammiersprache |
| 📁 **pathlib** | Plattformunabhängige Pfadoperationen |
| 📝 **builtins** | Datei-I/O, Sortierung |

---

## ⚙️ KONFIGURATION

Alle Einstellungen sind am Anfang der Datei:

```python
FOLDER_PATH = r"C:\Users\USER\Downloads\AutoMate"

emoji_mapping = {
    "AutoMate": "🤖",
    "Python": "🐍",
    "WorkingTimeTracker": "⏱️",
    "MediaTracker": "🎬",
    "CopySync": "🔄",
    "FolderForge": "🔨",
    "NameShift": "🔄",
    "README.md": "📄",
}

DEFAULT_FOLDER_EMOJI = "📁"
DEFAULT_FILE_EMOJI = "📄"
```
- FOLDER_PATH – Pfad zum gewünschten Startordner.
- emoji_mapping – Weist bestimmten Namen ein Emoji zu (Groß-/Kleinschreibung beachten).
- DEFAULT_*_EMOJI – Fallback-Emojis, wenn kein Mapping existiert.

---

## 📁 STRUKTUR

### 📂 Hauptverzeichnis
```Text
🌳 TreeMapper/
├── 🐍 TreeMapper.py
├── 🐍 TreeMapper - NoComment.py
└── 📄 README.md
```

### 🐍 TreeMapper - Beispiel Run
```text
🤖 AutoMate/
├── 🐍 Python/
│   └── ⏱️ WorkingTimeTracker/
│   ├── 🎬 MediaTracker/
│   ├── 🔄 CopySync/
│   ├── 🔨 FolderForge/
│   └── 🔄 NameShift/
└── 📄 README.md
```

### 📁 Struktur-Legende
```text
🌳 TreeMapper/
├── 🐍 .py                    # Python-Skripte (Hauptprogramm & Varianten)
├── 📄 README.md              # Projektbeschreibung (diese Datei)
└── 📘 .txt                   # Exportierte Baumdatei (baum.txt)
```

---

## ⚡ QUICK START

### 📦 Git & GitHub
```bash
# 1. Repository klonen
git clone https://github.com/mucahid-emin-tomakin/AutoMate.git
cd AutoMate

# 2. In den ein Projektfodler wechseln
cd AutoMate/Python/TreeMapper

# 3. Konfiguration anpassen (FOLDER_PATH und Emojis)
#    → Öffne TreeMapper.py und setze den gewünschten Pfad

# 4. Tool ausführen (nur Standardbibliothek nötig)
python TreeMapper.py

# 5. Ergebnis prüfen
#    → baum.txt enthält die Baumstruktur
```

### 🐍 Python virtueller Umgebung
```bash
# Mit virtueller Umgebung
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
python TreeMapper.py
```

---

## 🖼️ SCREENSHOTS

### baum.txt
```text
🤖 AutoMate/
├── 🐍 Python/
│   └── ⏱️ WorkingTimeTracker/
│   ├── 🎬 MediaTracker/
│   ├── 🔄 CopySync/
│   ├── 🔨 FolderForge/
│   └── 🔄 NameShift/
└── 📄 README.md
```

### 📋 Fallback-Emojis
```Text
📁 Documents/
├── 📄 file1.txt
├── 📁 Subfolder/
│   └── 📄 file2.pdf
└── 📁 Archive/
    └── 📄 old.log
```

---

## ⚠️ WICHTIGE HINWEISE

### 📌 Vor der Verwendung
- ✅ FOLDER_PATH auf das Zielverzeichnis setzen (absoluter oder relativer Pfad).
- ✅ Emoji-Mapping nach Bedarf anpassen – Namen müssen exakt mit Ordnern/Dateien übereinstimmen.
- ✅ Das Skript benötigt keine externen Pakete – nur Python-Standardbibliothek.

### 🔒 Sicherheit
- ⚠️ Das Tool ändert keine Dateien – es erstellt nur eine Textdatei.
- ⚠️ Bei fehlenden Berechtigungen für Ordner wird der Ordner stillschweigend übersprungen.
- ⚠️ Die Ausgabedatei baum.txt wird im aktuellen Arbeitsverzeichnis erstellt (überschreibt bestehende Datei).

### 💡 Tipps
- ✅ Verwende relative Pfade, wenn der Baum relativ zum Skript erstellt werden soll: FOLDER_PATH = "."
- ✅ Füge weitere Emojis im Mapping hinzu – z. B. "TreeMapper": "🌳".
- ✅ Für die Einbindung in READMEs: Kopiere den Inhalt von baum.txt in einen Codeblock.
- ✅ Kombiniere mit tree /F unter Windows oder tree unter Linux – aber Emojis machen es schöner.

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
🤖 AutoMate | 🔧 Automation Scripts | 🐍 Python | 🌳 TreeMapper

## 📊 REPOSITORY STATISTIK

| Metrik | Wert | Trend |
|--------|------|-------|
| **Stars** | ![GitHub Stars](https://img.shields.io/github/stars/mucahid-emin-tomakin/AutoMate) | 📈 |
| **Forks** | ![GitHub Forks](https://img.shields.io/github/forks/mucahid-emin-tomakin/AutoMate) | 🔄 |
| **Issues** | ![GitHub Issues](https://img.shields.io/github/issues/mucahid-emin-tomakin/AutoMate) | ✅ |
| **Letztes Update** | ![GitHub Last Commit](https://img.shields.io/github/last-commit/mucahid-emin-tomakin/AutoMate) | 🕐 |

---

### 🔧 Made with ❤️ on Python
