# 🧹 PathPurge

![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-0078D6?logo=windows&logoColor=white)
![Registry](https://img.shields.io/badge/Registry-FF6B6B?logo=windows&logoColor=white)
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

**PathPurge** ist ein Python-basiertes Tool zur **Bereinigung der Windows-Umgebungsvariable `PATH`**. Es analysiert alle Einträge, erkennt tote Pfade, doppelte Einträge und Ordner ohne ausführbare Dateien – und hilft Ihnen interaktiv, die PATH-Variable zu optimieren.

**Warum dieses Tool?**
- Die `PATH`-Variable wird oft mit der Zeit unübersichtlich durch viele Installationen und Deinstallationen.
- Tote Pfade verlangsamen die Konsolen-Suche und können zu Fehlern führen.
- Doppelte Einträge sind überflüssig und blähen die Variable auf.
- Ordner ohne `.exe`-Dateien (nur DLLs, Configs etc.) sind meistens unnötig für die Kommandozeile.

**Für wen ist das?**
- Entwickler, die ihre System-Umgebung sauber halten möchten.
- Administratoren, die Windows-Rechner optimieren.
- Jeder, der Probleme mit der Konsole (`python`, `pip`, `docker` etc.) hat.

Das Tool ist Teil der **SystemTools**-Familie und wird dort zusammen mit weiteren System-Optimierungslösungen weiterentwickelt.

---

## ✨ FEATURES

### 🔍 PATH-Analyse
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 🔴 Tote Pfade | Erkennt automatisch nicht existierende Ordner | ✅ |
| 🔄 Doppelte Einträge | Entfernt Duplikate (behält ersten) | ✅ |
| 🟡 EXE-Prüfung | Erkennt Ordner ohne `.exe`-Dateien | ✅ |
| 🟢 Behalten | Sicherheits-Check: Ordner mit EXE werden automatisch behalten | ✅ |
| 📋 Übersicht | Klare Vorschau aller zu bearbeitenden Einträge | ✅ |

### 🛡️ Sicherheit
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 💾 Backup | Erstellt vor jeder Änderung ein Backup | ✅ |
| 🧪 Interaktiv | Jeder Eintrag wird einzeln bestätigt | ✅ |
| 🔧 Registry | Direkter Zugriff auf Windows-Registry | ✅ |
| 📢 Benachrichtigung | Windows wird informiert, dass sich die Umgebungsvariablen geändert haben | ✅ |

### 🎨 Benutzerfreundlichkeit
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 🖥️ Schöne Ausgabe | Klare, farbige Konsolenausgabe mit Trennlinien | ✅ |
| 🇩🇪 Deutsch | Vollständig auf Deutsch (für Benutzer) | ✅ |
| 📊 Zusammenfassung | Überblick über vorher/nachher | ✅ |
| ⚡ Schnell | Analysiert hunderte Einträge in Sekunden | ✅ |

---

## 🚀 TOOL

| Sprache / Format | Zweck |
|------------------|-------|
| Python 3.6+ | Kernlogik & Ausführung |
| Windows Registry | Speicherort der PATH-Variable |
| TXT | Backup-Datei |

### 🐍 Verwendete Bibliotheken
| Bibliothek | Zweck |
|------------|-------|
| 🐍 **Python 3.6+** | Hauptprogrammiersprache |
| 📁 **pathlib** | Moderne Dateipfad-Handhabung |
| 📝 **os, sys** | Systemoperationen |
| 🔧 **ctypes** | Windows-API-Aufrufe (Admin-Check & Benachrichtigung) |
| 💾 **winreg** | Registry-Zugriff (Lesen & Schreiben) |

---

## ⚙️ KONFIGURATION

Das Skript benötigt **keine externe Konfigurationsdatei**. Alle Einstellungen sind direkt im Code am Anfang der Datei `PathPurge.py` zu finden:
```python
# ============================== SETTINGS ==============================

BACKUP_DIR = Path(__file__).parent  # Backup-Ordner (Standard: Skript-Ordner)

# ============================== EMOJIS (optional) ==============================

# Das Skript verwendet standardmäßig diese Emojis für die Ausgabe:
#   🔴 = zu löschende Einträge (rot)
#   🟡 = zur Entscheidung (gelb)
#   🟢 = behaltene Einträge (grün)
#   ✅ = bestätigt
#   ⏩ = übersprungen
#   ❌ = Fehler
#   ℹ️  = Information
#   ✨ = Erfolg
```
Wenn Sie Änderungen am Backup-Verzeichnis oder an der Emoji-Darstellung wünschen, können Sie die entsprechenden Variablen im Code anpassen.

---

## 📁 STRUKTUR

### 📂 Hauptverzeichnis
```Text
🧹 PathPurge/
├── 🐍 PathPurge.py
├── 🐍 PathPurge.py
└── 📄 README.md
```

### 📁 Struktur-Legende
```text
🧹 PathPurge/               # Hauptprojektordner
├── 🐍 .py                  # Python-Skript (Hauptprogramm)
├── 📘 .txt                 # Backup-Dateien (automatisch generiert)
└── 📄 README.md            # Projektdokumentation (diese Datei)
```

---

## ⚡ QUICK START

### 📦 Git & GitHub
```bash
# 1. Repository klonen
git clone https://github.com/mucahid-emin-tomakin/AutoMate.git
cd AutoMate

# 2. In den ein Projektfodler wechseln
cd AutoMate/Python/PathPurge

# 3. Skript als Administrator ausführen (wichtig!)
#    → Rechtsklick auf PowerShell → "Als Administrator ausführen"

# 4. Tool ausführen (nur Standardbibliothek nötig)
python PathPurge.py
# Oder mit dem Python Launcher (empfohlen, wenn python nicht funktioniert):
py PathPurge.py

# 5. Ergebnis prüfen
#    → PATH_BACKUP_*.txt wurde im Skript-Ordner erstellt
#    → PATH-Variable wurde bereinigt
```

### 🐍 Python virtueller Umgebung
```bash
# Mit virtueller Umgebung
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
python PathPurge.py
```

---

## 🖼️ SCREENSHOTS

### 🐍 PathPurge - Beispiel Run
```text
======================================================================
  🧹 WINDOWS PATH-REINIGER (PYTHON-VERSION)
======================================================================

----------------------------------------------------------------------
  📋 VORSCHAU – SYSTEM
----------------------------------------------------------------------

  🔴 AUTOMATISCH ZU LÖSCHEN (existieren nicht): 2
     ❌ C:\AlterMüll\Pfad1
     ❌ C:\AlterMüll\Pfad2

  🟡 ZUR ENTSCHEIDUNG (keine .exe-Dateien): 1
     📁 C:\Program Files\NVIDIA Corporation\NVIDIA App\NvDLISR
        Enthält: NGXWrapper.dll, nvngx_dlisr.dll

  🟢 BEHALTEN (haben .exe-Dateien): 15
     (15 Einträge – werden automatisch behalten)

  🔧 Möchtest du diese 3 Einträge bearbeiten?
     (j/n): j

----------------------------------------------------------------------
  ⚙️  ENTSCHEIDUNG – SYSTEM
----------------------------------------------------------------------

  [1/2] 📁 C:\Users\tomak\AppData\Local\Programs\Python\Python312\
      Enthaltene Dateien (Beispiele):
        • Lib
        • Scripts
        • share
      ➡️  Diesen Eintrag LÖSCHEN? (j/n): j
      ✅ Wird gelöscht.

----------------------------------------------------------------------
  📊 ERGEBNIS – SYSTEM
----------------------------------------------------------------------
  Vorher: 18 Einträge
  Nachher: 17 Einträge
  Gelöscht: 1 Einträge
```

### 🎯 Hauptmenü & Analyse
```text
======================================================================
  🧹 WINDOWS PATH-REINIGER (PYTHON-VERSION)
======================================================================
  Dieses Skript analysiert und bereinigt Ihre PATH-Umgebungsvariable.
  Es erstellt ein Backup, bevor Änderungen vorgenommen werden.

  📁 Backup gespeichert unter: C:\Users\USER\Downloads\PATH_BACKUP_...

======================================================================
  🖥️  SYSTEM-PATH (HKLM) – BETRIFFT ALLE BENUTZER
======================================================================

  🔍 Analysiere System-PATH (18 Einträge)...

----------------------------------------------------------------------
  📋 VORSCHAU – SYSTEM
----------------------------------------------------------------------

  🔴 AUTOMATISCH ZU LÖSCHEN (existieren nicht): 2
     ❌ C:\AlterMüll\Pfad1
     ❌ C:\AlterMüll\Pfad2

  🟡 ZUR ENTSCHEIDUNG (keine .exe-Dateien): 3
     📁 C:\Users\tomak\AppData\Local\Programs\Python\Python312\
        Enthält: Lib, Scripts, share
     📁 C:\Program Files\NVIDIA Corporation\NVIDIA App\NvDLISR
        Enthält: NGXWrapper.dll, nvngx_dlisr.dll
     📁 C:\Program Files\Razer Chroma SDK\bin
        Enthält: (leer)

  🟢 BEHALTEN (haben .exe-Dateien): 13
     (13 Einträge – werden automatisch behalten)

  🔧 Möchtest du diese 5 Einträge bearbeiten?
     (j/n):
```

### 📋 Interaktive Entscheidung
```text
----------------------------------------------------------------------
  ⚙️  ENTSCHEIDUNG – SYSTEM
----------------------------------------------------------------------

  [1/3] 📁 C:\Users\tomak\AppData\Local\Programs\Python\Python312\
      Enthaltene Dateien (Beispiele):
        • Lib
        • Scripts
        • share
      ➡️  Diesen Eintrag LÖSCHEN? (j/n): j
      ✅ Wird gelöscht.

  [2/3] 📁 C:\Program Files\NVIDIA Corporation\NVIDIA App\NvDLISR
      Enthaltene Dateien (Beispiele):
        • NGXWrapper.dll
        • nvngx_dlisr.dll
      ➡️  Diesen Eintrag LÖSCHEN? (j/n): n
      ⏩ Bleibt erhalten.
```

### 📊 Abschluss-Zusammenfassung
```text
======================================================================
  📊 GESAMT-ZUSAMMENFASSUNG
======================================================================
  SYSTEM: 18 → 15 Einträge
  USER  : 4 → 4 Einträge

  ⏳ Änderungen dauerhaft in der Registry speichern?
     (j/n): j
  ✅ System-PATH aktualisiert.

======================================================================
  🎉 FERTIG!
======================================================================
  Windows wurde benachrichtigt.
  Bitte starte alle geöffneten Konsolen (CMD, PowerShell) NEU.
  Ein Neustart des PCs ist NICHT erforderlich.
```

---

## ⚠️ WICHTIGE HINWEISE

### 📌 Vor der Verwendung
- ✅ **Als Administrator ausführen!** – Registry-Änderungen benötigen erhöhte Rechte.
- ✅ **Backup wird automatisch erstellt** – Sie können jederzeit zurückkehren.
- ✅ **Das Tool löscht keine Programme** – es entfernt nur Einträge aus der PATH-Variable.
- ✅ **Nur Windows** – das Skript nutzt Windows-spezifische APIs (`winreg`, `ctypes`).

### 🔒 Sicherheit
- ⚠️ **Das Tool verändert die Registry** – aber nur die `PATH`-Variable.
- ⚠️ **Vor jeder Änderung wird ein Backup erstellt** – im Skript-Ordner.
- ⚠️ **Jeder Eintrag wird einzeln bestätigt** – Sie haben volle Kontrolle.
- ⚠️ **Bei Fehlern wird nichts gespeichert** – das Skript bricht ab, wenn etwas schiefgeht.

### 💡 Tipps
- ✅ **Verwenden Sie `py` statt `python`** – der Python Launcher funktioniert immer.
- ✅ **Doppelte Einträge werden automatisch entfernt** – Sie müssen nichts tun.
- ✅ **Führen Sie das Skript regelmäßig aus** – z.B. einmal im Monat.
- ✅ **Prüfen Sie das Backup bei Unsicherheit** – es enthält den kompletten alten PATH.

### 🔧 Fehlerbehebung
| Problem | Lösung |
|---------|--------|
| `Python wurde nicht gefunden` | Verwenden Sie `py PathPurge.py` statt `python PathPurge.py` |
| `Keine Administrator-Rechte` | Rechtsklick auf PowerShell → "Als Administrator ausführen" |
| `winreg nicht gefunden` | Führen Sie das Skript auf Windows aus (nicht Linux/macOS) |
| `Registry-Schreibfehler` | Prüfen Sie die Berechtigungen oder führen Sie das Skript als Administrator aus |

### 🐛 Bekannte Einschränkungen
- Das Skript funktioniert nur unter **Windows** (wegen Registry-Zugriff).
- Es werden nur **existierende Ordner** geprüft – UNC-Pfade (Netzwerk) werden nicht unterstützt.
- Bei sehr langen PATH-Einträgen (>2048 Zeichen) kann Windows Probleme haben – das Skript warnt nicht davor.

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
| **Interessen** | Python, Windows, System-Automation | ⚙️ |

**Teil der AutoMate Familie:**
🤖 AutoMate | 🔧 Automation Scripts | 🐍 Python | 🧹 PathPurge

## 📊 REPOSITORY STATISTIK

| Metrik | Wert | Trend |
|--------|------|-------|
| **Stars** | ![GitHub Stars](https://img.shields.io/github/stars/mucahid-emin-tomakin/AutoMate) | 📈 |
| **Forks** | ![GitHub Forks](https://img.shields.io/github/forks/mucahid-emin-tomakin/AutoMate) | 🔄 |
| **Issues** | ![GitHub Issues](https://img.shields.io/github/issues/mucahid-emin-tomakin/AutoMate) | ✅ |
| **Letztes Update** | ![GitHub Last Commit](https://img.shields.io/github/last-commit/mucahid-emin-tomakin/AutoMate) | 🕐 |

---

### 🔧 Made with ❤️ on Python
