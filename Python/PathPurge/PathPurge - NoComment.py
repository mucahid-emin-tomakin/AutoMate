#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PathPurge - NoComment.py

# ============================== IMPORTS ==============================

import os
import sys
import ctypes
import winreg
from datetime import datetime
from pathlib import Path

# ============================== HELPER FUNCTIONS (TERMINAL) ==============================

def print_separator(char='=', length=70):
    print(char * length)

def print_header(text, char='=', length=70):
    print_separator(char, length)
    print(f"  {text.upper()}")
    print_separator(char, length)

def print_subheader(text, char='-', length=70):
    print_separator(char, length)
    print(f"  {text}")
    print_separator(char, length)

# ============================== HELPER FUNCTIONS (ADMIN CHECK) ==============================

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

if not is_admin():
    print("❌ FEHLER: Dieses Skript muss als Administrator ausgeführt werden!")
    print("   Rechtsklick auf die .py-Datei -> 'Mit PowerShell ausführen' als Admin?")
    print("   Oder: Starte CMD/PowerShell als Admin und rufe 'python clean_path.py' auf.")
    sys.exit(1)

# ============================== HELPER FUNCTIONS (REGISTRY) ==============================

def get_backup_dir():
    return Path(__file__).parent

def read_path_from_reg(hkey, subkey):
    try:
        key = winreg.OpenKey(hkey, subkey, 0, winreg.KEY_READ)
        value, reg_type = winreg.QueryValueEx(key, "Path")
        winreg.CloseKey(key)
        if value is None or value == "":
            return [], reg_type
        return value.split(';'), reg_type
    except FileNotFoundError:
        return [], winreg.REG_EXPAND_SZ
    except Exception as e:
        print(f"⚠️  Fehler beim Lesen von {subkey}: {e}")
        return [], winreg.REG_EXPAND_SZ

def write_path_to_reg(hkey, subkey, path_list, reg_type):
    if not path_list:
        new_value = ""
    else:
        new_value = ';'.join(path_list)
    try:
        key = winreg.CreateKey(hkey, subkey)
        winreg.SetValueEx(key, "Path", 0, reg_type, new_value)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"❌ Fehler beim Schreiben von {subkey}: {e}")
        return False

def notify_environment_change():
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    SMTO_ABORTIFHUNG = 0x0002
    ctypes.windll.user32.SendMessageTimeoutW(
        HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment",
        SMTO_ABORTIFHUNG, 5000, None
    )

# ============================== HELPER FUNCTIONS (CLEANUP) ==============================

def analyze_path_list(paths, owner_name):
    if not paths:
        return [], [], [], []

    paths = [p.strip() for p in paths if p and p.strip()]
    unique_paths = list(dict.fromkeys(paths))

    to_remove_auto = []
    to_ask = []
    to_keep = []

    print(f"\n  🔍 Analysiere {owner_name}-PATH ({len(unique_paths)} Einträge)...")

    for p in unique_paths:
        expanded = os.path.expandvars(p)
        
        if not os.path.exists(expanded):
            to_remove_auto.append(p)
            continue

        try:
            entries = os.listdir(expanded)
            exe_count = sum(
                1 for entry in entries
                if entry.lower().endswith('.exe') and os.path.isfile(os.path.join(expanded, entry))
            )
        except:
            exe_count = 0

        if exe_count == 0:
            to_ask.append(p)
        else:
            to_keep.append(p)

    return to_remove_auto, to_ask, to_keep, unique_paths

def interactive_clean(paths, owner_name):
    if not paths:
        return []

    to_remove_auto, to_ask, to_keep, unique_paths = analyze_path_list(paths, owner_name)
    
    print_subheader(f"📋 VORSCHAU – {owner_name.upper()}-PATH", '-')
    
    print(f"\n  🔴 AUTOMATISCH ZU LÖSCHEN (existieren nicht): {len(to_remove_auto)}")
    if to_remove_auto:
        for p in to_remove_auto:
            print(f"     ❌ {p}")
    else:
        print("     (keine)")

    print(f"\n  🟡 ZUR ENTSCHEIDUNG (keine .exe-Dateien): {len(to_ask)}")
    if to_ask:
        for p in to_ask:
            expanded = os.path.expandvars(p)
            try:
                files = os.listdir(expanded)
                sample = ', '.join(files[:4])
                if len(files) > 4:
                    sample += f" ... ({len(files)} Dateien)"
            except:
                sample = "(kein Zugriff)"
            print(f"     📁 {p}")
            print(f"        Enthält: {sample}")
    else:
        print("     (keine)")

    print(f"\n  🟢 BEHALTEN (haben .exe-Dateien): {len(to_keep)}")
    if to_keep and len(to_keep) <= 5:
        for p in to_keep:
            print(f"     ✅ {p}")
    elif to_keep:
        print(f"     ({len(to_keep)} Einträge – werden automatisch behalten)")

    total_candidates = len(to_remove_auto) + len(to_ask)
    if total_candidates == 0:
        print("\n  ✨ Keine überflüssigen Einträge gefunden – alles sauber!")
        return unique_paths
    
    print(f"\n  🔧 Möchtest du diese {total_candidates} Einträge bearbeiten?")
    while True:
        choice = input("     (j/n): ").strip().lower()
        if choice in ['j', 'n']:
            break
    
    if choice == 'n':
        print("     ⏩ Übersprungen – es wird NICHTS gelöscht.")
        return unique_paths
    
    final_remove = set(to_remove_auto)
    
    if to_ask:
        print_subheader(f"⚙️  ENTSCHEIDUNG – {owner_name.upper()}", '-')
        for idx, p in enumerate(to_ask, 1):
            expanded = os.path.expandvars(p)
            print(f"\n  [{idx}/{len(to_ask)}] 📁 {p}")
            try:
                files = os.listdir(expanded)
                print("      Enthaltene Dateien (Beispiele):")
                for f in files[:6]:
                    print(f"        • {f}")
                if len(files) > 6:
                    print(f"        ... und {len(files) - 6} weitere")
            except:
                print("      (kein Zugriff auf Inhalt)")
            
            while True:
                choice = input("      ➡️  Diesen Eintrag LÖSCHEN? (j/n): ").strip().lower()
                if choice in ['j', 'n']:
                    break
            if choice == 'j':
                final_remove.add(p)
                print("      ✅ Wird gelöscht.")
            else:
                print("      ⏩ Bleibt erhalten.")
    
    final_list = [p for p in unique_paths if p not in final_remove]
    
    print_subheader(f"📊 ERGEBNIS – {owner_name.upper()}", '-')
    print(f"  Vorher: {len(unique_paths)} Einträge")
    print(f"  Nachher: {len(final_list)} Einträge")
    print(f"  Gelöscht: {len(final_remove)} Einträge")
    
    return final_list

# ============================== MAIN EXECUTION ==============================

def main():
    print_header("🧹 WINDOWS PATH-REINIGER (PYTHON-VERSION)")
    print("  Dieses Skript analysiert und bereinigt Ihre PATH-Umgebungsvariable.")
    print("  Es erstellt ein Backup, bevor Änderungen vorgenommen werden.\n")

    backup_dir = get_backup_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = backup_dir / f"PATH_BACKUP_{timestamp}.txt"

    sys_paths, sys_type = read_path_from_reg(
        winreg.HKEY_LOCAL_MACHINE,
        r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
    )
    usr_paths, usr_type = read_path_from_reg(
        winreg.HKEY_CURRENT_USER,
        "Environment"
    )

    # Backup speichern
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(f"=== SYSTEM PATH (Typ: {sys_type}) ===\n")
        f.write(';'.join(sys_paths) if sys_paths else "(leer)")
        f.write("\n\n=== USER PATH (Typ: {usr_type}) ===\n")
        f.write(';'.join(usr_paths) if usr_paths else "(leer)")
    print(f"  📁 Backup gespeichert unter: {backup_file}")

    print_header("🖥️  SYSTEM-PATH (HKLM) – BETRIFFT ALLE BENUTZER", '=')
    new_sys_paths = interactive_clean(sys_paths, "System")

    print_header(f"👤 BENUTZER-PATH (HKCU) – BETRIFFT NUR {os.environ['USERNAME']}", '=')
    new_usr_paths = interactive_clean(usr_paths, "User")

    print_header("📊 GESAMT-ZUSAMMENFASSUNG", '=')
    print(f"  SYSTEM: {len(sys_paths)} → {len(new_sys_paths)} Einträge")
    print(f"  USER  : {len(usr_paths)} → {len(new_usr_paths)} Einträge")

    if len(sys_paths) == len(new_sys_paths) and len(usr_paths) == len(new_usr_paths):
        print("\n  ℹ️  Keine Änderungen vorgenommen – PATH bleibt unverändert.")
        return

    print("\n  ⏳ Änderungen dauerhaft in der Registry speichern?")
    confirm = input("     (j/n): ").strip().lower()
    if confirm != 'j':
        print("  ❌ Abbruch. Es wurde NICHTS verändert.")
        return

    success = True
    if not write_path_to_reg(
        winreg.HKEY_LOCAL_MACHINE,
        r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
        new_sys_paths,
        sys_type
    ):
        success = False
    else:
        print("  ✅ System-PATH aktualisiert.")

    if not write_path_to_reg(
        winreg.HKEY_CURRENT_USER,
        "Environment",
        new_usr_paths,
        usr_type
    ):
        success = False
    else:
        print("  ✅ Benutzer-PATH aktualisiert.")

    if success:
        notify_environment_change()
        print_header("🎉 FERTIG!", '=')
        print("  Windows wurde benachrichtigt.")
        print("  Bitte starte alle geöffneten Konsolen (CMD, PowerShell) NEU.")
        print("  Ein Neustart des PCs ist NICHT erforderlich.")
    else:
        print("\n  ⚠️  Es gab Fehler beim Schreiben – bitte prüfe die Registry manuell.")

# ============================== PROGRAM START ==============================

if __name__ == "__main__":
    main()