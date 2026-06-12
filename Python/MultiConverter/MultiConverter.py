#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MultiConverter.py

# Import required system modules
import os
import subprocess
import sys
import shutil

def main():
    # ======== 1. Header ========
    # Display program title with decorative lines (exact batch-style output)
    print("============================================================================")
    print("                         MultiConverter (ffmpeg)")
    print("============================================================================")
    
    # ======== 2. Folder selection ========
    # Start with current working directory
    current_dir = os.getcwd()
    print(f"Aktueller Ordner: {current_dir}")
    print("---------------------------------------------------------------")
    # Ask user if a different folder should be used
    use_other = input("Mochtest du einen anderen Ordner? (J/N): ").strip()
    if use_other.upper() == "J":
        new_dir = input("Pfad eingeben: ").strip()
        if new_dir:
            current_dir = new_dir
    # Attempt to change to the specified directory
    try:
        os.chdir(current_dir)
    except FileNotFoundError:
        # Folder does not exist -> show error and exit
        print("----------------------------------------------------------------------------")
        print("                     [FEHLER] Ordner nicht gefunden!")
        print("----------------------------------------------------------------------------")
        input("Drücke Enter zum Beenden...")
        sys.exit(1)
    
    # ======== 3. List files and select ========
    # Show file selection menu
    print("============================================================================")
    print("                          Dateien auswahlen")
    print("============================================================================")
    print("Auswahlmoglichkeiten: [A]lle  [1]  [1,3]  [1-3]  oder [1-3,5,7-9]")
    print("-----------------------------------------------------------------")
    
    # List all files (excluding subdirectories) and sort alphabetically
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    files.sort()
    
    # If no files are found, abort
    if not files:
        print("----------------------------------------------------------------------------")
        print("                  [ACHTUNG] Keine Dateien gefunden!")
        print("----------------------------------------------------------------------------")
        input("Drücke Enter zum Beenden...")
        sys.exit(1)
    
    # Display numbered list of files (1-based as in batch script)
    for idx, fname in enumerate(files, start=1):
        print(f"  [{idx}] {fname}")
    
    print("-----------------------------------------------------------------")
    sel_input = input("Deine Auswahl: ").strip()
    print("--------------------------------")
    
    # Parse user selection (supports "A", single numbers, comma lists, ranges, mixed)
    selected_indices = parse_selection(sel_input, len(files))
    if not selected_indices:
        # No valid selection -> error and exit
        print("----------------------------------------------------------------------------")
        print("                   [FEHLER] Keine gultige Auswahl!")
        print("----------------------------------------------------------------------------")
        input("Drücke Enter zum Beenden...")
        sys.exit(1)
    
    # Build list of selected file names from indices (convert to 0‑based)
    selected_files = [files[i] for i in selected_indices]
    print("Ausgewahlte Dateien:")
    for f in selected_files:
        print(f"  - {f}")
    
    # ======== 4. Target format ========
    # Show format selection menu
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
    
    # Map number to file extension (same as batch if-cascade)
    format_map = {
        "1":"png","2":"jpg","3":"jpeg","4":"gif","5":"bmp","6":"tiff","7":"webp","8":"heic",
        "9":"mp4","10":"webm","11":"avi","12":"mkv","13":"mov","14":"flv",
        "15":"mp3","16":"wav","17":"ogg","18":"flac","19":"aac","20":"m4a"
    }
    target_format = format_map.get(format_num)
    if not target_format:
        # Invalid number -> error and exit
        print("----------------------------------------------------------------------------")
        print("                      [FEHLER] Ungultige Nummer!")
        print("----------------------------------------------------------------------------")
        input("Drücke Enter zum Beenden...")
        sys.exit(1)
    
    print(f"Gewahltes Format: {target_format}")
    print("------------------------")
    
    # ======== 5. Check ffmpeg ========
    # Check if ffmpeg is available in PATH
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
    
    # Iterate over all selected files
    for input_file in selected_files:
        # Build output filename by replacing extension with target format
        name, _ = os.path.splitext(input_file)
        output_file = f"{name}.{target_format}"
        print(f"[>>] {input_file} --> {output_file}")
        
        # Choose conversion function based on target format category
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
    # Final summary and pause
    print("============================================================================")
    print("                       Konvertierung abgeschlossen!")
    print("============================================================================")
    print(f"Erfolgreich: {success}")
    print(f"Fehlgeschlagen: {failed}")
    print("------------------------")
    input("Drücke Enter zum Beenden...")

def parse_selection(sel, max_count):
    """Convert user input (A, 1, 1,3, 1-3, 1-3,5,7-9) into list of 0‑based indices."""
    # Case "A" -> select all files
    if sel.strip().upper() == "A":
        return list(range(max_count))
    # Normalize: remove spaces, replace semicolons with commas
    sel = sel.replace(" ", "").replace(";", ",")
    indices = set()
    # Process each comma-separated part
    for part in sel.split(","):
        if not part:
            continue
        if "-" in part:
            # Handle range like "3-7"
            try:
                start, end = map(int, part.split("-"))
                if start > end:
                    start, end = end, start
                # Add all numbers from start to end (inclusive)
                for i in range(start, end+1):
                    if 1 <= i <= max_count:
                        indices.add(i-1)      # convert to 0‑based
            except:
                continue
        else:
            # Handle single number
            try:
                i = int(part)
                if 1 <= i <= max_count:
                    indices.add(i-1)
            except:
                continue
    return sorted(indices)

def run_ffmpeg(cmd_args, infile, outfile):
    """Execute ffmpeg with given extra arguments, suppress output, return success."""
    cmd = ["ffmpeg", "-i", infile] + cmd_args + ["-y", outfile]
    # Run silently (stdout/stderr redirected) as batch does with 2>nul
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Success if output file exists (same logic as batch "if exist")
    return os.path.exists(outfile)

def convert_image(infile, outfile):
    """Simple image conversion without extra codec flags."""
    return run_ffmpeg([], infile, outfile)

def convert_video(infile, outfile):
    """Try stream copy first (fast), fall back to full re-encode if that fails."""
    if run_ffmpeg(["-c", "copy"], infile, outfile):
        return True
    # Fallback: re-encode video (slower but more compatible)
    return run_ffmpeg([], infile, outfile)

def convert_audio(infile, outfile, fmt):
    """Audio conversion: for MP3 try libmp3lame first, otherwise standard."""
    if fmt == "mp3":
        # First attempt with explicit MP3 encoder
        if run_ffmpeg(["-vn", "-acodec", "libmp3lame"], infile, outfile):
            return True
        # Fallback without codec specification
        return run_ffmpeg(["-vn"], infile, outfile)
    else:
        # For other audio formats (wav, flac, ogg, aac, m4a) just strip video track
        return run_ffmpeg(["-vn"], infile, outfile)

if __name__ == "__main__":
    main()