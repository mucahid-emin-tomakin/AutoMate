#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import shutil
import time
import re
from pathlib import Path

# ==================================================
#  KONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).parent.absolute()
MP3_DIR = BASE_DIR / "MP3"
MP4_DIR = BASE_DIR / "MP4"
ARCHIVE_MP3 = BASE_DIR / "ArchiveMP3.txt"
ARCHIVE_MP4 = BASE_DIR / "ArchiveMP4.txt"
LIST_MP3 = BASE_DIR / "ListMP3.txt"
LIST_MP4 = BASE_DIR / "ListMP4.txt"
COOKIE_FILE = BASE_DIR / "cookies.txt"

# ==================================================
#  HILFSFUNKTIONEN
# ==================================================

def find_program(name):
    """Prüft, ob ein Programm (yt-dlp, ffmpeg, deno) im PATH oder im Skriptordner existiert."""
    if shutil.which(name):
        return shutil.which(name)
    local_exe = BASE_DIR / f"{name}.exe"
    return str(local_exe) if local_exe.exists() else None
def collect_expected_ids(ytdlp, input_file):
    """
    Liest die URLs aus input_file, expandiert Playlists und sammelt alle Video-IDs.
    Gibt eine Liste der IDs zurück.
    """
    if not input_file.exists():
        print(f"Fehler: Listendatei {input_file} nicht gefunden")
        return []
    with open(input_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]
    expected_ids = []
    for url in urls:
        cmd = [ytdlp, "--flat-playlist", "--print", "id", url]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=60)
            ids = [line.strip() for line in result.stdout.splitlines() if line.strip()]
            if not ids:
                print(f"Warnung: Keine IDs für {url} gefunden.")
            expected_ids.extend(ids)
            print(f"  → {len(ids)} IDs extrahiert")
        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Extrahieren von {url}: {e}")
        except subprocess.TimeoutExpired:
            print(f"Zeitüberschreitung bei {url}")
    return expected_ids
def get_archive_ids(archive_file):
    """Liest die Archivdatei und gibt die Liste der Video-IDs zurück."""
    if not archive_file.exists():
        return []
    with open(archive_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    ids = []
    for line in lines:
        parts = line.split()
        if parts:
            ids.append(parts[-1])
    return ids
def check_completeness(expected_ids, archive_ids, output_dir, mode):
    """Prüft, ob alle erwarteten Videos vorhanden sind."""
    file_count = len(list(output_dir.glob("*.mp3"))) if mode == "MP3" else len(list(output_dir.glob("*.mp4")))
    expected_count = len(expected_ids)
    archived_count = len(archive_ids)
    missing_ids = set(expected_ids) - set(archive_ids)
    extra_archived = set(archive_ids) - set(expected_ids)

    print("\n" + "=" * 60)
    print("📊 VOLLSTÄNDIGKEITSPRÜFUNG")
    print("=" * 60)
    print(f"Erwartete Videos (laut Liste/Playlists): {expected_count}")
    print(f"Im Archiv verzeichnete Videos:          {archived_count}")
    print(f"Tatsächliche {mode}-Dateien im Ordner:   {file_count}")
    if missing_ids:
        print(f"\n❌ Fehlende Videos ({len(missing_ids)}):")
        for vid in list(missing_ids)[:10]:
            print(f"   - {vid}")
        if len(missing_ids) > 10:
            print(f"   ... und {len(missing_ids)-10} weitere.")
    else:
        print("\n✅ Alle erwarteten Videos wurden erfolgreich heruntergeladen!")
    if extra_archived:
        print(f"\n⚠️ Archiv enthält {len(extra_archived)} IDs, die nicht in der Liste erwartet wurden.")
    print("=" * 60)

# ==================================================
#  DYNAMISCHE 4‑ZEILEN‑ANZEIGE
# ==================================================

def dynamic_progress(process, mode_name):
    """Liest die Ausgabe von yt-dlp und zeigt eine sich aktualisierende 4‑Zeilen‑Oberfläche."""
    prog_re = re.compile(r'\[download\]\s+(\d+(?:\.\d+)?)%')
    dest_re = re.compile(r'\[ExtractAudio\] Destination:\s+(.+\.mp3)|\[Merger\] Merged into\s+(.+\.mp4)|\[download\] Destination:\s+(.+\.(?:mp3|mp4|webm))')
    current_percent = 0
    current_title = ""
    bar_len = 40
    mid = bar_len // 2
    sys.stdout.write("\033[?25l")
    try:
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if not line:
                continue
            line = line.rstrip()
            m = prog_re.search(line)
            if m:
                current_percent = round(float(m.group(1)))
            m = dest_re.search(line)
            if m:
                dest_path = m.group(1) or m.group(2) or m.group(3)
                if dest_path:
                    title = Path(dest_path).stem
                    current_title = title[:48] + "..." if len(title) > 51 else title
            # Balken zeichnen
            filled = int(current_percent / 99 * bar_len)
            left = []
            right = []
            for i in range(mid + 1):
                if i < filled:
                    left.append('=' if i != mid else '')
                else:
                    left.append(' ' if i != mid else '')
            for i in range(mid + 1, bar_len):
                if i < filled:
                    right.append('=')
                else:
                    right.append(' ')
            bar_chars = left + right
            while len(bar_chars) < bar_len:
                bar_chars.append(' ')
            bar = ''.join(bar_chars)
            sys.stdout.write("\033[1;1H\033[J")
            print("=" * 65)
            print(f"= Download: {current_percent:3}% I{bar}I 100%")
            print(f"= Title: {' ' * 3}{current_title}")
            print("=" * 65)
            sys.stdout.flush()
            time.sleep(0.2)
        # Finale Anzeige
        final_bar = ('=' * mid) + ('=' * (bar_len - mid - 1))
        sys.stdout.write("\033[1;1H\033[J")
        print("=" * 45)
        print(f"Download: 99% I{final_bar}I 100%")
        print(f"Aktuell: {' ' * 12}Fertig!")
        print("=" * 45)
    finally:
        sys.stdout.write("\033[?25h")

# ==================================================
#  HAUPTPROGRAMM
# ==================================================

def main():
    if sys.platform == "win32":
        subprocess.run("title YouTube Downloader - Vollständigkeitsprüfung", shell=True)

    # ==================================================
    #  Prüfen, ob yt-dlp und ffmpeg verfügbar sind
    # ==================================================

    ytdlp = find_program("yt-dlp")
    if not ytdlp:
        print("Fehler: yt-dlp nicht gefunden!")
        sys.exit(1)
    ffmpeg = find_program("ffmpeg")
    if not ffmpeg:
        print("Fehler: ffmpeg nicht gefunden!")
        sys.exit(1)
    if not find_program("deno"):
        print("Hinweis: Deno nicht gefunden (optional).")
        time.sleep(1)

    # ==================================================
    #  Cookie-Unterstützung
    # ==================================================

    cookie_args = ["--cookies", str(COOKIE_FILE)] if COOKIE_FILE.exists() else []

    # ==================================================
    #  Auswahl MP3 / MP4
    # ==================================================

    print("=" * 45)
    print("   YouTube Batch Downloader (MP3 oder MP4)")
    print("=" * 45)
    print("\nWähle das Format:")
    print("  1 - MP3 (nur Audio, beste Qualität)")
    print("  2 - MP4 (Video + Audio, beste Qualität)")
    choice = input("\nBitte 1 oder 2 eingeben: ").strip()
    if choice == "1":
        MODE = "MP3"
        LIST_FILE = LIST_MP3
        ARCHIVE_FILE = ARCHIVE_MP3
        OUTPUT_DIR = MP3_DIR
        FORMAT_OPTS = ["--extract-audio", "--audio-format", "mp3", "--audio-quality", "0",
                       "--format", "bestaudio[ext=m4a]/bestaudio"]
    elif choice == "2":
        MODE = "MP4"
        LIST_FILE = LIST_MP4
        ARCHIVE_FILE = ARCHIVE_MP4
        OUTPUT_DIR = MP4_DIR
        FORMAT_OPTS = ["--format", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                       "--merge-output-format", "mp4"]
    else:
        print("Ungültige Eingabe.")
        sys.exit(1)
    if not LIST_FILE.exists():
        print(f"Fehler: {LIST_FILE} nicht gefunden!")
        sys.exit(1)
    OUTPUT_DIR.mkdir(exist_ok=True)

    # ==================================================
    #  Vor dem Download: Sammle erwartete Video-IDs
    # ==================================================

    print("\n📋 Sammle alle erwarteten Video-IDs aus den URLs (Playlists werden aufgelöst)...")
    expected_ids = collect_expected_ids(ytdlp, LIST_FILE)
    print(f"✅ Insgesamt {len(expected_ids)} Videos werden erwartet.\n")
    if not expected_ids:
        print("Keine gültigen URLs gefunden.")
        sys.exit(1)

    # ==================================================
    #  Start des Downloads (mit dynamischer Anzeige)
    # ==================================================

    print("Starte Download (Playlists werden vollständig geladen)...")
    cmd = [
        ytdlp,
        "--ignore-errors",
        "--no-overwrites",
        "--continue",
        "--download-archive", str(ARCHIVE_FILE),
        # Kein --no-playlist → Playlists werden komplett geladen
        "--no-write-thumbnail",
        "--no-write-info-json",
        "--concurrent-fragments", "4",
        "--sleep-interval", "5",
        "--limit-rate", "1M",
        "--output", str(OUTPUT_DIR / "%(title)s.%(ext)s"),
        "--js-runtimes", "deno",
        "--batch-file", str(LIST_FILE)
    ] + FORMAT_OPTS + cookie_args

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True, encoding='utf-8', errors='replace', bufsize=1)
        dynamic_progress(process, MODE)
        process.wait()
        if process.returncode != 0:
            print(f"yt-dlp beendet mit Fehlercode {process.returncode}")
        else:
            print("Download erfolgreich beendet")
    except Exception as e:
        print(f"Fehler beim Starten von yt-dlp: {e}")
    finally:
        sys.stdout.write("\033[?25h")

    # ==================================================
    #  Vollständigkeitsprüfung nach dem Download
    # ==================================================

    archive_ids = get_archive_ids(ARCHIVE_FILE)
    check_completeness(expected_ids, archive_ids, OUTPUT_DIR, MODE)
    input("\nDrücke Enter zum Beenden...")

if __name__ == "__main__":
    main()