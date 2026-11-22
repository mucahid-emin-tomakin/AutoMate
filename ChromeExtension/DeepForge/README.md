# 🧩 DeepForge

![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)
![Chrome Extension](https://img.shields.io/badge/Chrome%20Extension-Manifest%20V3-4285F4?logo=googlechrome&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES2022+-F7DF1E?logo=javascript&logoColor=black)
![DeepSeek](https://img.shields.io/badge/Target-chat.deepseek.com-4FACFE)
![HTML5 & CSS3](https://img.shields.io/badge/Standalone%20HTML-CSS%20%2B%20SVG-E34F26?logo=html5&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/Status-Aktiv-brightgreen)

---

## 📖 INHALTSVERZEICHNIS

- [📝 PROJEKTBESCHREIBUNG](#-projektbeschreibung)
  - [✨ Export-Workflow im Überblick](#-export-workflow-im-überblick)
- [✨ FEATURES](#-features)
  - [📦 Export-Formate & Datenaufbereitung](#-export-formate--datenaufbereitung)
  - [🔍 DOM-Parsing, Tabellen, Quellen & Diagramme](#-dom-parsing-tabellen-quellen--diagramme)
  - [📑 Anhang- & PDF-Erfassung](#-anhang---pdf-erfassung)
  - [🎨 Standalone-HTML: UI, Navigation & Interaktion](#-standalone-html-ui-navigation--interaktion)
  - [🛡️ Zuverlässigkeit, Sicherheit & Diagnose](#-zuverlässigkeit-sicherheit--diagnose)
- [🚀 TOOL](#-tool)
  - [🧩 Architektur der 10 Logischen Code-Abschnitte](#-architektur-der-10-logischen-code-abschnitte)
- [⚙️ KONFIGURATION](#️-konfiguration)
  - [📦 Voraussetzungen](#-voraussetzungen)
  - [✅ Überprüfung im Browser](#-überprüfung-im-browser)
  - [🎛️ Konfigurierbare Variablen (`content.js` – Abschnitt 1)](#️-konfigurierbare-variablen-contentjs--abschnitt-1)
- [📁 STRUKTUR](#-struktur)
  - [📂 Hauptverzeichnis (im `AutoMate`-Repository)](#-hauptverzeichnis-im-automate-repository)
  - [📂 Export-Ergebnisse (Downloads)](#-export-ergebnisse-downloads)
  - [📁 Struktur-Legende](#-struktur-legende)
- [⚡ QUICK START](#-quick-start)
  - [📦 Installation (einmalig)](#-installation-einmalig)
  - [▶️ Export starten (auf `chat.deepseek.com`)](#️-export-starten-auf-chatdeepseekcom)
  - [🧪 Diagnose-Befehle (DevTools-Konsole)](#-diagnose-befehle-devtools-konsole)
- [🖼️ SCREENSHOTS](#️-screenshots)
  - [🎬 DEMO](#-demo)
- [⚠️ WICHTIGE HINWEISE](#️-wichtige-hinweise)
  - [📌 Vor der Verwendung](#-vor-der-verwendung)
  - [🔒 Sicherheit & Datenschutz](#-sicherheit--datenschutz)
  - [🔧 Bekannte Einschränkungen & Tipps](#-bekannte-einschränkungen--tipps)
- [📝 LIZENZ](#-lizenz)
- [👤 AUTOR](#-autor)
- [📊 REPOSITORY STATISTIK](#-repository-statistik)

---

## 📝 PROJEKTBESCHREIBUNG

> **DeepForge** bindet sich direkt in die Benutzeroberfläche von `chat.deepseek.com` ein und bietet über ein kompaktes Dropdown-Menü den Export kompletter Konversationen als **JSON (`.json`)**, **Markdown (`.md`)**, **Plain Text (`.txt`)** oder als **eigenständiges interaktives HTML-Dokument (`.html`)** – inklusive Anhängen, PDF-Seitenbildern, Quellen und Inhaltsverzeichnis.

**DeepForge** ist eine modulare Chrome-Extension für **chat.deepseek.com**, mit der sich umfangreiche KI-Konversationen inklusive Gedankengängen (`chain_of_thought`), Tabellen, Code-Blöcken, Quellenangaben, Datei-Anhängen und mehrseitigen PDF-Dokumenten zuverlässig sichern und weiterverarbeiten lassen.

**Das Problem:**
- Lange DeepSeek-Chats mit vielen Nachrichten, Tabellen und Code-Blöcken lassen sich im Browser nicht sauber in einem Rutsch archivierbar sichern.
- Reine Copy-&-Paste-Auszüge verlieren Struktur, Tabellenformatierungen, Quellenbezüge oder Denkprozesse (`chain_of_thought`).
- Hochgeladene Text-/Markdown-Dateien und insbesondere **mehrseitige PDF-Anhänge** sind bei einem einfachen Seiten-Speichern nicht als durchsuchbare oder blätterbare Inhalte im Archiv enthalten.
- Externe Abhängigkeiten oder fehlende Styles machen gespeicherte HTML-Seiten oft unvollständig oder unübersichtlich.

**Die Lösung:**
- **DeepForge** extrahiert alle Nachrichten, Rollen (`user` / `assistant`), `chain_of_thought`-Blöcke, Anhänge, Tabellen, Code-Blöcke, Quellen und den Konversationstitel strukturiert aus dem DOM.
- **Vier Export-Formate** decken sowohl Weiterverarbeitung (`JSON`, `MD`, `TXT`) als auch komfortables Nachlesen (`HTML`) ab.
- **PDF- & Anhang-Erfassung** ermittelt dynamisch die Seitenzahl mehrseitiger PDFs und erfasst Seiten als Bilder sowie Text-/Markdown-Anhänge in den HTML-Export.
- **Standalone-HTML-Engine** bettet Styles, CSS-Variablen, `@font-face`-Schriften (inkl. `BlackChancery`), SVG-Filter, TOC mit Scrollspy, Quellen-Overlay, Datei-/PDF-Drawer, Code-Copy/Download und Scroll-Fortschrittsbalken direkt ein.
- **Zentrale Konfiguration & Diagnose** bündelt Timeouts, Selektoren, nicht erfassbare Dateiendungen sowie `[DeepForge]`-Logs und Toasts an einer Stelle.

**Für wen ist das?**
- Für Studierende und Forschende, die Lernchats, Literaturanalysen, Rechenwege und PDF-Anhänge dauerhaft archivieren möchten.
- Für Entwickler und Technische Redakteure, die Code, Tabellen und strukturierte Antworten als `.md`, `.json` oder `.txt` weiterverwenden wollen.
- Für alle, die lange DeepSeek-Verläufe als übersichtliches, offline nutzbares HTML-Archiv mit Inhaltsverzeichnis und Drawer behalten möchten.

Teil der **AutoMate**-Familie: 🤖 AutoMate | 🔧 Automation Scripts | 🐍 Python | 🧩 DeepForge

### ✨ Export-Workflow im Überblick
- **Direkter Zugriff in DeepSeek:** Über den integrierten Export-Button öffnet sich das Format-Menü (`JSON`, `MD`, `TXT`, `HTML`).
- **Live-Fortschritt & Schutz:** Während der Extraktion, Diagramm-Aufbereitung, Anhang-/PDF-Erfassung und HTML-Erzeugung führt ein Exporting-Overlay durch die Schritte und verhindert parallele Doppel-Exports.
- **Eigenständiges HTML-Archiv:** Die erzeugte `.html`-Datei funktioniert offline ohne externe Extension und bringt ein eigenes Inhaltsverzeichnis (TOC) mit Scrollspy, Quellen-Overlay, Datei-/PDF-Drawer sowie Code-Copy/Download mit.

---

## ✨ FEATURES

### 📦 Export-Formate & Datenaufbereitung
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 📄 **JSON-Export** | Strukturierter Export mit Titel, URL, Datum, Rollen, Inhalten, Anhängen und `chain_of_thought` | ✅ |
| 📝 **Markdown-Export (`.md`)** | Sauberes Markdown mit konvertierten Tabellen, Code-Blöcken und Quellen | ✅ |
| 📜 **Plain-Text-Export (`.txt`)** | Klarer Text-Export für schnelle Suche, Archivierung und Weiterverarbeitung | ✅ |
| 🌐 **Standalone-HTML-Export (`.html`)** | Eigenständiges HTML-Dokument mit eingebetteten Assets und interaktiver Oberfläche | ✅ |
| 🧠 **Chain-of-Thought-Unterstützung** | Erfasst und übernimmt `chain_of_thought`-Inhalte von Assistant-Nachrichten | ✅ |
| 📎 **User-Anhänge & Titel** | Extrahiert Anhang-Metadaten (Namen/Größen) sowie den Konversationstitel | ✅ |

### 🔍 DOM-Parsing, Tabellen, Quellen & Diagramme
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 📊 **Tabellen-Konvertierung** | Wandelt HTML-Tabellen sauber in Markdown-Tabellen um | ✅ |
| 💻 **Code-Block-Extraktion** | Erkennt Sprachangaben und Code-Inhalte aus `<pre>`- und Code-Blöcken | ✅ |
| 🔗 **Quellen-Normalisierung** | Bereinigt und normalisiert Web-Referenzen (`normalizeAssistantContent`) | ✅ |
| 📈 **Diagramm-Bereitschaft** | Wartet auf Diagramm-Blöcke (`DIAGRAM_READY_TIMEOUT_MS`) und bereitet sie vor | ✅ |
| 🖨️ **Print-Modus-Steuerung** | Löst `beforeprint` und `afterprint` mit konfigurierbaren Wartezeiten aus | ✅ |

### 📑 Anhang- & PDF-Erfassung
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 📂 **Text- & Markdown-Anhänge** | Erfasst Inhalte von `.md`-, `.txt`- und weiteren lesbaren Text-Anhängen | ✅ |
| 📕 **Mehrseitige PDF-Discovery** | Erkennt dynamisch die Gesamtseitenzahl (`PDF_DISCOVERY_MAX_MS`, `PDF_DISCOVERY_STABLE_MS`) | ✅ |
| 🖼️ **Seitenweises PDF-Rendering** | Erfasst PDF-Seiten nacheinander mit `PDF_PAGE_TIMEOUT_MS` und `PDF_PAGE_SETTLE_MS` | ✅ |
| 🚫 **Endungs-Filter (`NON_CAPTURABLE_EXTENSIONS`)** | Überspringt nicht erfassbare Formate (Bilder, Audio/Video, Archive, Office-Dateien) | ✅ |

### 🎨 Standalone-HTML: UI, Navigation & Interaktion
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 🧭 **Inhaltsverzeichnis (TOC) & Scrollspy** | Fixiertes TOC mit Ein-/Ausklappen, Smooth-Scroll und aktiver Scrollspy-Markierung | ✅ |
| 📚 **Quellen-Overlay** | Zeigt Quellen gebündelt an (Titel/Close im RGB-Stil, Einträge in weißer `BlackChancery` mit TOC-Hover) | ✅ |
| 🗂️ **Datei- & PDF-Drawer** | Seiten-Drawer für Textinhalte und seitenweise PDF-Ansichten inkl. Seitenhinweis | ✅ |
| 📋 **Code-Copy & Download** | Kopier- und Download-Funktion für Code-Blöcke direkt im exportierten HTML | ✅ |
| 🌈 **CSS-, Font- & SVG-Einbettung** | Bettet Stylesheets, CSS-Variablen, `@font-face` (`BlackChancery` u. a.) und `#df-electric` SVG-Filter ein | ✅ |
| 📊 **Scroll-Fortschrittsbalken** | Dynamische Scroll-Indikatoren für TOC, Drawer und Quellenliste (mit `requestAnimationFrame`-Drosselung) | ✅ |

### 🛡️ Zuverlässigkeit, Sicherheit & Diagnose
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 🔒 **Export-Sperre (`isExporting`)** | Verhindert parallele Doppel-Exports bei erneutem Klick während eines Laufs | ✅ |
| 🔌 **Kontext-Prüfung (`isExtensionContextValid`)** | Erkennt ungültige Extension-Kontexte vor und während des Exports | ✅ |
| ⚙️ **Einstellungen (`getSettings`)** | Lädt Konfiguration aus `chrome.storage.sync` mit sauberem Fallback auf `SETTINGS_DEFAULTS` | ✅ |
| 🛡️ **HTML-Escaping & Bereinigung** | Escapt Sonderzeichen sicher und entfernt UI-/Steuerelemente sowie überflüssige Nodes | ✅ |
| 🪵 **Diagnose-System (`DF_DEBUG`)** | Strukturierte Logs über `[DeepForge]`, `[DeepForge-Warning]` und `[DeepForge-Error]` plus Toasts | ✅ |

---

## 🚀 TOOL

| Bereich / Technologie | Zweck |
|---------------------|-------|
| **Chrome Extension (Manifest V3)** | Content-Script-Ausführung gezielt auf `chat.deepseek.com` |
| **JavaScript (ES2022+)** | DOM-Extraktion, Format-Konverter, PDF-Capture, HTML-Generator, UI-Steuerung |
| **HTML5 / CSS3 / SVG** | Standalone-Exportdokument, Animationen, `#df-electric`-Filter, Drawer & Overlays |
| **Chrome Storage API (`chrome.storage.sync`)** | Persistente Speicherung von Erweiterungs-Einstellungen mit Defaults |

### 🧩 Architektur der 10 Logischen Code-Abschnitte
| Abschnitt | Schwerpunkt |
|-----------|-------------|
| **1. Konfiguration, Debug & Utils** | `DF_DEBUG`, Timeouts, `TOC_MAX_LABEL_LENGTH`, `NON_CAPTURABLE_EXTENSIONS`, `DF_SELECTORS`, `SETTINGS_DEFAULTS`, `dfLog`/`dfWarn`/`dfError`, `isExtensionContextValid`, `getSettings` |
| **2. UI-Feedback (Toasts & Overlays)** | Toast-Benachrichtigungen und Exporting-Overlay mit Fortschrittstexten |
| **3. SVG-Filter & UI-Steuerung** | `#df-electric`-SVG-Filter, Export-Button und Dropdown-Menü |
| **4. Diagramm-Vorbereitung** | Erkennung, Warten auf Fertigstellung und Aufbereitung von Diagramm-Code-Blöcken |
| **5. DOM-Parsing (TeX, Tabellen, Code, Quellen)** | Umwandlung von Assistant-Inhalten, Tabellen, Code und Referenzen |
| **6. Chat-Extraktion** | Auslesen von Konversationstitel, User-/Assistant-Nachrichten, `chain_of_thought` und Anhängen |
| **7. Format-Konverter** | Erzeugung von JSON-, Markdown- und Plain-Text-Ausgaben |
| **8. Anhang- & PDF-Erfassung** | Auslesen von Text-/Markdown-Anhängen sowie Discovery und Capture von PDF-Seiten |
| **9. Standalone-HTML-Engine** | Aufbereitung des DOM, Style-/Font-Inlining, TOC, Quellen-Overlay, Drawer, Code-Aktionen & Scroll-Progress |
| **10. Export-Orchestrierung & Bootstrap** | `collectAllMessagesFromChat`, `downloadChat`, `exportChat` (inkl. `isExporting`-Lock) und `init` |

---

## ⚙️ KONFIGURATION

### 📦 Voraussetzungen
1. **Google Chrome** (oder Chromium-basierter Browser mit Extension-Unterstützung)
2. **Zugriff auf `chat.deepseek.com`** mit einem aktiven Konversationsverlauf
3. **Entpackter Projektordner** (`ChromeExtension/DeepForge/`) lokal auf dem Rechner

### ✅ Überprüfung im Browser
1. In Chrome `chrome://extensions` öffnen und den **Entwicklermodus** aktivieren.
2. Nach dem Laden der Erweiterung `chat.deepseek.com` öffnen und die DevTools-Konsole (`F12`) prüfen – bei `DF_DEBUG = true` erscheinen die `[DeepForge]`-Initialisierungslogs.

### 🎛️ Konfigurierbare Variablen (`content.js` – Abschnitt 1)
| Variable / Objekt | Standard | Beschreibung |
|-------------------|----------|--------------|
| `DF_DEBUG` | `false` | Aktiviert (`true`) oder deaktiviert (`false`) ausführliche Konsolen-Logs |
| `PDF_PAGE_TIMEOUT_MS` | `60000` | Maximale Wartezeit (ms) pro PDF-Seite beim Erfassen |
| `PDF_PAGE_SETTLE_MS` | `850` | Wartezeit (ms) nach dem Scrollen auf eine PDF-Seite vor dem Capture |
| `PDF_DISCOVERY_MAX_MS` | `120000` | Maximale Gesamtdauer (ms) für die Ermittlung der PDF-Seitenzahl |
| `PDF_DISCOVERY_STABLE_MS` | `6500` | Stabilitätszeit (ms), nach der eine erkannte PDF-Seitenzahl als final gilt |
| `BEFOREPRINT_DELAY_MS` | `1500` | Wartezeit (ms) nach dem Auslösen von `beforeprint` |
| `DIAGRAM_READY_TIMEOUT_MS` | `30000` | Maximale Wartezeit (ms), bis Diagramm-Blöcke bereit sind |
| `AFTERPRINT_DELAY_MS` | `500` | Wartezeit (ms) im `finally`-Block nach `afterprint` und `clearToasts()` |
| `TOAST_DURATION_ERROR_MS` | `6000` | Anzeigedauer (ms) für Fehler-Toasts |
| `TOAST_DURATION_WARNING_MS` | `4000` | Anzeigedauer (ms) für Warn-Toasts |
| `TOC_MAX_LABEL_LENGTH` | `60` | Maximale Zeichenlänge für Einträge im HTML-Inhaltsverzeichnis |
| `NON_CAPTURABLE_EXTENSIONS` | `Set(...)` | Dateiendungen (Bilder, Medien, Archive, Office), die nicht als Text/PDF erfasst werden |
| `DF_SELECTORS` | `{ ... }` | Zentrale CSS-Selektoren für Nachrichten, Anhänge, PDFs, Code, Quellen und Titel |
| `SETTINGS_DEFAULTS` | `{ ... }` | Standardwerte für `autoExport`, `notifyNewMessages` und `exportWebReferences` |

---

## 📁 STRUKTUR

### 📂 Hauptverzeichnis (im `AutoMate`-Repository)
```text
🧩 ChromeExtension/
└── 📂 DeepForge/
    ├── 📂 fonts/                   # Eingebettete Schriftarten (z. B. BlackChancery.ttf, Magnificent.ttf)
    ├── 📂 icons/                   # Extension-Icons (icon16.png, icon48.png, icon128.png)
    ├── 📂 assets/                  # Screenshots / GIFs für Dokumentation
    ├── 📄 manifest.json            # Extension-Manifest (Konfiguration & Berechtigungen)
    ├── ⚙️ background.js            # Hintergrundskript der Extension
    ├── 🐍 content.js               # Hauptskript (10 modulare Abschnitte für Extraktion, Capture & HTML-Export)
    ├── 🎨 styles.css               # Stylesheets der Extension
    └── 📄 README.md                # Projektdokumentation
```

### 📂 Export-Ergebnisse (Downloads)
```text
Downloads/
├── 📄 <Konversationstitel>.json   # Strukturierter JSON-Export
├── 📝 <Konversationstitel>.md     # Markdown-Export mit Tabellen & Quellen
├── 📜 <Konversationstitel>.txt    # Plain-Text-Export
└── 🌐 <Konversationstitel>.html   # Eigenständiges HTML mit TOC, Drawer, Quellen & eingebetteten Assets
```

### 📁 Struktur-Legende
```text
🧩 DeepForge/
├── 📂 Ordner
├── 📄 Konfigurations- & Dokumentationsdatei (.json, .md)
├── 🐍 Skriptdatei (.js)
├── 📝 Markdown- & Text-Export (.md, .txt)
└── 🌐 Eigenständiger HTML-Export (.html)
```

---

## ⚡ QUICK START

### 📦 Installation (einmalig)
```powershell
# 1. Repository klonen
git clone [https://github.com/mucahid-emin-tomakin/AutoMate.git](https://github.com/mucahid-emin-tomakin/AutoMate.git)
cd AutoMate/ChromeExtension/DeepForge
```

### 📦 Extention Laden (einmalig)
1. In Google Chrome **`chrome://extensions`** öffnen.
2. Oben rechts den **Entwicklermodus** aktivieren.
3. Auf **„Entpackte Erweiterung laden“** klicken und den Ordner `ChromeExtension/DeepForge` auswählen.

### ▶️ Export starten (auf `chat.deepseek.com`)
1. Einen Chat auf **`https://chat.deepseek.com`** öffnen und warten, bis die Nachrichten geladen sind.
2. Den **Export-Button** von DeepForge anklicken und im Dropdown **`JSON`**, **`MD`**, **`TXT`** oder **`HTML`** wählen.
3. Den Fortschritt im Exporting-Overlay abwarten – die Datei wird automatisch heruntergeladen.

### 🧪 Diagnose-Befehle (DevTools-Konsole)
```javascript
// Warn-Toast und [DeepForge-Warning] testen (im Content-Script-Kontext)
dfWarn('Keine Nachrichten zum Exportieren gefunden.');

// Fehler-Toast und [DeepForge-Error] testen (im Content-Script-Kontext)
dfError('Fehler beim Export.', new Error('Test-Fehler für Diagnose'));
```

---

## 🖼️ SCREENSHOTS


### 🎬 DEMO


---

## ⚠️ WICHTIGE HINWEISE

### 📌 Vor der Verwendung
* ✅ Die Extension arbeitet gezielt auf **`chat.deepseek.com`** – auf anderen Seiten wird die Initialisierung übersprungen.
* ✅ Bei umfangreichen Chats mit vielen oder langen PDF-Anhängen (z. B. 20–40+ Seiten) kann ein `HTML`-Export mehrere Minuten dauern.
* ✅ Falls die Extension neu geladen wurde, während ein Tab offen ist, hilft ein **Neuladen der Seite (`F5`)**, falls der Extension-Kontext ungültig geworden ist.

### 🔒 Sicherheit & Datenschutz
* ✅ Alle Extraktionen, Formatierungen und HTML-Generierungen laufen **lokal im Browser** ohne externen Backend-Server.
* ✅ Exportierte `.html`-Dateien enthalten eingebettete Styles, Schriften und Anhangsdaten – prüfe vor dem Weitergeben, ob vertrauliche Chat- oder PDF-Inhalte enthalten sind.
* ⚠️ Keine Tokens, Passwörter oder sensiblen Zugangsdaten in Konfigurationsdateien oder Logs ablegen.

### 🔧 Bekannte Einschränkungen & Tipps
* ⚠️ **Selektoren (`DF_SELECTORS`):** Wenn DeepSeek seine DOM-Klassen ändert, lassen sich die Selektoren zentral in Abschnitt 1 anpassen.
* ⚠️ **Nicht erfassbare Dateiformate:** Dateien aus `NON_CAPTURABLE_EXTENSIONS` (z. B. Archive, Medien, Office-Formate) werden bewusst nicht als Text/PDF-Seiten erfasst.
* 💡 **Debug-Modus:** Für normale Nutzung `const DF_DEBUG = false` belassen und für Fehlersuche temporär auf `true` setzen.

---

## 📝 LIZENZ

Dieses Projekt ist unter der **MIT License** lizenziert – frei für persönliche und kommerzielle Nutzung.

---

## 👤 AUTOR

**Mücahid Emin Tomakin (TomaKing)**

| Platform | Link | Icon |
| --- | --- | --- |
| **GitHub** | [@mucahid-emin-tomakin](https://github.com/mucahid-emin-tomakin) | 🐙 |
| **Automation** | Skript-Entwickler & Automatisierer | 🤖 |
| **Interessen** | Chrome Extensions, Python, System-Automation, KI-Pipelines | ⚙️ |

**Teil der AutoMate Familie:**
🤖 AutoMate | 🔧 Automation Scripts | 🐍 Python | 🧩 DeepForge

## 📊 REPOSITORY STATISTIK

| Metrik | Wert | Trend |
|--------|------|-------|
| **Stars** | ![GitHub Stars](https://img.shields.io/github/stars/mucahid-emin-tomakin/AutoMate) | 📈 |
| **Forks** | ![GitHub Forks](https://img.shields.io/github/forks/mucahid-emin-tomakin/AutoMate) | 🔄 |
| **Issues** | ![GitHub Issues](https://img.shields.io/github/issues/mucahid-emin-tomakin/AutoMate) | ✅ |
| **Letztes Update** | ![GitHub Last Commit](https://img.shields.io/github/last-commit/mucahid-emin-tomakin/AutoMate) | 🕐 |

---

### 🧩 Made with ❤️ for DeepForge — für strukturierte Chat- & HTML-Archive
