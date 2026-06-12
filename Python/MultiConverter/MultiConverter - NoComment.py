#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MultiConverter - NoComment.py

import os
import subprocess
import sys
import shutil

def main():
    # ======== 1. Header ========
    print("============================================================================")
    print("                         MultiConverter (ffmpeg)")
    print("============================================================================")
    
    # ======== 2. Folder selection ========
    current_dir = os.getcwd()
    print(f"Aktueller Ordner: {current_dir}")
    print("---------------------------------------------------------------")
    use_other = input("Mochtest du einen anderen Ordner? (J/N): ").strip()
    if use_other.upper() == "J":
        new_dir = input("Pfad eingeben: ").strip()
        if new_dir:
            current_dir = new_dir
    try:
        os.chdir(current_dir)
    except FileNotFoundError:
        print("----------------------------------------------------------------------------")
        print("                     [FEHLER] Ordner nicht gefunden!")
        print("----------------------------------------------------------------------------")
        input("Drücke Enter zum Beenden...")
        sys.exit(1)
    
    # ======== 3. List files and select ========
    print("============================================================================")
    print("                          Dateien auswahlen")
    print("============================================================================")
    print("Auswahlmoglichkeiten: [A]lle  [1]  [1,3]  [1-3]  oder [1-3,5,7-9]")
    print("-----------------------------------------------------------------")
    
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    files.sort()
    
    if not files:
        print("----------------------------------------------------------------------------")
        print("                  [ACHTUNG] Keine Dateien gefunden!")
        print("----------------------------------------------------------------------------")
        input("Drücke Enter zum Beenden...")
        sys.exit(1)
    
    for idx, fname in enumerate(files, start=1):
        print(f"  [{idx}] {fname}")
    
    print("-----------------------------------------------------------------")
    sel_input = input("Deine Auswahl: ").strip()
    print("--------------------------------")
    
    selected_indices = parse_selection(sel_input, len(files))
    if not selected_indices:
        print("----------------------------------------------------------------------------")
        print("                   [FEHLER] Keine gultige Auswahl!")
        print("----------------------------------------------------------------------------")
        input("Drücke Enter zum Beenden...")
        sys.exit(1)
    
    selected_files = [files[i] for i in selected_indices]
    print("Ausgewahlte Dateien:")
    for f in selected_files:
        print(f"  - {f}")
    
    # ======== 4. Target format ========
    print("============================================================================")
    print("                        Zielformat auswahlen")
    print("============================================================================")
    print("  Bild-Formate:    [1] png     [2] jpg     [3] jpeg    [4] gif")
    print("                   [5] bmp     [6] tiff    [7] webp    [8] heic")
    print("  Video-Formate:   [9] mp4     [10] webm   [11] avi    [12] mkv")
    print("                   [13] mov    [14] flv")
    print("  Audio-Formate:   [15] mp3    [16] wav    [17] ogg    [18] flac")
    print("                   [19] aac    [20] m4a")
    print("---------------------------------------------------------------")
    
    format_num = input("Format-Nummer (1-20): ").strip()
    print("------------------------")
    
    format_map = {
        "1":"png","2":"jpg","3":"jpeg","4":"gif","5":"bmp","6":"tiff","7":"webp","8":"heic",
        "9":"mp4","10":"webm","11":"avi","12":"mkv","13":"mov","14":"flv",
        "15":"mp3","16":"wav","17":"ogg","18":"flac","19":"aac","20":"m4a"
    }
    target_format = format_map.get(format_num)
    if not target_format:
        print("----------------------------------------------------------------------------")
        print("                      [FEHLER] Ungultige Nummer!")
        print("----------------------------------------------------------------------------")
        input("Drücke Enter zum Beenden...")
        sys.exit(1)
    
    print(f"Gewahltes Format: {target_format}")
    print("------------------------")
    
    # ======== 5. Check ffmpeg ========
    if not shutil.which("ffmpeg"):
        print("----------------------------------------------------------------------------")
        print("                     [FEHLER] ffmpeg nicht gefunden!")
        print("----------------------------------------------------------------------------")
        print("Bitte installiere ffmpeg: https://ffmpeg.org/download.html")
        input("Drücke Enter zum Beenden...")
        sys.exit(1)
    
    # ======== 6. Conversion ========
    print("============================================================================")
    print("                         Konvertierung lauft...")
    print("============================================================================")
    
    success = 0
    failed = 0
    
    for input_file in selected_files:
        name, _ = os.path.splitext(input_file)
        output_file = f"{name}.{target_format}"
        print(f"[>>] {input_file} --> {output_file}")
        
        if target_format in {"png","jpg","jpeg","gif","bmp","tiff","webp","heic"}:
            ok = convert_image(input_file, output_file)
        elif target_format in {"mp4","webm","avi","mkv","mov","flv"}:
            ok = convert_video(input_file, output_file)
        elif target_format in {"mp3","wav","ogg","flac","aac","m4a"}:
            ok = convert_audio(input_file, output_file, target_format)
        else:
            ok = False
        
        if ok:
            print(f"  [OK] {output_file}")
            success += 1
        else:
            print(f"  [FAIL] {input_file}")
            failed += 1
    
    # ======== 7. Final ========
    print("============================================================================")
    print("                       Konvertierung abgeschlossen!")
    print("============================================================================")
    print(f"Erfolgreich: {success}")
    print(f"Fehlgeschlagen: {failed}")
    print("------------------------")
    input("Drücke Enter zum Beenden...")

def parse_selection(sel, max_count):
    if sel.strip().upper() == "A":
        return list(range(max_count))
    sel = sel.replace(" ", "").replace(";", ",")
    indices = set()
    for part in sel.split(","):
        if not part:
            continue
        if "-" in part:
            try:
                start, end = map(int, part.split("-"))
                if start > end:
                    start, end = end, start
                for i in range(start, end+1):
                    if 1 <= i <= max_count:
                        indices.add(i-1)
            except:
                continue
        else:
            try:
                i = int(part)
                if 1 <= i <= max_count:
                    indices.add(i-1)
            except:
                continue
    return sorted(indices)

def run_ffmpeg(cmd_args, infile, outfile):
    cmd = ["ffmpeg", "-i", infile] + cmd_args + ["-y", outfile]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return os.path.exists(outfile)

def convert_image(infile, outfile):
    return run_ffmpeg([], infile, outfile)

def convert_video(infile, outfile):
    if run_ffmpeg(["-c", "copy"], infile, outfile):
        return True
    return run_ffmpeg([], infile, outfile)

def convert_audio(infile, outfile, fmt):
    if fmt == "mp3":
        if run_ffmpeg(["-vn", "-acodec", "libmp3lame"], infile, outfile):
            return True
        return run_ffmpeg(["-vn"], infile, outfile)
    else:
        return run_ffmpeg(["-vn"], infile, outfile)

if __name__ == "__main__":
    main()