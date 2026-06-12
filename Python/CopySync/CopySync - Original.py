#!/usr/bin/env python
# -*- coding: utf-8 -*-
# CopySync - Original.py

import os
import sys
import csv
import shutil
import hashlib
import time
from pathlib import Path

# ============================================================================
# KONFIGURATION - HIER IHRE PFADE EINTRAGEN
# ============================================================================

SOURCE_DRIVE = r"F:\\"                    # Festplatte A (Quelle)
TARGET_DRIVE = r"E:\\"                	  # Festplatte B (Ziel)
CHECK_CSV = "CheckComplete.csv"           # Ergebnis-Datei
LOG_FILE = "BackupAutomationLog.txt"      # Logdatei

# Optionale Einstellungen
USE_HASH_COMPARISON = False               # Hash-Vergleich aktivieren? -> False = schnell, True = gründlich (langsam)
EXCLUDE_ITEMS = [                         # Zu ignorierende Elemente
    '$RECYCLE.BIN',
    'System Volume Information',
    '.Trash',
    '.Trashes',
    'Thumbs.db',
    'desktop.ini'
]

# ============================================================================
# HILFSFUNKTIONEN
# ============================================================================

def log_message(message, print_also=True):
    """Schreibt Nachricht in Logdatei"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    
    with open(LOG_FILE, 'a', encoding='utf-8') as log:
        log.write(log_entry + "\n")
    
    if print_also:
        print(message)

def get_file_hash(file_path, buffer_size=65536):
    """Berechnet SHA-256 Hash einer Datei"""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(buffer_size)
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()
    except Exception:
        return None

def print_header(title):
    """Gibt einen schönen Header aus"""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

# ============================================================================
# SCHRITT 1: KOMPLETTEN VERGLEICH DURCHFÜHREN
# ============================================================================

def perform_complete_comparison():
    """Vergleicht alle Dateien und Ordner, gibt fehlende zurück"""
    
    print_header("SCHRITT 1: VERGLEICHE ALLE DATEIEN UND ORDNER")
    log_message("START: Kompletter Vergleich")
    
    source_path = Path(SOURCE_DRIVE)
    target_path = Path(TARGET_DRIVE)
    
    if not source_path.exists():
        log_message(f"❌ FEHLER: Quellpfad existiert nicht: {SOURCE_DRIVE}")
        return []
    
    if not target_path.exists():
        log_message(f"❌ FEHLER: Zielpfad existiert nicht: {TARGET_DRIVE}")
        return []
    
    missing_items = []
    total_scanned = 0
    start_time = time.time()
    
    log_message(f"Quelle: {SOURCE_DRIVE}")
    log_message(f"Ziel:   {TARGET_DRIVE}")
    log_message(f"Hash-Vergleich: {'JA' if USE_HASH_COMPARISON else 'NEIN'}")
    
    print(f"Scanne Quellverzeichnis...")
    
    # Durchsuche alle Dateien und Ordner
    for root, dirs, files in os.walk(SOURCE_DRIVE):
        # Ignoriere unerwünschte Verzeichnisse
        dirs[:] = [d for d in dirs if d not in EXCLUDE_ITEMS]
        
        current_path = Path(root)
        relative_path = current_path.relative_to(source_path)
        
        # Prüfe Verzeichnisse
        for dir_name in dirs:
            if dir_name in EXCLUDE_ITEMS:
                continue
                
            source_dir = source_path / relative_path / dir_name
            target_dir = target_path / relative_path / dir_name
            
            if not target_dir.exists():
                missing_items.append({
                    'type': 'directory',
                    'path': str(relative_path / dir_name),
                    'source_path': str(source_dir),
                    'target_path': str(target_dir),
                    'reason': 'Verzeichnis fehlt'
                })
            
            total_scanned += 1
        
        # Prüfe Dateien
        for file_name in files:
            if file_name in EXCLUDE_ITEMS:
                continue
            
            source_file = source_path / relative_path / file_name
            target_file = target_path / relative_path / file_name
            
            # Datei existiert nicht im Ziel
            if not target_file.exists():
                missing_items.append({
                    'type': 'file',
                    'path': str(relative_path / file_name),
                    'source_path': str(source_file),
                    'target_path': str(target_file),
                    'reason': 'Datei fehlt',
                    'size': os.path.getsize(source_file) if source_file.exists() else 0
                })
                total_scanned += 1
                continue
            
            # Größenvergleich
            try:
                source_size = os.path.getsize(source_file)
                target_size = os.path.getsize(target_file)
                
                if source_size != target_size:
                    missing_items.append({
                        'type': 'file',
                        'path': str(relative_path / file_name),
                        'source_path': str(source_file),
                        'target_path': str(target_file),
                        'reason': f'Unterschiedliche Größe ({source_size} vs {target_size} Bytes)',
                        'size': source_size
                    })
                
                # Hash-Vergleich (falls aktiviert)
                elif USE_HASH_COMPARISON:
                    source_hash = get_file_hash(source_file)
                    target_hash = get_file_hash(target_file)
                    
                    if source_hash and target_hash and source_hash != target_hash:
                        missing_items.append({
                            'type': 'file',
                            'path': str(relative_path / file_name),
                            'source_path': str(source_file),
                            'target_path': str(target_file),
                            'reason': 'Unterschiedlicher Inhalt (Hash)',
                            'size': source_size
                        })
            
            except Exception as e:
                missing_items.append({
                    'type': 'file',
                    'path': str(relative_path / file_name),
                    'source_path': str(source_file),
                    'target_path': str(target_file),
                    'reason': f'Fehler beim Vergleich: {str(e)}',
                    'size': 0
                })
            
            total_scanned += 1
            
            # Fortschrittsanzeige
            if total_scanned % 1000 == 0:
                elapsed = time.time() - start_time
                elapsed_str = time.strftime('%H:%M:%S', time.gmtime(elapsed))
                print(f"\rGescannt: {total_scanned} | Fehlend: {len(missing_items)} | Zeit: {elapsed_str}", end="")
    
    # Ergebnis anzeigen
    elapsed = time.time() - start_time
    elapsed_str = time.strftime('%H:%M:%S', time.gmtime(elapsed))
    
    print(f"\r{' '*80}")
    print(f"\nVergleich abgeschlossen!")
    print(f"Gescannte Elemente: {total_scanned}")
    print(f"Fehlende/fehlerhafte Elemente: {len(missing_items)}")
    print(f"Benötigte Zeit: {elapsed_str}")
    
    log_message(f"Vergleich abgeschlossen: {total_scanned} Elemente gescannt, {len(missing_items)} Probleme gefunden")
    
    return missing_items

# ============================================================================
# SCHRITT 2: FEHLENDE ELEMENTE KOPIEREN
# ============================================================================

def copy_missing_items(missing_items):
    """Kopiert alle fehlenden Dateien und erstellt fehlende Ordner"""
    
    if not missing_items:
        print("\n✓ Keine fehlenden Elemente gefunden - nichts zu kopieren.")
        log_message("Keine fehlenden Elemente - Kopierschritt übersprungen")
        return True
    
    print_header("SCHRITT 2: KOPIERE FEHLENDE ELEMENTE")
    log_message(f"START: Kopiere {len(missing_items)} fehlende Elemente")
    
    stats = {
        'directories_created': 0,
        'files_copied': 0,
        'files_skipped': 0,
        'total_bytes': 0,
        'errors': 0,
        'start_time': time.time()
    }
    
    # Zuerst alle fehlenden Verzeichnisse erstellen
    print("Erstelle fehlende Verzeichnisse...")
    directories = [item for item in missing_items if item['type'] == 'directory']
    
    for i, item in enumerate(directories, 1):
        try:
            target_dir = Path(item['target_path'])
            target_dir.mkdir(parents=True, exist_ok=True)
            stats['directories_created'] += 1
            
            print(f"\rVerzeichnisse: {i}/{len(directories)}", end="")
            log_message(f"Verzeichnis erstellt: {item['path']}")
        
        except Exception as e:
            stats['errors'] += 1
            log_message(f"❌ Fehler beim Erstellen von {item['path']}: {str(e)}")
    
    if directories:
        print()  # Neue Zeile
    
    # Dann alle fehlenden Dateien kopieren
    files = [item for item in missing_items if item['type'] == 'file']
    
    if files:
        print(f"Kopiere {len(files)} fehlende Dateien...")
        
        for i, item in enumerate(files, 1):
            try:
                source_file = Path(item['source_path'])
                target_file = Path(item['target_path'])
                
                # Prüfen ob Quelle existiert
                if not source_file.exists():
                    log_message(f"⚠️ Quelle existiert nicht: {item['path']}")
                    stats['files_skipped'] += 1
                    continue
                
                # Zielverzeichnis sicherstellen
                target_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Datei kopieren
                file_size = os.path.getsize(source_file)
                shutil.copy2(source_file, target_file)
                
                stats['files_copied'] += 1
                stats['total_bytes'] += file_size
                
                # Fortschrittsanzeige
                if i % 10 == 0 or i == len(files):
                    elapsed = time.time() - stats['start_time']
                    percent = (i / len(files)) * 100
                    speed = stats['total_bytes'] / elapsed / 1024 / 1024 if elapsed > 0 else 0
                    
                    print(f"\rDateien: {i}/{len(files)} ({percent:.1f}%) | "
                          f"{stats['total_bytes']/1024**3:.2f} GB | "
                          f"{speed:.1f} MB/s", end="")
                
                log_message(f"Datei kopiert: {item['path']} ({file_size} Bytes)")
            
            except Exception as e:
                stats['errors'] += 1
                log_message(f"❌ Fehler beim Kopieren von {item['path']}: {str(e)}")
        
        print()  # Neue Zeile
    
    # Statistik anzeigen
    elapsed = time.time() - stats['start_time']
    elapsed_str = time.strftime('%H:%M:%S', time.gmtime(elapsed))
    
    print_header("KOPIER-STATISTIK")
    print(f"Benötigte Zeit:          {elapsed_str}")
    print(f"Erstellte Verzeichnisse: {stats['directories_created']}")
    print(f"Kopierte Dateien:        {stats['files_copied']}")
    print(f"Übersprungene Dateien:   {stats['files_skipped']}")
    print(f"Gesamtkopierte Daten:    {stats['total_bytes']/1024**3:.2f} GB")
    
    if elapsed > 0 and stats['files_copied'] > 0:
        avg_speed = stats['total_bytes'] / elapsed / 1024 / 1024
        print(f"Durchschnittsgeschw.:    {avg_speed:.1f} MB/s")
    
    print(f"Fehler:                  {stats['errors']}")
    
    log_message(f"Kopieren abgeschlossen: {stats['files_copied']} Dateien, "
                f"{stats['directories_created']} Verzeichnisse, "
                f"{stats['errors']} Fehler")
    
    return stats['errors'] == 0

# ============================================================================
# SCHRITT 3: ABSCHLIESSENDER VERGLEICH
# ============================================================================

def perform_final_check():
    """Führt abschließenden Vergleich durch um sicherzustellen dass alles kopiert wurde"""
    
    print_header("SCHRITT 3: ABSCHLIESSENDER KOMPLETT-CHECK")
    log_message("START: Abschließender Komplett-Check")
    
    # Kurzen Vergleich durchführen (nur auf fehlende Elemente prüfen)
    source_path = Path(SOURCE_DRIVE)
    target_path = Path(TARGET_DRIVE)
    
    remaining_issues = []
    checked_items = 0
    start_time = time.time()
    
    print("Prüfe ob alle Elemente vorhanden sind...")
    
    for root, dirs, files in os.walk(SOURCE_DRIVE):
        # Ignoriere unerwünschte Verzeichnisse
        dirs[:] = [d for d in dirs if d not in EXCLUDE_ITEMS]
        
        current_path = Path(root)
        relative_path = current_path.relative_to(source_path)
        
        # Verzeichnisse prüfen
        for dir_name in dirs:
            if dir_name in EXCLUDE_ITEMS:
                continue
                
            target_dir = target_path / relative_path / dir_name
            if not target_dir.exists():
                remaining_issues.append(f"Verzeichnis fehlt: {relative_path / dir_name}")
            
            checked_items += 1
        
        # Dateien prüfen
        for file_name in files:
            if file_name in EXCLUDE_ITEMS:
                continue
            
            target_file = target_path / relative_path / file_name
            if not target_file.exists():
                remaining_issues.append(f"Datei fehlt: {relative_path / file_name}")
            
            checked_items += 1
            
            # Fortschrittsanzeige
            if checked_items % 1000 == 0:
                elapsed = time.time() - start_time
                print(f"\rGeprüft: {checked_items} | Noch fehlend: {len(remaining_issues)}", end="")
    
    # Ergebnis
    elapsed = time.time() - start_time
    elapsed_str = time.strftime('%H:%M:%S', time.gmtime(elapsed))
    
    print(f"\r{' '*80}")
    
    if not remaining_issues:
        print(f"\n✅ HERZLICHEN GLÜCKWUNSCH!")
        print(f"✅ Alle {checked_items} Elemente wurden erfolgreich kopiert!")
        print(f"✅ Backup ist komplett und konsistent!")
        print(f"✅ Prüfzeit: {elapsed_str}")
        
        log_message(f"✅ ABSCHLIEßENDER CHECK BESTANDEN: Alle {checked_items} Elemente vorhanden")
        return True
    
    else:
        print(f"\n⚠️  WARNUNG: Es fehlen noch {len(remaining_issues)} Elemente!")
        print(f"⚠️  Geprüfte Elemente: {checked_items}")
        print(f"⚠️  Prüfzeit: {elapsed_str}")
        
        print("\nFehlende Elemente:")
        for issue in remaining_issues[:20]:  # Zeige nur die ersten 20
            print(f"  • {issue}")
        
        if len(remaining_issues) > 20:
            print(f"  ... und {len(remaining_issues) - 20} weitere")
        
        log_message(f"⚠️  ABSCHLIEßENDER CHECK FEHLGESCHLAGEN: {len(remaining_issues)} Elemente fehlen")
        
        # Fehlende Elemente in Datei speichern
        with open("remaining_issues.txt", 'w', encoding='utf-8') as f:
            f.write(f"Fehlende Elemente nach Backup - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            for issue in remaining_issues:
                f.write(f"{issue}\n")
        
        print(f"\nℹ️  Liste der fehlenden Elemente gespeichert in: remaining_issues.txt")
        
        return False

# ============================================================================
# SCHRITT 4: ERGEBNISSE SPEICHERN UND REPORT ERSTELLEN
# ============================================================================

def save_results_and_report(missing_items, success):
    """Speichert Ergebnisse und erstellt Report"""
    
    print_header("SCHRITT 4: ERSTELLE REPORT")
    
    # 1. CSV-Datei mit allen gefundenen Problemen
    if missing_items:
        with open(CHECK_CSV, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['type', 'path', 'reason', 'size', 'source_path', 'target_path']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(missing_items)
        
        print(f"✓ Detailierte Liste gespeichert als: {CHECK_CSV}")
    
    # 2. Zusammenfassung erstellen
    summary_file = "Backup_Summary.txt"
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("BACKUP-AUTOMATISIERUNG - ZUSAMMENFASSUNG\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"Zeitpunkt:               {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Quelle:                  {SOURCE_DRIVE}\n")
        f.write(f"Ziel:                    {TARGET_DRIVE}\n")
        f.write(f"Hash-Vergleich:          {'JA' if USE_HASH_COMPARISON else 'NEIN'}\n\n")
        
        f.write("ERGEBNISSE:\n")
        f.write("-"*40 + "\n")
        
        if not missing_items:
            f.write("✅ Keine Probleme gefunden - Backup war bereits komplett!\n")
        else:
            dirs_count = sum(1 for item in missing_items if item['type'] == 'directory')
            files_count = sum(1 for item in missing_items if item['type'] == 'file')
            
            f.write(f"Gefundene Probleme:       {len(missing_items)}\n")
            f.write(f"  • Fehlende Verzeichnisse: {dirs_count}\n")
            f.write(f"  • Fehlende/fehlerhafte Dateien: {files_count}\n\n")
            
            if success:
                f.write("✅ Alle fehlenden Elemente wurden erfolgreich kopiert!\n")
                f.write("✅ Abschließender Check bestanden!\n")
            else:
                f.write("⚠️  Einige Elemente konnten nicht kopiert werden.\n")
                f.write("⚠️  Bitte prüfen Sie die Logdatei für Details.\n")
        
        f.write("\nDATEIEN:\n")
        f.write("-"*40 + "\n")
        f.write(f"Detailierte CSV-Liste:    {CHECK_CSV}\n")
        f.write(f"Logdatei:                 {LOG_FILE}\n")
        f.write(f"Zusammenfassung:          {summary_file}\n")
        
        if os.path.exists("remaining_issues.txt"):
            f.write(f"Fehlende Elemente:        remaining_issues.txt\n")
    
    print(f"✓ Zusammenfassung gespeichert als: {summary_file}")
    print(f"✓ Logdatei: {LOG_FILE}")

# ============================================================================
# HAUPTFUNKTION - ABLAUFSTEUERUNG
# ============================================================================

def main():
    """Hauptfunktion - steuert den gesamten Ablauf"""
    
    # Logdatei initialisieren
    if os.path.exists(LOG_FILE):
        # Alte Logdatei umbenennen
        old_log = f"{LOG_FILE}.{time.strftime('%Y%m%d_%H%M%S')}.bak"
        os.rename(LOG_FILE, old_log)
        log_message(f"Alte Logdatei umbenannt zu: {old_log}", print_also=False)
    
    print_header("BACKUP-AUTOMATISIERUNG STARTET")
    print(f"Quelle:      {SOURCE_DRIVE}")
    print(f"Ziel:        {TARGET_DRIVE}")
    print(f"Hash-Check:  {'Aktiviert' if USE_HASH_COMPARISON else 'Deaktiviert'}")
    print(f"Logdatei:    {LOG_FILE}")
    print("="*70)
    
    total_start_time = time.time()
    
    try:
        # Schritt 1: Kompletter Vergleich
        missing_items = perform_complete_comparison()
        
        if not missing_items:
            # Alles ist bereits in Ordnung
            print("\n" + "✅" * 35)
            print("✅ ALLES BEREITS VOLLSTÄNDIG - NICHTS ZU TUN!")
            print("✅" * 35)
            
            success = True
        else:
            # Schritt 2: Fehlende Elemente kopieren
            copy_success = copy_missing_items(missing_items)
            
            # Schritt 3: Abschließender Check
            final_check_success = perform_final_check()
            
            success = copy_success and final_check_success
        
        # Schritt 4: Report erstellen
        save_results_and_report(missing_items, success)
        
    except KeyboardInterrupt:
        log_message("❌ ABGEBROCHEN durch Benutzer (Ctrl+C)")
        print("\n\n❌ Vorgang wurde durch Benutzer abgebrochen!")
        success = False
    
    except Exception as e:
        log_message(f"❌ UNBEKANNTER FEHLER: {str(e)}")
        print(f"\n\n❌ Ein unerwarteter Fehler ist aufgetreten: {e}")
        success = False
    
    # Gesamtstatistik
    total_time = time.time() - total_start_time
    total_time_str = time.strftime('%H:%M:%S', time.gmtime(total_time))
    
    print_header("GESAMT-ZUSAMMENFASSUNG")
    print(f"Gesamtzeit:        {total_time_str}")
    print(f"Erfolg:            {'✅ JA' if success else '❌ NEIN'}")
    print(f"Logdatei:          {LOG_FILE}")
    
    if success:
        print("\n" + "🎉" * 35)
        print("🎉 BACKUP-AUTOMATISIERUNG ERFOLGREICH ABGESCHLOSSEN!")
        print("🎉" * 35)
    else:
        print("\n" + "⚠️ " * 18)
        print("⚠️  BACKUP-AUTOMATISIERUNG MIT PROBLEMEN ABGESCHLOSSEN")
        print("⚠️ " * 18)
        print("\nBitte prüfen Sie die Logdatei für Details!")
    
    # Warten bevor das Fenster sich schließt (wenn nicht in Konsole)
    input("\nDrücken Sie Enter um das Programm zu beenden...")

# ============================================================================
# PROGRAMMSTART
# ============================================================================

if __name__ == "__main__":
    main()
