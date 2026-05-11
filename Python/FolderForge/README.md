# 🔨 FolderForge

![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Automation](https://img.shields.io/badge/Automation-FF6B6B?logo=robot&logoColor=white)
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

**FolderForge** ist ein Python-basiertes Tool zur automatischen Erstellung einer Ordnerstruktur aus einer einfachen, semikolongetrennten Namensliste.  
Statt dutzende Ordner manuell anzulegen, genügt ein konfigurierbarer Namensstring – das Skript erledigt den Rest.

**Warum dieses Tool?**
- Blitzschnelle Erstellung konsistenter Ordnerstrukturen für Projekte, Kurse oder Seminare.
- Bereits existierende Ordner werden erkannt und übersprungen – keine Duplikate.
- Übersichtliche Statistik am Ende: Erstellt, bereits vorhanden, Fehler.
- Null externe Abhängigkeiten – reines Python, sofort lauffähig.

**Für wen ist das?**
- Für Projektmanager, die einheitliche Strukturen anlegen wollen.
- Für Lehrende, die Semester-Ordner vorbereiten.
- Für jeden, der wiederkehrende Ordnerstrukturen braucht.

Das Tool ist Teil der **AutoMate**-Familie und wird dort zusammen mit weiteren Automatisierungslösungen weiterentwickelt.

---

## ✨ FEATURES

### 🔨 Ordner-Erstellung
| Feature | Beschreibung | Status |
|---------|-------------|--------|
| 📋 Listen-basierte Erstellung | Semikolongetrennte Namensliste | ✅ |
| 🔍 Existenz-Prüfung | Überspringt bereits vorhandene Ordner | ✅ |
| 📊 Statistik | Zählt Created / Existing / Errors | ✅ |
| 🧹 Namensbereinigung | Entfernt Leerzeichen um Namen | ✅ |
| 🚫 Leere Namen | Ignoriert leere Einträge automatisch | ✅ |
| ⚡ Keine Abhängigkeiten | Nur Python-Standardbibliothek | ✅ |

### 📁 Was es generiert
| Ergebnis | Beschreibung |
|----------|-------------|
| Ordnerstruktur | Alle Ordner aus der Liste im Zielverzeichnis |

---

## 🚀 TOOL

| Sprache / Format | Zweck |
|------------------|-------|
| Python 3.11+ | Kernlogik & Ausführung |
| os.makedirs | Ordner-Erstellung |
| String-Liste | Konfiguration der Ordnernamen |

### 🐍 Verwendete Bibliotheken
| Bibliothek | Zweck |
|------------|-------|
| 🐍 **Python 3.11** | Hauptprogrammiersprache |
| 📁 **os** | Dateisystem-Operationen & Pfadbehandlung |

---

## ⚙️ KONFIGURATION

Alle Einstellungen sind am Anfang der Datei:

```python
# ============================== CONFIGURATION ==============================

FOLDER_PATH = r"C:\Users\USER\Documents\Projekte"     # Zielverzeichnis
FOLDER_NAMES = "Ordner1;Ordner2;Ordner3"              # Semikolongetrennte Namensliste
FILE_ENCODING = "utf-8"                               # Zeichenkodierung
```

---

## 📁 STRUKTUR

### 📂 Hauptverzeichnis
```Text
🔨 FolderForge/
├── 🐍 FolderForge.py
├── 🐍 FolderForge - NoComment.py
└── 📄 README.md
```

### 🐍 FolderForge - Beispiel Run
```text
C:\Users\USER\Documents\Projekte/
├── 📁 Kalender
├── 📁 Meine Buchungen
├── 📁 Nachhaltigkeit in der Lehre
├── 📁 KI in der Lehre
├── 📁 Tipps und Tricks zur Mathematik
├── 📁 Online-Bibliothek
├── 📁 Forschungsorientierte Lehre
├── 📁 Wissenschaftliches Arbeiten
├── 📁 Digitale Lernkarten
└── 📁 Auslandsprogramm
```

### 📁 Struktur-Legende
```text
🔨 FolderForge/
├── 🐍 .py                    # Python-Skripte (Hauptprogramm & Varianten)
├── 📄 README.md              # Projektbeschreibung (diese Datei)
└── 📁 ...                    # Erstellte Ordner im Zielverzeichnis
```

---

## ⚡ QUICK START

### 📦 Git & GitHub
```bash
# 1. Repository klonen
git clone https://github.com/mucahid-emin-tomakin/AutoMate.git
cd AutoMate

# 2. In den ein Projektfodler wechseln
cd AutoMate/Python/FolderForge

# 3. Konfiguration anpassen
#    → FOLDER_PATH = Zielverzeichnis
#    → FOLDER_NAMES = gewünschte Ordnername

# 4. Tool ausführen (installiert fehlende Pakete automatisch)
python FolderForge.py

# 5. Ordner wurden im Zielverzeichnis erstellt
```

### 🐍 Python virtueller Umgebung
```bash
# Mit virtueller Umgebung
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
python FolderForge.py
```

---

## 🖼️ SCREENSHOTS

### Erfolgreiche Ausführung
```text
Target path: C:\Users\USER\Documents\Projekte
Folders to create: 10
----------------------------------------
✓ Created: Kalender
✓ Created: Meine Buchungen
→ Already exists: Nachhaltigkeit in der Lehre
✓ Created: KI in der Lehre
✓ Created: Tipps und Tricks zur Mathematik
✓ Created: Online-Bibliothek
✓ Created: Forschungsorientierte Lehre
✓ Created: Wissenschaftliches Arbeiten
✓ Created: Digitale Lernkarten
✓ Created: Auslandsprogramm
----------------------------------------
Created: 9 | Already existed: 1 | Errors: 0
Done.
```

### 📋 Mit Fehler (z. B. keine Schreibrechte)
```Text
Target path: C:\Users\USER\Documents\Projekte
Folders to create: 10
----------------------------------------
✓ Created: Kalender
✓ Created: Meine Buchungen
❌ Error: Nachhaltigkeit in der Lehre → Permission denied
----------------------------------------
Created: 2 | Already existed: 0 | Errors: 1
Done.
```

### 📋 Schritt 3 – Dateien umbenennen
```Text
==================================================
 STEP: RENAME FILES
==================================================
✓ Renamed: index(1).html  →  index 1.html
✓ Renamed: about(2).html  →  about 2.html

Files renamed: 2
```

---

## ⚠️ WICHTIGE HINWEISE

### 📌 Vor der Verwendung
- ✅ FOLDER_PATH muss auf ein existierendes Verzeichnis zeigen
- ✅ Ordnernamen mit ; trennen (Semikolon)
- ✅ Leere Einträge (z. B. ;;) werden automatisch ignoriert
- ✅ Keine externen Python-Pakete nötig – nur Standard-Bibliothek

### 🔒 Sicherheit
- ⚠️ Bereits existierende Ordner werden nicht überschrieben
- ⚠️ Bei fehlenden Schreibrechten wird der Fehler protokolliert und das Skript läuft weiter
- ⚠️ Sonderzeichen in Ordnernamen sind erlaubt, aber je nach Betriebssystem unterschiedlich

### 💡 Tipps
- ✅ FILE_ENCODING auf "utf-8" lassen für Umlaute und Sonderzeichen
- ✅ Die Namensliste kann beliebig lang sein – auch hunderte Ordner auf einmal
- ✅ Vor dem Produktivlauf: Test mit einem temporären Verzeichnis

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
🤖 AutoMate | 🔧 Automation Scripts | 🐍 Python | 🔨 FolderForge

## 📊 REPOSITORY STATISTIK

| Metrik | Wert | Trend |
|--------|------|-------|
| **Stars** | ![GitHub Stars](https://img.shields.io/github/stars/mucahid-emin-tomakin/AutoMate) | 📈 |
| **Forks** | ![GitHub Forks](https://img.shields.io/github/forks/mucahid-emin-tomakin/AutoMate) | 🔄 |
| **Issues** | ![GitHub Issues](https://img.shields.io/github/issues/mucahid-emin-tomakin/AutoMate) | ✅ |
| **Letztes Update** | ![GitHub Last Commit](https://img.shields.io/github/last-commit/mucahid-emin-tomakin/AutoMate) | 🕐 |

---

### 🔧 Made with ❤️ on Python
