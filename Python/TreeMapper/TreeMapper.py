#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TreeMapper

# ============================== IMPORTS ==============================

from pathlib import Path

# ============================== IMPORTS ==============================
# ============================== CONFIGURATION ==============================

FOLDER_PATH = r"C:\Users\tomak\Downloads\AutomationAnywhere\TTSFactory"
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
# Fallback emojis
DEFAULT_FOLDER_EMOJI = "📁"
DEFAULT_FILE_EMOJI = "📄"

# ============================== CONFIGURATION ==============================
# ============================== HELPER FUNCTIONS ==============================

def get_emoji(eintrag: Path) -> str:
    """Returns the emoji for a folder or file."""
    name = eintrag.name
    if name in emoji_mapping:
        return emoji_mapping[name]
    if eintrag.is_dir():
        return DEFAULT_FOLDER_EMOJI
    return DEFAULT_FILE_EMOJI

def baum_schreiben(pfad: Path, ausgabedatei, prefix: str = "", ist_letztes: bool = True):
    """
    Traverses the path and writes the tree structure into the file.
    """
    emoji = get_emoji(pfad)
    # Root entry (without connecting lines)
    if prefix == "":
        ausgabedatei.write(f"{emoji} {pfad.name}/\n")
        prefix = ""
    else:
        connector = "└── " if ist_letztes else "├── "
        ausgabedatei.write(f"{prefix}{connector}{emoji} {pfad.name}\n")

    # Continue only for directories
    if pfad.is_dir():
        # Sort contents: folders first, then files
        eintraege = sorted(pfad.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower()))
        anzahl = len(eintraege)
        for idx, eintrag in enumerate(eintraege, start=1):
            ist_letzter_eintrag = (idx == anzahl)
            # New prefix for the next level
            neuer_prefix = prefix + ("    " if ist_letztes else "│   ")
            baum_schreiben(eintrag, ausgabedatei, neuer_prefix, ist_letzter_eintrag)

# ============================== HELPER FUNCTIONS ==============================
# ============================== MAIN PROGRAM ==============================

if __name__ == "__main__":
    start_pfad = Path(FOLDER_PATH)
    if not start_pfad.exists():
        print(f"Fehler: Der Pfad '{start_pfad}' existiert nicht.")
        exit(1)

    ausgabe_datei = "baum.txt"
    with open(ausgabe_datei, "w", encoding="utf-8") as f:
        baum_schreiben(start_pfad, f)

    print(f"Baum wurde in '{ausgabe_datei}' gespeichert.")