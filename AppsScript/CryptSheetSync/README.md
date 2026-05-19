# 🔄 CryptSheetSync

![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)
![Apps Script](https://img.shields.io/badge/Apps%20Script-4285F4?logo=googleapps&logoColor=white)
![Google Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?logo=google-sheets&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/Status-Stabil-brightgreen)

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

**CryptSheetSync** ist ein Google‑Apps‑Script‑Projekt, das einzelne Blätter aus einer Quell‑Tabelle anhand von Dropdown‑Auswahlen in eine Ziel‑Tabelle importiert.
Dabei werden verschlüsselte Blattnamen und Zellinhalte **automatisch erkannt und entschlüsselt** – unabhängig davon, ob das Dropdown selbst im Klartext oder verschlüsselt vorliegt.
Ein flexibler **Präfix‑Mechanismus** erlaubt es, zu jedem Dropdown‑Wert Namenszusätze (z. B. Klassennamen) zu ergänzen, ohne die Suchlogik anpassen zu müssen.  
Ein intelligenter **🌙‑Filter** blendet nach dem Import alle Zeilen ohne 🌙‑Symbol aus, behält aber strukturelle Kopfzeilen bei.
Ein **automatischer Bereinigungsdienst** löscht temporäre Import‑Blätter nach einer einstellbaren Inaktivitätsdauer, während ein **Zähler** die Anzahl der Importe im Hauptblatt protokolliert.

### 📁 Workflow-Übersicht
Der Workflow findet in der **Google Drive-Umgebung** statt, genutzt über die Oberfläche von **CryptoSheetSync** – einer tabellenbasierten Importlösung mit integrierter Entschlüsselung.  
Der Benutzer navigiert über die Drive-Struktur oder direkt über die Tab-Oberfläche von CryptoSheetSync.

**2. Dropdown-gesteuerter Blattimport**  
- In `MainSheet` wählt der Benutzer über ein **Dropdown-Menü** aus, welches Blatt aus `SourceSheet` importiert werden soll.  
- Die **Blattnamen** in `SourceSheet` können **verschlüsselt** sein.  
- Das **Dropdown selbst** kann entweder im **Klartext** oder **verschlüsselt** vorliegen – CryptoSheetSync erkennt automatisch, ob eine Entschlüsselung nötig ist.

**3. Flexibler Präfix-Mechanismus**  
- Zu jedem Dropdown-Wert können **Namenszusätze** (z. B. Klassennamen, IDs) definiert werden.  
- Diese **Präfixe** werden bei der Suche nach dem Quellblatt **ignoriert** – d. h. das System findet das Blatt auch dann, wenn der tatsächliche Blattname zusätzliche Informationen enthält.  

**Beispiel:**  
Dropdown-Wert = `Klasse_A` → Gefunden wird Blatt mit Namen `Klasse_A_Mathe`

**4. Import & Entschlüsselung von Zellinhalten**  
- Die Daten des gefundenen Blattes werden nach `MainSheet` **kopiert**.  
- Dabei werden **Zellinhalte, die verschlüsselt sind**, automatisch **entschlüsselt**.  
- Die **Struktur** (Spalten, Kopfzeilen) bleibt erhalten.

**5. 🌙-Filter („Mond-Filter“)**  
- Nach dem Import werden alle Zeilen **ohne das 🌙-Symbol** (in einer definierten Spalte) **ausgeblendet**.  
- **Kopfzeilen** bleiben erhalten, auch wenn sie kein 🌙 enthalten.  
- Dies dient zur schnellen Fokussierung auf relevante Datensätze (z. B. „Nachtaktiv“, „abgeschlossen“, „priorisiert“).

**6. Automatische Bereinigung (Cleanup-Dienst)**  
- **Temporäre Import-Blätter** (z. B. Zwischenspeicher) werden automatisch gelöscht.  
- Löschung erfolgt nach einer **einstellbaren Inaktivitätsdauer** (z. B. 24 Stunden ohne Zugriff auf das temporäre Blatt).  
- Verhindert **Datenmüll** in der Drive-Ablage.

**7. Importzähler & Protokollierung**  
- Ein **Zähler** im Hauptblatt (`MainSheet`) dokumentiert, wie viele Importe bereits durchgeführt wurden.  
- **Optional:** Loggt auch Zeitstempel, Quelle, Ziel, Status (erfolgreich/fehlgeschlagen).

### 🔐 Sicherheitsaspekt (implizit)
Da Blattnamen und Zellinhalte verschlüsselt sein können, liegt die Vermutung nahe, dass ein **symmetrischer Schlüssel** (z. B. via `PropertiesService` von Apps Script) im Projekt hinterlegt ist.  
Der Nutzer muss den Schlüssel **nicht manuell pro Import** eingeben.

### ✅ Typischer Ablauf für den Endnutzer
1. **Öffne** `MainSheet` in Google Drive.  
2. **Wähle** im Dropdown ein gewünschtes Blatt aus `SourceSheet` (z. B. „Kurs 101“).  
3. **Klicke** auf „Importieren“ (nicht explizit im GIF, aber logisch).  
4. Das System **sucht** das Blatt (auch mit Präfix), **entschlüsselt** Namen & Inhalte.  
5. Die **Daten erscheinen** in `MainSheet`.  
6. Der **🌙-Filter** blendet irrelevante Zeilen aus.  
7. Der **Importzähler** erhöht sich um 1.  
8. **Temporäre Blätter** werden später automatisch gelöscht.

## ✨ FEATURES
### 🔄 Import & Verschlüsselungs‑Erkennung
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| **Dropdown‑Import** | Zellen A2, A4, B2 lösen Import aus | ✅ |
| **Präfix‑Map** | Pro Zelle mehrere Präfixe konfigurierbar (Klartext & verschlüsselt) | ✅ |
| **4‑Wege‑Suche** | Sucht pro Präfix alle Kombinationen: Klartext‑/Verschlüsselt‑Präfix × Dropdown‑Klartext/-Verschlüsselt | ✅ |
| **Auto‑Entschlüsselung** | A1‑Zellen werden entschlüsselt, wenn Quelle oder Präfix verschlüsselt waren | ✅ |
| **Intelligenter 🌙‑Filter** | Blendet Zeilen ohne 🌙 aus, erhält aber Zeilen mit Werten aus der Kopfzeile | ✅ |
| **Temporäre Blätter** | Importierte Blätter erhalten fortlaufende Nummern (0, 1, 2 …) | ✅ |
| **Automatische Bereinigung** | Löscht temporäre Blätter nach einstellbarer Inaktivität (Minuten) | ✅ |
| **Zähler & Zeitstempel** | Schreibt Anzahl der Importe und letzte Nutzung in die Master‑Tabelle | ✅ |
| **Doppelausführungsschutz** | `onEdit`-Handler kann nicht parallel laufen | ✅ |
| **Master‑Menü** | Verschlüsselungs‑Menü für die Quell‑Tabelle (separates Script) | ✅ |

---

## 🚀 TOOL

| Sprache / Format | Zweck |
|------------------|-------|
| **Google Apps Script** | Hauptlogik für Import, Verschlüsselung, Filter, Cleanup |
| **Google Sheets** | Quell‑ und Ziel‑Tabellen |
| **PropertiesService** | Speichert Zustände zwischen Script‑Ausführungen |

---

## ⚙️ KONFIGURATION

```javascript
// ===================================================================================================
//                                      CONFIGURATION 
// ===================================================================================================
const SOURCE_FILE_ID = "1pO86BY7zcCa6EVcWje9RjWLZ8BSd6xG1-qaJvYEX4rY";   // Quell-Tabelle
const MASTER_SHEET_NAME = "Main";                                        // Hauptblatt mit Dropdowns
const TEMP_SHEET_REGEX = /^\d+$/;                                        // Muster für temporäre Blätter
const CLEANUP_INTERVAL_MINUTES = 1;                                      // Minuten Inaktivität bis Löschung
const PREFIX_MAP = {
  "A2": ["ClassName - "],          // Präfix(e) für Zelle A2
};
```

---

## 📁 STRUKTUR

### 📂 Hauptverzeichnis
```Text
🔄 CryptSheetSync/
├── 🛠️ MainSheetCode.gs
├── 🛠️ MainSheetCode - NoComment.gs
├── 🛠️ SourceSheetCode.gs
├── 🛠️ SourceSheetCode - NoComment.gs
├── 📊 MainSheet.xlsx
├── 📊 SourceSheet.xlsx
├── 🎬 DemoConfiguration.gif
├── 🎬 DemoWorkflow.gif
└── 📄 README.md
```

### 📁 Struktur-Legende
```text
🔄 CryptSheetSync/
├── 🛠️ .gs                    # Google Apps Script (Hauptprogramm & Varianten)
├── 📊 .xlsx                  # Google Sheets Export (Quell- & Ziel-Tabellen)
├── 🎬 .gif                   # Video‑Datei
└── 📄 README.md              # Projektbeschreibung (diese Datei)
```

---

## ⚡ QUICK START

### 📦 Git & GitHub
```bash
# 1. Repository klonen
git clone https://github.com/mucahid-emin-tomakin/AutoMate.git
cd AutoMate

# 2. In den ein Projektfodler wechseln
cd AutoMate/AppsScript/CryptSheetSync
```

### 📊 Google Sheets
**Tabellen in Google Drive hochladen & als Sheets öffnen**
- Öffne Google Drive.
- Lade SourceSheet.xlsx und MainSheet.xlsx hoch (Neu → Datei-Upload).
- Klicke jede hochgeladene Datei mit rechts an und wähle „Öffnen mit → Google Tabellen“.
- Speichere beide als Google‑Sheets‑Dokument (Google konvertiert sie automatisch beim Öffnen).

### 🔗 Konfiguration
**Quell‑ID notieren & Prefix‑Map anpassen**
- Öffne die soeben konvertierte Quell‑Tabelle (ehemals SourceSheet.xlsx).
- Kopiere die Tabellen‑ID aus der URL:
```text
https://docs.google.com/spreadsheets/d/1pO86BY7zcCa6EVcWje9RjWLZ8BSd6xG1-qaJvYEX4rY/edit
                                 └────────────────── ID ──────────────────┘
```
- Öffne die Main‑Tabelle (ehemals MainSheet.xlsx). Gehe auf Erweiterungen → Apps Script.
- Ersetze dort den Platzhalter bei const SOURCE_FILE_ID = "..." durch deine kopierte ID.
- Passe bei Bedarf die PREFIX_MAP an (Präfixe für die Zellen A2, A4 etc.).

### 🛠️ Apps Script
- In der Main‑Tabelle (Import‑Logik):
  - Öffne den Script‑Editor (Erweiterungen → Apps Script), lösche den Standard‑Code und füge den Inhalt von MainSheetCode.gs ein.
  - Alternativ kannst du MainSheetCode - NoComment.gs verwenden, falls du die Kommentare nicht benötigst.
- In der Quell‑Tabelle (Verschlüsselungsmenü – optional):
  - Wiederhole den gleichen Vorgang mit dem Inhalt von SourceSheetCode.gs.
  - Dieses Script fügt das Menü 🔐 Encrypt hinzu, mit dem du Blattnamen und A1‑Zellen ver‑/entschlüsseln kannst.

### ▶️ Trigger erstellen
- Wechsle in den Script‑Editor der Main‑Tabelle.
- Wähle die Funktion createTriggers aus und klicke auf ▶️ Ausführen.
- Es erscheint ein Berechtigungsdialog: Konto wählen → Erweitert → Zu CryptSheetSync (unsicher) → Zulassen.
- Danach sind zwei Trigger aktiv: onEditHandler (bei Bearbeitung) und deleteIfInactive (zeitgesteuert).

### 🧪 Funktion testen
- Gehe zurück zur Main‑Tabelle, wähle im Blatt „Main“ in Zelle A2, A4 oder B2 einen Dropdown‑Wert aus (z. B. einen Sheet‑Namen).
- Das passende Blatt wird importiert, ggf. entschlüsselt und der 🌙‑Filter greift, falls der Eintrag mit 🌙 endete.

### 🎬 DemoConfiguration.gif
![DemoConfiguration](https://github.com/mucahid-emin-tomakin/AutoMate/blob/main/AppsScript/CryptSheetSync/DemoConfiguration.gif)
> **Hinweis:** Das Video zeigt die Konfiguration nach dem Klonen des Repositories.

---

## 🖼️ SCREENSHOTS

### 🎬 DemoWorkflow.gif
![DemoWorkflow](https://github.com/mucahid-emin-tomakin/AutoMate/blob/main/AppsScript/CryptSheetSync/DemoWorkflow.gif)
> **Hinweis:** Das Video demonstriert die Funktionsweise der Dateien.

---

## ⚠️ WICHTIGE HINWEISE

### 📌 Vor der Verwendung
- ✅ Die SOURCE_FILE_ID muss exakt stimmen – sonst schlagen alle Importe fehl.
- ✅ Das Blatt MASTER_SHEET_NAME (default: „Main“) muss existieren, damit Zähler/Zeitstempel geschrieben werden können.
- ✅ Die Zellen A3 (Zähler) und B3 (Zeitstempel) dürfen von dir nicht manuell überschrieben werden – sie werden automatisch befüllt.
- ✅ Das Cleanup‑Intervall sollte nicht unter 1 Minute liegen – sonst werden Blätter u. U. sofort gelöscht.

### 🔒 Sicherheit
- ⚠️ Das Script benötigt Zugriff auf deine Google‑Tabellen und Trigger. Erteile die Berechtigungen nur, wenn du dem Code vertraust.
- ⚠️ Verschlüsselte A1‑Zellen werden beim Import entschlüsselt – ein versehentlicher Doppel‑Aufruf von decryptImportedData kann die Daten verfälschen. Die aktuelle Version verhindert das.
- ⚠️ Temporäre Blätter werden nach CLEANUP_INTERVAL_MINUTES unwiderruflich gelöscht – bei Bedarf vorher manuell umbenennen.

### 💡 Tipps
- ✅ Du kannst in PREFIX_MAP für eine Zelle mehrere Präfixe eintragen, z. B. ["9/10E - ", "11/12E - "]. Das Script probiert alle nacheinander.
- ✅ Möchtest du den 🌙‑Filter deaktivieren, wähle einfach einen Dropdown‑Wert ohne angehängtes „🌙“.
- ✅ Wenn du neue Dropdown‑Zellen hinzufügst, ergänze einfach deren A1‑Notation in der PREFIX_MAP.
- ✅ Führe createTriggers nach jeder Änderung an Trigger‑relevanten Teilen erneut aus (vorhandene Trigger werden automatisch gelöscht).

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
| **Interessen** | Google Sheets, Apps Script, System‑Automation | ⚙️ |

**Teil der AutoMate Familie:**
🤖 AutoMate | 🔧 Automation Scripts | 🛠️ Apps Script | 🔄 CryptSheetSync

## 📊 REPOSITORY STATISTIK

| Metrik | Wert | Trend |
|--------|------|-------|
| **Stars** | ![GitHub Stars](https://img.shields.io/github/stars/mucahid-emin-tomakin/AutoMate) | 📈 |
| **Forks** | ![GitHub Forks](https://img.shields.io/github/forks/mucahid-emin-tomakin/AutoMate) | 🔄 |
| **Issues** | ![GitHub Issues](https://img.shields.io/github/issues/mucahid-emin-tomakin/AutoMate) | ✅ |
| **Letztes Update** | ![GitHub Last Commit](https://img.shields.io/github/last-commit/mucahid-emin-tomakin/AutoMate) | 🕐 |

---

### 🔧 Made with ❤️ on Apps Script
